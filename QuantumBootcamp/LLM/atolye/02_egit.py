# -*- coding: utf-8 -*-
"""
02_egit.py — LoRA ile fine-tune. Yönlendirici eğitimi.

66 örnek, üç epok, ~2 milyon eğitilebilir parametre. Modelin 1.5 milyar
ağırlığının %0,14'ü. Geri kalan her şey donuk.

Neden TRL/SFTTrainer değil: API'si sürümler arasında değişiyor, atölye
sabahı sürpriz istemiyoruz. Döngüyü elle yazmanın öğretici tarafı da var —
altında olağanüstü bir şey olmadığı buradan görünüyor.

Kritik ayrıntı: loss SADECE cevap token'ları üzerinden hesaplanıyor
(ornegi_kodla). Prompt token'larının etiketi -100. Bu maskeleme unutulursa
model soruları ezberler, etiketi değil.

Çalıştır:  python 02_egit.py
           python 02_egit.py --epok 4      (3 epok yetmediyse)

Üretir:    adapter/          LoRA ağırlıkları (birkaç MB)
           egitim_log.txt    loss düşüşü — derste bunu açıp gösteriyoruz
"""
from __future__ import annotations

import argparse
import random
import sys
import time

import ayar
import motor
from ekran import (MR, R, SN, SR, YS, altbaslik, alan, basarili, baslik,
                   bilgi, kutu, uyari)


def ornegi_kodla(tok, ornek, en_uzun=None):
    """Bir örneği (girdi, etiket) çiftine çevirir.

    girdi  : [ system + soru + assistant başlangıcı ] + [ etiket + eos ]
    etiket : [ -100, -100, ... -100 ]                 + [ etiket + eos ]
                     ^ prompt maskeli                          ^ öğrenilen kısım

    Prompt token'larının etiketi -100 — "bunları tahmin etmeyi öğrenme".
    Modelin öğrendiği tek şey: bu istemin ardından hangi kelime gelmeli.
    """
    en_uzun = en_uzun or ayar.EN_UZUN

    istem = motor.istem_metni(tok, ayar.SISTEM, ornek["soru"])
    istem_id = tok(istem, add_special_tokens=False)["input_ids"]
    cevap_id = tok(ornek["etiket"], add_special_tokens=False)["input_ids"]
    cevap_id = cevap_id + [tok.eos_token_id]      # eos: "burada dur"

    girdi = (istem_id + cevap_id)[:en_uzun]
    etiket = ([-100] * len(istem_id) + cevap_id)[:en_uzun]
    return girdi, etiket


def main():
    ap = argparse.ArgumentParser(description="LoRA eğitimi")
    ap.add_argument("--epok", type=int, default=ayar.EPOK)
    ap.add_argument("--lr", type=float, default=ayar.LR)
    ap.add_argument("--hizli", action="store_true", help="Enter beklemeden akar")
    args = ap.parse_args()

    import torch
    from peft import LoraConfig, get_peft_model

    baslik("02 · EĞİTİM — LoRA ile fine-tune", MR)

    torch.manual_seed(ayar.TOHUM)
    random.seed(ayar.TOHUM)

    tok, model = motor.yukle()
    model.config.use_cache = False           # eğitimde kv-cache kapalı

    toplam_p = sum(p.numel() for p in model.parameters())

    # 4 GB VRAM'e sığdırma stratejisi:
    #   küçük model  -> her şey fp32, en güvenli yol
    #   büyük model  -> taban fp16 kalır, sadece LoRA fp32'ye çıkar,
    #                   üstüne gradient checkpointing
    kucuk = toplam_p < 1e9
    if kucuk:
        model = model.float()
    else:
        model.gradient_checkpointing_enable()
        model.enable_input_require_grads()

    # ── veri ─────────────────────────────────────────────────────────
    altbaslik("VERİ")
    ornekler = motor.ornekleri_yukle(ayar.VERI)
    alan("dosya", str(ayar.VERI.relative_to(ayar.KOK)))
    alan("örnek", len(ornekler))
    for etiket in ayar.ETIKETLER:
        n = sum(1 for o in ornekler if o["etiket"] == etiket)
        alan("  " + etiket, f"{n:>2}  ({100 * n / len(ornekler):.0f}%)")

    kodlu = [ornegi_kodla(tok, o) for o in ornekler]
    en_uzun_ornek = max(len(g) for g, _ in kodlu)
    alan("en uzun", f"{en_uzun_ornek} token   (sınır: EN_UZUN={ayar.EN_UZUN})",
         SR if en_uzun_ornek >= ayar.EN_UZUN else "")
    alan("test verisi", "DOKUNULMADI — veri/test.jsonl ayrı duruyor", SN)

    # Maskelemeyi göster: derste bu kutuya bakıyoruz.
    g0, e0 = kodlu[0]
    ogrenilen = [t for t in e0 if t != -100]
    kutu(f"örnek       : {ornekler[0]['soru']}\n"
         f"cevap       : {ornekler[0]['etiket']}\n"
         f"girdi       : {len(g0)} token\n"
         f"maskeli     : {len(e0) - len(ogrenilen)} token  (-100, loss'a girmiyor)\n"
         f"öğrenilen   : {len(ogrenilen)} token  -> "
         f"{tok.convert_ids_to_tokens(ogrenilen)}",
         "loss maskesi — model neyi öğreniyor", SN)

    # ── LoRA ─────────────────────────────────────────────────────────
    altbaslik("LoRA")
    lora_ayari = LoraConfig(**ayar.LORA)
    model = get_peft_model(model, lora_ayari)

    if not kucuk:
        # Taban fp16, LoRA fp32: küçük ağırlıkların güncellemeleri
        # fp16'nın çözünürlüğünün altında kalıp yutulmasın.
        for p in model.parameters():
            if p.requires_grad:
                p.data = p.data.float()

    egitilebilir = sum(p.numel() for p in model.parameters() if p.requires_grad)
    toplam = sum(p.numel() for p in model.parameters())
    oran = 100 * egitilebilir / toplam

    kutu(f"LoraConfig(r={ayar.LORA['r']}, lora_alpha={ayar.LORA['lora_alpha']},\n"
         f"           lora_dropout={ayar.LORA['lora_dropout']},\n"
         f"           target_modules={ayar.LORA['target_modules']})",
         "eğittiğimiz şey", MR)
    alan("eğitilebilir", f"{egitilebilir:,}".replace(",", ".") +
         f"   ({egitilebilir / 1e6:.2f} M)", YS)
    alan("toplam", f"{toplam:,}".replace(",", ".") +
         f"   ({toplam / 1e6:.0f} M)")
    alan("oran", f"%{oran:.2f}", YS)
    alan("donuk", f"%{100 - oran:.2f}  — hiç dokunulmuyor", SN)

    # ── eğitim ───────────────────────────────────────────────────────
    altbaslik("EĞİTİM")
    alan("epok", args.epok)
    alan("lr", args.lr)
    alan("yığın", f"{ayar.YIGIN} x {ayar.BIRIKTIR} biriktirme "
                  f"= etkin {ayar.YIGIN * ayar.BIRIKTIR}")
    alan("cihaz", str(model.device))
    print()

    kayit = [
        f"model        : {ayar.MODEL}",
        f"veri         : {len(ornekler)} örnek, {ayar.VERI.name}",
        "dağılım      : " + "  ".join(
            f"{e}={sum(1 for o in ornekler if o['etiket'] == e)}"
            for e in ayar.ETIKETLER),
        f"en uzun      : {en_uzun_ornek} token (EN_UZUN={ayar.EN_UZUN})",
        f"LoRA         : r={ayar.LORA['r']}, alpha={ayar.LORA['lora_alpha']}, "
        f"target={','.join(ayar.LORA['target_modules'])}",
        f"eğitilebilir : {egitilebilir:,} / {toplam:,}  (%{oran:.2f})",
        f"epok         : {args.epok}   lr={args.lr}   "
        f"etkin yığın={ayar.YIGIN * ayar.BIRIKTIR}",
        "",
    ]

    cihaz = model.device
    iyilestirici = torch.optim.AdamW(
        [p for p in model.parameters() if p.requires_grad], lr=args.lr)
    model.train()

    t0 = time.time()
    adim = 0
    kayiplar = []
    for epok in range(1, args.epok + 1):
        sira = list(range(len(kodlu)))
        random.Random(ayar.TOHUM + epok).shuffle(sira)

        iyilestirici.zero_grad()
        for sayac, i in enumerate(sira, 1):
            girdi, etiket = kodlu[i]
            g = torch.tensor([girdi], device=cihaz)
            e = torch.tensor([etiket], device=cihaz)

            cikti = model(input_ids=g, labels=e)
            kayip = cikti.loss
            (kayip / ayar.BIRIKTIR).backward()
            kayiplar.append(float(kayip))

            if sayac % ayar.BIRIKTIR == 0 or sayac == len(sira):
                torch.nn.utils.clip_grad_norm_(
                    [p for p in model.parameters() if p.requires_grad], 1.0)
                iyilestirici.step()
                iyilestirici.zero_grad()
                adim += 1

                pencere = kayiplar[-ayar.BIRIKTIR:]
                ort = sum(pencere) / len(pencere)
                satir = f"epok {epok} | adım {adim:>3} | loss {ort:.3f}"
                print(f"   {SN}{satir}{R}", flush=True)
                kayit.append(satir)

    sure = time.time() - t0
    ilk = sum(kayiplar[:10]) / 10
    son = sum(kayiplar[-10:]) / 10

    print()
    alan("ilk loss", f"{ilk:.3f}")
    alan("son loss", f"{son:.3f}", YS)
    alan("düşüş", f"{ilk - son:.3f}", YS)

    # ── kaydet ───────────────────────────────────────────────────────
    altbaslik("KAYIT")
    model.save_pretrained(ayar.ADAPTER)
    tok.save_pretrained(ayar.ADAPTER)

    adapter_boyut = sum(f.stat().st_size
                        for f in ayar.ADAPTER.glob("adapter_model*"))
    toplam_boyut = sum(f.stat().st_size
                       for f in ayar.ADAPTER.rglob("*") if f.is_file())
    alan("klasör", str(ayar.ADAPTER.relative_to(ayar.KOK)) + "/")
    alan("adapter", f"{adapter_boyut / 1024 ** 2:.1f} MB", YS)
    alan("toplam", f"{toplam_boyut / 1024 ** 2:.1f} MB  (tokenizer dahil)")
    bilgi("Taban modelin 2.9 GB'ı diskte olduğu gibi duruyor — dokunulmadı.")

    kayit += [
        "",
        f"süre         : {sure:.0f} sn",
        f"ilk loss     : {ilk:.3f}",
        f"son loss     : {son:.3f}",
        f"adapter      : {adapter_boyut / 1024 ** 2:.1f} MB",
    ]
    ayar.EGITIM_LOG.write_text("\n".join(kayit) + "\n", encoding="utf-8")

    # ── süre: hoca buna bakıp canlı çalıştırıp çalıştırmayacağına karar verir ──
    altbaslik("SÜRE")
    print()
    kutu(f"{sure:.0f} saniye   ({sure / 60:.1f} dakika)\n"
         f"{args.epok} epok x {len(ornekler)} örnek = "
         f"{args.epok * len(ornekler)} geçiş, {adim} iyileştirme adımı",
         "eğitim ne kadar sürdü", YS if sure < 120 else SR)
    print()
    if sure < 120:
        bilgi("2 dakikanın altında — derste canlı çalıştırılabilir.")
    else:
        uyari(f"{sure:.0f} sn: derste canlı çalıştırmayın, adapter'ı önceden üretin.")

    print()
    basarili(f"adapter kaydedildi -> {ayar.ADAPTER.name}/")
    basarili(f"log kaydedildi     -> {ayar.EGITIM_LOG.name}")
    print()
    bilgi("Sıradaki:  python 03_sonra.py")
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
        sys.exit(0)
    except Exception as e:
        # Bu makinede en olası hata bu; ne yapılacağını söyleyerek çıkalım.
        if "out of memory" in str(e).lower():
            print()
            uyari("CUDA out of memory.")
            uyari("1) Tarayıcıyı ve GPU kullanan diğer uygulamaları kapatın.")
            uyari("2) Yetmezse ayar.py icindeki EN_UZUN'u 192'den 128'e düşürün")
            uyari("   (sunumdaki sayıları etkilemez).")
            print()
            sys.exit(1)
        raise
