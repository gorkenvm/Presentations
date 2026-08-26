# -*- coding: utf-8 -*-
"""
02_fewshot.py — Biçim düzelir, olgu düzelmez.

Dört bölüm:
  ①  Üç örnek cevap gösterilir  → biçim öğretiliyor (kısa, sayı veren, resmî)
  ②  Aynı soru few-shot ile     → cevap artık katalog kaydı gibi görünüyor
  ③  Yan yana karşılaştırma     → ama içindeki sayı hâlâ uydurma  ⭐
  ④  Token maliyeti             → her istekte ödenen bedel

Atölyenin en öğretici anı ③. Yavaşla.

Çalıştır:  python 02_fewshot.py
"""
import re
import sys

from ortak import (CY, KL, KR, MR, MV, R, SN, SR, YS, altbaslik, alan, baslik,
                   bilgi, duraklat, kutu, parca_bul, sor, yukle)

SORU = "Data Scientist Path kaç saat sürüyor ve ücreti ne kadar?"
HEDEF_PARCA = "Data Scientist Path"

SISTEM = """Sen Miuul eğitim platformunun öğrenci destek asistanısın.
Sorulara kısa, net ve sayı vererek cevap ver."""

# Örnekler BAŞKA eğitimlerle ilgili ve hepsi DOĞRU (katalogdan alındı).
# Yani modele olgu değil, BİÇİM öğretiyoruz.
# Data Scientist Path bu örneklerde GEÇMİYOR.
ORNEKLER = [
    ("Makine Öğrenmesi kursu kaç saat?",
     "Makine Öğrenmesi kursu 13 saattir, ücreti 90 USD'dir."),
    ("CRM Analitiği kursunun ücreti ne kadar?",
     "CRM Analitiği kursu 6 saattir, ücreti 28 USD'dir."),
    ("Data Analyst Path ne kadar sürüyor?",
     "Data Analyst Path 60 saattir, ücreti 220 USD'dir."),
]


def mesajlari_kur(few_shot: bool):
    m = [{"role": "system", "content": SISTEM}]
    if few_shot:
        for s, c in ORNEKLER:
            m.append({"role": "user", "content": s})
            m.append({"role": "assistant", "content": c})
    m.append({"role": "user", "content": SORU})
    return m


def istem_token(mesajlar) -> int:
    """Bu mesaj listesi modele gönderilirken kaç token yakıyor?"""
    tok, _ = yukle()
    metin = tok.apply_chat_template(mesajlar, tokenize=False,
                                    add_generation_prompt=True)
    return len(tok(metin)["input_ids"])


def sayilari_bul(metin: str):
    return re.findall(r"\b(\d{1,5})\b", metin)


def tek(metin: str, n: int = 300) -> str:
    return " ".join(metin.split())[:n]


def main():
    baslik("02 — FEW-SHOT:  biçim düzelir, olgu düzelmez")
    bilgi("Aynı soru, aynı model. Tek fark: prompt'a üç örnek cevap koyuyoruz.")
    duraklat("başlamak için Enter")

    # ── ① Örnekler ───────────────────────────────────────────────────
    altbaslik("① PROMPT'A KOYDUĞUMUZ ÜÇ ÖRNEK")
    bilgi("Dikkat: üçü de BAŞKA eğitimlerle ilgili ve üçü de DOĞRU.")
    bilgi("Modele olgu değil, BİÇİM öğretiyoruz: kısa, sayı veren, resmî.")
    print()
    for i, (s, c) in enumerate(ORNEKLER, 1):
        print(f"{SN}  {i}. kullanıcı {R}: {s}")
        print(f"{SN}     asistan  {R}: {YS}{c}{R}")
        print()
    bilgi("Data Scientist Path bu üç örnekte GEÇMİYOR.")
    bilgi("Yani soracağımız şeyin cevabını modele söylemedik.")
    duraklat()

    # ── ② Few-shot ile cevap ─────────────────────────────────────────
    altbaslik("② AYNI SORUYU ŞİMDİ SORALIM")
    alan("soru", SORU, KL)
    print()
    mesajlar = mesajlari_kur(few_shot=True)
    cevap = sor("", "", sicaklik=0.0, en_fazla=120, mesajlar=mesajlar)
    kutu(tek(cevap), "few-shot ile model", MV)
    print()
    bilgi("Biçim tuttu: kısa, resmî, tam da istediğimiz kalıpta.")
    duraklat()

    # ── ③ Yan yana ⭐ ────────────────────────────────────────────────
    altbaslik("③ PEKİ DOĞRU MU?  —  kataloğun kendisiyle yan yana", KR)
    parca = parca_bul(HEDEF_PARCA)
    gercek_satir = next((s for s in parca["metin"].split("\n")
                         if s.startswith("Süre:")), parca["metin"][:200])
    print()
    print(f"{SR}{KL}   few-shot cevabı {R}")
    kutu(tek(cevap), renk=SR)
    print(f"{YS}{KL}   katalog — {parca['baslik']} {R}")
    kutu(gercek_satir, renk=YS)
    print()

    dogru = set(re.findall(r"Süre:\s*(\d+)", parca["metin"])) | \
        set(re.findall(r"Ücret:\s*(\d+)", parca["metin"]))
    model_sayilari = set(sayilari_bul(cevap))
    alan("katalogda", ", ".join(sorted(dogru, key=int)) or "—", YS, 12)
    alan("modelde", ", ".join(sorted(model_sayilari, key=int)[:6]) or "—", SR, 12)
    print()

    tutan = dogru & model_sayilari
    if model_sayilari and not tutan:
        print(f"{KR}{KL}   → Cevap daha profesyonel görünüyor. Ama doğru değil.{R}")
        print(f"{KR}{KL}   → Sadece DAHA İNANDIRICI YANLIŞ oldu.{R}")
    elif tutan == dogru:
        print(f"{SR}   ! Model bu turda doğru sayıları tutturdu — nadir ama olur.{R}")
        bilgi("Tutturması da tesadüf: kataloğu görmedi, tahmin etti.")
    elif tutan:
        print(f"{SR}{KL}   → Yarısını tutturdu ({', '.join(tutan)}), "
              f"yarısını uydurdu.{R}")
        bilgi("En sinsi hâli bu: cevabın bir kısmı doğru olunca tamamı doğru sanılır.")
    else:
        print(f"{SR}   ! Model sayı vermedi. Yine de olguyu getirmedi.{R}")
    print()
    bilgi("Few-shot BİÇİM öğretir. Biçim öğretmek bilgi öğretmek değildir.")
    duraklat()

    # ── ④ Maliyet ────────────────────────────────────────────────────
    altbaslik("④ BEDELİ NE?", MR)
    az = istem_token(mesajlari_kur(few_shot=False))
    cok = istem_token(mesajlari_kur(few_shot=True))
    print()
    alan("few-shot yok", f"{az:>4} token", SN, 16)
    alan("few-shot var", f"{cok:>4} token   (her istekte)", MR, 16)
    alan("fark", f"{cok - az:>4} token   ×{cok / max(az, 1):.1f}", KR, 16)
    print()
    bilgi("Bu fark her çağrıda tekrar ödeniyor. 3 örnek az; 10 örnek çok.")
    bilgi("Geçici işler ve prototip için ideal. Kalıcı boru hattında pahalı.")
    print()

    kutu("Biçim düzeldi, olgu düzelmedi.\n"
         "Modelin bilmediği bir sayıyı, ona güzel cevap örnekleri\n"
         "göstererek öğretemezsiniz.\n"
         "\n"
         "Eksik olan şey kataloğun KENDİSİ.\n"
         "Sırada onu prompt'a sokacağız → 03_rag.py",
         "buradan çıkan ders", CY)
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
