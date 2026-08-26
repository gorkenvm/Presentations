# -*- coding: utf-8 -*-
"""
araclar.py — Kayıt veritabanına bakan üç fonksiyon.

Atölyenin kilit cümlesi burada saklı:
    Bu fonksiyonlar Python'da duruyor, modelin İÇİNDE değil.
    Model bunları çalıştırmıyor — sadece "şunu çağır" diye bir metin üretiyor.
    Çağıran, bizim programımız.

Fine-tune'un öğrettiği şey yetenek değil, alışkanlık: hafızadan cevaplamak
yerine doğru JSON'u üretme alışkanlığı.

NOT: veri/kayitlar.json'daki kişiler tamamen kurgudur. Katalog gerçek,
öğrenciler değil.
"""
from __future__ import annotations

import json
import pathlib
import re

VERI = pathlib.Path(__file__).parent / "veri" / "kayitlar.json"

with open(VERI, encoding="utf-8") as f:
    KAYITLAR = json.load(f)


# ═════════════════════════════════════════════════════════════════════
#  Üç araç
# ═════════════════════════════════════════════════════════════════════

def ilerleme_durumu(no: str) -> str:
    """Öğrencinin aktif eğitimindeki ilerleme yüzdesini döndürür."""
    k = KAYITLAR.get(str(no).strip())
    if not k:
        return f"{no} numaralı kayıt bulunamadı."
    i = k["ilerleme"]
    return (f"{k['ad']} — {k['aktif_egitim']}: "
            f"%{i['yuzde']} tamamlandı "
            f"({i['tamamlanan_modul']}/{i['toplam_modul']} modül)")


def canli_ders_programi(no: str) -> str:
    """Öğrencinin haftalık canlı ders takvimini döndürür."""
    k = KAYITLAR.get(str(no).strip())
    if not k:
        return f"{no} numaralı kayıt bulunamadı."
    if not k["canli_ders"]:
        return (f"{k['ad']} — {k['aktif_egitim']} video tabanlı bir program, "
                f"canlı ders yok. Kendi hızınızda ilerliyorsunuz.")
    dersler = [f"{d['gun']} {d['saat']} — {d['konu']}" for d in k["canli_ders"]]
    return f"{k['ad']} — canlı ders takvimi: " + "; ".join(dersler)


def odeme_durumu(no: str) -> str:
    """Öğrencinin ödenmemiş eğitim ücreti bakiyesini döndürür."""
    k = KAYITLAR.get(str(no).strip())
    if not k:
        return f"{no} numaralı kayıt bulunamadı."
    o = k["odeme"]
    if o["kalan_usd"] == 0:
        return f"{k['ad']} — ödemesi tamamlanmış, kalan borç yok."
    return (f"{k['ad']} — toplam {o['toplam_usd']} USD, "
            f"ödenen {o['odenen_usd']} USD, "
            f"kalan {o['kalan_usd']} USD")


ARACLAR = {
    "ilerleme_durumu": ilerleme_durumu,
    "canli_ders_programi": canli_ders_programi,
    "odeme_durumu": odeme_durumu,
}


# ── İki sistem promptu ───────────────────────────────────────────────
#
# Atölyenin 04. bölümü bu ikisini karşılaştırıyor:
#
#   ARAC_TARIFI  uzun. Araçları tarif eder. Ham modelin araç çağırabilmesi
#                için ŞART — ve bedeli her istekte tekrar ödenir.
#   KISA_SISTEM  kısa. Hiçbir araçtan söz etmez. Ham model bununla araç
#                çağıramaz; fine-tune edilmiş model çağırabilir.
#
# Eğitimi KISA_SISTEM ile yapıyoruz. Ölçülebilir iddia şu:
# fine-tune, uzun talimatı modele gömdü — artık göndermiyoruz.

KISA_SISTEM = "Sen Miuul eğitim platformunun öğrenci destek asistanısın."

ARAC_TARIFI = """Sen Miuul eğitim platformunun öğrenci destek asistanısın.

Öğrenciye özel bilgiler için aşağıdaki araçlardan birini çağır.
Araç çağırırken SADECE tek satır JSON yaz, başka hiçbir şey yazma:
{"tool": "<araç adı>", "args": {"no": "<kayıt numarası>"}}

Araçlar:
- ilerleme_durumu      : öğrencinin eğitimindeki ilerleme yüzdesi
- canli_ders_programi  : öğrencinin haftalık canlı ders takvimi
- odeme_durumu         : öğrencinin kalan eğitim ücreti borcu

Kayıt numarası verilmemişse araç çağırma, numarayı sor.
Katalog ve eğitim içeriği soruları araçla cevaplanmaz; bunlarda tek satır yaz:
Bu soru için araç gerekmiyor.
Selamlaşma ve sohbette normal, kısa bir cevap ver."""

ARACSIZ_CEVAP = "Bu soru için araç gerekmiyor."

# Beş adımlı akışın 4. adımı: aracın sonucunu modele GERİ verirken
# kullandığımız kalıp. Eğitimde ve çıkarımda AYNI metin olmak zorunda —
# aksi halde model eğitildiği durumu tanımaz.
ARAC_SONUC_ISTEMI = "ARAÇ SONUCU: {sonuc}\n\nBu sonucu öğrenciye tek cümleyle söyle."


# ═════════════════════════════════════════════════════════════════════
#  Ayrılmış test seti
# ═════════════════════════════════════════════════════════════════════
#
# Beş soru. Hiçbiri veri/ornekler.jsonl'de YOK — ne bu ifadeyle, ne de
# bu (araç, numara) ikilisiyle. Ezber değil, genelleme ölçüyoruz.
#
# Beş soru gerçek bir değerlendirme değil, göz kararıdır. Bunu atölyede
# söylüyoruz: en büyük eksiğimiz bu.

TEST_SORULARI = [
    # (soru, beklenen araç ya da None, beklenen numara)
    ("482289 numaralı öğrencinin ilerlemesi ne durumda?", "ilerleme_durumu", "482289"),
    ("Perşembe günü canlı dersim var mı? Kayıt no 482241", "canli_ders_programi", "482241"),
    ("482215 numaralı kaydın kalan ödemesi ne kadar?", "odeme_durumu", "482215"),
    ("Bootcamp programları video tabanlı mı, canlı mı?", None, None),
    ("Nasıl gidiyor, iyi misin?", None, None),
]

# 04'te ÖNCE/SONRA karşılaştırması sadece araç gerektirenlerle yapılıyor
ARAC_TESTLERI = [t for t in TEST_SORULARI if t[1] is not None]


def puanla(cevap: str, beklenen_arac, beklenen_no):
    """Bir cevabı ayrılmış test setine göre puanlar.

    Döner: (dogru_mu, aciklama)
    """
    cagri = ayristir(cevap)
    if beklenen_arac is None:
        # Araç gerekmiyordu: JSON basmamış olmalı
        if cagri is None:
            return True, "araç çağırmadı"
        return False, f"gereksiz araç çağırdı: {cagri.get('tool')}"

    if not gecerli_mi(cagri):
        return False, "geçerli araç çağrısı yok"
    if cagri["tool"] != beklenen_arac:
        return False, f"yanlış araç: {cagri['tool']}"
    if str(cagri["args"]["no"]).strip() != beklenen_no:
        return False, f"yanlış numara: {cagri['args']['no']}"
    return True, ozet(cagri)


# ═════════════════════════════════════════════════════════════════════
#  Model çıktısını ayrıştırma
# ═════════════════════════════════════════════════════════════════════

def _ilk_json_blogu(metin: str) -> str | None:
    """Metindeki ilk dengeli { ... } bloğunu çıkarır."""
    basla = metin.find("{")
    if basla == -1:
        return None
    derinlik = 0
    for i in range(basla, len(metin)):
        if metin[i] == "{":
            derinlik += 1
        elif metin[i] == "}":
            derinlik -= 1
            if derinlik == 0:
                return metin[basla:i + 1]
    return None


def ayristir(metin: str) -> dict | None:
    """Model çıktısından araç çağrısını çıkarır. Çıkaramazsa None.

    Bilerek toleranslı: ```json çitleri, tek tırnak, baştaki laf salatası —
    hepsini affeder. Yine de başarısızsa model gerçekten JSON üretmemiştir.
    """
    if not metin:
        return None
    temiz = re.sub(r"```(?:json)?", "", metin).strip()
    blok = _ilk_json_blogu(temiz)
    if blok is None:
        return None
    for aday in (blok, blok.replace("'", '"')):
        try:
            v = json.loads(aday)
        except Exception:
            continue
        if isinstance(v, dict) and "tool" in v:
            return v
    return None


def gecerli_mi(cagri: dict | None) -> bool:
    """Ayrıştırılan çağrı gerçekten çalıştırılabilir mi?"""
    if not isinstance(cagri, dict):
        return False
    if cagri.get("tool") not in ARACLAR:
        return False
    args = cagri.get("args")
    return isinstance(args, dict) and bool(str(args.get("no", "")).strip())


def calistir(cagri: dict) -> str:
    """Ayrıştırılmış çağrıyı gerçekten çalıştırır."""
    fn = ARACLAR[cagri["tool"]]
    return fn(str(cagri["args"]["no"]).strip())


def ozet(cagri: dict) -> str:
    """Çağrıyı okunur tek satıra çevirir: ilerleme_durumu("482137")"""
    return f'{cagri["tool"]}("{cagri["args"]["no"]}")'


if __name__ == "__main__":
    import sys
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    print(ilerleme_durumu("482137"))
    print(odeme_durumu("482154"))
    print(canli_ders_programi("482137"))
    print(canli_ders_programi("482166"))
    print(ilerleme_durumu("999999"))
    print("---")
    for ham in ['{"tool":"ilerleme_durumu","args":{"no":"482137"}}',
                '```json\n{"tool": "odeme_durumu", "args": {"no": "482154"}}\n```',
                "İlerlemenizi öğrenmek için panelinize giriş yapmanız gerekir.",
                "{'tool': 'canli_ders_programi', 'args': {'no': '482241'}}"]:
        c = ayristir(ham)
        print(f"{str(c):<64} gecerli={gecerli_mi(c)}")
