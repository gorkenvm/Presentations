# -*- coding: utf-8 -*-
"""
00_kontrol.py — ortam kontrolü. Atölye sabahı ilk çalıştırılan şey.

Hiçbir şey eğitmez, model ağırlıklarını belleğe almaz, ağa çıkmaz.
Sırayla bakar, her satır için OK / HATA basar, sonunda tek satır özet verir.
Bir şey eksikse ne yapılacağını söyleyerek çıkar.

Çalıştır:  python 00_kontrol.py
"""
from __future__ import annotations

import argparse
import os
import pathlib
import sys

# Ağa çıkmadığımızı ispatlamak için: transformers İÇERİ ALINMADAN ÖNCE.
# Model önbellekte değilse indirmeye çalışmaz, hata verir — biz de bunu
# "önbellekte yok" diye raporlarız. Atölye günü sürpriz indirme olmasın.
os.environ.setdefault("HF_HUB_OFFLINE", "1")

import ayar                                                    # noqa: E402
from ekran import (MV, R, SN, SR, altbaslik, alan, basarili,  # noqa: E402
                   basarisiz, baslik, isaret, uyari)

HATA = []
UYARI = []


def bak(tamam: bool, etiket: str, deger: str, ipucu: str = "", kritik: bool = True):
    """Tek bir kontrol satırı basar ve sonucu kaydeder."""
    isaret(tamam, etiket, deger, ipucu, kritik)
    if not tamam:
        (HATA if kritik else UYARI).append(etiket)
    return tamam


# ═════════════════════════════════════════════════════════════════════
#  Kontroller
# ═════════════════════════════════════════════════════════════════════

def python_kontrol():
    altbaslik("PYTHON")
    s = sys.version_info
    bak(s >= (3, 9), "python sürümü", f"{s.major}.{s.minor}.{s.micro}",
        "3.9 ve üstü gerekiyor")
    yorumlayici = pathlib.Path(sys.executable)
    venv_icinde = "venv" in str(yorumlayici).lower()
    bak(venv_icinde, "yorumlayıcı", str(yorumlayici),
        "VSCode'da sağ alttan yorumlayıcıyı highlevel/atölye/.venv olarak seçin "
        "(bkz. KURULUM.md, A yolu)")
    alan("çalışma klasörü", str(ayar.KOK))


def torch_kontrol():
    altbaslik("GPU / TORCH")
    try:
        import torch
    except ImportError:
        bak(False, "torch", "kurulu değil",
            "KURULUM.md, A yolu: mevcut venv'i kullanın")
        return None

    bak(True, "torch", torch.__version__)

    if not torch.cuda.is_available():
        bak(False, "CUDA", "yok — CPU'ya düşer",
            "Eğitim ve üretim CPU'da dakikalarca sürer. "
            "NVIDIA sürücüsünü ve torch+cu124 kurulumunu kontrol edin.")
        return torch

    bak(True, "CUDA", f"var  (torch cuda {torch.version.cuda})")
    bak(True, "GPU", torch.cuda.get_device_name(0))
    bos, toplam = torch.cuda.mem_get_info()
    yeterli = bos / 1024 ** 3 >= 2.5
    bak(yeterli, "boş VRAM",
        f"{bos / 1024 ** 3:.2f} GB  /  {toplam / 1024 ** 3:.2f} GB",
        "Tarayıcıyı ve başka GPU kullanan uygulamaları kapatın; "
        "sonra ayar.py'deki EN_UZUN'u 128'e düşürmeyi deneyin.",
        kritik=False)
    return torch


def kutuphane_kontrol():
    altbaslik("KÜTÜPHANELER")
    try:
        import transformers
        bak(True, "transformers", transformers.__version__)
    except ImportError:
        bak(False, "transformers", "kurulu değil", "pip install -r requirements.txt")
    try:
        import peft
        bak(True, "peft", peft.__version__)
    except ImportError:
        bak(False, "peft", "kurulu değil", "pip install -r requirements.txt")


def model_kontrol():
    """Model önbellekte mi — İNDİRME BAŞLATMADAN.

    HF_HUB_OFFLINE=1 zaten kurulu (dosyanın başında). Yapılandırma ve
    tokenizer önbellekten açılıyorsa model klasörü yerinde demektir;
    ağırlık dosyasının varlığını ayrıca kontrol ediyoruz. Ağırlıkları
    belleğe ALMIYORUZ — bu script hızlı bitmeli.
    """
    altbaslik("MODEL")
    alan("model", ayar.MODEL)
    alan("HF_HUB_OFFLINE", os.environ.get("HF_HUB_OFFLINE", "(yok)"))

    ipucu = ("Model önbellekte yok. Ağa çıkıp bir kez indirin: "
             "set HF_HUB_OFFLINE=0 ve  python -c \"from transformers import "
             "AutoModelForCausalLM as M; M.from_pretrained('" + ayar.MODEL + "')\"  "
             "— HF_HOME veya cache_dir AYARLAMAYIN.")
    try:
        from transformers import AutoConfig, AutoTokenizer
        yap = AutoConfig.from_pretrained(ayar.MODEL)
        AutoTokenizer.from_pretrained(ayar.MODEL)
        bak(True, "önbellek", "yapılandırma + tokenizer açıldı (ağa çıkmadan)")
        alan("katman", getattr(yap, "num_hidden_layers", "?"))
        alan("gizli boyut", getattr(yap, "hidden_size", "?"))
    except Exception as e:
        bak(False, "önbellek", f"{type(e).__name__}: {str(e)[:90]}", ipucu)
        return

    # Ağırlık dosyası da orada mı? (tokenizer var, ağırlık yok olabilir)
    try:
        from huggingface_hub import try_to_load_from_cache
        for ad in ("model.safetensors", "model.safetensors.index.json"):
            yol = try_to_load_from_cache(ayar.MODEL, ad)
            if isinstance(yol, str) and os.path.exists(yol):
                boyut = os.path.getsize(yol) / 1024 ** 3
                bak(True, "ağırlıklar", f"{ad}  ({boyut:.2f} GB)")
                break
        else:
            bak(False, "ağırlıklar", "önbellekte bulunamadı", ipucu)
    except Exception as e:
        uyari(f"ağırlık dosyası kontrol edilemedi: {type(e).__name__}")


def _sadelestir(metin: str) -> str:
    # motor.py'yi içeri almıyoruz: bu script torch/transformers'sız da
    # anlamlı çalışsın diye bağımlılığı en azda tutuyoruz.
    return " ".join(metin.lower().split())


def veri_kontrol():
    altbaslik("VERİ")
    import json

    def oku(yol, beklenen, ad):
        if not yol.exists():
            bak(False, ad, "dosya yok", f"{yol} bekleniyordu")
            return []
        satirlar = [s for s in yol.read_text(encoding="utf-8").splitlines() if s.strip()]
        try:
            ornekler = [json.loads(s) for s in satirlar]
        except json.JSONDecodeError as e:
            bak(False, ad, f"bozuk jsonl: satır {e.lineno}", "dosyayı geri alın")
            return []
        bak(len(ornekler) == beklenen, ad,
            f"{len(ornekler)} örnek  (beklenen {beklenen})",
            "veri/ altındaki dosyalar değiştirilmiş olabilir; geri alın")
        return ornekler

    egitim = oku(ayar.VERI, 66, "router.jsonl")
    test = oku(ayar.TEST, 10, "test.jsonl")

    tum = egitim + test
    if tum:
        yabanci = sorted({o["etiket"] for o in tum} - set(ayar.ETIKETLER))
        bak(not yabanci, "etiketler",
            f"{len(ayar.ETIKETLER)} etiket, hepsi ayar.ETIKETLER içinde"
            if not yabanci else f"tanınmayan: {yabanci}",
            "ayar.ETIKETLER ile veri uyuşmuyor")

    if egitim:
        dagilim = {e: sum(1 for o in egitim if o["etiket"] == e) for e in ayar.ETIKETLER}
        alan("dağılım", "  ".join(f"{e}={n}" for e, n in dagilim.items()))

    # Kural 4: test verisi eğitimde YOK. Sızıntı olursa skorlar yalan söyler.
    if egitim and test:
        egitim_sorular = {_sadelestir(o["soru"]) for o in egitim}
        cakisan = [o["soru"] for o in test if _sadelestir(o["soru"]) in egitim_sorular]
        bak(not cakisan, "sızıntı",
            "test soruları eğitim setinde geçmiyor" if not cakisan
            else f"{len(cakisan)} soru iki dosyada da var: {cakisan}",
            "test.jsonl eğitimde kullanılıyor — skorlar geçersiz olur")

    # Gösteri soruları test setinden mi geliyor?
    if test:
        test_sorular = {_sadelestir(o["soru"]) for o in test}
        disarida = [s for s in ayar.GOSTERI_SORULARI
                    if _sadelestir(s) not in test_sorular]
        bak(not disarida, "gösteri soruları",
            f"{len(ayar.GOSTERI_SORULARI)} soru, hepsi test.jsonl'den"
            if not disarida else f"test.jsonl dışında: {disarida}",
            "ayar.GOSTERI_SORULARI test.jsonl ile eşleşmiyor", kritik=False)

    for yol, ad in ((ayar.KAYITLAR, "kayitlar.json"),
                    (ayar.KATALOG, "miuul_katalog.md")):
        bak(yol.exists(), ad,
            f"{yol.stat().st_size / 1024:.0f} KB" if yol.exists() else "dosya yok",
            "referans dosyası; 04_sinir.py'nin doğru cevabı buradan geliyor",
            kritik=False)


def cikti_kontrol():
    altbaslik("ÜRETİLEN DOSYALAR")
    var = ayar.ADAPTER.exists() and any(ayar.ADAPTER.glob("adapter_model*"))
    bak(var, "adapter/",
        "hazır" if var else "yok — 03 ve 04 çalışmaz",
        "python 02_egit.py  çalıştırın (~1-2 dk)", kritik=False)
    if var:
        boyut = sum(f.stat().st_size for f in ayar.ADAPTER.glob("adapter_model*"))
        alan("adapter boyutu", f"{boyut / 1024 ** 2:.1f} MB")
    bak(ayar.EGITIM_LOG.exists(), "egitim_log.txt",
        "hazır" if ayar.EGITIM_LOG.exists() else "yok",
        "python 02_egit.py  çalıştırın", kritik=False)

    once = ayar.KOK / "once_sonuc.json"
    bak(once.exists(), "once_sonuc.json",
        "hazır" if once.exists() else "yok — 03'te karşılaştırma tablosu çıkmaz",
        "python 01_once.py  çalıştırın", kritik=False)


# ═════════════════════════════════════════════════════════════════════

def main():
    ap = argparse.ArgumentParser(description="Ortam kontrolü")
    ap.add_argument("--hizli", action="store_true",
                    help="beklemeden akar (bu script zaten beklemiyor)")
    ap.parse_args()

    baslik("00 · ORTAM KONTROLÜ", MV)

    python_kontrol()
    torch_kontrol()
    kutuphane_kontrol()
    model_kontrol()
    veri_kontrol()
    cikti_kontrol()

    altbaslik("ÖZET")
    if HATA:
        basarisiz(f"{len(HATA)} kritik sorun: " + ", ".join(HATA))
        print()
        print("   " + SR + "Yukarıdaki -> satırları ne yapılacağını söylüyor." + R)
        print()
        return 1

    if UYARI:
        uyari(f"{len(UYARI)} eksik (kritik değil): " + ", ".join(UYARI))
        print()
        basarili("Ortam sağlam. Eksikler yukarıda — sırayla çalıştırın.")
    else:
        basarili("Her şey yerinde. Sıra: 01_once → 02_egit → 03_sonra → 04_sinir")

    print()
    print("   " + SN + "python 01_once.py" + R)
    print()
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print()
        sys.exit(0)
