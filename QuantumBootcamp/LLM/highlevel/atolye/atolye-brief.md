# LLM Atölyesi — 2. Saat Planı

**Ders:** Deep Learning MasterClass · 2. Ders — Large Language Models
**Sunucu:** Veysel Murat Görken
**Süre:** 60 dakika, VSCode üzerinden canlı
**Ön koşul:** 1. saatte Transformer mimarisi slaytlarla derinlemesine anlatıldı (87 slayt)

---

## 1. Bu saatin tek cümlesi

> Halüsinasyon bir arıza değil, modelin çalışma biçiminin doğal sonucu.
> Onu yok edemeyiz; **doğru katmanda** ele alırız.

Katılımcının bu saatten çıkarken bilmesi gereken tek şey: **hangi problem hangi araçla çözülür.**
Kod ezberlemeyecekler — karar verebilecekler.

### Neden bu saat 1. saate muhtaç

Katılımcı transformer eğitmeyecek. Ama:

- **RAG**, bağlam penceresine metin enjekte etmektir → attention'ın o metne bakacağını bilmek gerekir
- **Fine-tune**, `q_proj / k_proj / v_proj` ağırlıklarını oynatmaktır → o üç kutunun ne olduğunu bilmek gerekir
- **Halüsinasyon**, "en olası sonraki token"in doğrulukla ilgisi olmamasıdır → autoregressive üretimi bilmek gerekir

1. saat bu üç bağı kurmak içindi. 2. saat o bağları **görünür kılmak** için.

---

## 2. Dürüst çerçeve — bu atölyenin omurgası

Dört teknik bir merdiven **değil**. Farklı katmanlara müdahale ediyorlar:

| Teknik | Neyi düzeltir | Halüsinasyona etkisi |
|---|---|---|
| **Prompt** | Görev tanımı, sınırlar | Azaltır — "bilmiyorsan bilmiyorum de" izni gerçekten işe yarar |
| **Few-shot** | **Biçim** | Biçimi düzeltir, **olguyu düzeltmez.** Rakam hâlâ yanlış |
| **RAG** | **Olgu** | Olgusal halüsinasyonun asıl çözümü budur |
| **Fine-tune** | **Davranış** | Olguyu çözmez — **kötüleştirebilir.** Dolaylı fayda: "hafızandan cevaplama, aracı çağır" alışkanlığı |

> ⚠️ **Atölyenin en kritik cümlesi:**
> Fine-tune ile modele bilgi öğretmeye çalışmak, onu emin tonla yanlış konuşmaya alıştırmanın bilinen yoludur.
> Bilgi eksikse RAG. Davranış yanlışsa fine-tune.

Bu tabloyu 2. saatin başında bir kez, sonunda bir kez göster. Aradaki 50 dakika bu tablonun kanıtı.

---

## 3. Senaryo — Çınar Üniversitesi Öğrenci Asistanı

Bir üniversitenin öğrenci işleri chatbot'u. İki tür soru geliyor:

| Soru | Cevabın yeri | Çözüm |
|---|---|---|
| "Devamsızlık sınırı kaç?" | Yönetmelikte, **belgede** | RAG |
| "Benim ortalamam kaç? No: 20210451" | Öğrenci **veritabanında** | Araç çağırma → fine-tune |

Bu ikilik senaryonun can damarı. Aynı asistan içinde yan yana duruyorlar ve **birbirinin yerine geçemiyorlar.**

### Üniversite neden uydurma?

**Çınar Üniversitesi diye bir okul yok — ve olmaması demonun şartı.**

1. Model uydurma bir okulun yönetmeliğini bilemez → halüsinasyon **garanti** gerçekleşir. Gerçek bir okul seçersen model doğru bilebilir ve demo çöker.
2. Belgedeki sayıları biz belirleriz → "model %35 dedi, belgede %30 yazıyor" kontrastı kesinleşir.
3. Katılımcı salondan kendi okulu hakkında yanlış bir bilgiyle çıkmaz.

**Ekranda bir kez söyle:** "Bu üniversite uydurma, yönetmeliği ben yazdım. Gerçek bir okulun kuralı sanmayın."

---

## 4. Dakika dakika akış (60 dk)

| Dk | Bölüm | Dosya | Ekranda ne oluyor |
|---|---|---|---|
| 0–4 | **Avianca'ya dönüş** | — | Dersin başındaki davayı hatırlat. "Şimdi aynı şeyi canlı yapalım" |
| 4–12 | **Prompt** | `01_prompt.py` | Kötü prompt → uydurma. İyi prompt → kısmen düzelir |
| 12–20 | **Few-shot** | `02_fewshot.py` | Biçim oturur, **rakam hâlâ yanlış** ⭐ |
| 20–34 | **RAG** | `03_rag.py` | Yönetmelik gelir → doğru madde + kaynak |
| 34–36 | **Köprü** | — | "Benim ortalamam kaç?" → RAG çaresiz ⭐ |
| 36–52 | **Fine-tune** | `04_finetune.py` | ÖNCE bozuk → LoRA → SONRA doğru JSON |
| 52–57 | **Sınırlar** | `05_test.py` | Unutma testi + karar tablosu |
| 57–60 | **Kapanış** | — | Harita, yapmadıklarımız, repo linki |

Gecikme olursa **RAG'den 4 dakika kıs**, fine-tune'a dokunma. Fine-tune'un ÖNCE/SONRA kontrastı bu saatin ürünü.

---

## 5. Bölüm bölüm — ne gösterilecek, ne söylenecek

### 5.1 Açılış (0–4 dk)

Ekranda hiç kod yok. Tek soru:

> "Avianca davasında avukat, olmayan mahkeme kararlarını mahkemeye sundu.
> Model neden uydurdu? Çünkü onun işi doğru cevap vermek değil — **en olası sonraki token'ı üretmek.**
> Bir saattir anlattığım şey tam olarak buydu. Şimdi aynı arızayı kendi elimizle üretelim."

Senaryoyu tanıt, uydurma üniversite uyarısını yap, VSCode'da klasörü göster.

### 5.2 Prompt (4–12 dk) — `01_prompt.py`

**Üç çalıştırma, arka arkaya:**

1. **Çıplak soru:** `"Devamsızlık sınırı kaç?"` → model bir sayı uydurur (%20, %30, ne gelirse)
2. **Aynı soruyu 3 kez sor** → **her seferinde farklı sayı** ⭐
   Bu, halüsinasyonu göstermenin en ucuz ve en ikna edici yolu. Uydurma olduğunu kanıtlamak için belgeye bile gerek yok — model kendi kendiyle çelişiyor.
3. **İyi prompt:** rol + kapsam + **"emin değilsen 'bilmiyorum' de"** → model çoğu zaman geri çekilir

**Söylenecek:**
> "Prompt'u zaten biliyorsunuz. Söylemek istediğim şu: iyi yazılmış bir prompt halüsinasyonu **azaltır**.
> En işe yarar tek cümle de şu: modele bilmeme izni vermek. Çoğu insan bunu yazmıyor."

**Söylenmeyecek:** "iyi prompt halüsinasyonu çözer."

### 5.3 Few-shot (12–20 dk) — `02_fewshot.py`

Aynı soru + 3 örnek cevap. Örnekler **biçim** öğretiyor: kısa, madde numarası veren, resmi ton.

Sonuç: **cevap artık yönetmelik maddesi gibi görünüyor — ama içindeki sayı hâlâ uydurma.**

**Bu atölyenin en öğretici anı. Yavaşla ve sor:**
> "Cevap şimdi daha profesyonel görünüyor, değil mi? Madde numarası bile var.
> Peki doğru mu? Hayır. Sadece **daha inandırıcı yanlış** oldu.
> Few-shot biçim öğretir. Biçim öğretmek bilgi öğretmek değildir."

Ek nokta: few-shot her istekte token yakar. 3 örnek × her çağrı = kalıcı maliyet.

**Nereye uygun:** geçici işler, tek seferlik dönüşümler, prototip. Kalıcı boru hattına few-shot yığmak pahalı.

### 5.4 RAG (20–34 dk) — `03_rag.py`

Üç adımı ekranda ayrı ayrı göster:

1. **Parçala + göm:** yönetmelik maddelere bölünür, her parça vektöre çevrilir
2. **Ara:** soru da vektöre çevrilir, kosinüs benzerliğiyle en yakın 3 parça bulunur
3. **Enjekte et:** bulunan parçalar prompt'a yapıştırılır, model **sadece o metinden** cevaplar

**Ekrana bulunan parçaları da yazdır** — kutu içinde. Katılımcı "model nereden buldu"yu görmeli.

**1. saate köprü:**
> "Buradaki tek numara şu: metni bağlam penceresine sokuyoruz.
> Attention o metne de bakıyor — dışarıdan gelen bir sihir yok,
> bir saat önce çizdiğimiz aynı mekanizma çalışıyor."

**Kaynak gösterimi zorunlu.** Cevabın altında "Madde 12" yazsın. RAG'in fine-tune'a karşı en büyük pratik üstünlüğü bu: **denetlenebilirlik.**

Kapanış cümlesi:
> "Halüsinasyon bitti mi? Bu soru için bitti. Çünkü cevabı modelin hafızasından değil, belgeden aldık."

### 5.5 Köprü (34–36 dk) ⭐

Yeni soru: **"Benim ortalamam kaç? Numaram 20210451"**

RAG'i aynen çalıştır. Sonuç: alakasız maddeler gelir, model ya uydurur ya "belgede yok" der.

> "RAG burada çaresiz. Çünkü bu bilgi hiçbir belgede yok — veritabanında.
> Belgede arayamazsınız, **sorgulamanız** gerekir.
> Peki model bir fonksiyonu kendi kendine nasıl çağıracak?"

Bu, "her şeyi RAG çözer" yanılgısını kıran an. Aceleye getirme.

### 5.6 Fine-tune (36–52 dk) — `04_finetune.py`

**Beş adım, hepsi ekranda:**

**① ÖNCE (3 dk).** Ham modele araçları sistem prompt'unda tarif et, soruyu sor.
Model ya laf salatası üretir ya bozuk JSON. `json.loads` patlar → kırmızı ekran.
> "Araç var, alışkanlık yok."

**② Veri (3 dk).** `ornekler.jsonl` açılır, 3-4 satır okunur.
Kritik nokta: **satırların ~%30'u araç gerektirmiyor.**
> "Bunlar olmazsa model her şeye JSON basmayı öğrenir. 'Merhaba' desen bile."

**③ LoRA config (5 dk) — KAÇIRMA.**
```python
LoraConfig(r=8, lora_alpha=16,
           target_modules=["q_proj", "k_proj", "v_proj", "o_proj"])
```
> "Bir saat önce çizdiğim üç LINEAR kutusunu hatırlıyor musunuz?
> `q_proj`, `k_proj`, `v_proj` — **eğittiğimiz tam olarak onlar.**"

**Atölyenin iki yarısını birleştiren cümle bu.** Ekranı dondur, slayta geri dön, göster.

Yanına iki rakam bas: **eğitilen parametre oranı (%0.X)** ve **adapter boyutu (MB)**.
LoRA'yı somutlaştıran şey bu iki sayı.

**④ Eğitim (2 dk) — CANLI YAPMA.**
Önceden alınmış `egitim_log.txt` dosyasını aç, loss'un düştüğünü göster.
> "Bu 8 dakika sürdü, sizi bekletmeyeyim. Kodu paylaşacağım, kendiniz çalıştırın."

**⑤ SONRA (3 dk).** Aynı soru, fine-tune edilmiş model:
```json
{"tool": "not_ortalamasi", "args": {"no": "20210451"}}
```
Parse edilir → fonksiyon çalışır → sonuç **modele geri verilir** → doğal cümle çıkar.

**Beş adımlı akışı ekranda çiz:**
```
1. Kullanıcı sorusu
2. Model → JSON araç çağrısı        ← fine-tune bunu öğretti
3. Program → fonksiyonu çalıştırır  ← modelin haberi yok
4. Sonuç → modele GERİ verilir      ← ikinci tur
5. Model → doğal cümle üretir
```

> "Modele bir yetenek kazandırmadık. `not_ortalamasi()` fonksiyonu Python'da duruyor, modelin içinde değil.
> Model o fonksiyonu çalıştırmıyor — sadece bir string üretiyor. Çağıran, bizim programımız.
> **Fine-tune yetenek değil alışkanlık kazandırır.**"

### 5.7 Sınırlar (52–57 dk) — `05_test.py`

**Unutma testi.** Fine-tune edilmiş modele: *"Merhaba, nasılsın?"*
Sohbet edebiliyor mu, yoksa buna da JSON mu basıyor?

- Sohbet ediyorsa → veri karışımı doğru kurulmuş, bunu söyle
- JSON basıyorsa → **catastrophic forgetting'i canlı yakaladın, daha da iyi.** Sakın gizleme.

> "Fine-tune bedava değil. Bir davranışı öğretirken başka bir davranışı bozabilirsiniz.
> Bu yüzden ayrılmış bir test seti ve gerçek bir değerlendirme lazım — biz bugün göz kararı yaptık."

Sonra karar tablosunu tekrar aç:

| İhtiyaç | Çözüm |
|---|---|
| Model **ne biliyor** eksik | RAG |
| Model **nasıl davranıyor** yanlış | Fine-tune |
| Sadece bir kereliğine gerek | Prompt / few-shot |

**Pratik sıra:** önce prompt → few-shot → RAG → **en son** fine-tune.
Fine-tune en pahalı, en kalıcı, geri alması en zor seçenek.

### 5.8 Kapanış (57–60 dk)

**Bugün ne gösterdik, ne göstermedik — dürüst ol:**

| Katman | Bugün |
|---|---|
| Prompt / few-shot | ✅ |
| RAG (basit, kosinüs benzerliği) | ✅ |
| SFT (ne öğretiliyor) | ✅ |
| LoRA (nasıl öğretiliyor) | ✅ |
| Quantization / QLoRA | ❌ 7B+ modelleri tek GPU'ya sığdırmak için |
| DPO / RLHF (tercih hizalama) | ❌ 1. saatte teorisini gördük |
| Full fine-tune | ❌ |
| Gerçek değerlendirme (test seti, metrik) | ❌ — en büyük eksiğimiz bu |
| Üretime alma (serving, versiyonlama) | ❌ |

> **Yanlış cümle:** "Bir de LoRA, SFT diye şeyler var, bu sadece küçük bir gösterim."
> **Doğru cümle:** "Gördüğünüz şeyin adı zaten **SFT + LoRA**. Üstünde quantization var — QLoRA. Bir de tercih hizalama var — DPO/RLHF."

Repo linkini paylaş, kodların çalıştırılabilir olduğunu söyle.

---

## 6. Ne zaman fine-tune yapılmalı (kapanış slaytı için)

**Yapılmalı:**

1. **Biçim ve şema disiplini** — JSON, XML, SQL, özel rapor formatı. Prompt'la %95 tutturursun; boru hattında %95 = her 20 istekten biri çöker.
2. **Üslup ve ses** — marka tonu, dilekçe dili, hasta notu biçemi. Tarif etmesi zor, örnekle göstermesi kolay. Fine-tune'un en güçlü alanı.
3. **Alan diline uyum** — tıp, hukuk, finans jargonu. Dikkat: *bilgi* değil, **terminoloji ve akıl yürütme kalıbı**.
4. **Maliyet/gecikme düşürme (distillation)** — sahadaki en yaygın kullanım. Büyük modelin ürettiği veriyle küçük modeli eğit; o dar görevde neredeyse aynı kalite, kat kat ucuz.
5. **Uzun sistem prompt'unu içselleştirme** — 2000 tokenlık talimatı her istekte göndermek yerine modele gömmek.
6. **Gizlilik / yerinde çalıştırma** — veri kurumdan çıkamıyorsa.

**Yapılmamalı:** güncel veya değişken bilgi. Fiyat, yönetmelik maddesi, stok. Modele gömersen her değişiklikte yeniden eğitirsin — ve model yanlış hatırlayıp emin tonla uydurur.

**Not:** büyük modellerde araç çağırma için fine-tune gerekmez, onlar zaten tool calling ile eğitilmiş geliyor. Bizim demoda küçük model kullanmamızın sebebi budur ve bunu söyle.

---

## 7. Dosya yapısı

```
atolye/
├── KURULUM.md              # 5 satırlık kurulum + model indirme
├── ortak.py                # model yükleme, sor(), renkli terminal, duraklat()
├── 01_prompt.py            # çıplak soru → 3 kez sor → iyi prompt
├── 02_fewshot.py           # biçim düzelir, rakam yanlış kalır
├── 03_rag.py               # parçala → göm → ara → enjekte et
├── 04_finetune.py          # ÖNCE → veri → LoRA → [log] → SONRA
├── 05_test.py              # unutma testi + karşılaştırma
├── veri/
│   ├── yonetmelik.md       # uydurma üniversite yönetmeliği (RAG korpusu)
│   ├── ogrenciler.json     # 15 sahte öğrenci (sahte DB)
│   └── ornekler.jsonl      # 50 satır fine-tune verisi
├── adapter/                # eğitim çıktısı (gitignore)
└── egitim_log.txt          # önceden alınmış eğitim çıktısı — YEDEK
```

Her dosya **tek başına çalışır**. Katılımcı istediğini ayrı çalıştırabilsin, sıra bağımlılığı olmasın.

---

## 8. Teknik seçimler ve gerekçeleri

### 8.1 Tek model mi, iki model mi?

**Tek model: `Qwen/Qwen2.5-0.5B-Instruct`** (alternatif: `google/gemma-3-270m-it`)

Gerekçe: dört demo aynı modelde koşarsa karşılaştırma temiz olur — değişen tek şey teknik. İki farklı model kullanırsak "büyük model zaten iyiydi" karışıklığı doğar.

**Risk ve cevabı:** salondan "model küçük olduğu için uyduruyor" itirazı gelecek.
Cevap hazır olsun: *"Avianca'da uyduran model küçük değildi. Küçük model sadece daha çabuk gösteriyor."*
İstersen aynı soruyu büyük bir modele sorup ekran görüntüsünü önceden al, yanına koy.

**Prova şartı:** Qwen2.5-0.5B, Qwen3-0.6B ve Gemma 3 270M'i kendi senaryonla dene.
Seçim kriteri tek: **fine-tune öncesi görünür şekilde çuvallayan, sonrası düzelen** hangisiyse o.

### 8.2 Eğitim döngüsü — manuel mi, TRL mi?

**Manuel döngü kullan** (repodaki gibi). Gerekçe: kod anlatmayacaksın, uzunluğu problem değil; buna karşılık TRL'in API'si sürümler arasında değişiyor ve atölye sabahı sürpriz istemezsin.

Ama kapanışta **10 satırlık `SFTTrainer` eşdeğerini bir slaytta göster**:
> "Gerçek hayatta bunun hazırı var, adı TRL. Bugün altını açtık ki ne yaptığını bilin."

### 8.3 RAG — LangChain kullanma

Tek demo için `sentence-transformers` + numpy kosinüs benzerliği yeter, ~20 satır, sürüm cehennemi yok.
LangChain/LlamaIndex soyutlamalarını açıklamak tek başına 10 dakika yer.

**Türkçe embedding modeli şart.** İngilizce MiniLM Türkçe yönetmelikte belirgin şekilde kötü sonuç verir ve demoyu baltalar → `intfloat/multilingual-e5-small` gibi çok dilli bir model kullan.

### 8.4 Sürümleri sabitle

Prova ettiğin sürümleri `requirements.txt`'e yaz. Atölye günü `pip install -U` yapma.

---

## 9. Yapılacaklar

- [ ] `veri/yonetmelik.md` — uydurma üniversite yönetmeliği, 12-15 madde. Devamsızlık, bütünleme, harç, mezuniyet, ders tekrarı, yatay geçiş. **Sayılar akılda kalıcı ve spesifik olsun** (%30 değil %28 gibi) — modelin uydurmasıyla çakışma ihtimali düşsün.
- [ ] `veri/ogrenciler.json` — 15 sahte öğrenci: numara, ad, GNO, borç, ders programı.
- [ ] Üç araç fonksiyonu: `not_ortalamasi(no)`, `ders_programi(no)`, `borc_sorgula(no)`.
- [ ] `veri/ornekler.jsonl` — 50 satır. **~%70 araç gerektiren, ~%30 gerektirmeyen.** Numara bazen verilmiş bazen sorulmalı; numara formatları çeşitli olsun.
- [ ] `ortak.py` — model yükleme, `sor()`, renkli çıktı, `duraklat()`, `--hizli` bayrağı.
- [ ] `01`–`05` betikleri.
- [ ] **Prova çalıştırması** — gerçek süreleri ölç, `egitim_log.txt`'i üret.
- [ ] Modeli önceden indir; atölye günü ağdan model çekme.
- [ ] Sunuma 4 slayt: dürüst çerçeve tablosu (§2), 5 adımlı araç akışı (§5.6), karar kuralı (§5.7), ne yapmadık (§5.8).

---

## 10. Riskler ve yedekler

| Risk | Yedek |
|---|---|
| Ağ yok / model inmiyor | Model önceden indirilmiş olsun, `HF_HUB_OFFLINE=1` ile prova et |
| Canlı eğitim uzun sürüyor | **Zaten canlı eğitmiyoruz** — `egitim_log.txt` hazır |
| Model beklenen hatayı yapmıyor | Her demonun çıktısını önceden kaydet, gerekirse kayıttan anlat |
| Süre taşıyor | RAG'den 4 dk kıs. Fine-tune'a dokunma |
| İlk çağrı çok yavaş | 1. saatin sonunda bir terminalde modeli yükle, ısınsın |
| "Küçük model olduğu için" itirazı | §8.1'deki cevap hazır |

---

## 11. Referans repo

`github.com/erturkkadir/bpe` — **GPL-3.0**. Türetip dağıtırsan türev de GPL-3 olmak zorunda.

Faydalanılabilecek yerler:

- `finetune/finetune_demo.py` — ÖNCE/SONRA kurgusu, renkli terminal, `duraklat()` deseni. **İskeleti al**, araçları ve veriyi değiştir.
- `finetune/tool_demo.py` — çıktıdan araç çağrısı ayrıştırma + dispatch döngüsü.
- `transformer.py` — sıfırdan decoder-only GPT, Türkçe yorumlu. `Head` sınıfı 20 satırda Q/K/V + √d ölçekleme + causal mask. **Vaktin varsa 2. saatin başında 2 dakika aç:** "bir saattir anlattığım şey, işte 12 satır." Bedeli sıfır, getirisi yüksek.
- `bpe_demo.py` — saf Python BPE. 1. saatte tokenizasyonu zaten anlattın; repoda dursun, isteyen çalıştırsın.

**Düzeltilecek hata:** `finetune_demo.py` içinde `VERI = pathlib.Path("veri/ornekler.jsonl")` yazıyor ama dosya `finetune/ornekler.jsonl`'de. İlk çalıştırmada `sys.exit(1)` yer.
