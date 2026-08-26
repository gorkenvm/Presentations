# -*- coding: utf-8 -*-
"""
05_test.py — Sınırlar. Fine-tune'un bedeli ne?

Üç bölüm:
  ①  UNUTMA TESTİ   eğitilmiş model hâlâ sohbet edebiliyor mu,
                    yoksa her şeye JSON mu basıyor? (catastrophic forgetting)
  ②  KARIŞIK TEST   ayrılmış 5 soru: 3 araçlı, 2 araçsız
  ③  KARAR TABLOSU  hangi problem hangi katmanda çözülür

Model burada çuvallarsa GİZLEME. Canlı yakalanmış bir catastrophic
forgetting, kusursuz bir demodan daha öğreticidir.

Çalıştır:  python 05_test.py
           python 05_test.py --ham     (adapter'sız — karşılaştırma için)
"""
import pathlib
import sys

from araclar import TEST_SORULARI, ayristir, puanla
from ortak import (ADAPTER, CY, KL, KR, MV, R, SN, SR, YS, altbaslik, alan,
                   baslik, basarili, basarisiz, bilgi, duraklat, kutu, sor)
from araclar import KISA_SISTEM

KOK = pathlib.Path(__file__).parent

# Eğitim verisinde OLMAYAN sorular. Asıl unutma testi bunlar:
# modelin dar bir göreve eğitilirken genel yeteneğini yitirip
# yitirmediğini ancak eğitim dağılımının dışında görebilirsiniz.
UNUTMA_SORULARI = [
    ("Merhaba, nasılsın?", "eğitimde var — sohbet örneği"),
    ("2 + 2 kaç eder?", "eğitimde YOK — genel yetenek"),
    ("Python'da liste ile tuple farkı nedir?", "eğitimde YOK — genel yetenek"),
    ("Bugün hava nasıl?", "eğitimde YOK — bilemez ama JSON da basmamalı"),
]

KARAR = [
    ("Model NE BİLİYOR eksik", "RAG", YS),
    ("Model NASIL DAVRANIYOR yanlış", "Fine-tune", MV),
    ("Sadece bir kereliğine gerek", "Prompt / few-shot", SR),
]


def bolum_unutma():
    altbaslik("① UNUTMA TESTİ — model sohbet etmeyi unuttu mu?", MV)
    bilgi("Modeli tek bir işe eğittik: JSON araç çağrısı üretmek.")
    bilgi("Bedeli ne oldu? Eğitim dağılımının DIŞINA çıkıp bakalım.")
    print()

    bozuk = 0
    for soru, not_ in UNUTMA_SORULARI:
        cevap = sor(KISA_SISTEM, soru, sicaklik=0.0, en_fazla=90)
        tek = " ".join(cevap.split())
        json_basti = ayristir(cevap) is not None
        bozuk += json_basti
        isaret = f"{KR}✗ JSON bastı{R}" if json_basti else f"{YS}✓ sohbet etti{R}"
        print(f"   {KL}{soru}{R}   {SN}({not_}){R}")
        print(f"   {SN}→{R} {tek[:110]}")
        print(f"   {isaret}")
        print()

    if bozuk == 0:
        basarili("Model sohbet edebiliyor. Veri karışımı işini görmüş:")
        bilgi("araçsız örnekler (%27) modelin genel davranışını korudu.")
    else:
        basarisiz(f"{bozuk}/{len(UNUTMA_SORULARI)} soruda JSON bastı.")
        print()
        kutu("İşte catastrophic forgetting — canlı yakaladık.\n"
             "Bir davranışı öğretirken başka bir davranışı bozduk.\n"
             "\n"
             "Çözüm daha çok veri değil, daha DENGELİ veri:\n"
             "modelin karşılaşacağı her durum karışımda temsil edilmeli.",
             "gizlemiyoruz", KR)
    duraklat()
    return bozuk


def bolum_karisik():
    altbaslik("② KARIŞIK TEST — ayrılmış 5 soru", CY)
    bilgi("Hiçbiri eğitim verisinde yok. Ezber değil, genelleme ölçüyoruz.")
    print()

    arac_dogru = arac_toplam = 0
    aracsiz_dogru = aracsiz_toplam = 0

    for soru, arac, no in TEST_SORULARI:
        cevap = sor(KISA_SISTEM, soru, sicaklik=0.0, en_fazla=90)
        ok, aciklama = puanla(cevap, arac, no)
        if arac:
            arac_toplam += 1
            arac_dogru += ok
            tur = f"{MV}araçlı  {R}"
        else:
            aracsiz_toplam += 1
            aracsiz_dogru += ok
            tur = f"{SR}araçsız {R}"
        isaret = f"{YS}✓{R}" if ok else f"{KR}✗{R}"
        print(f"   {isaret} {tur} {soru[:44]:<44} {SN}{aciklama[:30]}{R}")

    print()
    alan("araç gerektiren", f"{arac_dogru}/{arac_toplam}",
         YS if arac_dogru == arac_toplam else SR, 18)
    alan("araç gerektirmeyen", f"{aracsiz_dogru}/{aracsiz_toplam}",
         YS if aracsiz_dogru == aracsiz_toplam else SR, 18)
    alan("toplam", f"{arac_dogru + aracsiz_dogru}/{len(TEST_SORULARI)}", KL, 18)
    print()

    kutu("Beş soruyla göz kararı yaptık. Bu bir değerlendirme DEĞİL.\n"
         "\n"
         "Gerçek işte gereken: ayrılmış test seti (yüzlerce örnek),\n"
         "tanımlı metrik, birden çok tohumla tekrar, ve eğitim öncesi\n"
         "belirlenmiş bir başarı eşiği.\n"
         "\n"
         "Bugünün en büyük eksiği bu. Söylemeden geçmeyelim.",
         "dürüst olalım", SR)
    duraklat()


def bolum_karar():
    altbaslik("③ KARAR TABLOSU — hangi problem, hangi katman?", CY)
    print()
    print(f"   {SN}{'ihtiyaç':<38}{'çözüm'}{R}")
    print(f"   {SN}{'─' * 62}{R}")
    for ihtiyac, cozum, renk in KARAR:
        print(f"   {ihtiyac:<38}{renk}{KL}{cozum}{R}")
    print()

    kutu("Pratik sıra:  prompt → few-shot → RAG → EN SON fine-tune\n"
         "\n"
         "Fine-tune en pahalı, en kalıcı, geri alması en zor seçenek.\n"
         "Bir üstteki basamak işi görüyorsa oraya çıkmayın.",
         "sıra", CY)
    print()

    kutu("Fine-tune ile modele BİLGİ öğretmeye çalışmak, onu emin tonla\n"
         "yanlış konuşmaya alıştırmanın bilinen yoludur.\n"
         "\n"
         "Bilgi eksikse     → RAG\n"
         "Davranış yanlışsa → fine-tune\n"
         "\n"
         "Bugün ikisini de yaptık ve birbirinin yerine geçmediğini gördük:\n"
         "  'Data Scientist Path kaç saat'  → RAG çözdü, fine-tune çözemezdi\n"
         "  'benim ilerlemem ne durumda'    → araç çözdü, RAG çözemedi\n"
         "\n"
         "Kataloğu modele gömseydiniz, fiyat her değiştiğinde yeniden\n"
         "eğitmeniz gerekirdi — ve model eski fiyatı emin tonla söylerdi.",
         "atölyenin tek cümlesi", KR)
    print()


def main():
    ham = "--ham" in sys.argv

    baslik("05 — SINIRLAR:  fine-tune'un bedeli", MV)

    if ham:
        bilgi("--ham: adapter YÜKLENMİYOR. Karşılaştırma için ham model.")
        from ortak import yukle
        yukle()
    else:
        adapter_yolu = KOK / ADAPTER
        if not adapter_yolu.exists():
            basarisiz(f"{ADAPTER}/ yok. Önce:  python egit.py")
            sys.exit(1)
        from ortak import yukle
        yukle(adapter=str(adapter_yolu))

    duraklat("başlamak için Enter")

    bolum_unutma()
    bolum_karisik()
    bolum_karar()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
