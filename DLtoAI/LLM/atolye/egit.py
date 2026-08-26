# -*- coding: utf-8 -*-
"""
egit.py — LoRA ile SFT. ATÖLYEDE ÇALIŞTIRILMAZ.

Bunu provada bir kez çalıştırıyoruz; iki şey üretiyor:
    adapter/          eğitilmiş LoRA ağırlıkları  (~birkaç MB)
    egitim_log.txt    loss düşüşü — atölyede bunu açıp gösteriyoruz

Neden canlı eğitmiyoruz: 40 kişi Enter'a basmış sizi bekliyorken
loss'un düşmesini izlemek dersin en sıkıcı 8 dakikası olur.

Neden TRL/SFTTrainer değil: API'si sürümler arasında değişiyor ve
atölye sabahı sürpriz istemiyoruz. Altını açmanın öğretici tarafı da var —
gerçek hayatta TRL kullanın, kapanışta o slaytı gösteriyoruz.

Çalıştır:  python egit.py            (varsayılan ayarlar)
           python egit.py --epok 4
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys
import time

from ortak import (KL, MR, MV, R, SN, SR, YS, altbaslik, alan, baslik, bilgi,
                   basarili, kutu)
from araclar import ARAC_SONUC_ISTEMI, KISA_SISTEM

KOK = pathlib.Path(__file__).parent
VERI = KOK / "veri" / "ornekler.jsonl"
LOG = KOK / "egitim_log.txt"

# ── LoRA ayarları ────────────────────────────────────────────────────
# r         : düşük ranklı matrislerin rankı. Büyüdükçe kapasite ve boyut artar.
# lora_alpha: ölçekleme. Yaygın kural alpha = 2*r.
# target    : 1. saatte çizdiğimiz attention kutuları. Eğittiğimiz tam olarak bunlar.
R_ = 8
ALPHA = 16
DROPOUT = 0.05
HEDEF_KATMANLAR = ["q_proj", "k_proj", "v_proj", "o_proj"]

EPOK = 3
LR = 2e-4
YIGIN = 1          # 4 GB VRAM'e göre
BIRIKTIR = 8       # etkin yığın = YIGIN * BIRIKTIR
EN_UZUN = 320


def ornekleri_yukle():
    satirlar = []
    with open(VERI, encoding="utf-8") as f:
        for s in f:
            s = s.strip()
            if s:
                satirlar.append(json.loads(s))
    return satirlar


def mesajlari_kur(ornek):
    """Bir örneği konuşmaya çevirir.

    İki tür örnek var:
      1. tur : soru → JSON araç çağrısı  (ya da araçsız cevap)
      2. tur : soru → JSON → ARAÇ SONUCU → doğal cümle

    2. tur örnekleri şart. Yoksa model araç sonucunu görünce
    yine JSON basar ve beş adımlı akışın son adımı çöker.
    """
    m = [{"role": "system", "content": KISA_SISTEM},
         {"role": "user", "content": ornek["soru"]}]
    if "arac_sonucu" in ornek:
        m.append({"role": "assistant", "content": ornek["arac_cagrisi"]})
        m.append({"role": "user", "content": ARAC_SONUC_ISTEMI.format(
            sonuc=ornek["arac_sonucu"])})
    return m


def ornegi_kodla(tok, ornek, en_uzun=EN_UZUN):
    """Bir örneği (girdi, etiket) çiftine çevirir.

    Kritik ayrıntı: loss SADECE cevap token'ları üzerinden hesaplanıyor.
    Prompt token'larının etiketi -100 — yani "bunları tahmin etmeyi öğrenme".
    Bu maskeleme unutulursa model soruları ezberlemeye başlar.
    """
    istem = tok.apply_chat_template(
        mesajlari_kur(ornek), tokenize=False, add_generation_prompt=True)

    istem_id = tok(istem, add_special_tokens=False)["input_ids"]
    cevap_id = tok(ornek["cevap"], add_special_tokens=False)["input_ids"]
    cevap_id = cevap_id + [tok.eos_token_id]

    girdi = (istem_id + cevap_id)[:en_uzun]
    etiket = ([-100] * len(istem_id) + cevap_id)[:en_uzun]
    return girdi, etiket


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--epok", type=int, default=EPOK)
    ap.add_argument("--lr", type=float, default=LR)
    ap.add_argument("--r", type=int, default=R_)
    ap.add_argument("--cikti", default="adapter")
    ap.add_argument("--hizli", action="store_true")   # ortak.py yutuyor
    args = ap.parse_args()

    import torch
    from peft import LoraConfig, get_peft_model
    from ortak import MODEL, yukle

    baslik("EĞİTİM — SFT + LoRA   (atölyede çalıştırılmaz)", MR)

    tok, model = yukle()
    model.config.use_cache = False

    toplam_p = sum(p.numel() for p in model.parameters())
    # 4 GB VRAM'e sığdırma stratejisi:
    #   küçük model  → her şey fp32, en güvenli yol
    #   büyük model  → taban fp16 kalır, sadece LoRA fp32'ye çıkar,
    #                  üstüne gradient checkpointing
    kucuk = toplam_p < 1e9
    if kucuk:
        model = model.float()
    else:
        model.gradient_checkpointing_enable()
        model.enable_input_require_grads()

    # ── veri ─────────────────────────────────────────────────────────
    altbaslik("VERİ")
    ornekler = ornekleri_yukle()
    arac_sayisi = sum(1 for o in ornekler if o["cevap"].lstrip().startswith("{"))
    alan("dosya", str(VERI.relative_to(KOK)))
    alan("örnek", len(ornekler))
    alan("araçlı", f"{arac_sayisi}  (%{100 * arac_sayisi / len(ornekler):.0f})")
    alan("araçsız", f"{len(ornekler) - arac_sayisi}  "
                    f"(%{100 * (len(ornekler) - arac_sayisi) / len(ornekler):.0f})")

    kodlu = [ornegi_kodla(tok, o) for o in ornekler]
    alan("en uzun", f"{max(len(g) for g, _ in kodlu)} token")

    # ── LoRA ─────────────────────────────────────────────────────────
    altbaslik("LoRA")
    ayar = LoraConfig(
        r=args.r,
        lora_alpha=ALPHA,
        lora_dropout=DROPOUT,
        target_modules=HEDEF_KATMANLAR,
        bias="none",
        task_type="CAUSAL_LM",
    )
    model = get_peft_model(model, ayar)

    if not kucuk:
        # Taban fp16, LoRA fp32: küçük ağırlıkların güncellemeleri
        # fp16'nın çözünürlüğünün altında kalıp yutulmasın.
        for p in model.parameters():
            if p.requires_grad:
                p.data = p.data.float()

    egitilebilir = sum(p.numel() for p in model.parameters() if p.requires_grad)
    toplam = sum(p.numel() for p in model.parameters())
    kutu(f"LoraConfig(r={args.r}, lora_alpha={ALPHA},\n"
         f"           target_modules={HEDEF_KATMANLAR})",
         "eğittiğimiz şey", MR)
    alan("eğitilebilir", f"{egitilebilir / 1e6:.2f} M", YS)
    alan("toplam", f"{toplam / 1e6:.0f} M")
    alan("oran", f"%{100 * egitilebilir / toplam:.2f}", YS)

    # ── eğitim ───────────────────────────────────────────────────────
    altbaslik("EĞİTİM")
    cihaz = model.device
    iyilestirici = torch.optim.AdamW(
        [p for p in model.parameters() if p.requires_grad], lr=args.lr)
    model.train()

    kayit = [
        f"model        : {MODEL}",
        f"veri         : {len(ornekler)} örnek "
        f"({arac_sayisi} araçlı / {len(ornekler) - arac_sayisi} araçsız)",
        f"LoRA         : r={args.r}, alpha={ALPHA}, "
        f"target={','.join(HEDEF_KATMANLAR)}",
        f"eğitilebilir : {egitilebilir / 1e6:.2f} M / {toplam / 1e6:.0f} M "
        f"(%{100 * egitilebilir / toplam:.2f})",
        f"epok         : {args.epok}   lr={args.lr}   "
        f"etkin yığın={YIGIN * BIRIKTIR}",
        "",
    ]

    t0 = time.time()
    adim = 0
    kayiplar = []
    for epok in range(1, args.epok + 1):
        import random
        sira = list(range(len(kodlu)))
        random.Random(1234 + epok).shuffle(sira)

        iyilestirici.zero_grad()
        for sayac, i in enumerate(sira, 1):
            girdi, etiket = kodlu[i]
            g = torch.tensor([girdi], device=cihaz)
            e = torch.tensor([etiket], device=cihaz)

            cikti = model(input_ids=g, labels=e)
            kayip = cikti.loss
            (kayip / BIRIKTIR).backward()
            kayiplar.append(float(kayip))

            if sayac % BIRIKTIR == 0 or sayac == len(sira):
                torch.nn.utils.clip_grad_norm_(
                    [p for p in model.parameters() if p.requires_grad], 1.0)
                iyilestirici.step()
                iyilestirici.zero_grad()
                adim += 1

                ort = sum(kayiplar[-BIRIKTIR:]) / len(kayiplar[-BIRIKTIR:])
                satir = f"epok {epok} | adım {adim:>3} | loss {ort:.3f}"
                print(f"   {SN}{satir}{R}", flush=True)
                kayit.append(satir)

    sure = time.time() - t0
    print()
    alan("süre", f"{sure:.0f} sn")
    alan("ilk loss", f"{sum(kayiplar[:10]) / 10:.3f}")
    alan("son loss", f"{sum(kayiplar[-10:]) / 10:.3f}")

    # ── kaydet ───────────────────────────────────────────────────────
    altbaslik("KAYIT")
    cikti_yolu = KOK / args.cikti
    model.save_pretrained(cikti_yolu)
    tok.save_pretrained(cikti_yolu)

    boyut = sum(f.stat().st_size for f in cikti_yolu.rglob("*") if f.is_file())
    adapter_boyut = sum(f.stat().st_size for f in cikti_yolu.glob("adapter_model*"))
    alan("klasör", str(cikti_yolu.relative_to(KOK)))
    alan("adapter", f"{adapter_boyut / 1024 ** 2:.1f} MB", YS)
    alan("toplam", f"{boyut / 1024 ** 2:.1f} MB  (tokenizer dahil)")

    kayit += [
        "",
        f"süre         : {sure:.0f} sn",
        f"ilk loss     : {sum(kayiplar[:10]) / 10:.3f}",
        f"son loss     : {sum(kayiplar[-10:]) / 10:.3f}",
        f"adapter      : {adapter_boyut / 1024 ** 2:.1f} MB",
    ]
    LOG.write_text("\n".join(kayit) + "\n", encoding="utf-8")

    print()
    basarili(f"adapter kaydedildi → {args.cikti}/")
    basarili(f"log kaydedildi     → {LOG.name}")
    print()
    bilgi("Şimdi:  python 04_finetune.py --sonra")
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
