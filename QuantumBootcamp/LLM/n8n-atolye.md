# n8n Atölyesi — Miuul Öğrenci Destek Asistanı

**Senaryo:** Miuul eğitim platformunun öğrenci destek asistanı.
İki tür soru geliyor ve **ikisi aynı yolla çözülmüyor** — bütün atölye bunun üzerine kurulu.

| Soru | Cevabın yeri | Çözüm |
|---|---|---|
| "Data Scientist Path kaç saat, ücreti ne?" | **Katalogda** — `veri/miuul_katalog.md` | RAG · n8n |
| "Benim ilerlemem ne durumda? No 482137" | **Kayıt sisteminde** — `veri/kayitlar.json` | Araç çağırma · fine-tune · Colab |

**Veri:** `atölye/veri/` altında. Katalog gerçek (miuul.com, 24 Ağustos 2026), öğrenci kayıtları kurgu.

**Bu dosya n8n bölümünü kapsıyor.** Fine-tune bölümü Colab/lokalde, `04_finetune.py` ile.

> **Sürüm notu:** aşağıdaki node isimleri n8n'in güncel sürümünden doğrulandı.
> Panelde bulamazsan görünen ada göre ara — akış mantığı aynı.

---

## 0 · Hazırlık (dersten önce)

**Ortam:** `n8n.cloud` ücretsiz deneme. Self-host istersen `npx n8n` — ama Cloud'da dosya/port derdi çıkmaz.

**Kimlik:** `Credentials → OpenAI` altına API anahtarını bir kez gir. `gpt-4o-mini` yeterli ve ucuz.

**Beş workflow aç:**
```
01-basit  ·  02-halusinasyon  ·  03-fewshot  ·  04-rag-yukle  ·  05-rag-sorgu
```
Sınıfta sekme değiştirerek ilerlersin, tek akışı bozup durmazsın.

**Katalog dosyasını hazırla:** `veri/miuul_katalog.md` 77 KB. Set node'una yapıştırmak yerine
**Form Trigger ile yükleyeceğiz** (bkz. bölüm 4) — hem daha temiz, hem "belgeyi sisteme veriyoruz" anı oluyor.

**Doğru cevaplar** (provada teyit et, sınıfta kontrol için lazım):

| Soru | Doğru cevap |
|---|---|
| Data Scientist Path | **68 saat · 300 USD · Kariyer Yolculuğu · 9 modül · 4.5/5** |
| 482137 ilerleme | Elif Yaman · AI Data Scientist Bootcamp · **%60 (6/10 modül)** |
| 482154 ödeme | Mert Doğan · toplam 550, ödenen 220, **kalan 330 USD** |

---

## 1 · `01-basit` — En basit hâli (4 dk)

```
[Manual Trigger] → [Basic LLM Chain]
                        └── [OpenAI Chat Model]
```

**Basic LLM Chain** · *Source for Prompt* → `Define below` · metin:
```
Data Scientist Path kaç saat sürüyor ve ücreti ne kadar?
```

**Çalıştır.** Cevap gelir — akıcı, kendinden emin.

> "İki kutu. Soru giriyor, cevap çıkıyor. Bir LLM uygulamasının en basit hâli bu. Şimdi bu cevabın doğru olup olmadığına bakalım."

---

## 2 · `02-halusinasyon` — Uydurmayı canlı yakala (8 dk) ⭐

`01-basit`'i kopyala. **OpenAI Chat Model** node'unda `Options → Temperature` → **0.9**.

**Üç kez arka arkaya çalıştır**, her seferinde çıktıyı sınıfa göster.

Beklenen: her seferinde **farklı bir saat ve farklı bir fiyat.**

> "Belgeye bakmama bile gerek yok — model kendi kendisiyle çelişiyor. Demek ki bilmiyor, üretiyor."

Şimdi kataloğu aç, gerçek satırı göster: **68 saat, 300 USD.**

> "Model bu sayıyı bilemez. Miuul'un kataloğu onun eğitim verisinde ya hiç yoktu ya da güncelliğini yitirdi. Ama yine de bir sayı söyledi. İşte halüsinasyon."

**Bonus (30 sn):** Temperature'ı `0` yap, üç kez daha çalıştır — artık hep aynı cevap.
> "Tutarlı oldu ama doğru olmadı. Tutarlılık ile doğruluk aynı şey değil."

---

## 3 · `03-fewshot` — Biçim düzelir, olgu düzelmez (8 dk)

`02`'yi kopyala. **Basic LLM Chain** → `Add Option → System Message`:

```
Sen Miuul eğitim platformunun öğrenci destek asistanısın.
Cevapların kısa olsun, katalog kaydı biçiminde ver.

Örnekler:

Soru: Zaman Serileri eğitimi kaç saat?
Cevap: Zaman Serileri — Kurs · 7 saat · 55 USD · 4.5/5

Soru: MS SQL Sorgulama ne kadar sürüyor?
Cevap: MS SQL Sorgulama — Kurs · 9 saat · 28 USD · 4.4/5

Soru: Özellik Mühendisliği hakkında bilgi verir misin?
Cevap: Özellik Mühendisliği — Kurs · 7 saat · 28 USD · 4.7/5
```

**Aynı soruyu sor.** Cevap artık **birebir katalog kaydı biçiminde** gelecek — tire, nokta, sıralama, hepsi doğru. **Ama içindeki sayılar hâlâ uydurma.**

Ekranı ikiye böl: solda n8n çıktısı, sağda kataloğun 304. satırı.

> "Cevap artık gerçek bir katalog kaydına benziyor. Biçim kusursuz. Peki doğru mu? Hayır — sadece daha inandırıcı yanlış oldu. Few-shot biçim öğretir. Biçim öğretmek bilgi öğretmek değildir."

**Maliyet notu (30 sn):** üç örnek her istekte tekrar gönderiliyor.
> "Geçici işler için ideal. Kalıcı bir boru hattına few-shot yığmak pahalıya patlar."

---

## 4 · `04-rag-yukle` — Kataloğu sisteme ver (7 dk)

```
[n8n Form Trigger]  (dosya alanı)
        ↓
[Extract from File]  (operation: Text)
        ↓
[Simple Vector Store]  (mode: Insert Documents)
        ├── [Embeddings OpenAI]
        └── [Default Data Loader]
                └── [Recursive Character Text Splitter]
```

**Ayarlar:**

| Node | Ayar |
|---|---|
| **n8n Form Trigger** | Bir alan ekle: tip `File`, ad `katalog` |
| **Extract from File** | *Operation* → `Text`, *Input Binary Field* → `katalog` |
| **Default Data Loader** | *Type of Data* → `JSON` · *Mode* → `Load Specific Data` · alan: `data` |
| **Recursive Character Text Splitter** | *Chunk Size* `700` · *Chunk Overlap* `100` |
| **Simple Vector Store** | *Operation Mode* → `Insert Documents` · *Memory Key* → `miuul` |

**Çalıştır**, form linkini aç, `miuul_katalog.md`'yi yükle.

Çıktıda kaç parça oluştuğunu göster (~100 civarı).

> "Kataloğu parçalara böldük ve her parçayı bir vektöre çevirdik. Anlam artık ölçülebilir bir şey — az önce teoride konuştuğumuz embedding tam olarak bu."

**Chunk size neden 700?** Katalogdaki her eğitim kaydı ~600–900 karakter. Bir kayıt ortadan bölünürse süre bir parçada, ücret diğerinde kalır ve RAG yanlış cevap verir. Provada bunu kontrol et.

---

## 5 · `05-rag-sorgu` — Bilgiyi getir, pencereye koy (10 dk)

Burada **iki yol** var. Sınıf için **A yolunu** öneriyorum: getirilen parçaları öğrenci **görüyor**.

### A · Arama görünür (önerilen)

```
[Manual Trigger] → [Simple Vector Store]  (mode: Get Many)
                        └── [Embeddings OpenAI]
                   → [Edit Fields (Set)]     bağlamı birleştir
                   → [Basic LLM Chain]
                        └── [OpenAI Chat Model]
```

| Node | Ayar |
|---|---|
| **Simple Vector Store** | *Operation Mode* → `Get Many` · *Memory Key* → `miuul` (birebir aynı!) · *Prompt* → soru · *Limit* → `4` |
| **Edit Fields (Set)** | *Mode* → `JSON`, içerik: bulunan parçaların metinlerini tek alanda birleştir |
| **Basic LLM Chain** | prompt: aşağıdaki kalıp |

**Prompt kalıbı:**
```
Sadece aşağıdaki katalog parçalarına dayanarak cevapla.
Bilgi parçalarda yoksa "katalogda bulamadım" de, tahmin etme.

KATALOG:
{{ $json.baglam }}

SORU: Data Scientist Path kaç saat sürüyor ve ücreti ne kadar?
```

**Çalıştır.** İki şeyi ayrı ayrı göster:

1. **Vector Store çıktısı** — hangi parçalar geldi, benzerlik skorlarıyla. ⭐ Öğrenci aramanın gerçekten olduğunu burada görüyor.
2. **Model çıktısı** — **68 saat, 300 USD.** Doğru.

> "Modele hiç dokunmadık. Ağırlıklar aynı, hiçbir eğitim yapmadık. Tek yaptığımız doğru sayfayı bulup pencereye koymak. Attention o metne de bakıyor — dışarıdan gelen bir sihir yok."

### B · Tek kutuda (kısa yol)

Vakit daralırsa: `[Question and Answer Chain]` + `[Vector Store Retriever]` + `[Simple Vector Store (Retrieve)]`.
Daha az node ama **arama adımı gizli kalıyor** — öğretici değeri düşük.

### İki soru daha (sınıf istesin, sen yaz)

```
Deep Learning Path kaç modülden oluşuyor?
AI Engineer Paketi'nin içinde hangi eğitimler var?
```

---

## 6 · RAG'in çuvalladığı an (5 dk) ⭐ **BU ADIMI ATLAMA**

Aynı `05-rag-sorgu` akışında **sadece soruyu değiştir:**

```
Benim ilerlemem ne durumda? Kayıt numaram 482137
```

**Çalıştır.** Vector Store alakasız katalog parçaları getirecek — bootcamp açıklamaları, modül listeleri. Model ya "katalogda bulamadım" diyecek ya da uyduracak.

> "RAG burada çaresiz. Çünkü bu bilgi hiçbir belgede yok — kayıt sisteminde, bir veritabanında. Belgede **aramazsınız**, **sorgularsınız**.
>
> Doğru cevap şu: Elif Yaman, AI Data Scientist Bootcamp, yüzde 60. Bu bilgi `kayitlar.json` içinde duruyor ve oraya ulaşmanın tek yolu bir fonksiyon çağırmak.
>
> Peki model bir fonksiyonu kendi kendine nasıl çağıracak? İşte Colab'a bu yüzden geçiyoruz."

n8n'i burada kapat.

---

## 7 · İki uyarı

**① "n8n'de araç çağırma da var" itirazı gelirse — gelecektir.**

Doğru. AI Agent node'una tool bağlayıp `gpt-4o-mini` ile bu işi n8n'de de yapabilirsin. Ama cevabın hazır olsun:

> "Evet, yapabiliriz — çünkü GPT-4o-mini zaten araç çağırmayı öğrenmiş olarak geliyor. Biz Colab'da bunu **bilmeyen** küçük bir modele sıfırdan öğreteceğiz. Amaç aracı çalıştırmak değil, bir modele yeni bir davranışın nasıl kazandırıldığını görmek."

Bu cümle, atölyenin ikinci yarısının niye var olduğunu açıklıyor. Hazırda tut.

**② "Bunlar hazır kutular, biz Python yazıyoruz" itirazı.**

30 saniye ekranda göster — `03_rag.py` zaten bunu yapıyor:

```python
model    = SentenceTransformer("intfloat/multilingual-e5-small")
parcalar = parcala()                      # 1  katalogu kayıtlara böl
V        = model.encode(parcalar)         # 2  vektöre çevir
q        = model.encode([soru])[0]
skor     = V @ q                          # 3  en yakını bul
baglam   = en_yakin_3(parcalar, skor)     # 4  pencereye koy
```

> "n8n'in o dört kutusunun yaptığı şey bu. Kutuları anladıysanız kodu da anladınız. İkisini de paylaşacağım."

---

## 8 · Riskler ve yedekler

| Risk | Yedek |
|---|---|
| Ağ / API hatası | **Provada her adımın ekran görüntüsünü al** |
| Üç denemede de aynı cevap | Temperature `0.9`, gerekirse `1.1` |
| RAG yanlış parça getiriyor | Chunk size `700` → `500`, Limit `4` → `6` |
| Vector Store boş | Yükleme akışını tekrar çalıştır · **Memory Key iki node'da birebir aynı mı?** |
| Form Trigger dosya almıyor | Yedek: Edit Fields (Set) node'una kataloğun **ilk 30 eğitimini** yapıştır |
| Süre taşıyor | Bölüm 3'ü 5 dakikaya indir · **bölüm 6'ya dokunma** |

**Provada mutlaka:** beş akışı da baştan sona bir kez çalıştır, çıktıları kaydet,
ve Data Scientist Path sorusunun **68 saat / 300 USD** döndürdüğünü teyit et.

---

## 9 · Zaman planı (n8n bölümü — 42 dk)

| Dk | Bölüm |
|---|---|
| 0–4 | `01-basit` — en basit hâli |
| 4–12 | `02-halusinasyon` — üç kez çalıştır ⭐ |
| 12–20 | `03-fewshot` — biçim düzelir, sayı yanlış kalır |
| 20–27 | `04-rag-yukle` — kataloğu yükle, parçala, vektörle |
| 27–37 | `05-rag-sorgu` — ara, göster, cevapla |
| 37–42 | **RAG'in çuvallaması** ⭐ → Colab'a köprü |

Kalan 18 dakika: Colab'da fine-tune + karar tablosu + kapanış.
