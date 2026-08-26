# -*- coding: utf-8 -*-
"""
04_finetune.py — Davranışı değiştir.

Altı bölüm:
  ①  ÖNCE      ham model iki koşulda denenir
                 A) kısa prompt  → araçtan haberi yok, çağıramıyor
                 B) uzun tarif   → kısmen çağırıyor, her istekte token yakıyor
  ②  VERİ      56 örnek, üç kategori — modelin göreceği HER TUR veride
  ③  LoRA      ⭐ 1. saate köprü: eğittiğimiz şey q_proj/k_proj/v_proj/o_proj
  ④  EĞİTİM    canlı yapılmaz, egitim_log.txt gösterilir
  ⑤  SONRA     kısa prompt + eğitilmiş model → beş adımlı tam akış
  ⑥  TABLO     üç koşul yan yana: token maliyeti × güvenilirlik

Çalıştır:  python 04_finetune.py            (tam akış — önerilen)
           python 04_finetune.py --once     (sadece ① ② ③ ④)
           python 04_finetune.py --sonra    (sadece ⑤ ⑥)
"""
import json
import pathlib
import sys

import araclar
from araclar import (ARAC_SONUC_ISTEMI, ARAC_TARIFI, ARAC_TESTLERI,
                     KISA_SISTEM, ayristir, calistir, gecerli_mi, ozet,
                     puanla)
from ortak import (ADAPTER, CY, KL, KR, MR, MV, R, SN, SR, YS, altbaslik,
                   alan, baslik, basarili, basarisiz, bilgi, duraklat, kutu,
                   sor, yukle)

KOK = pathlib.Path(__file__).parent
VERI = KOK / "veri" / "ornekler.jsonl"
LOG = KOK / "egitim_log.txt"

DEMO_SORU = "Benim ilerlemem ne durumda? Kayıt numaram 482137"

BES_ADIM = """1.  Kullanıcı sorusu
2.  Model → JSON araç çağrısı          ← fine-tune bunu öğretti
3.  Program → fonksiyonu çalıştırır    ← modelin haberi yok
4.  Sonuç → modele GERİ verilir        ← ikinci tur
5.  Model → doğal cümle üretir"""


def istem_token(sistem, kullanici):
    tok, _ = yukle()
    metin = tok.apply_chat_template(
        [{"role": "system", "content": sistem},
         {"role": "user", "content": kullanici}],
        tokenize=False, add_generation_prompt=True)
    return len(tok(metin)["input_ids"])


def test_kosusu(sistem, baslik_, renk):
    """Ayrılmış araç sorularını çalıştırır, kaç tanesi doğru sayar."""
    print(f"\n{renk}{KL}   {baslik_}{R}")
    dogru = 0
    for soru, arac, no in ARAC_TESTLERI:
        cevap = sor(sistem, soru, sicaklik=0.0, en_fazla=90)
        ok, aciklama = puanla(cevap, arac, no)
        dogru += ok
        isaret = f"{YS}✓{R}" if ok else f"{KR}✗{R}"
        print(f"   {isaret} {soru[:46]:<46} {SN}{aciklama[:34]}{R}")
    print(f"   {renk}{KL}   → {dogru}/{len(ARAC_TESTLERI)}{R}")
    return dogru


# ═════════════════════════════════════════════════════════════════════
#  ① ÖNCE
# ═════════════════════════════════════════════════════════════════════

def bolum_once():
    altbaslik("① ÖNCE — ham model, iki koşul", KR)

    # ── A) kısa prompt ───────────────────────────────────────────────
    print()
    print(f"{SN}   KOŞUL A — sistem promptunda araçlardan hiç söz etmiyoruz{R}")
    kutu(KISA_SISTEM, f"sistem promptu   [{istem_token(KISA_SISTEM, DEMO_SORU)} token]", SN)
    alan("soru", DEMO_SORU, KL)
    print()
    cevap_a = sor(KISA_SISTEM, DEMO_SORU, sicaklik=0.0, en_fazla=120)
    kutu(" ".join(cevap_a.split()), "model", MV)
    cagri_a = ayristir(cevap_a)
    if gecerli_mi(cagri_a):
        basarili(f"ayrıştırma: {ozet(cagri_a)}")
        bilgi("Beklenmedik — model tarifsiz de çağırdı. Koşul B'ye bakın.")
    else:
        basarisiz("ayrıştırma: BAŞARISIZ — ortada JSON yok")
        bilgi("Doğal bir sonuç: modelin araçların varlığından haberi yok.")
    duraklat()

    # ── B) uzun tarif ────────────────────────────────────────────────
    print()
    print(f"{SN}   KOŞUL B — araçları sistem promptunda tarif ediyoruz{R}")
    kutu(ARAC_TARIFI,
         f"sistem promptu   [{istem_token(ARAC_TARIFI, DEMO_SORU)} token]", SR)
    dogru_b = test_kosusu(ARAC_TARIFI, "ayrılmış test — ham model + tarif", SR)
    fark = istem_token(ARAC_TARIFI, DEMO_SORU) - istem_token(KISA_SISTEM, DEMO_SORU)
    print()
    if dogru_b == len(ARAC_TESTLERI):
        bilgi("Tarif edince çalışıyor — ve bunu saklamıyoruz.")
        bilgi("Modern instruct modelleri araç çağırmayı zaten biliyor;")
        bilgi("büyük modellerde bu iş için fine-tune GEREKMEZ.")
    else:
        bilgi("Tarif edince kısmen çalışıyor.")
    print()
    bilgi("Ama bir bedeli var:")
    bilgi(f"  bu tarif HER istekte gönderiliyor — {fark} fazladan token,")
    bilgi("  her seferinde, her kullanıcı için.")
    bilgi("  Üç araçta {} token. Otuz araçta bunun on katı.".format(fark))
    print()
    kutu("Araç var — ama talimat PROMPT'ta duruyor, modelde değil.\n"
         "Sorumuz şu: bu talimatı prompt'tan alıp MODELE koyabilir miyiz?\n"
         "\n"
         "Bu, fine-tune'un en yaygın gerçek kullanımlarından biri:\n"
         "uzun sistem promptunu içselleştirmek.",
         "① özet", KR)
    duraklat()
    return dogru_b


# ═════════════════════════════════════════════════════════════════════
#  ② VERİ
# ═════════════════════════════════════════════════════════════════════

def bolum_veri():
    altbaslik("② VERİ — modele ne gösteriyoruz?")
    ornekler = [json.loads(s) for s in open(VERI, encoding="utf-8") if s.strip()]

    tur1 = [o for o in ornekler if "arac_sonucu" not in o
            and o["cevap"].lstrip().startswith("{")]
    tur2 = [o for o in ornekler if "arac_sonucu" in o]
    aracsiz = [o for o in ornekler if "arac_sonucu" not in o
               and not o["cevap"].lstrip().startswith("{")]

    print()
    alan("dosya", "veri/ornekler.jsonl")
    alan("örnek", len(ornekler))
    print()
    n = len(ornekler)
    print(f"   {YS}araç çağrısı (JSON){R:<12}   {len(tur1):>3}   %{100*len(tur1)/n:.0f}")
    print(f"   {MV}araç sonucu → cümle{R:<12}   {len(tur2):>3}   %{100*len(tur2)/n:.0f}")
    print(f"   {SR}araç gerekmiyor{R:<16}   {len(aracsiz):>3}   %{100*len(aracsiz)/n:.0f}")
    print()

    ornek_tur1 = next(o for o in tur1 if "482137" in o["soru"])
    ornek_aracsiz = next(o for o in aracsiz
                         if o["cevap"] == araclar.ARACSIZ_CEVAP)
    ornek_sohbet = next(o for o in aracsiz if "Merhaba" in o["soru"])
    ornek_tur2 = tur2[0]

    for etiket, o, renk in (("araç çağrısı", ornek_tur1, YS),
                            ("araç gerekmiyor  ⭐", ornek_aracsiz, SR),
                            ("sohbet  ⭐", ornek_sohbet, SR),
                            ("ikinci tur  ⭐", ornek_tur2, MV)):
        print(f"   {renk}{KL}{etiket}{R}")
        print(f"      {SN}soru {R}: {o['soru'][:62]}")
        if "arac_sonucu" in o:
            print(f"      {SN}→ JSON{R}: {o['arac_cagrisi'][:62]}")
            print(f"      {SN}→ araç{R}: {o['arac_sonucu'][:62]}")
        print(f"      {SN}cevap{R}: {renk}{o['cevap'][:62]}{R}")
        print()

    kutu("Yıldızlı üç satır türü olmasaydı model HER ŞEYE JSON basmayı\n"
         "öğrenirdi — 'merhaba' desen bile. Ve araç sonucunu görünce\n"
         "cümle kurmak yerine yine JSON üretirdi.\n"
         "\n"
         "Kural: modelin karşılaşacağı HER durum veride olmalı.",
         "veri karışımı neden böyle", CY)
    duraklat()


# ═════════════════════════════════════════════════════════════════════
#  ③ LoRA  ⭐
# ═════════════════════════════════════════════════════════════════════

def bolum_lora():
    altbaslik("③ LoRA — neyi eğitiyoruz?  ⭐", MR)
    import egit

    print()
    kutu(f"LoraConfig(r={egit.R_}, lora_alpha={egit.ALPHA},\n"
         f"           target_modules={egit.HEDEF_KATMANLAR})",
         "egit.py", MR)
    print()
    kutu("Bir saat önce çizdiğimiz üç LINEAR kutusunu hatırlıyor musunuz?\n"
         "00_attention.py'de isimlerini de gördük.\n"
         "\n"
         "q_proj · k_proj · v_proj · o_proj\n"
         "\n"
         "EĞİTTİĞİMİZ TAM OLARAK ONLAR.",
         "1. saate köprü", CY)
    print()
    duraklat("rakamlara bak")

    _, model = yukle()
    toplam = sum(p.numel() for p in model.parameters())

    # Eğitilebilir parametre sayısını egit.py'nin bıraktığı logdan okuyoruz;
    # log yoksa LoRA formülünden hesaplıyoruz: her hedef katman için
    # r × (giriş + çıkış) parametre.
    sayim = None
    if LOG.exists():
        for satir in LOG.read_text(encoding="utf-8").splitlines():
            if satir.startswith("eğitilebilir"):
                sayim = satir.split(":", 1)[1].strip()
    if sayim is None:
        n = 0
        for ad, kat in model.named_modules():
            if ad.rsplit(".", 1)[-1] in egit.HEDEF_KATMANLAR and hasattr(kat, "in_features"):
                n += egit.R_ * (kat.in_features + kat.out_features)
        sayim = f"{n / 1e6:.2f} M / {toplam / 1e6:.0f} M (%{100 * n / toplam:.2f})"

    print()
    alan("eğitilebilir", sayim, YS, 14)
    alan("toplam", f"{toplam / 1e6:.0f} M parametre", "", 14)

    adapter_yolu = KOK / ADAPTER
    if adapter_yolu.exists():
        boyut = sum(f.stat().st_size
                    for f in adapter_yolu.glob("adapter_model*"))
        alan("adapter", f"{boyut / 1024 ** 2:.1f} MB", YS, 14)
    else:
        alan("adapter", "(henüz eğitilmedi)", SR, 14)
    print()
    bilgi("Modelin %99'undan fazlası donmuş durumda. Değişen küçük bir yama.")
    bilgi("Aynı temel modelin üstüne başka görevler için başka adapter'lar")
    bilgi("takabilirsiniz — LoRA'nın asıl cazibesi bu.")
    duraklat()


# ═════════════════════════════════════════════════════════════════════
#  ④ EĞİTİM
# ═════════════════════════════════════════════════════════════════════

def bolum_egitim():
    altbaslik("④ EĞİTİM — canlı yapmıyoruz")
    print()
    if not LOG.exists():
        basarisiz(f"{LOG.name} yok. Önce:  python egit.py")
        return
    satirlar = LOG.read_text(encoding="utf-8").splitlines()
    loss_satirlari = [s for s in satirlar if s.startswith("epok")]
    ust = [s for s in satirlar if not s.startswith("epok") and s.strip()]

    kutu("\n".join(ust[:5]), "egitim_log.txt — ayarlar", SN)
    print()
    gosterilecek = loss_satirlari[:2] + ["..."] + loss_satirlari[-3:] \
        if len(loss_satirlari) > 6 else loss_satirlari
    for s in gosterilecek:
        print(f"   {SN}{s}{R}")
    print()
    for s in ust[5:]:
        print(f"   {SN}{s}{R}")
    print()
    bilgi("Loss düşüyor: model istediğimiz cevapları giderek daha olası buluyor.")
    bilgi("Sizi bekletmemek için önceden eğittik. Kodu paylaşacağım — egit.py.")
    duraklat()


# ═════════════════════════════════════════════════════════════════════
#  ⑤ SONRA
# ═════════════════════════════════════════════════════════════════════

def bolum_sonra():
    altbaslik("⑤ SONRA — eğitilmiş model, KISA prompt", YS)

    adapter_yolu = KOK / ADAPTER
    if not adapter_yolu.exists():
        basarisiz(f"{ADAPTER}/ yok. Önce:  python egit.py")
        sys.exit(1)

    yukle(adapter=str(adapter_yolu))
    print()
    kutu(KISA_SISTEM,
         f"sistem promptu   [{istem_token(KISA_SISTEM, DEMO_SORU)} token]  "
         f"— araç tarifi YOK", YS)
    dogru = test_kosusu(KISA_SISTEM, "ayrılmış test — fine-tune edilmiş model", YS)
    duraklat()

    # ── beş adımlı akış ──────────────────────────────────────────────
    altbaslik("BEŞ ADIMLI AKIŞ — tek soru, baştan sona", CY)
    print()
    kutu(BES_ADIM, "araç çağırma nasıl çalışıyor", CY)
    print()
    duraklat("çalıştır")

    print()
    print(f"{SN}   1. kullanıcı sorusu{R}")
    alan("   soru", DEMO_SORU, KL)

    print(f"\n{SN}   2. model → JSON{R}")
    cevap = sor(KISA_SISTEM, DEMO_SORU, sicaklik=0.0, en_fazla=90)
    kutu(cevap.strip(), "model çıktısı", MV)
    cagri = ayristir(cevap)
    if not gecerli_mi(cagri):
        basarisiz("ayrıştırma başarısız — beş adımlı akış burada durur")
        return dogru
    basarili(f"ayrıştırma: {ozet(cagri)}")

    print(f"\n{SN}   3. program → fonksiyonu çalıştırır{R}")
    sonuc = calistir(cagri)
    kutu(sonuc, f"araclar.py :: {ozet(cagri)}", SR)
    bilgi("Bu satırı Python çalıştırdı. Modelin haberi bile yok.")

    print(f"\n{SN}   4. sonuç → modele GERİ verilir{R}")
    ikinci = ARAC_SONUC_ISTEMI.format(sonuc=sonuc)
    kutu(ikinci, "ikinci tur girdisi", SN)

    print(f"\n{SN}   5. model → doğal cümle{R}")
    son = sor("", "", sicaklik=0.0, en_fazla=120, mesajlar=[
        {"role": "system", "content": KISA_SISTEM},
        {"role": "user", "content": DEMO_SORU},
        {"role": "assistant", "content": cevap.strip()},
        {"role": "user", "content": ikinci},
    ])
    kutu(" ".join(son.split()), "model", YS)
    print()

    kutu("Modele YETENEK kazandırmadık.\n"
         "not_ortalamasi() Python'da duruyor, modelin içinde değil.\n"
         "Model onu çalıştırmıyor — sadece bir string üretiyor.\n"
         "Çağıran, bizim programımız.\n"
         "\n"
         "Fine-tune yetenek değil, ALIŞKANLIK kazandırır.",
         "kilit cümle", CY)
    duraklat()
    return dogru


# ═════════════════════════════════════════════════════════════════════
#  ⑥ TABLO
# ═════════════════════════════════════════════════════════════════════

def bolum_tablo(dogru_b, dogru_sonra):
    altbaslik("⑥ ÜÇ KOŞUL YAN YANA")
    kisa_t = istem_token(KISA_SISTEM, DEMO_SORU)
    uzun_t = istem_token(ARAC_TARIFI, DEMO_SORU)
    n = len(ARAC_TESTLERI)
    print()
    print(f"   {SN}{'koşul':<34}{'sistem promptu':>16}{'ayrılmış test':>16}{R}")
    print(f"   {SN}{'─' * 66}{R}")
    print(f"   {'ÖNCE — araç tarifi yok':<34}{kisa_t:>13} tok"
          f"{KR}{'0/%d' % n:>16}{R}")
    print(f"   {'ÖNCE — araç tarifi var':<34}{uzun_t:>13} tok"
          f"{SR}{'%d/%d' % (dogru_b, n):>16}{R}")
    print(f"   {'SONRA — araç tarifi yok':<34}{kisa_t:>13} tok"
          f"{YS}{'%d/%d' % (dogru_sonra, n):>16}{R}")
    print()

    kutu(f"Fine-tune'un yaptığı şeyi tek cümleyle söyleyelim:\n"
         f"{uzun_t - kisa_t} tokenlık talimatı prompt'tan alıp MODELE gömdü.\n"
         f"\n"
         f"Yapmadığı şeyi de söyleyelim: ham modeli 'beceriksizken becerikli'\n"
         f"hâle getirmedi. 2. satıra bakın — tarif verildiğinde ham model de\n"
         f"çağırabiliyordu. Kazandığımız şey doğruluk değil, prompt maliyeti\n"
         f"ve talimatı taşımaktan kurtulmak.",
         "ne kazandık, ne kazanmadık", CY)
    print()
    bilgi("Bu fark üç araçta küçük görünür. Otuz araçlı gerçek bir sistemde")
    bilgi("sistem promptu 2000 token olur ve her istekte tekrar ödenir.")
    print()
    kutu("Dikkat: bu ÖLÇÜ değil, göz kararı. Üç soru hiçbir şey kanıtlamaz.\n"
         "Gerçek işte ayrılmış test seti, metrik ve tekrar gerekir.\n"
         "Bugünün en büyük eksiği bu — 05_test.py'de üstüne konuşuyoruz.",
         "dürüst olalım", SR)
    print()


def main():
    sadece_once = "--once" in sys.argv
    sadece_sonra = "--sonra" in sys.argv

    baslik("04 — FINE-TUNE:  davranışı değiştir", MR)
    if not sadece_sonra:
        bilgi("RAG olguyu getirdi. Ama 'ortalamam kaç' hâlâ cevapsız —")
        bilgi("çünkü o bilgi belgede değil, veritabanında.")
        duraklat("başlamak için Enter")

    dogru_b = 0
    if not sadece_sonra:
        dogru_b = bolum_once()
        bolum_veri()
        bolum_lora()
        bolum_egitim()

    if not sadece_once:
        dogru_sonra = bolum_sonra()
        bolum_tablo(dogru_b, dogru_sonra)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
