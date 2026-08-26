# -*- coding: utf-8 -*-
"""
motor.py — model yükleme, üretim ve ölçüm.

Neden ayrı dosya: 01_once.py ile 03_sonra.py'nin modele giden girdisi
BİREBİR AYNI olmak zorunda (brief §3, kural 1). Aynı kodu iki dosyaya
kopyalarsak er ya da geç biri kayar. Üretim parametreleri burada, tek yerde:

    EN_FAZLA_YENI = 120     ÖNCE de SONRA da aynı bütçeyle üretir
    do_sample     = False   deterministik; her koşuda aynı çıktı

SONRA için max_new_tokens'ı küçültmek hile olurdu — fine-tune'lu model
eos üretip kendiliğinden duruyor, gösterilmesi gereken de tam olarak bu.

Ölçüm yardımcıları (sadelestir / skorla / istem_karsilastir) da burada:
01_once.py ile 04_sinir.py aynı ölçüyü kullansın.
"""
from __future__ import annotations

import json
import re
import unicodedata

import ayar
from ekran import R, SN

# ── üretim parametreleri — ÖNCE ve SONRA için ORTAK ──────────────────
EN_FAZLA_YENI = 120


# ═════════════════════════════════════════════════════════════════════
#  Veri
# ═════════════════════════════════════════════════════════════════════

def ornekleri_yukle(yol) -> list:
    """jsonl dosyasını okur, sözlük listesi döndürür (soru + etiket)."""
    ornekler = []
    with open(yol, encoding="utf-8") as f:
        for satir in f:
            satir = satir.strip()
            if satir:
                ornekler.append(json.loads(satir))
    return ornekler


# ═════════════════════════════════════════════════════════════════════
#  Ölçüm
# ═════════════════════════════════════════════════════════════════════

# Harf, rakam ve alt çizgi dışındaki her şey atılır.
# Alt çizgi KALIR — canli_ders tek kelime sayılıyor.
_NOKTALAMA = re.compile(r"[^\w\s]", re.UNICODE)


def sadelestir(metin: str) -> str:
    """Karşılaştırma için normalleştirir: küçük harfe indir, noktalamayı at.

    Ayrıca birleşen aksanları düşürür. İki sebebi var:
      - Python'da büyük noktalı I harfinin lower() hali İKİ karakter üretir
        (i + birleşen nokta). Aksan düşmezse öyle bir çıktı hiçbir zaman
        "ilerleme" etiketine eşit olamaz — ölçüm yalan söyler.
      - Model "ödeme" yazarsa "odeme" etiketiyle eşleşsin.

    Bu esneklik sadece HAM modelin lehine çalışır; fine-tune'lu model
    etiketi zaten harfi harfine yazıyor. Ham modele haksızlık etmeyelim.
    """
    m = unicodedata.normalize("NFD", metin.lower())
    m = "".join(c for c in m if not unicodedata.combining(c))
    m = _NOKTALAMA.sub("", m)
    return " ".join(m.split())


def tam_esleme(cikti: str, etiket: str) -> bool:
    """Çıktının TAMAMI etikete eşit mi. Asıl ölçü bu."""
    return sadelestir(cikti) == sadelestir(etiket)


def icinde_geciyor(cikti: str, etiket: str) -> bool:
    """Etiket kelimesi çıktının herhangi bir yerinde geçiyor mu.

    Ham model bazen "bu bir ilerleme sorusu" diyor; bunu sıfır saymak
    haksızlık olur. Ama tam eşleşme OLMADIĞINI da göstermek gerekir —
    o yüzden iki skoru yan yana basıyoruz.
    """
    desen = r"(?<!\w)" + re.escape(sadelestir(etiket)) + r"(?!\w)"
    return re.search(desen, sadelestir(cikti)) is not None


def skorla(kayitlar: list) -> dict:
    """Kayıt listesini iki skora ve ortalama token sayısına indirger."""
    tam = sum(1 for k in kayitlar if tam_esleme(k["cikti"], k["etiket"]))
    icinde = sum(1 for k in kayitlar if icinde_geciyor(k["cikti"], k["etiket"]))
    tokenlar = [k["token"] for k in kayitlar]
    return {
        "toplam": len(kayitlar),
        "tam": tam,
        "icinde": icinde,
        "ort_token": sum(tokenlar) / len(tokenlar) if tokenlar else 0.0,
    }


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


def yukle(adapter=None, sessiz: bool = False):
    """Ham modeli yükler; adapter verilirse LoRA'yı üstüne bindirir.

    cache_dir / HF_HOME BİLEREK ayarlanmıyor: model varsayılan Hugging Face
    önbelleğinde duruyor, farklı yol verirsek 3 GB yeniden iner.
    """
    global _tok, _model
    from transformers import AutoModelForCausalLM, AutoTokenizer

    cihaz, veri_tipi = cihaz_bilgisi()

    if _model is None:
        if not sessiz:
            print(SN + "   model yükleniyor: " + ayar.MODEL +
                  "  (" + cihaz + ") ..." + R, flush=True)
        _tok = AutoTokenizer.from_pretrained(ayar.MODEL)
        _model = AutoModelForCausalLM.from_pretrained(
            ayar.MODEL, dtype=veri_tipi, attn_implementation="sdpa").to(cihaz)
        _model.eval()

    if adapter is not None:
        from peft import PeftModel
        if not sessiz:
            print(SN + "   LoRA adaptörü bindiriliyor: " +
                  str(adapter) + " ..." + R, flush=True)
        _model = PeftModel.from_pretrained(_model, str(adapter))
        _model.eval()

    return _tok, _model


def mesajlari_kur(sistem: str, soru: str) -> list:
    """Tek yerden: eğitim de, ÖNCE de, SONRA da bu biçimi kullanıyor."""
    return [{"role": "system", "content": sistem},
            {"role": "user", "content": soru}]


def istem_metni(tok, sistem: str, soru: str) -> str:
    """Chat şablonu uygulanmış, modele giden ham istem metni."""
    return tok.apply_chat_template(
        mesajlari_kur(sistem, soru), tokenize=False, add_generation_prompt=True)


def sor(tok, model, sistem: str, soru: str, en_fazla: int = EN_FAZLA_YENI):
    """Modele bir soru sorar. Döner: (ham_cikti, uretilen_token_sayisi).

    Çıktı olduğu gibi döner — kırpma, düzeltme, regex yok.
    """
    import torch

    girdi = tok(istem_metni(tok, sistem, soru),
                return_tensors="pt", add_special_tokens=False).to(model.device)

    with torch.no_grad():
        cikti = model.generate(
            **girdi,
            max_new_tokens=en_fazla,
            do_sample=False,                 # deterministik
            pad_token_id=tok.eos_token_id,
        )

    yeni = cikti[0][girdi["input_ids"].shape[1]:]
    ozel = {tok.eos_token_id, tok.pad_token_id}
    uretilen = sum(1 for t in yeni.tolist() if t not in ozel)
    return tok.decode(yeni, skip_special_tokens=True).strip(), uretilen


def sor_hepsi(tok, model, sistem: str, ornekler: list, geri=None) -> list:
    """Bir örnek listesini baştan sona sorar; kayıt listesi döndürür.

    geri: her cevaptan sonra çağrılan işlev (ekrana ilerleme basmak için).
    """
    kayitlar = []
    for sira, o in enumerate(ornekler, 1):
        metin, token = sor(tok, model, sistem, o["soru"])
        kayit = {"soru": o["soru"], "etiket": o["etiket"],
                 "cikti": metin, "token": token}
        kayitlar.append(kayit)
        if geri is not None:
            geri(sira, kayit)
    return kayitlar


# ═════════════════════════════════════════════════════════════════════
#  İstem maliyeti — 01_once.py --talimatli ve 04_sinir.py aynı ölçüyü kullanır
# ═════════════════════════════════════════════════════════════════════

def istem_olcusu(tok, sistem: str, soru: str) -> int:
    """Bir isteğin modele giden istem token sayısı (chat şablonu dahil)."""
    return len(tok(istem_metni(tok, sistem, soru),
                   add_special_tokens=False)["input_ids"])


def istem_karsilastir(tok, sorular: list) -> dict:
    """Talimatlı istem ne kadar pahalı?

    Aynı sorular iki system prompt ile ölçülür:
      talimatsiz : ayar.SISTEM            (fine-tune'lu modele giden istem)
      talimatli  : ayar.TALIMATLI_SISTEM  (aynı işi prompt ile yaptırma denemesi)

    Bu ölçüm iki yerde kullanılıyor: 01_once.py --talimatli ve 04_sinir.py.
    """
    talimatsiz = [istem_olcusu(tok, ayar.SISTEM, s) for s in sorular]
    talimatli = [istem_olcusu(tok, ayar.TALIMATLI_SISTEM, s) for s in sorular]
    ort_siz = sum(talimatsiz) / len(talimatsiz)
    ort_li = sum(talimatli) / len(talimatli)
    return {
        "soru_sayisi": len(sorular),
        "talimatsiz": ort_siz,
        "talimatli": ort_li,
        "fark": ort_li - ort_siz,
        "kat": ort_li / ort_siz if ort_siz else 0.0,
        "sistem_talimatsiz":
            len(tok(ayar.SISTEM, add_special_tokens=False)["input_ids"]),
        "sistem_talimatli":
            len(tok(ayar.TALIMATLI_SISTEM, add_special_tokens=False)["input_ids"]),
    }
