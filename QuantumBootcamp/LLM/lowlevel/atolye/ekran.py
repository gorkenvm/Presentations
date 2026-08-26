# -*- coding: utf-8 -*-
"""
ekran.py — terminal sunumu.

Bu scriptler projeksiyona yansıyacak; salonun arkasından okunması lazım.
Burada sadece renk / kutu / hizalama var, hiçbir model işi yok.

highlevel/atölye/ortak.py'deki yaklaşımın ihtiyacımız kadarı buraya
kopyalandı — o dosyaya bağımlılık kurmuyoruz, bu klasör tek başına ayakta.

Renkleri kapatmak (çıktıyı dosyaya yazarken):
    set ATOLYE_RENKSIZ=1
"""
from __future__ import annotations

import os
import sys
import textwrap
import unicodedata

import ayar

# ── Windows konsolu: Türkçe karakterler ve ANSI renkleri ─────────────
if sys.platform == "win32":
    try:
        import ctypes
        _k32 = ctypes.windll.kernel32
        _k32.SetConsoleMode(_k32.GetStdHandle(-11), 7)  # VIRTUAL_TERMINAL
    except Exception:
        pass
for _akis in (sys.stdout, sys.stderr):
    try:
        _akis.reconfigure(encoding="utf-8")
    except Exception:
        pass


GENISLIK = 78

# Renk iki sebeple kapanır: ATOLYE_RENKSIZ=1 ya da çıktı bir dosyaya/boruya
# gidiyorsa (kosu_01.log gibi) — kaçış dizileri log dosyasını kirletmesin.
RENKLI = (not ayar.RENKSIZ) and sys.stdout.isatty()

# Bütün scriptlerde ortak bayrak: Enter beklemeden baştan sona akar.
HIZLI = "--hizli" in sys.argv


def _r(kod: str) -> str:
    return kod if RENKLI else ""


R  = _r("\033[0m")
KL = _r("\033[1m")      # kalın
SN = _r("\033[2m")      # sönük
KR = _r("\033[91m")     # kırmızı
YS = _r("\033[92m")     # yeşil
SR = _r("\033[93m")     # sarı
MV = _r("\033[94m")     # mavi
MR = _r("\033[95m")     # mor
CY = _r("\033[96m")     # camgöbeği


def gorunen_uzunluk(metin: str) -> int:
    """ANSI kodlarını ve birleşen aksanları saymadan görünen karakter sayısı."""
    temiz, i = [], 0
    while i < len(metin):
        if metin[i] == "\033":
            while i < len(metin) and metin[i] != "m":
                i += 1
            i += 1
            continue
        temiz.append(metin[i])
        i += 1
    return sum(0 if unicodedata.combining(c) else 1 for c in temiz)


def sar(metin: str, genislik: int) -> list:
    """Metni satırlara böler; mevcut satır sonlarını korur.

    Sadece SARAR — kırpmaz. Model çıktısının tek karakteri bile kaybolmayacak.
    """
    satirlar = []
    for ham in metin.split("\n"):
        if not ham.strip():
            satirlar.append("")
        else:
            satirlar.extend(textwrap.wrap(ham, genislik) or [""])
    return satirlar


def baslik(metin: str, renk: str = CY):
    print()
    print(renk + "═" * GENISLIK + R)
    print(renk + KL + "  " + metin + R)
    print(renk + "═" * GENISLIK + R)


def altbaslik(metin: str, renk: str = SR):
    print()
    print(renk + KL + "▸ " + metin + R)
    print(SN + "─" * GENISLIK + R)


def ayrac():
    print(SN + "─" * GENISLIK + R)


def kutu(metin: str, baslik_: str = "", renk: str = SN, ic: int = GENISLIK - 4):
    """Metni çerçeve içinde basar. Uzun satırları kendisi sarar, kırpmaz."""
    if baslik_:
        ust = "┌─ " + baslik_ + " " + "─" * max(0, ic - gorunen_uzunluk(baslik_) - 1)
    else:
        ust = "┌" + "─" * (ic + 2)
    print(renk + ust + "┐" + R)
    for p in sar(metin, ic):
        bosluk = " " * max(0, ic - gorunen_uzunluk(p))
        print(renk + "│" + R + " " + p + bosluk + " " + renk + "│" + R)
    print(renk + "└" + "─" * (ic + 2) + "┘" + R)


def alan(etiket: str, deger, renk: str = "", genislik: int = 14):
    print(SN + str(etiket).ljust(genislik) + ":" + R + " " + renk + str(deger) + R)


def bilgi(metin: str):
    print(SN + "   " + metin + R)


def basarili(metin: str):
    print(YS + "   [+] " + metin + R)


def basarisiz(metin: str):
    print(KR + "   [-] " + metin + R)


def uyari(metin: str):
    print(SR + "   [!] " + metin + R)


def isaret(tamam: bool, etiket: str, deger: str = "", ipucu: str = "",
           kritik: bool = True):
    """00_kontrol.py'nin satır biçimi:  OK / EKSİK / HATA  etiket : değer."""
    if tamam:
        im = YS + " OK  " + R
    elif kritik:
        im = KR + "HATA " + R
    else:
        im = SR + "EKSİK" + R
    print("  " + im + " " + str(etiket).ljust(22) + SN + ":" + R + " " + str(deger))
    if ipucu and not tamam:
        print("        " + SR + "-> " + ipucu + R)


def cubuk(oran: float, uzunluk: int = 20, renk: str = MV) -> str:
    """0..1 arası bir oranı görsel çubuğa çevirir."""
    dolu = max(0, min(uzunluk, round(oran * uzunluk)))
    return renk + "#" * dolu + SN + "." * (uzunluk - dolu) + R


def tablo(basliklar: list, satirlar: list, renkler: list | None = None):
    """Basit hizalı tablo. renkler: her sütun için ANSI kodu (ya da None)."""
    sutun = len(basliklar)
    genislikler = [gorunen_uzunluk(str(b)) for b in basliklar]
    for s in satirlar:
        for i in range(sutun):
            genislikler[i] = max(genislikler[i], gorunen_uzunluk(str(s[i])))

    def cizgi(sol, orta, sag):
        return SN + sol + orta.join("─" * (g + 2) for g in genislikler) + sag + R

    print(cizgi("┌", "┬", "┐"))
    hucre = [KL + str(b).ljust(genislikler[i]) + R for i, b in enumerate(basliklar)]
    print(SN + "│" + R + " " + (" " + SN + "│" + R + " ").join(hucre) + " " + SN + "│" + R)
    print(cizgi("├", "┼", "┤"))
    for s in satirlar:
        hucre = []
        for i, d in enumerate(s):
            renk = renkler[i] if renkler else ""
            dolgu = " " * max(0, genislikler[i] - gorunen_uzunluk(str(d)))
            hucre.append(renk + str(d) + R + dolgu)
        print(SN + "│" + R + " " + (" " + SN + "│" + R + " ").join(hucre) + " " + SN + "│" + R)
    print(cizgi("└", "┴", "┘"))


def duraklat(mesaj: str = "devam için Enter"):
    """--hizli varsa beklemez. Çıktı dosyaya gidiyorsa da beklemez."""
    if HIZLI or not sys.stdin.isatty():
        print()
        return
    try:
        input("\n" + SN + "   [Enter] " + mesaj + R)
    except EOFError:
        print()
    except KeyboardInterrupt:
        print()
        sys.exit(0)


def yukleniyor(metin: str):
    print(SN + "   " + metin + " ..." + R, flush=True)
