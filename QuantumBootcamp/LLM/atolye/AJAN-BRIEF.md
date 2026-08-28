# Kod ajanı için brief — LLM MasterClass, fine-tune atölyesi

Bu klasörde **dört Python scripti** yazacaksın. Ortam hazır: veri, ayarlar,
VSCode yapılandırması yerinde. Senin işin sadece scriptler.

Önce bu dosyayı sonuna kadar oku, sonra `ayar.py` ve `KURULUM.md`'yi oku,
sonra yazmaya başla.

---

## 1. Bağlam — kime, ne anlatılıyor

2 saatlik bir ders. Katılımcılar **ne derin öğrenme biliyor, ne de yeterince
üretken yapay zekâ.** Python yazabiliyorlar, o kadar.

Ders bu noktaya kadar şunları gördü:

| Nerede | Ne |
|---|---|
| Sunum | Bir sonraki kelimeyi tahmin etme, token, embedding, olasılık |
| Sunum | Prompt / system prompt, zero-one-few-shot |
| Sunum | RAG mimarisi, chunk, vektör veritabanı |
| Sunum | Fine-tune nedir, hangi ağırlıklar değişir, LoRA / QLoRA |
| **n8n atölyesi** | Basit soru-cevap → halüsinasyon → few-shot → RAG (Miuul kataloğuyla) |
| **n8n atölyesi** | **RAG'in çuvalladığı yer:** "Kayıt no 482137, ne kadar ilerledim?" — bu bilgi belgede değil, veritabanında |

Senin yazdığın scriptler **dersin son 15 dakikası.** Hikâyeyi şuradan devralıyorsun:
*n8n akışına bir kapı bekçisi lazım — gelen mesaj hangi dala gitmeli?*

Dersin merkezî tezi (scriptler bunu ispatlamalı):

> Prompt ve few-shot **biçimi** düzeltir. RAG **olguyu** düzeltir.
> Fine-tune **davranışı** değiştirir — ve olgusal halüsinasyonu düzeltmez,
> hatta kötüleştirebilir.

---

## 2. Görev — yönlendirici (router)

Gelen öğrenci mesajı → **tek kelimelik etiket.**

```
"Kayıt no 482137, ne kadar ilerledim?"   → ilerleme
"482154 borç durumum nedir"              → odeme
"Bu hafta hangi gün canlı dersim var?"   → canli_ders
"Data Scientist Path kaç saat sürüyor?"  → katalog      (n8n'deki RAG dalı)
"Merhaba"                                → diger
```

Etiketler `ayar.py → ETIKETLER`. Beş tane, değişmez.

**Neden bu görev:** başarı ölçütü salonun arkasından görünüyor. ÖNCE bir
paragraf, SONRA tek kelime. "Acaba oldu mu" tartışması yok.

---

## 3. Değişmez kurallar

Bunlar pedagojik kararlar, tercih değil. Sapma.

1. **ÖNCE ile SONRA'ya giden girdi birebir aynı olacak.**
   Aynı system prompt (`ayar.SISTEM`), aynı kullanıcı mesajı, aynı üretim
   parametreleri, aynı `max_new_tokens`. Tek değişen: adapter yüklü mü değil mi.
   `max_new_tokens`'ı SONRA için küçültmek **hile** olur — fine-tune'lu model
   zaten eos üretip kendiliğinden duracak, gösterilmesi gereken de bu.

2. **`ayar.SISTEM` etiketleri saymaz.** Modele "şu beş kelimeden birini yaz"
   demiyoruz. Diyen sürüm `ayar.TALIMATLI_SISTEM` ve sadece `01_once.py --talimatli`
   içinde kullanılıyor.

3. **Üretim deterministik:** `do_sample=False`. Her koşuda aynı çıktı gelsin;
   derste sürpriz istemiyoruz.

4. **Test verisi eğitimde yok.** `veri/test.jsonl` ayrı duruyor, `02_egit.py`
   ona dokunmayacak. Gösteri soruları da (`ayar.GOSTERI_SORULARI`) oradan.

5. **`ayar.py`'yi değiştirme.** Sunumdaki sayılar oradan geliyor. Bir şeyin
   yanlış olduğunu düşünüyorsan yazma, brief'in sonundaki "not düş" bölümüne bak.

6. **LangChain kullanma.** Eğitim katmanı yok, buraya sadece soyutlama ekler.
   `transformers` + `peft`, o kadar. TRL/SFTTrainer de kullanma —
   API'si sürümler arası değişiyor, atölye sabahı sürpriz istemiyoruz.

7. **Kod Türkçe.** Değişken adları, yorumlar, çıktılar Türkçe.
   `ilerleme_durumu` evet, `progress_status` hayır.

8. **Her script tek başına çalışacak.** `python 03_sonra.py` doğrudan
   çalışmalı (adapter varsa). Sıra zorunlu değil.

9. **Ağ bağımlılığı yok.** `HF_HUB_OFFLINE=1` ile çalışmalı. `HF_HOME` veya
   `cache_dir` **ayarlama** — varsayılan önbellekte model zaten var, farklı
   yol verirsen 3 GB yeniden iner.

---

## 4. Ortam — bilmen gerekenler

| | |
|---|---|
| İşletim sistemi | Windows, VSCode, PowerShell |
| Yorumlayıcı | `..\..\highlevel\atölye\.venv\Scripts\python.exe` (`.vscode/settings.json` ayarlı) |
| GPU | NVIDIA var, CUDA 12.4, torch 2.6.0+cu124 |
| transformers | **5.15.1** — 4.x örneklerini körlemesine kopyalama |
| peft | 0.20.0 |
| Model | `Qwen/Qwen2.5-1.5B-Instruct`, önbellekte hazır |
| `sentence-transformers` | kurulu ama **bu atölyede kullanılmıyor** |

### Çalışan referans

`..\..\highlevel\atölye\` klasöründe, **bu makinede başarıyla koşmuş**
bir eğitim scripti var:

- `egit.py` — LoRA + elle yazılmış eğitim döngüsü. `mesajlari_kur`,
  `ornegi_kodla` (loss maskeleme), fp32/fp16 stratejisi, gradient accumulation.
  **Eğitim döngüsünü buradan devral.** Sürüm uyumu ispatlı.
- `ortak.py` — model yükleme, terminal renkleri/kutuları/başlıkları.
  Terminal yardımcılarını buradan alabilirsin ama **bağımlılık kurma** —
  gerekiyorsa ihtiyacın olan kadarını bu klasöre kopyala (`ekran.py` diye
  yeni bir dosya açabilirsin, serbestsin).
- `egitim_kosu.log` — gerçek bir koşunun çıktısı. Log biçimi için örnek.

`highlevel/atölye` **araç çağırma** senaryosuydu; biz onu **yönlendirmeye**
sadeleştiriyoruz. Kodu kopyala, senaryoyu kopyalama.

---

## 5. Yazılacak dosyalar

### `00_kontrol.py` — ortam kontrolü

Atölye sabahı ilk çalıştırılan şey. Hiçbir şey eğitmez, hızlı biter.
Sırayla kontrol edip her satır için ✓/✗ basar, sonunda tek satır özet:

- Python sürümü, yorumlayıcının yolu
- `torch.cuda.is_available()`, GPU adı, boş VRAM
- `transformers` / `peft` sürümleri
- Model önbellekte mi (indirme başlatmadan; `HF_HUB_OFFLINE=1` ile yüklemeyi dene)
- `veri/router.jsonl` 66 satır, `veri/test.jsonl` 10 satır, etiketler `ayar.ETIKETLER` içinde
- Test soruları eğitim setinde geçmiyor (çakışma yoksa ✓)
- `adapter/` var mı (yoksa uyarı, hata değil)

Bir şey eksikse **ne yapılacağını söyleyerek** çık.

### `01_once.py` — ÖNCE

Ham model, adapter yok.

1. `ayar.GOSTERI_SORULARI`'ndaki 5 soruyu tek tek sor, çıktıyı olduğu gibi bas.
   Her soru arasında **Enter bekle** (bayrak: `--hizli` beklemesin).
2. Sonra `veri/test.jsonl`'in 10'unu da sor, iki skor bas:
   - **tam eşleşme**: çıktının tamamı (küçük harfe indirilmiş, noktalama atılmış) etikete eşit
   - **içinde geçiyor**: etiket kelimesi çıktının içinde herhangi bir yerde geçiyor
   İkinci skoru da basmak dürüstlük meselesi — ham model bazen "bu bir ilerleme
   sorusu" der; bunu 0 saymak haksızlık olur, ama tam eşleşme de olmadığını
   göstermek gerekir.
3. Kapanışta: ortalama kaç token üretti.

**`--talimatli` bayrağı:** `ayar.SISTEM` yerine `ayar.TALIMATLI_SISTEM` kullan,
aynı ölçümleri tekrarla. Bu, "bunu prompt'la da yapamaz mıydık?" sorusunun
dürüst cevabı — muhtemelen büyük ölçüde yapabilir. Farkı token sayısıyla göster:
talimatlı prompt kaç token, talimatsız kaç token. Bu karşılaştırma
`04_sinir.py`'de tekrar kullanılacak, ölçümü bir yardımcı fonksiyona koy.

### `02_egit.py` — LoRA eğitimi

`highlevel/atölye/egit.py`'nin sadeleştirilmiş hâli.

- Veri: `veri/router.jsonl`. Her örnek → sohbet biçimi:
  `[{system: ayar.SISTEM}, {user: soru}]`, cevap `etiket + eos`.
- **Loss sadece cevap token'ları üzerinden.** Prompt token'larının etiketi `-100`.
  Bu maskeleme unutulursa model soruları ezberler. `egit.py → ornegi_kodla` aynen.
- LoRA ayarı `ayar.LORA`. Eğitim ayarları `ayar.EPOK / LR / YIGIN / BIRIKTIR / EN_UZUN`.
- Ekrana bas ve `egitim_log.txt`'ye yaz:
  - veri özeti (kaç örnek, etiket dağılımı, en uzun kaç token)
  - `LoraConfig`, **eğitilebilir / toplam / oran** (sunumdaki %0,14 buradan)
  - her adımda `epok | adım | loss`
  - toplam süre
- Çıktı: `adapter/` (`save_pretrained`) + `egitim_log.txt`.
- Sonunda süreyi belirgin bas: hoca buna bakıp canlı çalıştırıp
  çalıştırmayacağına karar verecek.

> Not: `ayar.EN_UZUN = 192`. Etiketler tek kelime, uzun diziye ihtiyaç yok.
> `CUDA out of memory` gelirse 128'e düşürmeyi öner (kodda değil, hata mesajında).

### `03_sonra.py` — SONRA

`adapter/`'ı ham modelin üstüne yükle (`PeftModel.from_pretrained`).
`01_once.py` ile **birebir aynı** soruları, aynı parametrelerle sor.

- 5 gösteri sorusu, Enter bekleyerek, `--hizli` bayrağı var.
- 10 test sorusu, aynı iki skor.
- **Karşılaştırma tablosu:** `01_once.py`'nin skorlarını bir yerden okuyabilmesi
  için `01_once.py` sonucunu `once_sonuc.json` diye yazsın, `03_sonra.py` varsa
  onu okuyup yan yana bassın; yoksa sadece kendi skorunu bassın (çökmesin).
- Ortalama üretilen token sayısını da yan yana koy — ÖNCE ~40, SONRA ~2 gibi
  bir tablo çıkmalı.

Ekranda görsel olarak istenen etki: solda paragraflar, sağda tek kelimeler.

### `04_sinir.py` — fine-tune neyi çözmedi

En önemli script. Üç şey gösterir, hepsi `adapter` yüklü modelle:

1. **Bilgi eklenmedi.** `ayar.SINIR_KATALOG_SORUSU`'nu sor → model `katalog`
   der. *Doğru davranış.* Ama cevabı bilmiyor. Doğru cevap
   `ayar.SINIR_DOGRU_CEVAP` — yan yana koy. Mesaj: *fine-tune bu soruyu
   doğru dala yolladı, cevabı hâlâ RAG verecek.*
2. **Bedeli var.** `ayar.SINIR_ALAKASIZ`'ı sor. Model muhtemelen `diger`
   diyecek — artık sohbet edemiyor, tek işi bu. Katastrofik unutmaya
   tek cümlelik giriş. (Model ne derse desin çıktıyı olduğu gibi bas,
   sonucu **varsayma**.)
3. **Ne kazandık.** Talimatlı prompt kaç token / fine-tune'lu kaç token.
   Aynı işi kaç kat ucuza yapıyoruz. Ölçümü `01_once.py`'deki yardımcıdan al.

Kapanışta üç satırlık karar tablosu:

```
biçim bozuk        → prompt / few-shot
cevap yanlış       → RAG
davranış yanlış    → fine-tune
```

---

## 6. Terminal sunumu

Bu scriptler **projeksiyona yansıyacak.** Çıktı okunaklı olmalı:

- Başlık bantları, bölüm ayraçları, hizalanmış alanlar. `ortak.py`'deki
  `baslik / altbaslik / alan / kutu` yaklaşımı iyi bir örnek.
- Renk kullan ama `ATOLYE_RENKSIZ=1` ortam değişkeniyle kapanabilsin
  (`ayar.RENKSIZ` hazır). Çıktıyı log dosyasına yönlendirirken lazım.
- Model çıktısını **asla kısaltma, kırpma, düzeltme.** Ham çıktı ne ise o.
  Demonun bütün inandırıcılığı buna bağlı.
- Uzun beklemelerde (model yükleme) "yükleniyor…" bas, `flush=True`.
- `--hizli` bayrağı bütün scriptlerde olsun: Enter beklemeden baştan sona akar.
  Prova ve kayıt için.
- Yazı tipi Consolas varsayılıyor; ASCII kutu karakterleri (`─ │ ┌ ┐`) sorun değil,
  emoji kullanma.

---

## 7. Kabul kriterleri

Bitirmeden önce şunları **çalıştırıp** doğrula:

- [ ] `python 00_kontrol.py` — hepsi ✓
- [ ] `python 01_once.py --hizli` — 5 soruda da model paragraf/cümle yazıyor,
      tam eşleşme skoru düşük
- [ ] `python 02_egit.py` — hatasız bitiyor, `adapter/` ve `egitim_log.txt` oluşuyor,
      loss düşüyor, süreyi basıyor
- [ ] `python 03_sonra.py --hizli` — 5 soruda da çıktı **tek kelime** ve
      `ayar.ETIKETLER` içinde; tam eşleşme skoru en az **8/10**
- [ ] `python 04_sinir.py --hizli` — üç bölüm de çalışıyor
- [ ] Aynı scriptler `set HF_HUB_OFFLINE=1` altında da çalışıyor
- [ ] `set ATOLYE_RENKSIZ=1` ile çıktı dosyaya düzgün yazılıyor

Koşu çıktılarını `kosu_01.log`, `kosu_03.log` … diye kaydet, teslim ederken ver.

**Kritik kriter — bu tutmazsa demo ölür:**
> ÖNCE beceremeyecek, SONRA becerecek.

ÖNCE zaten tek kelime veriyorsa haber ver, `ayar.py`'yi kendi başına değiştirme.
(Muhtemel sebep: `SISTEM`'in yanlış kullanılması, ya da model çok iyi —
o durumda `set ATOLYE_MODEL=Qwen/Qwen2.5-0.5B-Instruct` ile dene.)

SONRA 8/10'un altında kalıyorsa önce `EPOK`'u 4-5'e çıkarmayı dene ve
**bunu rapor et** — `ayar.py`'ye yazma.

---

## 8. Yapma

- Web arayüzü, Gradio, Streamlit yazma.
- Notebook üretme (Colab defteri isteniyorsa ayrıca söylenecek).
- `veri/` altındaki dosyaları değiştirme veya yeniden üretme.
- Quantization (QLoRA / bitsandbytes) ekleme — sunumda anlatılıyor,
  atölyede çalıştırılmıyor. Windows'ta bitsandbytes ayrı bir dert.
- Yeni bağımlılık ekleme. Gerekiyorsa önce sor.
- Model çıktısını regex'le "düzeltme". Ham çıktı gösterilecek.

## 9. Not düş

Bir şeyin yanlış ya da eksik olduğunu düşünüyorsan `NOTLAR.md` diye bir
dosya aç ve oraya yaz. Ayarları veya veriyi kendi başına değiştirme;
bunlar sunumla eşleşiyor.
