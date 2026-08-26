# -*- coding: utf-8 -*-
"""
01_prompt.py — Halüsinasyonu canlı yakala.

Dört bölüm:
  ①  Çıplak soru        → model dürüst: "bilmiyorum"
  ②  Rol verilmiş model → aynı soru, şimdi uyduruyor  ⭐ asıl ders burada
  ③  Aynı soru 3 kez    → her seferinde başka sayı    ⭐ en ucuz kanıt
  ④  İyi prompt         → modele "bilmiyorum" deme izni

②'nin önemi: halüsinasyonu üreten şey modelin kötülüğü değil, ona
verdiğimiz ROL. Bir asistan rolüne soktuğunuz an "bilmiyorum" demek
o rolün dışına çıkmak oluyor. Avianca davasında da olan buydu.

Bu bölümde kataloğun doğru cevabını GÖSTERMİYORUZ. Gerek yok:
model kendi kendisiyle çelişiyor, kanıt bu.

Çalıştır:  python 01_prompt.py
"""
import re
import sys

from ortak import (CY, KL, KR, MV, R, SN, SR, YS, altbaslik, alan, baslik,
                   bilgi, duraklat, kutu, sor)

SORU = "Data Scientist Path kaç saat sürüyor ve ücreti ne kadar?"

# ③ bölümündeki üç deneme için tohumlar. Provada seçildi:
# üçünün de FARKLI sayı üretmesi demonun şartı.
TOHUMLAR = [7, 11, 99]
SICAKLIK = 1.0

ROL = """Sen Miuul eğitim platformunun öğrenci destek asistanısın.
Miuul kataloğundaki eğitimler hakkında öğrencilere bilgi verirsin.
Sorulara kısa ve net cevap ver."""

IYI_PROMPT = """Sen Miuul eğitim platformunun öğrenci destek asistanısın.
Sadece sana verilen resmî katalog bilgisine dayanarak cevap ver.
Elinde katalog kaydı yoksa veya emin değilsen "Bu bilgiye sahip değilim" de
ve öğrenciyi miuul.com'a yönlendir.
Süre, ücret veya tarih TAHMİN ETME."""


def sayilari_bul(metin: str):
    """Cevaptaki süre ve ücret sayılarını çıkarır."""
    return re.findall(r"\b(\d{1,5})\b", metin)


def tek(metin: str, n: int = 200) -> str:
    return " ".join(metin.split())[:n]


def main():
    baslik("01 — PROMPT:  halüsinasyonu canlı yakalayalım")
    bilgi("Senaryo: Miuul eğitim platformunun öğrenci destek asistanı.")
    bilgi("Katalog gerçek — miuul.com'dan alındı. Model onu görmüyor.")
    duraklat("başlamak için Enter")

    # ── ① Çıplak soru ────────────────────────────────────────────────
    altbaslik("① ÇIPLAK SORU — modele hiçbir rol vermeden soralım")
    alan("sistem", "(yok)", SN)
    alan("soru", SORU, KL)
    print()
    cevap1 = sor("", SORU, sicaklik=0.0, en_fazla=130)
    kutu(tek(cevap1, 400), "model", MV)
    print()
    bilgi("Model burada büyük ölçüde dürüst: bilmediğini söylüyor.")
    bilgi("Peki sorun yok mu? Sorun tam da buradan sonra başlıyor.")
    duraklat()

    # ── ② Rol ⭐ ─────────────────────────────────────────────────────
    altbaslik("② AYNI SORU — ama model artık BİR ROLDE", KR)
    bilgi("Gerçek hayatta bu modelleri böyle çalıştırıyoruz:")
    bilgi("bir kuruma asistan olarak koyup müşterinin karşısına çıkarıyoruz.")
    print()
    kutu(ROL, "sistem promptu", SR)
    alan("soru", SORU, KL)
    print()
    cevap2 = sor(ROL, SORU, sicaklik=0.0, en_fazla=130)
    kutu(tek(cevap2, 400), "model", MV)
    print()

    s2 = sayilari_bul(cevap2)
    if s2:
        print(f"{KR}{KL}   → Sayı verdi: {', '.join(s2[:6])}{R}")
    print()
    kutu("Halüsinasyonu üreten şey modelin kötülüğü değil, ona verdiğimiz ROL.\n"
         "Bir asistan rolüne soktuğunuz an, 'bilmiyorum' demek o rolün\n"
         "DIŞINA çıkmak oluyor. Model rolü bozmamayı tercih ediyor.\n"
         "\n"
         "Avianca davasında da olan buydu: avukat modeli 'bana emsal karar\n"
         "bul' rolüne soktu. Model rolü oynadı.",
         "atölyenin ilk kilit cümlesi", KR)
    duraklat()

    # ── ③ Üç kez sor ─────────────────────────────────────────────────
    altbaslik("③ AYNI SORUYU ÜÇ KEZ SORALIM — sıcaklık %.1f" % SICAKLIK, KR)
    bilgi("Tek değişen şey örnekleme. Soru aynı, model aynı, katalog yine yok.")
    print()

    hepsi = []
    for i, tohum in enumerate(TOHUMLAR, 1):
        c = sor(ROL, SORU, sicaklik=SICAKLIK, en_fazla=130, tohum=tohum)
        hepsi.append(c)
        print(f"{SR}{KL}{i}. deneme{R}  {tek(c, 210)}")
        print()

    sayilar = [sayilari_bul(c)[:5] for c in hepsi]
    print(SN + "─" * 78 + R)
    for i, grup in enumerate(sayilar, 1):
        alan("%d. deneme" % i, ", ".join(grup) if grup else "(sayı geçmedi)", KR)
    print()

    kumeler = {tuple(g) for g in sayilar if g}
    if len(kumeler) > 1:
        print(f"{KR}{KL}   → Üç deneme, üç farklı cevap.{R}")
        print()
        bilgi("Kataloğa bakmamıza bile gerek yok.")
        bilgi("Model KENDİ KENDİSİYLE çelişiyor — demek ki bilmiyor, üretiyor.")
    else:
        print(f"{SR}   → Bu turda cevaplar çakıştı. TOHUMLAR listesini değiştirin{R}")
        bilgi("(01_prompt.py başındaki TOHUMLAR satırı).")
    duraklat()

    # ── ④ İyi prompt ─────────────────────────────────────────────────
    altbaslik("④ İYİ PROMPT — modele 'bilmiyorum' deme izni verelim", YS)
    kutu(IYI_PROMPT, "sistem promptu", YS)
    alan("soru", SORU, KL)
    print()
    cevap4 = sor(IYI_PROMPT, SORU, sicaklik=0.0, en_fazla=130)
    kutu(tek(cevap4, 400), "model", MV)
    print()

    # Üç ayrı sonuç var; hangisi olduğunu ÖLÇEREK söylüyoruz.
    sayilar4 = sayilari_bul(cevap4)
    geri_cekildi = any(k in cevap4.lower() for k in
                       ("sahip değilim", "bilmiyorum", "emin değil", "miuul.com",
                        "katalog", "bilgim yok", "erişimim"))
    if geri_cekildi and sayilar4:
        print(f"{SR}{KL}   ~ İkisini birden yaptı: hem 'bilmiyorum' dedi, "
              f"hem sayı ekledi.{R}")
        bilgi(f"Eklediği sayılar: {', '.join(sayilar4[:5])}")
        bilgi("En sık görülen sonuç bu. Prompt uydurmayı azaltıyor ama kesmiyor.")
    elif sayilar4:
        print(f"{KR}   ! Model yine sayı verdi: {', '.join(sayilar4[:5])}{R}")
        bilgi("İyi prompt garanti değil. Zaten iddiamız da bu değil.")
    elif geri_cekildi:
        print(f"{YS}   ✓ Model geri çekildi: sayı uydurmadı, "
              f"bilmediğini söyledi.{R}")
    else:
        print(f"{SR}   ~ Model sayı uydurmadı — ama net de olamadı.{R}")
        bilgi("Yarım başarı: uydurmayı bıraktı, yerine laf kalabalığı koydu.")
    print()

    kutu("Prompt halüsinasyonu AZALTIR, çözmez.\n"
         "En işe yarar tek cümle: modele bilmeme izni vermek.\n"
         "Çoğu insan bu cümleyi yazmıyor.\n"
         "\n"
         "Ama hâlâ bir sorun var: model doğru cevabı hâlâ BİLMİYOR.\n"
         "Sırada onu düzeltmeye çalışacağız → 02_fewshot.py",
         "buradan çıkan ders", CY)
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
