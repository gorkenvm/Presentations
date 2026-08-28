# -*- coding: utf-8 -*-
"""
04_sinir.py — fine-tune neyi ÇÖZMEDİ.

Dersin en önemli 4 dakikası. 03_sonra.py'de bir şey kazandık; burada
bedelini ve sınırını gösteriyoruz. Üç bölüm, hepsi adapter YÜKLÜ modelle:

  1. Bilgi eklenmedi   — doğru dala yolluyor, cevabı hâlâ bilmiyor
  2. Bedeli var        — artık sohbet edemiyor (katastrofik unutma)
  3. Ne kazandık       — talimatlı istem kaç token, fine-tune'lu kaç token

Model ne derse desin çıktı olduğu gibi basılır. Hiçbir sonuç varsayılmıyor;
ekranda ne çıkarsa o konuşulur.

Çalıştır:  python 04_sinir.py
           python 04_sinir.py --hizli

Gerekli:   adapter/   -> python 02_egit.py
"""
from __future__ import annotations

import argparse
import sys

import ayar
import motor
from ekran import (CY, KL, KR, MV, R, SN, SR, YS, alan, basarisiz, baslik,
                   bilgi, duraklat, kutu, tablo)


def adaptersiz_sor(tok, model, sistem, soru):
    """Aynı süreçte, adaptörü geçici olarak devre dışı bırakıp sorar.

    PeftModel.disable_adapter() taban ağırlıkları olduğu gibi bırakır —
    modeli ikinci kez yüklemeye gerek yok. Karşılaştırma birebir adil:
    aynı istem, aynı parametreler, tek fark adaptörün açık/kapalı olması.
    """
    with model.disable_adapter():
        return motor.sor(tok, model, sistem, soru)


def main():
    ap = argparse.ArgumentParser(description="Fine-tune neyi çözmedi")
    ap.add_argument("--hizli", action="store_true", help="Enter beklemeden akar")
    ap.parse_args()

    baslik("04 · SINIR — fine-tune neyi ÇÖZMEDİ", KR)

    if not (ayar.ADAPTER.exists() and any(ayar.ADAPTER.glob("adapter_model*"))):
        basarisiz(f"{ayar.ADAPTER.name}/ bulunamadı.")
        print()
        bilgi("Önce eğitimi çalıştırın:   python 02_egit.py")
        print()
        return 1

    bilgi("Üç bölüm. Hepsi adapter YÜKLÜ modelle, ayar.SISTEM ile,")
    bilgi(f"do_sample=False, max_new_tokens={motor.EN_FAZLA_YENI} — 03 ile aynı.")

    tok, model = motor.yukle(adapter=ayar.ADAPTER)
    duraklat("başla")

    # ═════════════════════════════════════════════════════════════════
    #  1. BİLGİ EKLENMEDİ
    # ═════════════════════════════════════════════════════════════════
    baslik("1 · BİLGİ EKLENMEDİ — doğru dal, eksik cevap", CY)

    soru = ayar.SINIR_KATALOG_SORUSU
    cikti, token = motor.sor(tok, model, ayar.SISTEM, soru)

    print()
    print(CY + KL + "  " + soru + R)
    print()
    kutu(cikti or "(boş çıktı)",
         f"fine-tune'lu modelin cevabı   ({token} token)", YS)
    kutu(ayar.SINIR_DOGRU_CEVAP, "doğru cevap — veri/miuul_katalog.md içinde", MV)

    print()
    if motor.sadelestir(cikti) == "katalog":
        print("   Model soruyu " + YS + "doğru dala" + R + " yolladı: katalog.")
        print("   " + KL + "Doğru davranış." + R + " Ama saatini de, ücretini de bilmiyor.")
    else:
        print("   Model '" + cikti + "' dedi. Beklenen daldı: katalog.")
        print("   Ne derse desin, cevabın kendisini zaten bilmiyor.")
    print()
    print("   Fine-tune modele " + KL + "bilgi eklemedi" + R +
          " — ne yapacağını öğretti.")
    print("   Bu sorunun cevabını n8n'deki " + KL + "RAG dalı" + R + " verecek.")
    print("   Yönlendirici ile RAG rakip değil; " + KL + "aynı akışın iki parçası" + R + ".")
    duraklat()

    # ═════════════════════════════════════════════════════════════════
    #  2. BEDELİ VAR
    # ═════════════════════════════════════════════════════════════════
    baslik("2 · BEDELİ VAR — model artık sadece bu işi yapıyor", CY)

    soru = ayar.SINIR_ALAKASIZ
    cikti, token = motor.sor(tok, model, ayar.SISTEM, soru)
    ham_cikti, ham_token = adaptersiz_sor(tok, model, ayar.SISTEM, soru)

    print()
    print(CY + KL + "  " + soru + R)
    print()
    kutu(ham_cikti or "(boş çıktı)",
         f"adapter KAPALI — ham model   ({ham_token} token)", SN)
    kutu(cikti or "(boş çıktı)",
         f"adapter AÇIK — fine-tune'lu   ({token} token)", SR)

    print()
    gecerli = motor.sadelestir(cikti) in [motor.sadelestir(e)
                                          for e in ayar.ETIKETLER]
    if gecerli:
        print("   Fine-tune'lu model soruyu cevaplamadı; " + KL + "etiketledi" + R + ".")
        print("   Ham model ne yaptıysa yukarıda duruyor — ikisini karşılaştırın.")
    else:
        print("   Fine-tune'lu modelin çıktısı yukarıda; etiket listesinde değil.")
        print("   Ham modelin cevabıyla karşılaştırın.")
    print()
    print("   Buna " + KL + "katastrofik unutma" + R + " deniyor: bir davranışı")
    print("   öğretirken bir başkasını bozarsınız. 66 örnekle 8 MB'lık adapter")
    print("   eğittik ve model genel sohbeti bıraktı.")
    print()
    bilgi("Pratikte sonucu şu: bu model artık genel amaçlı asistan değil,")
    bilgi("tek işi olan bir parça. n8n akışında zaten tek işi var — sorun değil.")
    bilgi("Ama aynı modeli müşteriyle sohbet için de kullanacaksanız, sorun.")
    duraklat()

    # ═════════════════════════════════════════════════════════════════
    #  3. NE KAZANDIK
    # ═════════════════════════════════════════════════════════════════
    baslik("3 · NE KAZANDIK — aynı işi kaç kat ucuza", CY)

    # Ölçüm 01_once.py ile aynı yardımcıdan geliyor: motor.istem_karsilastir
    test = motor.ornekleri_yukle(ayar.TEST)
    olcu = motor.istem_karsilastir(tok, [o["soru"] for o in test])

    print()
    bilgi(f"{olcu['soru_sayisi']} test sorusu, chat şablonu dahil, istek başına ortalama")
    print()
    tablo(["yöntem", "system prompt", "istem / istek"],
          [["prompt ile (talimatlı istem)",
            f"{olcu['sistem_talimatli']} token",
            f"{olcu['talimatli']:.0f} token"],
           ["fine-tune ile (ayar.SISTEM)",
            f"{olcu['sistem_talimatsiz']} token",
            f"{olcu['talimatsiz']:.0f} token"]])
    print()
    alan("fark", f"{olcu['fark']:.0f} token / istek", SR)
    alan("kat", f"{olcu['kat']:.1f}x", YS)
    print()
    print("   Günde 10.000 istek: " + KL +
          f"{olcu['fark'] * 10000 / 1e6:.1f} milyon token/gün" + R + " fark.")
    print("   Üstüne cevap tarafı da kısaldı — 03_sonra.py'deki token tablosu.")
    print()
    bilgi("Karşılığında: bir eğitim koşusu, bir adapter dosyası, ve model")
    bilgi("artık başka bir iş yapamıyor. Takas bu.")
    duraklat()

    # ═════════════════════════════════════════════════════════════════
    #  KARAR TABLOSU
    # ═════════════════════════════════════════════════════════════════
    baslik("KARAR — elinizdeki sorun hangisi?", MV)
    print()
    kutu("biçim bozuk        ->  prompt / few-shot\n"
         "cevap yanlış       ->  RAG\n"
         "davranış yanlış    ->  fine-tune",
         "üç satırda özet", KL)
    print()
    print("   Fine-tune " + KL + "davranış" + R + " değiştirir.")
    print("   Olgusal halüsinasyonu " + KL + "düzeltmez" + R +
          " — bazen kötüleştirir:")
    print("   model artık daha kendinden emin, ama bilgisi hâlâ eskisi kadar.")
    print()
    print("   n8n akışında üçü birden var:")
    print("     " + SN + "few-shot" + R + "   biçimi tutturur")
    print("     " + SN + "RAG" + R + "        katalog sorusunu cevaplar")
    print("     " + SN + "fine-tune" + R + "  mesajı doğru dala yollar")
    print()
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print()
        sys.exit(0)
