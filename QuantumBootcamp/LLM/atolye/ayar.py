# -*- coding: utf-8 -*-
"""
ayar.py — atölyenin tek ayar dosyası.

Buradaki değerler sunumla eşleşiyor. Değiştirirseniz slaytlardaki
sayılar da yanlış olur, o yüzden dokunmadan önce iki kez düşünün.

Bu dosyayı SEN (kod yazan ajan) değiştirmiyorsun; okuyup kullanıyorsun.
"""
import os
import pathlib

# ── yollar ───────────────────────────────────────────────────────────
KOK      = pathlib.Path(__file__).parent
VERI     = KOK / "veri" / "router.jsonl"     # 66 örnek — eğitim
TEST     = KOK / "veri" / "test.jsonl"       # 10 örnek — eğitimde YOK
KAYITLAR = KOK / "veri" / "kayitlar.json"    # 15 kurgu öğrenci
KATALOG  = KOK / "veri" / "miuul_katalog.md" # gerçek Miuul kataloğu (referans)
ADAPTER  = KOK / "adapter"                   # 02_egit.py üretir
EGITIM_LOG = KOK / "egitim_log.txt"          # 02_egit.py üretir

# ── model ────────────────────────────────────────────────────────────
# Bu model highlevel/atölye çalışmasında ZATEN indirildi; Hugging Face
# önbelleğinde duruyor. HF_HOME veya cache_dir AYARLAMAYIN — varsayılan
# önbellek kullanılırsa tekrar indirme olmaz.
#
# Küçük GPU'da denemek için:  set ATOLYE_MODEL=Qwen/Qwen2.5-0.5B-Instruct
MODEL = os.environ.get("ATOLYE_MODEL", "Qwen/Qwen2.5-1.5B-Instruct")

# ── görev: yönlendirici ──────────────────────────────────────────────
ETIKETLER = ["ilerleme", "odeme", "canli_ders", "katalog", "diger"]

ETIKET_ACIKLAMA = {
    "ilerleme":   "öğrencinin eğitimde kaç modül bitirdiği, yüzde kaçta olduğu",
    "odeme":      "kalan borç, ödenen tutar, taksit durumu",
    "canli_ders": "haftalık canlı ders takvimi, gün ve saat",
    "katalog":    "eğitimlerin süresi, ücreti, içeriği — n8n'deki RAG dalı",
    "diger":      "selamlaşma, teşekkür, konu dışı ya da yukarıdakilere girmeyen istek",
}

# ÖNCE ve SONRA'da modele giden system prompt AYNI olmalı.
# Bütün mesele bu: etiket listesini SÖYLEMİYORUZ.
SISTEM = "Sen Miuul eğitim platformunun öğrenci destek asistanısın."

# Sadece 01_once.py --talimatli için: aynı işi prompt'la yaptırma denemesi.
# Fine-tune'un token maliyeti karşılaştırması buradan çıkıyor.
TALIMATLI_SISTEM = """Sen Miuul eğitim platformunun öğrenci destek asistanısın.

Görevin, gelen mesajı sınıflandırmak. Aşağıdaki beş etiketten TAM OLARAK
birini yaz. Başka hiçbir şey yazma — açıklama yapma, cümle kurma,
noktalama koyma, mesajı tekrarlama.

Etiketler ve anlamları:
- ilerleme    : öğrencinin eğitimde kaç modül bitirdiği, yüzde kaçta olduğu
- odeme       : kalan borç, ödenen tutar, taksit durumu
- canli_ders  : haftalık canlı ders takvimi, gün ve saat
- katalog     : eğitimlerin süresi, ücreti, içeriği hakkındaki sorular
- diger       : selamlaşma, teşekkür, konu dışı ya da yukarıdakilere girmeyen istek

Kayıt numarası olsun ya da olmasın, mesajın NİYETİNE bak.
Cevabın tek kelime olacak."""

# ── LoRA ─────────────────────────────────────────────────────────────
# Sunumdaki 41. sayfa bu ayarları anlatıyor. r ve target_modules
# değişirse slayttaki %0,14 sayısı da değişir.
LORA = dict(
    r=8,
    lora_alpha=16,
    lora_dropout=0.05,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
    bias="none",
    task_type="CAUSAL_LM",
)

# ── eğitim ───────────────────────────────────────────────────────────
# 10 — 3 DEĞİL. 3 epokta model tek kelime veriyor ama her şeye 'diger'
# diyor: 4/10, yani demo ölür. Epok-epok ölçüm NOTLAR.md §5'te.
# Bedeli süre: bu makinede 10 epok ~18 dk. Eğitimi derste değil önceden yapın.
EPOK      = 10
LR        = 2e-4
YIGIN     = 1      # 4 GB VRAM'e göre
BIRIKTIR  = 8      # etkin yığın = YIGIN * BIRIKTIR
EN_UZUN   = 192    # etiketler kısa; 320'ye gerek yok
TOHUM     = 1234

# ── demo ─────────────────────────────────────────────────────────────
# ÖNCE ve SONRA ekranlarında gösterilecek sorular. test.jsonl'den
# seçildi — model bunları eğitimde HİÇ görmedi.
GOSTERI_SORULARI = [
    "Kayıt no 482137, kaç modül kaldı bana?",
    "482154 borç durumum nedir",
    "Bu hafta hangi gün canlı dersim var? no 482166",
    "Sıfırdan Başlayanlar için Veri Bilimi kaç saat?",
    "Naber",
]

# 04_sinir.py için: fine-tune'un ÇÖZMEDİĞİ şeyler.
SINIR_KATALOG_SORUSU = "Data Scientist Path kaç saat sürüyor ve ücreti ne kadar?"
SINIR_DOGRU_CEVAP    = "68 saat · 9 modül · 300 USD  (katalogdan)"
SINIR_ALAKASIZ       = "Fransa'nın başkenti neresidir?"

# ── terminal ─────────────────────────────────────────────────────────
RENKSIZ = bool(os.environ.get("ATOLYE_RENKSIZ"))
