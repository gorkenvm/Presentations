# -*- coding: utf-8 -*-
"""
prova.py — Bütün demoları baştan sona çalıştırır, süreleri ölçer,
çıktıları yedek/ klasörüne kaydeder.

İki işe yarıyor:
  1) SÜRE      hangi bölüm kaç dakika sürüyor, gerçekten ölçülmüş olsun
  2) YEDEK     atölye günü model beklenmedik bir şey yaparsa,
               kaydedilmiş çıktıdan anlatabilesiniz

Atölyeden önce bir kez çalıştırın:
    python prova.py

Tek bir demoyu yeniden almak için:
    python prova.py 03_rag.py
"""
import os
import pathlib
import subprocess
import sys
import time

KOK = pathlib.Path(__file__).parent
YEDEK = KOK / "yedek"

DEMOLAR = [
    ("00_attention.py", []),
    ("01_prompt.py", []),
    ("02_fewshot.py", []),
    ("03_rag.py", []),
    ("04_finetune.py", []),
    ("05_test.py", []),
    ("05_test.py", ["--ham"]),      # karşılaştırma: adapter'sız hâli
]

# Atölyedeki hedef süreler (dakika) — akis.md'deki plan
HEDEF = {
    "00_attention.py": 3,
    "01_prompt.py": 7,
    "02_fewshot.py": 6,
    "03_rag.py": 14,
    "04_finetune.py": 16,
    "05_test.py": 6,
}


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    secilen = [a for a in sys.argv[1:] if not a.startswith("-")]
    demolar = [(d, b) for d, b in DEMOLAR if not secilen or d in secilen]

    YEDEK.mkdir(exist_ok=True)
    ortam = dict(os.environ)
    ortam["ATOLYE_RENKSIZ"] = "1"
    ortam["PYTHONIOENCODING"] = "utf-8"

    sonuclar = []
    for demo, bayraklar in demolar:
        ad = demo.replace(".py", "") + ("".join(bayraklar).replace("--", "_")
                                        if bayraklar else "")
        hedef = YEDEK / f"{ad}.txt"
        print(f"\n{'=' * 70}\n  {demo} {' '.join(bayraklar)}\n{'=' * 70}", flush=True)

        t0 = time.time()
        p = subprocess.run(
            [sys.executable, demo, "--hizli"] + bayraklar,
            cwd=KOK, env=ortam, capture_output=True, text=True,
            encoding="utf-8", errors="replace")
        sure = time.time() - t0

        hedef.write_text(
            f"# {demo} {' '.join(bayraklar)}\n"
            f"# üretim süresi: {sure:.0f} sn  (Enter beklemeden)\n"
            f"# çıkış kodu: {p.returncode}\n"
            f"{'=' * 70}\n\n{p.stdout}\n"
            + (f"\n--- stderr ---\n{p.stderr}" if p.stderr.strip() else ""),
            encoding="utf-8")

        durum = "OK" if p.returncode == 0 else f"HATA({p.returncode})"
        print(p.stdout[-1500:] if p.returncode else p.stdout[-700:], flush=True)
        if p.returncode:
            print("--- stderr ---\n" + p.stderr[-2000:], flush=True)
        print(f"\n  → {durum}  {sure:.0f} sn  →  yedek/{hedef.name}", flush=True)
        sonuclar.append((demo, bayraklar, durum, sure))

    # ── özet ─────────────────────────────────────────────────────────
    print(f"\n\n{'=' * 70}\n  ÖZET\n{'=' * 70}")
    print(f"  {'demo':<26}{'durum':<10}{'model süresi':>14}{'hedef':>10}")
    print("  " + "-" * 62)
    toplam = 0.0
    for demo, bayraklar, durum, sure in sonuclar:
        toplam += sure
        h = HEDEF.get(demo, 0)
        print(f"  {demo + ' ' + ' '.join(bayraklar):<26}{durum:<10}"
              f"{sure:>11.0f} sn{h:>8} dk")
    print("  " + "-" * 62)
    print(f"  {'TOPLAM':<26}{'':<10}{toplam:>11.0f} sn"
          f"{sum(HEDEF.values()):>8} dk")
    print()
    print("  'model süresi' = sadece üretim. Anlatım ve Enter'lar hariç.")
    print("  Hedefin yarısını geçiyorsa o bölümde en_fazla değerlerini düşürün.")
    print()


if __name__ == "__main__":
    main()
