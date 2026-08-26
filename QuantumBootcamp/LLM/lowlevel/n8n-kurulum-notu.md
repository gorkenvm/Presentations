# n8n Atölyesi — Kurulum ve Prova Notu

İki tam set kuruldu. Her akışın kanvasında Türkçe anlatım notları var.

## OpenAI seti (ana)

| Akış | Link |
|---|---|
| `01-basit` | https://n8n.vmgorken.com/workflow/17ffWRoQSBSPeoZd |
| `02-halusinasyon` | https://n8n.vmgorken.com/workflow/ug0gFZerTpRUN67C |
| `03-fewshot` | https://n8n.vmgorken.com/workflow/ZmsZ71U8V1R4JbpC |
| `04-rag-yukle` | https://n8n.vmgorken.com/workflow/TaIAFIV2RzsTLzPL |
| `05-rag-sorgu` | https://n8n.vmgorken.com/workflow/NAninbm3l4iaD7Tx |
| `06-agent-sohbet` | https://n8n.vmgorken.com/workflow/wpXjY7LTEc3dUb0d |

Model `gpt-4o-mini` · Embedding `text-embedding-3-small` · Memory Key `miuul`

## Gemini seti (ücretsiz yedek)

| Akış | Link |
|---|---|
| `01g-basit` | https://n8n.vmgorken.com/workflow/xf2C2G6rzSGiM5Nb |
| `03g-fewshot` | https://n8n.vmgorken.com/workflow/GQzWXr0uGH8I63BH |
| `04g-rag-yukle` | https://n8n.vmgorken.com/workflow/qzzTg3OpKZKukByl |
| `05g-rag-sorgu` | https://n8n.vmgorken.com/workflow/PpgjUvjVH9pRHM3n |
| `06g-agent-sohbet` | https://n8n.vmgorken.com/workflow/RMqG0CfdH60h6SEh | 🔴 test edilmedi |

Model `models/gemini-3.6-flash` · Embedding `models/gemini-embedding-001` · Memory Key `miuul-gemini`

**`02g` yok.** Gemini determinizmi desteklemiyor (aşağıda ölçüm var), o yüzden
halüsinasyon gösterisi `01g`'nin içinde. Numaralar `03/04/05`'te OpenAI setiyle
birebir eşleşiyor ki ders ortasında sağlayıcı değiştirmen gerekirse aynı numaralı
sekmeye geçebilesin.

---

## KLASÖRLER — senin yapman gereken tek şey

n8n MCP arayüzünde **klasör oluşturma komutu yok** (sadece var olanları listeleyebiliyorum,
şu an hiç klasör yok). İki klasörü sen aç, ben içine taşıyayım:

1. n8n → **Overview** → sağ üstteki **Create** → **Folder**
2. `atolye1-openai` ve `atolye1-gemini` adlarıyla iki klasör aç
3. Bana haber ver, akışları programatik olarak taşıyayım —
   ya da sürükle-bırak ile sen de taşıyabilirsin

---

## Dokümandan ayrılan noktalar (hepsi ölçüme dayanıyor)

### 1. `01` ve `02`'ye kısa bir System Message eklendi

Dokümandaki çıplak soruyla gpt-4o-mini sayı uydurmuyor, kaçamak cevap veriyor
("kuruma göre değişir, 500–3000 USD"). Bu cevapla halüsinasyon gösterisi ölü doğuyor.
Eklenen iki satır sadece rolü söylüyor, örnek ya da veri içermiyor.

Yan faydası: `02 → 03` farkı artık **sadece üç few-shot örneği**. Dokümanın
orijinalinde bu adımda rol talimatı ve biçim örnekleri birlikte ekleniyordu.

### 2. Temperature: `01` → 0, `02` → 1.1

n8n varsayılanı `0.7`; doküman `01`'de temperature'a dokunmadığı için `01` de
oynaktı ve `02`'nin varlık sebebi kalmıyordu. Ölçüm:

| # | 01 (temp 0) | 02 (temp 1.1) |
|---|---|---|
| 1 | 120 saat · 1.200 USD | 60 saat · 499 USD |
| 2 | 120 saat · 1.200 USD | 100 saat · 2.500 USD |
| 3 | 120 saat · 1.200 USD | 100 saat · 1.200 USD |

Doküman `0.9` diyordu ama orada üç denemeden ikisi tıpatıp aynı geldi.

Dokümanın "bonus: temperature 0 yap, tutarlı ama yanlış" adımı artık ayrı bir hamle
değil — `01` zaten o durum. `02`'den sonra `01`'e dönüp kapatıyorsun.

**Sınıfta dikkat:** Temperature, Basic LLM Chain panelinde değil, altındaki
Chat Model node'unda (`Options → Sampling Temperature`). İki akışın chain panelleri
birebir aynı görünür; o node'u açıp göstermezsen "ikisi aynı şey" sorusu gelir.

### 3. Chunk Size `700` → `1200`, Overlap `100` → `150`

Dokümandaki `700` ölçülünce zayıf çıktı. Katalogdaki 84 eğitim kaydının uzunluğu
601–3058 karakter, ortancası 753:

| Chunk | Tek parçada kalan kayıt |
|---|---|
| 700 | **12/84 (%14)** |
| 1000 | 69/84 (%82) |
| **1200** | **79/84 (%94)** |

`700`'de kayıtların %86'sı ikiye bölünüyordu. Süre/ücret satırı kaydın tepesinde
olduğu için fiyat sorusu yine çalışıyordu — ama `Modüller:` satırı **eğitimin adı
olmadan** ayrı parçaya düşüyordu. Senin "AI Engineer Paketi'nin içinde hangi
eğitimler var?" sorusuna **"katalogda bulamadım"** gelmesinin sebebi tam olarak buydu.

Chunk 1200 ile test ettim: AI Engineer kaydı (770 karakter) tek parçada kalıyor,
aramada **0.696 skorla birinci** geliyor, cevap tam doğru:
> Data Scientist Path, Deep Learning Path, Generative AI & Prompt Engineer

**Bu yüzden `04`'ü yeniden çalıştırman şart** — eski depo `700` ile kurulmuştu.

### 4. `05`'e Chat Trigger eklendi

Artık iki tetikleyici var:
- **Çalıştır** → `Soru` node'undaki sabit soru (prova ve ekran görüntüsü için)
- **Sohbet** → sol alttaki Chat düğmesi, sınıfta canlı soru yazarsın

`Soru` node'u ikisini birleştiriyor: `$json.chatInput ?? "varsayılan soru"`.
Sohbetten gelirse onu, Çalıştır'dan gelirse varsayılanı kullanıyor. Arama ve
prompt ikisi de buradan besleniyor, yani 6. bölümde hâlâ tek yer değişiyor.

### 5. `04`'te Input Binary Field bir ifade

Elle `katalog` yazmak yerine `{{ Object.keys($binary)[0] }}`. n8n sürümüne göre
binary anahtarı `katalog` ya da `katalog_0` olabiliyor; bu ifade ikisinde de çalışır.

---

## Gemini'ye özel bulgular

**Determinizm yok.** `temperature: 0`, `topK: 1`, `topP: 0.01` ile greedy decoding
zorlandı, art arda çalıştırmalar yine **750 USD** ve **450 USD** döndü. Dört
çalıştırmada dört farklı cevap. `02g`'nin bu yüzden karşılığı yok.

**İki model adı emekli olmuş** — ikisi de 404 verdi:
- `gemini-2.5-flash` → *"no longer available to new users"* → **`models/gemini-3.6-flash`**
- `text-embedding-004` → *"not found for API version v1beta"* → **`models/gemini-embedding-001`**

**Rol cümlesine fazladan bir satır gerekti:** *"Aralık verme, tahmin ifadesi
kullanma; tek bir kesin sayı söyle."* Bu olmadan Gemini "350–450 USD arası" diyor.

**Ücretsiz katman uyarısı:** Gemini'nin ücretsiz katmanında gönderilen içerik Google
tarafından ürün geliştirmede kullanılıyor. Katalog halka açık pazarlama metni,
öğrenci kayıtları kurgu — sizin için sorun değil ama bilinmeli.

**Elenen ücretsiz seçenekler:** Groq ve OpenRouter'da embedding modeli yok, `04`/`05`
hiç çalışmaz. Ollama ücretsiz ama n8n kendi sunucunda, laptopundaki Ollama'ya erişemez.

---

## "Lost connection to the server"

**OpenAI kotasıyla ilgisi yok.** Sunucudaki n8n sağlıklı: bu oturumda 15'ten fazla
çalıştırma yaptım, REST API'de tek kopma olmadı. Senin çalıştırmaların da sunucuda
**başarıyla tamamlanmış**. Sorun tarayıcıya açılan canlı push kanalında (websocket).

Sunucu agent'ına sorulacaklar:
1. **Reverse proxy websocket ayarları** — nginx ise `proxy_http_version 1.1`,
   `proxy_set_header Upgrade $http_upgrade`, `Connection "upgrade"`,
   `proxy_read_timeout 3600s` (varsayılan 60 sn, n8n için çok kısa)
2. Cloudflare proxy açık mı
3. `N8N_PUSH_BACKEND` — `websocket` ise `sse` deneyin
4. `docker logs n8n --tail 200`
5. `docker inspect n8n --format '{{.RestartCount}}'` — sıfır değilse teşhis yanlış,
   konteyner gerçekten yeniden başlıyor demektir, belleğe bakılmalı

**Derste koparsa:** tekrar çalıştırma, **Executions** sekmesine bak — çalıştırma orada.

---

## Prova kontrol listesi

1. **`04-rag-yukle`'yi çalıştır**, formdan `veri/miuul_katalog.md` yükle.
   *(Bu adımı test edemedim — form gönderimi tarayıcı gerektiriyor.)*
   Beklenen: **~70 parça**
2. **`05-rag-sorgu`** → Çalıştır → **68 saat · 300 USD**
3. Sohbet panelinden sor: `AI Engineer Paketi'nin içinde hangi eğitimler var?`
   → üç modül gelmeli
4. Sohbete `Benim ilerlemem ne durumda? Kayıt numaram 482137` → çuvallamalı
5. Gemini setinde `01g`'yi üç kez çalıştır, `04g` + `05g`'yi baştan sona bir kez geçir
6. Her adımın ekran görüntüsünü al

**Simple Vector Store bellekte.** n8n yeniden başlarsa depo boşalır — dersten hemen
önce `04`'ü (ve/veya `04g`'yi) bir kez daha çalıştır.

---

## 06 · Agent + Hafıza (yeni)

`05` aynen duruyor — aramayı ve skorları açıkta gösteren, atölyenin 5. bölümünü
anlatan hâli. `06` onun yanına eklendi: **AI Agent + Simple Memory + Katalog Arama aracı.**

**Ne yapıyor:** cevaptan sonra bağlama dayalı takip sorusu sorulabiliyor.

```
Sen : Data Scientist Path kaç saat sürüyor?
Bot : 68 saat. Kaynak: Eğitim 44 — Data Scientist Path
Sen : peki ücreti?
Bot : 300 USD.
```

**Kritik tasarım kararı — system message'da yazılı:**
> Geçmiş, SORGUYU tamamlamak için kullanılır; CEVABI vermek için değil.

Bu satır olmadan agent ikinci soruda aramayı atlayıp hafızadaki cevabı tekrarlıyordu
(kurarken bu tuzağa düştüm, ölçtüm, düzelttim). Şimdi "peki ücreti?" sorusunu
hafızayla tamamlayıp aracı **"Data Scientist Path ücret"** diye çağırıyor,
cevap her zaman katalogdan geliyor.

### Sohbet penceresinde neden ham JSON çıkıyordu

Chat Trigger `responseMode: lastNode` kullanıyor — yani **son node'un çıktısını
olduğu gibi** sohbete basıyor. Detay alanları son node'da kaldığı sürece pencerede
şu görünüyordu:

```
{ "cevap": "Merhaba! Ben Miuul...", "arama_sayisi": 0, "aramalar": [] }
```

**Çözüm:** akış üçe ayrıldı.

```
Agent → Getirilen Parçalar → Cevap
```

- **Getirilen Parçalar** — inceleme içindir, tüm detay burada durur
- **Cevap** — sohbete giden son node, içinde sadece `output` var

Artık sohbet penceresinde düz cevap görünüyor, chunk'lar ortadaki node'da duruyor.

*(Not: `arama_sayisi: 0` her zaman hata değil — "merhaba" gibi katalogla ilgisi
olmayan mesajlarda agent arama yapmıyor, bu doğru davranış.)*

### Chunk'lar nerede görünüyor

Agent'ta arama tool çağrısının içine gizlendiği için **`Getirilen Parçalar`**
node'unu ekledim. Agent'ın `returnIntermediateSteps` çıktısını ayrıştırıyor:

```
cevap         → agent ne cevapladı
arama_sayisi  → kaç kez arama yaptı
aramalar[]
  ├ sorgu        → aracı NASIL çağırdı
  ├ parca_sayisi → kaç chunk döndü
  └ parcalar[]   → chunk metinlerinin tamamı
```

Test çıktısı (gerçek): `arama_sayisi: 1`, `sorgu: "Data Scientist Path süre ücret"`,
`parca_sayisi: 2`, cevap **68 saat · 300 USD**.

**Sınıfta yapılacak gösteri:** takip sorusundan sonra bu node'u aç ve `sorgu` alanını
göster — sen "peki ücreti?" yazdın, agent "Data Scientist Path ücret" diye aradı.

### İki tuzak (ikisine de düştüm, ikisi de çözüldü)

**1. Enable Streaming açıkken `intermediateSteps` dolmuyor** → `Getirilen Parçalar`
boş kalıyor. Agent'ta streaming kapatıldı.

**2. Sabit sessionId hafızayı biriktiriyor** → ikinci çalıştırmada agent aramayı
atlıyor. `Çalıştır` yolu artık `calistir-<execution id>` üretiyor, her manuel
çalıştırma temiz başlıyor. Sohbet penceresi kendi kalıcı id'sini kullanıyor,
takip soruları orada çalışıyor.

### Dersin neresinde?

Dokümanın 7. bölümü *"n8n'de araç çağırma da var"* itirazını öngörüyor —
`06` o itirazın canlı hâli. **`05`'ten sonra göster, yerine değil.**
6. bölüm burada da çalışıyor: agent'ın elinde sadece katalog arama aracı var,
`482137` sorusunu yine cevaplayamıyor. *Aracın var olması yetmiyor, doğru aracın olması gerekiyor.*

---

## 🔴 Gemini kotası tükendi — `06g` test edilemedi

`06g-agent-sohbet` kuruldu ama **çalıştırılamadı**. Art arda 429 geldi:
> *"The service is receiving too many requests from you"*

O noktada `01g` bile aynı hatayı verdi, yani sorun akışta değil **hesabın Gemini
kotasında**. Bu oturumda yaklaşık 25–30 test çağrısı yeterli oldu.

**Bu, Gemini'yi yedek olarak zayıflatıyor.** Ölçtüğüm üç sorun:

| Sorun | Ölçüm |
|---|---|
| Kota tükenmesi | ~25–30 çağrı sonrası tüm Gemini akışları 429 |
| Takılma | `flash-lite` 6 koşudan 3'ünde 18–64 sn |
| Yavaşlık | `3.6-flash` ort. 5,6 sn; agent turu ~10 sn (OpenAI ~2,5 sn) |

**Öneri:** ana anlatımı OpenAI setiyle yap. Gemini'ye geçmen gerekirse önce bir
deneme çalıştırması yapıp kotanın açık olduğunu doğrula.

**Kota yenilenince `06g` için yapılacaklar:** `04g` → yükle, `06g` → Çalıştır,
cevap 68 saat / 300 USD gelmeli, `arama_sayisi` 1 olmalı.
