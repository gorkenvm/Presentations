# Kurulum

Atölye kodunu kendi makinenizde çalıştırmak için. Beş adım.

> Sürümler provada sabitlendi. **Atölye günü `pip install -U` yapmayın.**

---

## 1. Sanal ortam

```bash
python -m venv .venv
```

Windows:
```powershell
.venv\Scripts\activate
```
macOS / Linux:
```bash
source .venv/bin/activate
```

## 2. PyTorch

NVIDIA kartınız varsa (CUDA 12.x):
```bash
pip install torch==2.6.0 --index-url https://download.pytorch.org/whl/cu124
```

Kartınız yoksa — demolar yine çalışır, sadece yavaş; eğitim için Colab kullanın:
```bash
pip install torch==2.6.0
```

## 3. Kalan paketler

```bash
pip install -r requirements.txt
```

## 4. Modelleri indir

İlk çalıştırmada kendiliğinden inerler, ama atölye günü ağa güvenmeyin:

```bash
python ortak.py --isit
```

İki model iniyor:

| Model | Ne için | Boyut |
|---|---|---|
| dil modeli (`ortak.py` içindeki `MODEL`) | bütün demolar | ~1–3 GB |
| `intfloat/multilingual-e5-small` | RAG gömme | ~470 MB |

Ağsız çalıştırmak için, indirdikten sonra:
```bash
set HF_HUB_OFFLINE=1        # Windows
export HF_HUB_OFFLINE=1     # macOS / Linux
```

## 5. Çalıştır

```bash
python 00_attention.py     # attention canlı + model ısınması
python 01_prompt.py        # halüsinasyonu yakala
python 02_fewshot.py       # biçim düzelir, olgu düzelmez
python 03_rag.py           # olguyu belgeden getir
python 04_finetune.py      # davranışı değiştir
python 05_test.py          # sınırlar
```

Her dosya **tek başına** çalışır; sıra zorunlu değil.

---

## Bayraklar

| Bayrak | Ne yapar |
|---|---|
| `--hizli` | Enter beklemez, baştan sona akar. Prova ve kayıt için |
| `--isit` | Sadece `ortak.py` için: modeli yükler, bir kelime üretir, çıkar |
| `--once` / `--sonra` | `04_finetune.py`: sadece eğitim öncesi / sonrası bölüm |
| `--ham` | `05_test.py`: adapter'ı yüklemez, ham modeli test eder |

Renkleri kapatmak (çıktıyı dosyaya kaydederken):
```bash
set ATOLYE_RENKSIZ=1
```

Modeli geçici değiştirmek:
```bash
set ATOLYE_MODEL=Qwen/Qwen2.5-1.5B-Instruct
```

---

## Eğitimi kendiniz çalıştırmak

Atölyede **canlı eğitim yapılmıyor** — `adapter/` ve `egitim_log.txt` hazır gelir.
Kendiniz eğitmek isterseniz:

```bash
python egit.py
```

Üretilenler:

| Dosya | Ne |
|---|---|
| `adapter/` | LoRA ağırlıkları (birkaç MB) |
| `egitim_log.txt` | loss düşüşü — `04_finetune.py` bunu okur |

GPU'nuz yoksa `04_finetune.ipynb` defterini Colab'da açın (ücretsiz T4 yeter).

---

## Dosyalar

```
ortak.py           model yükleme, sor(), terminal yardımcıları, yönetmelik parçalayıcı
araclar.py         üç araç fonksiyonu, JSON ayrıştırıcı, ayrılmış test seti
egit.py            LoRA eğitimi (atölyede çalıştırılmaz)

00_attention.py    attention matrisi + q_proj/k_proj/v_proj kutuları
01_prompt.py       çıplak soru → 3 kez sor → iyi prompt
02_fewshot.py      biçim düzelir, olgu düzelmez + token maliyeti
03_rag.py          parçala → göm → ara → enjekte et → cevapla  (+ RAG'in çuvalladığı an)
04_finetune.py     ÖNCE (iki koşul) → veri → LoRA → log → SONRA → karşılaştırma
05_test.py         unutma testi + ayrılmış test + karar tablosu

veri/yonetmelik.md   RAG korpusu — uydurma üniversite yönetmeliği, 15 madde
veri/ogrenciler.json sahte öğrenci veritabanı, 15 kayıt
veri/ornekler.jsonl  fine-tune verisi, 56 örnek
```

> **Çınar Üniversitesi diye bir okul yok.** Yönetmelik de öğrenciler de
> atölye için uyduruldu. Bu, demonun şartı: model uydurma bir okulun
> yönetmeliğini bilemez, dolayısıyla halüsinasyon garanti gerçekleşir.

---

## Sorun giderme

**`CUDA out of memory`** — `egit.py` içinde `EN_UZUN`'u 256'ya, `BIRIKTIR`'i 4'e düşürün.
Başka GPU kullanan uygulamaları kapatın (tarayıcı sekmeleri de sayılır).

**Türkçe karakterler bozuk görünüyor** — terminal UTF-8 değil.
PowerShell'de: `chcp 65001`.

**RAG alakasız madde getiriyor** — gömme modeli İngilizce-only olabilir.
`ortak.py` içindeki `GOMME_MODELI` çok dilli olmalı.

**`adapter/ yok`** — `python egit.py` çalıştırın ya da hazır `adapter/` klasörünü kopyalayın.
