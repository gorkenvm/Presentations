# -*- coding: utf-8 -*-
"""
03_sonra.py — SONRA. Aynı model, üstünde 8 MB'lık LoRA adaptörü.

01_once.py ile BİREBİR aynı sorular, aynı system prompt (ayar.SISTEM),
aynı üretim parametreleri, aynı max_new_tokens. Tek fark: adapter yüklü.

max_new_tokens'ı burada küçültmek hile olurdu. Bütçe hâlâ 120 token;
model eos üretip kendiliğinden duruyor. Gösterilmesi gereken de bu.

Çalıştır:  python 03_sonra.py
           python 03_sonra.py --hizli      Enter beklemez (prova / kayıt)

Gerekli:   adapter/          -> python 02_egit.py
İsteğe:    once_sonuc.json   -> python 01_once.py  (yoksa tablo tek sütun olur)
"""
from __future__ import annotations

import argparse
import json
import sys

import ayar
import motor
from ekran import (CY, KL, KR, MV, R, SN, SR, YS, altbaslik, alan, basarili,
                   basarisiz, baslik, bilgi, duraklat, kutu, tablo, uyari)

SONUC = ayar.KOK / "once_sonuc.json"


def once_sonucunu_oku():
    """01_once.py'nin talimatsız koşusunu okur. Yoksa None döner — çökmez."""
    if not SONUC.exists():
        return None
    try:
        tumu = json.loads(SONUC.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None
    return tumu.get("talimatsiz")


def main():
    ap = argparse.ArgumentParser(description="SONRA — fine-tune'lu model")
    ap.add_argument("--hizli", action="store_true", help="Enter beklemeden akar")
    args = ap.parse_args()

    baslik("03 · SONRA — aynı model + LoRA adaptörü", YS)

    # ── adapter var mı ───────────────────────────────────────────────
    if not (ayar.ADAPTER.exists() and any(ayar.ADAPTER.glob("adapter_model*"))):
        basarisiz(f"{ayar.ADAPTER.name}/ bulunamadı.")
        print()
        bilgi("Önce eğitimi çalıştırın:")
        bilgi("   python 02_egit.py")
        print()
        return 1

    once = once_sonucunu_oku()

    # ── kurulum: 01_once.py ile aynı olduğunu göster ─────────────────
    altbaslik("KURULUM")
    alan("model", ayar.MODEL)
    alan("adapter", f"{ayar.ADAPTER.name}/  "
         f"({sum(f.stat().st_size for f in ayar.ADAPTER.glob('adapter_model*')) / 1024 ** 2:.1f} MB)",
         YS)
    alan("system prompt", "ayar.SISTEM  — 01_once.py ile AYNI")
    alan("üretim", f"do_sample=False (deterministik), "
                   f"max_new_tokens={motor.EN_FAZLA_YENI}  — AYNI")
    print()
    kutu(ayar.SISTEM, "modele giden system prompt — değişmedi", SN)
    print()
    bilgi("Etiket listesi hâlâ isteme yazılmıyor. Model onu ağırlıklarından biliyor.")

    if once is None:
        print()
        uyari("once_sonuc.json yok — karşılaştırma tablosu tek sütun olacak.")
        uyari("İsterseniz önce: python 01_once.py")

    tok, model = motor.yukle(adapter=ayar.ADAPTER)
    duraklat("gösteriye geç")

    # ── gösteri: aynı 5 soru ─────────────────────────────────────────
    baslik("GÖSTERİ — 01_once.py'deki aynı 5 soru", CY)

    test = motor.ornekleri_yukle(ayar.TEST)
    etiket_haritasi = {o["soru"]: o["etiket"] for o in test}
    once_gosteri = {k["soru"]: k for k in (once or {}).get("gosteri", [])}

    gosteri_kayitlari = []
    for sira, soru in enumerate(ayar.GOSTERI_SORULARI, 1):
        etiket = etiket_haritasi.get(soru, "?")
        cikti, token = motor.sor(tok, model, ayar.SISTEM, soru)
        kayit = {"soru": soru, "etiket": etiket, "cikti": cikti, "token": token}
        gosteri_kayitlari.append(kayit)

        print()
        print(CY + KL + f"  [{sira}/{len(ayar.GOSTERI_SORULARI)}]  " + soru + R)
        print(SN + f"  beklenen etiket: {etiket}" + R)
        print()

        eski = once_gosteri.get(soru)
        if eski:
            kutu(eski["cikti"] or "(boş çıktı)",
                 f"ÖNCE — ham model   ({eski['token']} token)", SN)
        kutu(cikti or "(boş çıktı)",
             f"SONRA — fine-tune'lu   ({token} token)", YS)

        tam = motor.tam_esleme(cikti, etiket)
        ic = motor.icinde_geciyor(cikti, etiket)
        gecerli = motor.sadelestir(cikti) in [motor.sadelestir(e)
                                              for e in ayar.ETIKETLER]
        print("  " + (YS + "tam eşleşme  [+]" if tam else KR + "tam eşleşme  [-]") + R
              + "     "
              + (YS + "içinde geçiyor  [+]" if ic else KR + "içinde geçiyor  [-]") + R
              + "     "
              + (YS + "etiket listesinde  [+]" if gecerli
                 else KR + "etiket listesinde  [-]") + R)
        duraklat()

    # ── ölçüm: aynı 10 test sorusu ───────────────────────────────────
    baslik("ÖLÇÜM — aynı 10 test sorusu", CY)
    print()

    def ilerleme(sira, kayit):
        tam = motor.tam_esleme(kayit["cikti"], kayit["etiket"])
        im = (YS + "[+]" + R) if tam else (KR + "[-]" + R)
        print(f"   {sira:>2}/{len(test)}  {im} "
              + (YS if tam else KR) + kayit["cikti"].ljust(12) + R
              + SN + f" (beklenen {kayit['etiket']}, "
                     f"{kayit['token']} token)   {kayit['soru']}" + R,
              flush=True)

    kayitlar = motor.sor_hepsi(tok, model, ayar.SISTEM, test, geri=ilerleme)
    skor = motor.skorla(kayitlar)

    # ── karşılaştırma ────────────────────────────────────────────────
    altbaslik("ÖNCE  /  SONRA")
    toplam = skor["toplam"]

    if once:
        o = once["skor"]
        satirlar = [
            ["tam eşleşme",
             f"{o['tam']}/{o['toplam']}", f"{skor['tam']}/{toplam}"],
            ["içinde geçiyor",
             f"{o['icinde']}/{o['toplam']}", f"{skor['icinde']}/{toplam}"],
            ["ort. üretilen token",
             f"{o['ort_token']:.1f}", f"{skor['ort_token']:.1f}"],
            ["istem (istek başına)",
             f"{once['istem']['talimatsiz']:.0f} token",
             f"{once['istem']['talimatsiz']:.0f} token"],
        ]
        tablo(["ölçü", "ÖNCE (ham)", "SONRA (LoRA)"], satirlar)
        print()
        if o["ort_token"] > 0:
            alan("token tasarrufu",
                 f"{o['ort_token']:.1f} -> {skor['ort_token']:.1f} token  "
                 f"({o['ort_token'] / max(skor['ort_token'], 0.01):.0f}x daha kısa cevap)",
                 YS)
        bilgi(f"ÖNCE koşusu: {once.get('zaman', '?')}")
    else:
        tablo(["ölçü", "SONRA (LoRA)"],
              [["tam eşleşme", f"{skor['tam']}/{toplam}"],
               ["içinde geçiyor", f"{skor['icinde']}/{toplam}"],
               ["ort. üretilen token", f"{skor['ort_token']:.1f}"]])

    # ── kapanış ──────────────────────────────────────────────────────
    altbaslik("BURADA NE GÖRDÜK")
    print()
    if skor["tam"] >= 8:
        print("   Aynı model. Aynı istem. Aynı parametreler.")
        print("   Değişen tek şey: " + KL + "8 MB'lık adapter" + R +
              " — ağırlıkların %0,14'ü.")
        print()
        print("   Modele etiket listesini " + KL + "söylemedik" + R +
              "; davranışını değiştirdik.")
        print("   Artık n8n'deki switch düğümü bu çıktıyı doğrudan okuyabilir.")
    else:
        uyari(f"tam eşleşme {skor['tam']}/{toplam} — beklenen en az 8/10.")
        uyari("Adapter az epokla eğitilmiş olabilir. Ölçülen eğri NOTLAR.md'de;")
        uyari("bu makinede 10 epok 10/10 veriyor, 3 epok 4/10:")
        uyari("   python 02_egit.py --epok 10")
        uyari("ayar.py'ye YAZMAYIN — bayrakla geçin ve hocaya bildirin.")
    print()
    bilgi("Sıradaki:  python 04_sinir.py   — fine-tune neyi ÇÖZMEDİ")
    print()
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print()
        sys.exit(0)
