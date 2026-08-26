# -*- coding: utf-8 -*-
"""
ortak.py — Atölyedeki bütün demoların ortak altyapısı.

Üç şey var burada:
  1) Terminali okunur kılan yardımcılar (renk, kutu, duraklat)
  2) Modeli bir kez yükleyip paylaşan  yukle()
  3) Modele soru soran                 sor()

Atölyede bu dosya AÇILMAYACAK. Demolar bunu içeri aktarır; biz çıktıya bakarız.

Ortak bayraklar (her demoda geçerli):
    --hizli   Enter beklemeden akar (prova için)
    --isit    Sadece modeli yükler, bir kelime üretir, çıkar (ders öncesi ısıtma)
"""
from __future__ import annotations

import os
import pathlib
import re
import sys
import textwrap
import unicodedata

# Windows konsolunda Türkçe karakterler ve ANSI renkleri için
if sys.platform == "win32":
    try:
        import ctypes
        _k = ctypes.windll.kernel32
        _k.SetConsoleMode(_k.GetStdHandle(-11), 7)  # ENABLE_VIRTUAL_TERMINAL_PROCESSING
    except Exception:
        pass
for _akis in (sys.stdout, sys.stderr):
    try:
        _akis.reconfigure(encoding="utf-8")
    except Exception:
        pass


# ═════════════════════════════════════════════════════════════════════
#  Ayarlar
# ═════════════════════════════════════════════════════════════════════

# Atölyenin tek modeli. Faz 0 seçim testiyle belirlendi.
# Geçici değiştirmek için:  set ATOLYE_MODEL=...
MODEL = os.environ.get("ATOLYE_MODEL", "Qwen/Qwen2.5-1.5B-Instruct")

# RAG için çok dilli gömme modeli. Türkçe yönetmelikte İngilizce-only
# modeller belirgin şekilde kötü sonuç veriyor.
GOMME_MODELI = os.environ.get("ATOLYE_GOMME", "intfloat/multilingual-e5-small")

# Eğitilmiş LoRA adaptörünün yeri
ADAPTER = os.environ.get("ATOLYE_ADAPTER", "adapter")

HIZLI = "--hizli" in sys.argv

# Boruya yazıyorsak (prova kaydı, dosyaya yönlendirme) renk kapansın
RENKLI = sys.stdout.isatty() and os.environ.get("ATOLYE_RENKSIZ") != "1"


# ═════════════════════════════════════════════════════════════════════
#  Terminal yardımcıları
# ═════════════════════════════════════════════════════════════════════

def _k(kod: str) -> str:
    return kod if RENKLI else ""


R  = _k("\033[0m")
KL = _k("\033[1m")      # kalın
SN = _k("\033[2m")      # sönük
KR = _k("\033[91m")     # kırmızı
YS = _k("\033[92m")     # yeşil
SR = _k("\033[93m")     # sarı
MV = _k("\033[94m")     # mavi
MR = _k("\033[95m")     # mor
CY = _k("\033[96m")     # camgöbeği

GENISLIK = 78


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
    """Metni satırlara böler; mevcut satır sonlarını korur."""
    satirlar = []
    for ham in metin.split("\n"):
        if not ham.strip():
            satirlar.append("")
        else:
            satirlar.extend(textwrap.wrap(ham, genislik) or [""])
    return satirlar


def temizle():
    os.system("cls" if sys.platform == "win32" else "clear")


def baslik(metin: str, renk: str = CY):
    print()
    print(renk + "═" * GENISLIK + R)
    print(renk + KL + "  " + metin + R)
    print(renk + "═" * GENISLIK + R)


def altbaslik(metin: str, renk: str = SR):
    print()
    print(renk + KL + "▸ " + metin + R)
    print(SN + "─" * GENISLIK + R)


def kutu(metin: str, baslik_: str = "", renk: str = SN, ic: int = GENISLIK - 4):
    """Metni çerçeve içinde basar. Uzun satırları kendisi kırar."""
    if baslik_:
        ust = "┌─ " + baslik_ + " " + "─" * max(0, ic - gorunen_uzunluk(baslik_) - 1)
    else:
        ust = "┌" + "─" * (ic + 2)
    print(renk + ust + "┐" + R)
    for p in sar(metin, ic):
        bosluk = " " * max(0, ic - gorunen_uzunluk(p))
        print(renk + "│" + R + " " + p + bosluk + " " + renk + "│" + R)
    print(renk + "└" + "─" * (ic + 2) + "┘" + R)


def alan(etiket: str, deger, renk: str = "", genislik: int = 11):
    print(SN + etiket.ljust(genislik) + ":" + R + " " + renk + str(deger) + R)


def bilgi(metin: str):
    print(SN + "   " + metin + R)


def basarili(metin: str):
    print(YS + "   ✓ " + metin + R)


def basarisiz(metin: str):
    print(KR + "   ✗ " + metin + R)


def duraklat(mesaj: str = "devam için Enter"):
    if HIZLI:
        print()
        return
    try:
        input("\n" + SN + "   ⏎ " + mesaj + R)
    except (EOFError, KeyboardInterrupt):
        print()
        sys.exit(0)


def cubuk(oran: float, uzunluk: int = 22, renk: str = MV) -> str:
    """0..1 arası bir oranı görsel çubuğa çevirir."""
    dolu = max(0, min(uzunluk, round(oran * uzunluk)))
    return renk + "█" * dolu + SN + "·" * (uzunluk - dolu) + R


# ═════════════════════════════════════════════════════════════════════
#  Korpus — RAG'in okuduğu belge
# ═════════════════════════════════════════════════════════════════════

KOK = pathlib.Path(__file__).parent
KORPUS = KOK / "veri" / "miuul_katalog.md"


def parcala(yol: pathlib.Path | None = None) -> list:
    """Belgeyi parçalara böler ("chunking" — RAG'in ilk adımı).

    Kural basit: kendi başına bir satırda duran **kalın başlık** yeni bir
    parça başlatır; altındaki satırlar o parçanın gövdesidir.

    Burada işimiz kolay, çünkü belgeyi biz üretirken zaten başlıklara
    ayırdık. Gerçek hayatta parçalama stratejisi RAG kalitesinin yarısıdır:
    çok küçük parçalarsanız bağlam kopar, çok büyük tutarsanız arama şaşar.

    Döner: [{"no": 44, "baslik": "Eğitim 44 — Data Scientist Path",
             "ad": "Data Scientist Path", "metin": "...",
             "tam": "başlık\\nmetin"}, ...]
    """
    ham = (yol or KORPUS).read_text(encoding="utf-8")
    desen = re.compile(r"^\*\*([^*\n]+?)\*\*\s*$", re.MULTILINE)

    vurus = list(desen.finditer(ham))
    parcalar = []
    for i, m in enumerate(vurus):
        son = vurus[i + 1].start() if i + 1 < len(vurus) else len(ham)
        govde = re.sub(r"\n{2,}", "\n", ham[m.end():son].replace("**", "")).strip()
        if not govde:
            continue
        baslik_ = m.group(1).strip()
        sayi = re.search(r"(\d+)", baslik_)
        # "Eğitim 44 — Data Scientist Path" → ad = "Data Scientist Path"
        ad = re.sub(r"^[^—\-–]*[—\-–]\s*", "", baslik_).strip() or baslik_
        parcalar.append({
            "no": int(sayi.group(1)) if sayi else None,
            "baslik": baslik_,
            "ad": ad,
            "metin": govde,
            "tam": baslik_ + "\n" + govde,
        })
    return parcalar


def parca_bul(anahtar: str, yol: pathlib.Path | None = None) -> dict | None:
    """Başlığında verilen metin geçen ilk parçayı getirir.

    Demolarda "gerçek cevap bu" diye gösterdiğimiz parçayı buradan
    alıyoruz — elle kopyalamıyoruz ki belge değişirse demo da değişsin.
    """
    anahtar = anahtar.casefold()
    for p in parcala(yol):
        if anahtar in p["baslik"].casefold():
            return p
    return None


# ═════════════════════════════════════════════════════════════════════
#  Model
# ═════════════════════════════════════════════════════════════════════

_tok = None
_model = None


def cihaz_bilgisi():
    import torch
    if torch.cuda.is_available():
        return "cuda", torch.float16
    return "cpu", torch.float32


def yukle(attention_ile: bool = False, adapter: str | None = None):
    """Modeli bir kez yükler, sonraki çağrılarda aynısını döndürür.

    attention_ile=True  → attention matrisleri okunabilsin diye eager attention
    adapter='adapter'   → eğitilmiş LoRA adaptörünü üstüne bindirir
    """
    global _tok, _model
    if _model is not None and adapter is None:
        return _tok, _model

    from transformers import AutoModelForCausalLM, AutoTokenizer

    cihaz, veri_tipi = cihaz_bilgisi()

    if _model is None:
        print(SN + "   model yükleniyor: " + MODEL + "  (" + cihaz + ")" + R, flush=True)
        _tok = AutoTokenizer.from_pretrained(MODEL)
        _model = AutoModelForCausalLM.from_pretrained(
            MODEL,
            dtype=veri_tipi,
            attn_implementation="eager" if attention_ile else "sdpa",
        ).to(cihaz)
        _model.eval()

    if adapter:
        from peft import PeftModel
        print(SN + "   LoRA adaptörü bindiriliyor: " + adapter + R, flush=True)
        _model = PeftModel.from_pretrained(_model, adapter)
        _model.eval()

    return _tok, _model


def token_say(metin: str) -> int:
    tok, _ = yukle()
    return len(tok(metin)["input_ids"])


def sor(sistem: str,
        kullanici: str = "",
        sicaklik: float = 0.0,
        en_fazla: int = 180,
        mesajlar: list | None = None,
        tohum: int | None = None) -> str:
    """Modele bir soru sorar, cevabın metnini döndürür.

    sicaklik=0  → greedy, hep aynı cevap (tekrarlanabilir demolar için)
    sicaklik>0  → örnekleme, her seferinde farklı cevap (halüsinasyon demosu)
    mesajlar    → çok turlu konuşma (araç sonucunu modele geri verirken)
    """
    import torch
    tok, model = yukle()

    if mesajlar is None:
        mesajlar = []
        if sistem:
            mesajlar.append({"role": "system", "content": sistem})
        mesajlar.append({"role": "user", "content": kullanici})

    metin = tok.apply_chat_template(mesajlar, tokenize=False, add_generation_prompt=True)
    girdi = tok(metin, return_tensors="pt").to(model.device)

    if tohum is not None:
        torch.manual_seed(tohum)

    with torch.no_grad():
        cikti = model.generate(
            **girdi,
            max_new_tokens=en_fazla,
            do_sample=sicaklik > 0,
            temperature=sicaklik if sicaklik > 0 else None,
            top_p=0.9 if sicaklik > 0 else None,
            pad_token_id=tok.eos_token_id,
        )
    yeni = cikti[0][girdi["input_ids"].shape[1]:]
    return tok.decode(yeni, skip_special_tokens=True).strip()


def isit():
    """Ders öncesi: modeli yükle, ilk çağrının gecikmesi salonda geçmesin."""
    import time
    baslik("ISITMA — ders öncesi bir kez çalıştırın", MV)
    t0 = time.time()
    yukle()
    t1 = time.time()
    cevap = sor("Kısa cevap ver.", "Merhaba.", en_fazla=20)
    t2 = time.time()
    alan("yükleme", "%.1f sn" % (t1 - t0))
    alan("üretim", "%.1f sn" % (t2 - t1))
    alan("cevap", cevap[:60])
    print()
    basarili("model hazır. Artık ilk çağrı hızlı olacak.")
    print()


if __name__ == "__main__":
    if "--isit" in sys.argv:
        isit()
    else:
        print(__doc__)
