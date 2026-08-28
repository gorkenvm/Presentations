# -*- coding: utf-8 -*-
"""
01_once.py — ÖNCE. Ham model, adapter yok.

n8n akışına bir kapı bekçisi lazımdı: gelen mesaj hangi dala gitmeli?
Beklediğimiz tek kelime. Bakalım ham model ne yapıyor.

Bu script modele NE İSTEDİĞİMİZİ SÖYLEMİYOR. system prompt sadece
"Sen Miuul eğitim platformunun öğrenci destek asistanısın." (ayar.SISTEM).
Etiket listesini vermiyoruz — verseydik zaten yapardı, o ayrı bir deney:

    python 01_once.py --talimatli

Çalıştır:  python 01_once.py
           python 01_once.py --hizli        Enter beklemez (prova / kayıt)
           python 01_once.py --talimatli    etiketleri SAYAN system prompt

Üretir:    once_sonuc.json   — 03_sonra.py karşılaştırma tablosunda kullanıyor
"""
from __future__ import annotations

import argparse
import datetime
import json
import sys

import ayar
import motor
from ekran import (CY, KL, KR, MV, R, SN, SR, YS, altbaslik, alan, basarili,
                   baslik, bilgi, duraklat, kutu, tablo, uyari)

SONUC = ayar.KOK / "once_sonuc.json"


# ═════════════════════════════════════════════════════════════════════
#  Ekran parçaları — 03_sonra.py da aynı biçimi kullanıyor
# ═════════════════════════════════════════════════════════════════════

def soru_cevap_bas(sira: int, toplam: int, kayit: dict):
    """Bir soruyu ve modelin HAM cevabını basar. Kırpma yok."""
    print()
    print(CY + KL + f"  [{sira}/{toplam}]  " + kayit["soru"] + R)
    print(SN + f"  beklenen etiket: {kayit['etiket']}" + R)
    print()
    kutu(kayit["cikti"] if kayit["cikti"] else "(boş çıktı)",
         "modelin cevabı — ham, kırpılmadı", SN)

    tam = motor.tam_esleme(kayit["cikti"], kayit["etiket"])
    ic = motor.icinde_geciyor(kayit["cikti"], kayit["etiket"])
    print("  " + (YS + "tam eşleşme  [+]" if tam else KR + "tam eşleşme  [-]") + R
          + "     "
          + (YS + "içinde geçiyor  [+]" if ic else KR + "içinde geçiyor  [-]") + R
          + "     " + SN + f"{kayit['token']} token üretildi" + R)


def ilerleme_bas(sira: int, toplam: int, kayit: dict):
    """Ölçüm turunda tek satırlık ilerleme. Çıktı metni burada gösterilmiyor
    (kırpmamak için); tamamı once_sonuc.json içine yazılıyor."""
    tam = motor.tam_esleme(kayit["cikti"], kayit["etiket"])
    ic = motor.icinde_geciyor(kayit["cikti"], kayit["etiket"])
    im = (YS + "[+]" + R) if tam else (KR + "[-]" + R)
    im2 = (YS + "[+]" + R) if ic else (SN + "[ ]" + R)
    print(f"   {sira:>2}/{toplam}  {im} tam  {im2} içinde  "
          + SN + f"{kayit['token']:>3} token" + R
          + SN + "   " + kayit["soru"] + R, flush=True)


def skor_bas(skor: dict, baslik_: str = "SKOR"):
    altbaslik(baslik_)
    toplam = skor["toplam"]
    alan("tam eşleşme", f"{skor['tam']}/{toplam}"
         f"   (%{100 * skor['tam'] / toplam:.0f})",
         YS if skor["tam"] >= 0.8 * toplam else KR)
    alan("içinde geçiyor", f"{skor['icinde']}/{toplam}"
         f"   (%{100 * skor['icinde'] / toplam:.0f})", SR)
    alan("ort. token", f"{skor['ort_token']:.1f}")


def istem_maliyeti_bas(olcu: dict):
    """Talimatlı istem ne kadar pahalı — 04_sinir.py'de tekrar kullanılıyor."""
    altbaslik("İSTEM MALİYETİ")
    bilgi(f"{olcu['soru_sayisi']} soru, chat şablonu dahil, istek başına ortalama")
    print()
    tablo(
        ["system prompt", "sadece system", "istek başına istem"],
        [["ayar.SISTEM  (kısa)",
          f"{olcu['sistem_talimatsiz']} token",
          f"{olcu['talimatsiz']:.0f} token"],
         ["ayar.TALIMATLI_SISTEM",
          f"{olcu['sistem_talimatli']} token",
          f"{olcu['talimatli']:.0f} token"]],
    )
    print()
    alan("fark", f"+{olcu['fark']:.0f} token / istek", SR)
    alan("kat", f"{olcu['kat']:.1f}x daha pahalı istem", SR)


# ═════════════════════════════════════════════════════════════════════

def sonucu_kaydet(kip: str, veri: dict):
    """once_sonuc.json'a yazar. İki kipin sonucu da korunur:
    --talimatli koşusu talimatsız koşunun sonucunu silmesin."""
    tumu = {}
    if SONUC.exists():
        try:
            tumu = json.loads(SONUC.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            tumu = {}
    tumu[kip] = veri
    SONUC.write_text(json.dumps(tumu, ensure_ascii=False, indent=1),
                     encoding="utf-8")


def main():
    ap = argparse.ArgumentParser(description="ÖNCE — ham model")
    ap.add_argument("--hizli", action="store_true", help="Enter beklemeden akar")
    ap.add_argument("--talimatli", action="store_true",
                    help="ayar.TALIMATLI_SISTEM kullan (etiketleri sayan istem)")
    args = ap.parse_args()

    kip = "talimatli" if args.talimatli else "talimatsiz"
    sistem = ayar.TALIMATLI_SISTEM if args.talimatli else ayar.SISTEM

    baslik("01 · ÖNCE — ham model, fine-tune yok"
           + ("   [TALİMATLI İSTEM]" if args.talimatli else ""), MV)

    # ── kurulum ──────────────────────────────────────────────────────
    altbaslik("KURULUM")
    alan("model", ayar.MODEL)
    alan("adapter", "YOK — ham ağırlıklar", SN)
    alan("system prompt",
         "ayar.TALIMATLI_SISTEM" if args.talimatli else "ayar.SISTEM")
    alan("üretim", f"do_sample=False (deterministik), "
                   f"max_new_tokens={motor.EN_FAZLA_YENI}")
    alan("beklenen", "tek kelime: " + " / ".join(ayar.ETIKETLER))
    print()
    kutu(sistem, "modele giden system prompt", SN)

    if not args.talimatli:
        print()
        bilgi("Dikkat: bu istemde etiketlerin adı GEÇMİYOR. Modele ne")
        bilgi("istediğimizi söylemiyoruz — fine-tune'un işi tam olarak bunu")
        bilgi("söylemeden öğretmek.")

    tok, model = motor.yukle()

    # Modele giden tam metin — chat şablonu uygulanmış hâli
    altbaslik("MODELE GİDEN TAM METİN  (chat şablonu uygulanmış)")
    kutu(motor.istem_metni(tok, sistem, ayar.GOSTERI_SORULARI[0]),
         "ilk soru için", SN)
    duraklat("gösteriye geç")

    # ── gösteri: 5 soru, tek tek ─────────────────────────────────────
    baslik("GÖSTERİ — 5 soru, ham modelin cevabı", CY)

    # Gösteri soruları test.jsonl'den seçildi; doğru etiketi oradan alıyoruz.
    test = motor.ornekleri_yukle(ayar.TEST)
    etiket_haritasi = {o["soru"]: o["etiket"] for o in test}
    gosteri = [{"soru": s, "etiket": etiket_haritasi.get(s, "?")}
               for s in ayar.GOSTERI_SORULARI]

    gosteri_kayitlari = []
    for sira, o in enumerate(gosteri, 1):
        cikti, token = motor.sor(tok, model, sistem, o["soru"])
        kayit = {"soru": o["soru"], "etiket": o["etiket"],
                 "cikti": cikti, "token": token}
        gosteri_kayitlari.append(kayit)
        soru_cevap_bas(sira, len(gosteri), kayit)
        duraklat()

    # ── ölçüm: test setinin 10'u ─────────────────────────────────────
    baslik("ÖLÇÜM — test setinin 10 sorusu (model bunları eğitimde görmedi)", CY)
    bilgi("tam eşleşme   : çıktının TAMAMI etikete eşit  (küçük harf, noktalama atılmış)")
    bilgi("içinde geçiyor: etiket kelimesi çıktının herhangi bir yerinde geçiyor")
    bilgi("ikinci ölçü dürüstlük içindir — ham model bazen doğru kelimeyi")
    bilgi("cümlenin içinde söylüyor; bunu sıfır saymak haksızlık olurdu.")
    print()

    test_kayitlari = motor.sor_hepsi(
        tok, model, sistem, test,
        geri=lambda sira, kayit: ilerleme_bas(sira, len(test), kayit))

    skor = motor.skorla(test_kayitlari)
    skor_bas(skor)
    print()
    bilgi("Ham çıktıların tamamı once_sonuc.json içine yazıldı — hiçbiri kırpılmadı.")

    # ── istem maliyeti ───────────────────────────────────────────────
    olcu = motor.istem_karsilastir(tok, [o["soru"] for o in test])
    istem_maliyeti_bas(olcu)

    # ── kaydet ───────────────────────────────────────────────────────
    sonucu_kaydet(kip, {
        "model": ayar.MODEL,
        "kip": kip,
        "sistem": sistem,
        "en_fazla_yeni": motor.EN_FAZLA_YENI,
        "zaman": datetime.datetime.now().isoformat(timespec="seconds"),
        "skor": skor,
        "istem": olcu,
        "gosteri": gosteri_kayitlari,
        "test": test_kayitlari,
    })

    # ── kapanış ──────────────────────────────────────────────────────
    altbaslik("BURADA NE GÖRDÜK")
    print()
    if args.talimatli:
        # Etiketleri SAYAN istem: biçim düzelir, peki ya isabet?
        print("   Etiket listesini isteme yazdık. " + KL + "Biçim düzeldi" + R +
              f" — ortalama {skor['ort_token']:.1f} token,")
        print("   artık paragraf değil tek kelime.")
        print()
        print("   Ama isabet: " + KL + f"{skor['tam']}/{skor['toplam']}" + R +
              f".  Bedeli: istek başına {olcu['talimatli']:.0f} token, "
              f"{olcu['kat']:.1f} kat.")
        print()
        print("   " + SN + "Dersin tezi tam olarak bu:" + R)
        print("   " + SN + "prompt BİÇİMİ düzeltir; davranışı fine-tune değiştirir." + R)
        print("   " + SN + "Karşılaştırmak için: python 03_sonra.py" + R)
    elif skor["tam"] >= 0.8 * skor["toplam"]:
        uyari("Ham model zaten tek kelime veriyor. Demonun kontrastı kalmadı —")
        uyari("hocaya haber verin. ayar.py'yi kendi başınıza değiştirmeyin.")
        uyari("Denenecek: set ATOLYE_MODEL=Qwen/Qwen2.5-0.5B-Instruct")
    else:
        print("   Model soruyu " + KL + "anlıyor" + R +
              " ama bizim istediğimiz " + KL + "biçimde" + R + " cevaplamıyor.")
        print("   Paragraf yazıyor; n8n'deki switch düğümü bunu okuyamaz.")
        print()
        print("   " + SN + "Soru: bunu prompt ile de yapamaz mıydık?" + R)
        print("   " + SN + "Dürüst cevap:  python 01_once.py --talimatli" + R)
        print("   " + SN + "Bedeli yukarıdaki İSTEM MALİYETİ tablosunda." + R)
    print()
    basarili(f"sonuç kaydedildi -> {SONUC.name}  (kip: {kip})")
    print()
    bilgi("Sıradaki:  python 03_sonra.py" if args.talimatli
          else "Sıradaki:  python 02_egit.py")
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
        sys.exit(0)
