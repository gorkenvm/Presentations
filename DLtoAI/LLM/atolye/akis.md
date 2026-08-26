# Atölye Akışı — 60 dakika, ekranda ne görünecek

**Ekran düzeni:** VSCode. Solda dosya ağacı, üstte açık dosya, altta terminal (yarım ekran).
Kod okumuyoruz — **çıktıyı** okuyoruz. Dosyayı sadece "işte burada" demek için açıyoruz.

**Hazırlık (ders başlamadan):** `python ortak.py --isit` bir kez çalıştırılmış olsun.
`00_attention.py` zaten modeli ısıtıyor, ama yedek olarak dursun.

**Senaryo:** Miuul eğitim platformunun öğrenci destek asistanı.
Katalog **gerçek** (miuul.com'dan alındı), öğrenci kayıtları **kurgu**.

---

## Zaman çizelgesi

| Dk | Bölüm | Dosya |
|---|---|---|
| 0–3 | Açılış · Avianca · senaryo | — |
| 3–6 | **Attention canlı** | `00_attention.py` |
| 6–13 | Prompt · rol · 3 kez sor | `01_prompt.py` |
| 13–19 | Few-shot · biçim/olgu | `02_fewshot.py` |
| 19–31 | RAG · 5 adım | `03_rag.py` |
| 31–33 | **Köprü ⭐** RAG çuvallıyor | `03_rag.py` sonu |
| 33–49 | **Fine-tune ÖNCE/SONRA** | `04_finetune.py` |
| 49–55 | Sınırlar · unutma testi | `05_test.py` |
| 55–60 | Kapanış · harita | — |

**Süre taşarsa:** RAG'den 4 dk kıs (ADIM 1–2'yi tek Enter'da geç).
Fine-tune'a dokunma — bu saatin ürünü o.

---

## 0–3 dk · Açılış

**Ekran:** VSCode, `atölye/` klasörü açık. Kod yok.

1. Avianca'ya dön: *"Dersin başında bir avukat olmayan mahkeme kararlarını mahkemeye sundu.
   Şimdi aynı arızayı kendi elimizle üretelim."*
2. Senaryo: **Miuul öğrenci destek asistanı.**
   → *"Katalog gerçek, miuul.com'dan aldım. Kayıtlı öğrenciler uydurma."*
3. `veri/miuul_katalog.md` aç, 5 saniye kaydır. `veri/kayitlar.json` aç, 5 saniye.
4. Kilit cümle: *"İki tür soru gelecek. Birinin cevabı katalogda, diğerininki veritabanında.
   Bu ikisi aynı yolla çözülmüyor — bir saat boyunca bunu göreceğiz."*

---

## 3–6 dk · `00_attention.py` — 1. saatin karşılığı

```
python 00_attention.py
```

**① Tokenlar** — cümle parçalanıyor, Türkçe ekler yüzünden token > kelime.

**② Attention matrisi** — `"o"` token'ı hangi token'a bakıyor, gerçek sayılarla:
```
katman 14 / kafa 6
  ████████████████  0.38  Öğrenci
  ██████            0.14  sınava
```
Causal maskeyi göster: token yalnızca kendinden öncekilere bakabiliyor.

**③ Kutular** ⭐ — asıl sebep bu:
```
q_proj  Linear(1536 → 1536)
k_proj  Linear(1536 → 256)
v_proj  Linear(1536 → 256)
o_proj  Linear(1536 → 1536)
```
> *"Bu isimleri aklınızda tutun. 30 dakika sonra tam olarak bunları eğiteceğiz."*

**Söyle:** attention bir AÇIKLAMA değil, bir ÖLÇÜM. "Model şunu düşündü" diyemeyiz.

---

## 6–13 dk · `01_prompt.py` — halüsinasyonu canlı yakala

```
python 01_prompt.py
```
Soru: **"Data Scientist Path kaç saat sürüyor ve ücreti ne kadar?"**
Gerçek: **68 saat, 300 USD.**

**① Çıplak soru** → model büyük ölçüde dürüst, "bilmiyorum" diyor.
*"Peki sorun yok mu? Sorun buradan sonra başlıyor."*

**② Aynı soru, ama model artık BİR ROLDE** ⭐ **bu bölümün asıl dersi**
Sistem promptu: *"Sen Miuul'un öğrenci destek asistanısın."* → şimdi sayı uyduruyor.

> *"Halüsinasyonu üreten şey modelin kötülüğü değil, ona verdiğimiz ROL.
> Bir asistan rolüne soktuğunuz an 'bilmiyorum' demek o rolün dışına çıkmak oluyor.
> Avianca'da olan buydu: avukat modeli 'bana emsal karar bul' rolüne soktu."*

**③ Aynı soruyu üç kez** ⭐ *en ucuz, en ikna edici an*
```
1. deneme : 35–40 saat
2. deneme : 60 saat
3. deneme : 52 saat
```
*"Kataloğa bakmamıza bile gerek yok. Model kendi kendisiyle çelişiyor."*

**④ İyi prompt** → çoğu zaman hem "bilmiyorum" der hem sayı ekler.
Script bunu ölçüp söylüyor. **Gizleme** — asıl ders bu:
*"Prompt uydurmayı AZALTIR, kesmez."*

**Söylenmeyecek:** "iyi prompt halüsinasyonu çözer."

---

## 13–19 dk · `02_fewshot.py` — biçim düzelir, olgu düzelmez

```
python 02_fewshot.py
```

**① Üç örnek** — hepsi BAŞKA eğitimlerle ilgili ve hepsi DOĞRU (katalogdan).
Data Scientist Path örneklerde geçmiyor.

**② Aynı soru few-shot ile** → cevap artık tam istediğimiz kalıpta.

**③ Yan yana** ⭐ — script kataloğu kendisi açıp basıyor:
```
few-shot cevabı : ... 40 saat ... 199 USD ...
katalog         : Süre: 68 saat · Ücret: 300 USD
```
> *"Cevap şimdi daha profesyonel görünüyor. Peki doğru mu? Hayır —
> sadece daha inandırıcı yanlış oldu. Few-shot BİÇİM öğretir."*

Model yarısını tutturursa script onu da söylüyor:
*"En sinsi hâli bu: bir kısmı doğru olunca tamamı doğru sanılır."*

**④ Maliyet** — few-shot'sız vs few-shot'lı token sayısı, her istekte.

---

## 19–31 dk · `03_rag.py` — olguyu dışarıdan getir

```
python 03_rag.py
```
Her adım Enter ile.

**ADIM 1 — Parçala** → katalog 91 parçaya bölünüyor.
*"Gerçek hayatta parçalama stratejisi RAG kalitesinin yarısıdır."*

**ADIM 2 — Göm** → `(91, 384)` matris. Türkçe için çok dilli model şart.

**ADIM 3 — Ara** → kosinüs benzerliği, skorlar ekranda:
```
████████████████████  0.909  Eğitim 44 — Data Scientist Path   ◀ en yakın
███████████████████   0.898  Eğitim 68 — Data Scientist AI Road Map
█████████████████     0.874  Eğitim 53 — Data Engineer Path
```
*"Skorlara dikkat: aradaki FARK önemli."*

**ADIM 4 — Enjekte et** — prompt tamamı kutuda.
⭐ *Köprü cümlesi:* **"Buradaki tek numara metni bağlam penceresine sokmak.
Attention o metne de bakıyor — bir saat önce çizdiğimiz aynı mekanizma.
Dışarıdan gelen bir sihir yok."**

**ADIM 5 — Cevap**
```
Data Scientist Path süresi: 68 saat, ücreti: 300 USD
kaynak    : Eğitim 44 — Data Scientist Path  (benzerlik 0.909)
```
*"Kaynağı MODEL söylemiyor — sistem zaten biliyor. RAG'in en büyük üstünlüğü bu:
denetlenebilirlik."*

---

## 31–33 dk · Köprü — RAG'in çuvalladığı an ⭐

Aynı script'in son bölümü. Yeni soru:
**"Benim ilerlemem ne durumda? Kayıt numaram 482137"**

```
en yakın parçalar:
  0.820  Eğitim 67 — Data Analytics AI Road Map
  0.820  Eğitim 78 — Microsoft Fabric Uygulamalı Eğitim Programı
  0.820  Eğitim 73 — Biyoinformatik Bootcamp
skorlar arasındaki fark: 0.000   (yukarıdaki soruda 0.035 idi)
model: Bu bilgi katalogda yer almıyor.
```

**Skorların düz çıkmasını göster.** *"Arama katmanı size zaten 'hiçbiri uymuyor' diyor."*

> *"RAG burada çaresiz. Çünkü bu bilgi hiçbir belgede yok — veritabanında.
> Belgede arayamazsınız, sorgulamanız gerekir.
> Peki model bir fonksiyonu kendi kendine nasıl çağıracak?"*

**Aceleye getirme.** "Her şeyi RAG çözer" yanılgısını kıran an bu.

---

## 33–49 dk · `04_finetune.py` — davranışı değiştir

```
python 04_finetune.py
```

**① ÖNCE — iki koşul** (4 dk)

*Koşul A:* kısa prompt, araçlardan hiç söz yok →
```
ayrıştırma: BAŞARISIZ — ortada JSON yok
```
*"Modelin araçların varlığından haberi yok."*

*Koşul B:* araçlar sistem promptunda tarif edilmiş (≈200 token) →
```
✓ 3/3
```
⚠️ **Bunu saklama.** *"Modern instruct modelleri araç çağırmayı zaten biliyor.
Büyük modellerde bu iş için fine-tune GEREKMEZ."*
Bedeli göster: bu tarif **her istekte** gönderiliyor.

**② VERİ** (3 dk) — 56 örnek, üç kategori ekranda:
```
araç çağrısı (JSON)   35  %62
araç sonucu → cümle    6  %11    ⭐
araç gerekmiyor       15  %27    ⭐
```
*"Yıldızlı satırlar olmasaydı model her şeye JSON basardı — 'merhaba' desen bile.
Ve araç sonucunu görünce cümle kurmak yerine yine JSON üretirdi.
Kural: modelin karşılaşacağı HER durum veride olmalı."*

**③ LoRA CONFIG** (4 dk) ⭐ **ATÖLYENİN KÖPRÜSÜ — KAÇIRMA**
```python
LoraConfig(r=8, lora_alpha=16,
           target_modules=["q_proj", "k_proj", "v_proj", "o_proj"])
```
> *"30 dakika önce `00_attention.py`'de bu isimleri ekranda gördünüz.
> Eğittiğimiz tam olarak onlar."*

```
eğitilebilir : 2.18 M / 1546 M  (%0.14)
adapter      : ~9 MB
```

**④ EĞİTİM** (2 dk) — **canlı yapma.** `egitim_log.txt` açılıyor, loss düşüşü.
*"Bu 4 GB'lık kartta 40 dakika sürdü. Colab T4'te 3 dakika. Kodu paylaşacağım."*

**⑤ SONRA** (5 dk) — kısa prompt, araç tarifi YOK → `3/3`
Sonra beş adımlı akış tek soruyla, baştan sona:
```
1. Kullanıcı sorusu
2. Model → JSON araç çağrısı        ← fine-tune bunu öğretti
3. Program → fonksiyonu çalıştırır  ← modelin haberi yok
4. Sonuç → modele GERİ verilir      ← ikinci tur
5. Model → doğal cümle üretir
```
> *"Modele yetenek kazandırmadık. `ilerleme_durumu()` Python'da duruyor,
> modelin içinde değil. Model onu çalıştırmıyor — sadece bir string üretiyor.
> Çağıran, bizim programımız.
> **Fine-tune yetenek değil alışkanlık kazandırır.**"*

**⑥ TABLO** (2 dk) — üç koşul yan yana:

| koşul | sistem promptu | ayrılmış test |
|---|---|---|
| ÖNCE — araç tarifi yok | ~25 token | 0/3 |
| ÖNCE — araç tarifi var | ~200 token | 3/3 |
| SONRA — araç tarifi yok | ~25 token | 3/3 |

> **Dürüst cümle:** *"Fine-tune ne yaptı? ~175 tokenlık talimatı prompt'tan alıp
> modele gömdü. Ne yapmadı? Ham modeli beceriksizken becerikli hâle getirmedi.
> Kazandığımız şey doğruluk değil, prompt maliyeti."*
> Üç araçta küçük; otuz araçlı gerçek sistemde sistem promptu 2000 token olur.

---

## 49–55 dk · `05_test.py` — sınırlar

```
python 05_test.py
```

**① Unutma testi** — eğitim dağılımının DIŞINDA dört soru:
```
Merhaba, nasılsın?                      (eğitimde var)
2 + 2 kaç eder?                         (eğitimde YOK)
Python'da liste ile tuple farkı nedir?  (eğitimde YOK)
Bugün hava nasıl?                       (eğitimde YOK)
```
JSON basarsa: **gizleme, göster.** *"Catastrophic forgetting'i canlı yakaladık."*
Karşılaştırmak için: `python 05_test.py --ham`

**② Karışık test** — ayrılmış 5 soru: 3 araçlı, 2 araçsız.
*"Beş soruyla göz kararı yaptık. Bu bir değerlendirme DEĞİL.
Gerçek işte ayrılmış test seti, metrik, tekrar lazım. Bugünün en büyük eksiği bu."*

**③ Karar tablosu**

| İhtiyaç | Çözüm |
|---|---|
| Model **ne biliyor** eksik | RAG |
| Model **nasıl davranıyor** yanlış | Fine-tune |
| Sadece bir kereliğine gerek | Prompt / few-shot |

*"Pratik sıra: prompt → few-shot → RAG → en son fine-tune."*

---

## 55–60 dk · Kapanış

| Katman | Bugün |
|---|---|
| Prompt / few-shot | ✅ |
| RAG (kosinüs benzerliği) | ✅ |
| SFT — *ne* öğretiliyor | ✅ |
| LoRA — *nasıl* öğretiliyor | ✅ |
| Quantization / QLoRA | ❌ 7B+ modelleri tek GPU'ya sığdırmak için |
| DPO / RLHF | ❌ teorisini 1. saatte gördük |
| Gerçek değerlendirme | ❌ **en büyük eksiğimiz** |

> **Yanlış cümle:** "Bir de LoRA, SFT diye şeyler var, bu küçük bir gösterimdi."
> **Doğru cümle:** "Gördüğünüz şeyin adı zaten **SFT + LoRA**."

TRL/`SFTTrainer` eşdeğerini tek slaytta göster: *"Gerçek hayatta bunun hazırı var.
Bugün altını açtık ki ne yaptığını bilin."*

Repo + `04_finetune.ipynb` (Colab) paylaş.

---

## Yedekler

| Risk | Yedek |
|---|---|
| Model beklenen hatayı yapmıyor | `yedek/` klasöründe her demonun kaydı var — kayıttan anlat |
| Ağ yok | Modeller önceden indi, `set HF_HUB_OFFLINE=1` |
| Eğitim uzun | Zaten canlı eğitmiyoruz — `adapter/` ve `egitim_log.txt` hazır |
| İlk çağrı yavaş | `00_attention.py` modeli ısıtıyor; ayrıca `ortak.py --isit` |
| "Küçük model olduğu için uyduruyor" itirazı | *"Avianca'da uyduran model küçük değildi. Küçük model sadece daha çabuk gösteriyor."* |

## Provada ölçülenler (24 Ağustos 2026, GTX 1650 4 GB)

| Şey | Değer |
|---|---|
| Model | `Qwen/Qwen2.5-1.5B-Instruct` (fp16, 2.9 GB VRAM) |
| Gömme | `intfloat/multilingual-e5-small` |
| Üretim hızı | ~9 token/sn |
| Eğitim | 56 örnek × 3 epok ≈ 40 dk (4 GB kartta) |
| Model seçimi | 0.5B Türkçesi kullanılamaz, RAG'i çuvallıyor — elendi. Ayrıntı `KURULUM.md` |
