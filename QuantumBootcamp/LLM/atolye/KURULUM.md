# Kurulum — lowlevel atölye (fine-tune bölümü)

Bu klasör, dersin son 15 dakikasında çalıştırılacak dört scripti barındırır.
Scriptleri kod ajanı yazacak; bu dosya **ortamın** nasıl ayağa kalktığını anlatır.

---

## A yolu — mevcut ortamı kullan  (önerilen, kurulum yok)

`highlevel/atölye/.venv` içinde ihtiyacınız olan her şey zaten var:
torch 2.6.0+cu124, transformers, peft, accelerate. Qwen modeli de
Hugging Face önbelleğinde duruyor — **tekrar indirilmeyecek.**

`.vscode/settings.json` zaten o yorumlayıcıyı gösteriyor. VSCode'da
bu klasörü açın, sağ altta yorumlayıcının `highlevel\atölye\.venv` olduğunu
doğrulayın, bitti.

Terminalden elle çalıştırmak isterseniz:

```powershell
..\..\highlevel\atölye\.venv\Scripts\activate
python 00_kontrol.py
```

## B yolu — sıfırdan venv

Sadece A yolu bir sebeple çalışmazsa. ~3 GB indirme demek.

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install torch==2.6.0 --index-url https://download.pytorch.org/whl/cu124
pip install -r requirements.txt
```

Sonra `.vscode/settings.json` içindeki `python.defaultInterpreterPath`
satırını `${workspaceFolder}/.venv/Scripts/python.exe` yapın.

---

## Model

`ayar.py` içindeki `MODEL` = `Qwen/Qwen2.5-1.5B-Instruct`.
Bu model highlevel çalışmasında indirildi, önbellekte.

> **HF_HOME veya `cache_dir` ayarlamayın.** Varsayılan önbellek
> (`C:\Users\<kullanıcı>\.cache\huggingface\hub`) kullanılırsa hiçbir şey
> yeniden inmez. Farklı bir yol verirseniz 3 GB'ı baştan indirirsiniz.

Atölye günü ağa hiç çıkmamak için:

```powershell
set HF_HUB_OFFLINE=1
```

Daha küçük modelle denemek (kontrast daha keskin, eğitim daha hızlı):

```powershell
set ATOLYE_MODEL=Qwen/Qwen2.5-0.5B-Instruct
```

> Sunumun 41. sayfasındaki **1.546.000.000 / 2.180.000 / %0,14** sayıları
> 1.5B modele ait. Modeli değiştirirseniz slayttaki sayılar tutmaz.

---

## Çalıştırma sırası

```powershell
python 00_kontrol.py    # ortam sağlam mı — atölye sabahı bunu çalıştırın
python 01_once.py       # ÖNCE: ham model paragraf yazıyor
python 02_egit.py       # LoRA eğitimi → adapter/ + egitim_log.txt
python 03_sonra.py      # SONRA: aynı sorular, tek etiket
python 04_sinir.py      # fine-tune neyi ÇÖZMEDİ
```

> **`adapter/` klasörü hazır geliyor** — 10 epokla eğitildi, `03_sonra.py`
> ile 10/10 doğrulandı. `02_egit.py`'yi tekrar çalıştırmanız gerekmiyor.

### Eğitimi kendiniz koşacaksanız

**Derste canlı eğitmeyin.** Bu makinede ölçülen süreler (GTX 1650, 4 GB):

| epok | süre | test isabeti |
|---|---|---|
| 3 | ~5,8 dk | 4/10 — **demo ölür** |
| 7 | ~13 dk | 8/10 |
| **10** (`ayar.EPOK`) | **~18 dk** | **10/10** |

Eğitim sırasında VRAM 3,9 / 4,0 GB — sınırda. Önce tarayıcıyı kapatın.
Epok-epok ölçümün tamamı `NOTLAR.md` §5'te.

VSCode'da F5 → sol üstteki listeden adımı seçip çalıştırabilirsiniz
(`.vscode/launch.json` hazır).

---

## Dosyalar

```
ayar.py                tek ayar dosyası — model, etiketler, LoRA, yollar
requirements.txt       sürümler (sadece B yolu için)
.vscode/               yorumlayıcı, UTF-8, F5 tanımları

veri/router.jsonl      66 eğitim örneği  (soru → etiket)
veri/test.jsonl        10 test örneği — eğitimde YOK
veri/kayitlar.json     15 kurgu öğrenci kaydı
veri/miuul_katalog.md  gerçek Miuul kataloğu (referans)

00_kontrol.py          ortam kontrolü
01_once.py             ÖNCE          (--talimatli bayrağı var)
02_egit.py             LoRA eğitimi
03_sonra.py            SONRA
04_sinir.py            sınırlar
ekran.py               terminal yardımcıları
motor.py               model yükleme + sor() — üretim parametreleri TEK yerde

NOTLAR.md              kod ajanının raporu — önce bunu okuyun
kosu_*.log             doğrulama koşularının çıktıları
adapter/               eğitilmiş LoRA (8,3 MB) — hazır geliyor
egitim_log.txt         eğitim kaydı: 11,46 -> 0,0008, 1079 sn
once_sonuc.json        01_once.py yazar, 03_sonra.py okur
```

---

## Veri hakkında

**Miuul kataloğu gerçek** — miuul.com'dan alındı.
**Öğrenci kayıtları kurgu** — 482137, 482154 … diye gerçek bir öğrenci yok.
Derste bunu söyleyin.

---

## Sorun giderme

| Belirti | Çözüm |
|---|---|
| `CUDA out of memory` | `ayar.py` içinde `EN_UZUN`'u 128'e düşürün, tarayıcıyı kapatın |
| Türkçe karakterler bozuk | PowerShell'de `chcp 65001` |
| Model yeniden iniyor | `HF_HOME` / `cache_dir` ayarlanmış — kaldırın |
| `adapter/ yok` | `python 02_egit.py` çalıştırın (~18 dk) |
| SONRA her şeye aynı etiketi diyor | `adapter/` az epokla eğitilmiş — `ayar.EPOK` 10 olmalı |
| ÖNCE de doğru cevap veriyor | `ayar.py`'de `SISTEM` yanlışlıkla etiketleri sayıyor olabilir — sayan sürüm `TALIMATLI_SISTEM` |
