# Derin Öğrenme — Ders Notları

Bu belge, **Deep Learning MasterClass** dersinde anlatılanların yazıya dökülmüş hâlidir.
Slaytları takip etmenize gerek yok; baştan sona okunabilir bir metin olarak hazırlandı.

Ders üç soruya cevap arıyor: **Derin öğrenme nedir, nasıl öğrenir, hangi mimariler var?**
Sonunda Colab'da hazır modellerle bir yüz analizi ve nesne tanıma uygulaması çalıştırıyoruz.

---

## Bölüm 1 — Derin öğrenmenin hikâyesi

### Fikir 1986'da hazırdı

Derin öğrenmenin hikâyesi çoğu kişinin sandığından eski. Önce haritaya bakalım:

| Yıl | Olay | Neden önemli |
|---|---|---|
| 1950 | Turing'in sorusu | Turing zekâyı tanımlamak yerine ölçmeyi önerdi: taklit oyunu |
| 1956–1959 | İki terim doğuyor | Dartmouth'ta "yapay zekâ", Arthur Samuel'in dama programıyla "makine öğrenmesi" |
| 1957 | Perceptron | İlk öğrenen yapay nöron |
| 1986 | Backpropagation | Rumelhart, Hinton ve Williams sinir ağını eğitmenin yolunu buldu |
| 1990'lar | Herkes web'e koşuyor | Dot-com çılgınlığı; zekâ da para da internete aktı, sinir ağları gözden düştü |
| 2000'ler | Ilya, Hinton'ın kapısında | Toronto'da bir öğrenci herkesin "ölü" dediği alanı seçti |
| 2007 | NVIDIA CUDA | Oyun ekran kartı bilim aletine dönüştü; eğitim haftalardan günlere indi |
| 2009 | Veri geldi | Web 2.0 kullanıcıyı üretici yaptı; ImageNet milyonlarca etiketli görseli topladı |
| 2012 | AlexNet | Görüntü tanımada hata oranı bir yılda %26'dan %15'e düştü |
| 2015 | OpenAI | Musk, Altman, Brockman ve Sutskever kâr amacı gütmeyen bir laboratuvar kurdu |
| 2017 | Transformer | "Attention Is All You Need" — bugünkü dil modellerinin mimarisi |
| 2022 | ChatGPT | Ölçeklenen modellerde beklenmedik yetenekler belirdi |
| 2024 | Nobel ödülleri | Hinton'a Fizik (Hopfield ile), Hassabis ve Jumper'a Kimya (AlphaFold) |

Yapay zekâ ve makine öğrenmesi son on yılın icadı değil. 1986'da sinir ağını nasıl
eğiteceğimiz de belliydi. Ama patlama 2012'de geldi: **fikirle patlama arasında yirmi altı
yıl var.**

Bu yıllar neyi bekledi? İki şeyi: **veri** ve **hesaplama gücü**. Veri sosyal medyadan
ve Web 2.0'dan geldi, hesaplama gücü oyun ekran kartlarından. Bir de pes etmeyen birkaç
kişiye ihtiyaç vardı.

### Ilya Sutskever

Jobs'ın yanında Wozniak, Frodo'nun yanında Sam vardı. Sam Altman'ın yanındaki isim ise
**Ilya Sutskever** — OpenAI'ın arkasındaki bilimsel beyin.

Sovyetler Birliği'nde doğdu, çocukluğu Kudüs'te geçti, gençken ailesiyle Kanada'ya
taşındı. 90'larda herkes internet çılgınlığıyla meşgulken onun aklında başka sorular
vardı: Zekâ nedir? Beyin örüntüleri nasıl okur? Hafıza nasıl çalışır?

Toronto Üniversitesi'nde hayatını değiştirecek isimle tanıştı: **Geoffrey Hinton** —
sonradan hem Turing hem Nobel ödülü alacak, sinir ağlarını pratikte kullanılabilir kılmaya
uğraşan adam. Ilya, Hinton'ın kapısını çalıp yaz tatilinde laboratuvarda ücretsiz çalışmak
istedi.

Yıllar sonra kurduğu şirkette, Altman'ı etik vizyondan yoksun bulup yönetimden uzaklaştırma
girişiminde yer alacak kadar ilkeleri olan biri. Bu yüzden ona zaman zaman "yapay zekâ
çağının Oppenheimer'ı" deniyor: yarattığı şeyin gücünü en iyi bilen ve en çok endişe eden.

### Çöpten geleceğe: sinir ağları

2000'lerin başında yapay zekâ klasik programlamaya benziyordu: **bilgi elle kodlanıyordu.**

Bir bilgisayara kediyi tarif etmeyi deneyin:

- "Bıyığı vardır." — Ya fotoğrafta görünmüyorsa?
- "Tüylüdür." — Sphynx kedisinin tüyü yoktur.
- "Kulakları sivridir." — Scottish Fold'un kulakları kıvrıktır.
- Ya kedi arkasını dönmüşse? Ya ışık kötüyse? Ya yarısı kadrajda değilse?

Tek bir kedi için gereken kural sayısı on binlere çıkıyordu. Hinton'ın fikri basitti:

> Kural yazmayalım. Milyonlarca kedi fotoğrafı gösterelim, ağırlıkları model veriden
> kendisi ayarlasın.

Amaç bilgisayara balık vermek değildi — **balık tutmayı öğretmekti.** Gereken tek şey çok
veri ve çok hesaptı. O dönem ikisi de yoktu.

### Eksik parça: veri

Kaynak Web 2.0 oldu: sosyal medya, forumlar, Wikipedia. Kullanıcı artık sadece okumuyor,
üretiyordu. **ImageNet** (2009, Fei-Fei Li ve ekibi) bu yığını etiketleyip hiyerarşik
sınıflarla tek çatı altında topladı ve dönemin en büyük görüntü tanıma yarışmasına
dönüştü. Formül hazırdı: **veri + hesaplama gücü + sinir ağı.**

### AlexNet devrimi

2012 ImageNet yarışmasına Toronto'dan bir ekip katıldı: Alex Krizhevsky, Ilya Sutskever
ve Geoffrey Hinton. İki oyun ekran kartında eğittikleri ağın adı **AlexNet**.

| Yıl | 2010 | 2011 | **2012** | 2013 | 2014 | 2015 |
|---|---|---|---|---|---|---|
| Top-5 hata oranı | %28,2 | %25,8 | **%15,3** | %11,7 | %6,7 | %3,6 |

O güne kadar hata oranı yılda bir iki puan düşüyordu. AlexNet onu bir anda on puandan
fazla aşağı çekti. Herkes önce hile olduğunu sandı. Ama düşüş hiç durmadı: 2015'te hata
oranı insan performansının altına indi.

O gün, bir anlamda ChatGPT'nin de doğum günüydü. Klasik yöntemler kenara atıldı, herkes
bu yöne döndü.

### Güç savaşları, OpenAI ve Transformer

Soru artık "derin öğrenme işe yarıyor mu" değildi; **"bu teknolojiyi kim kontrol edecek"**
idi.

- **Önce Google.** Devler trene atladı; en kolay yol satın almaktı. Google, Hinton ve
  ekibinin şirketini aldı. Ilya'nın artık veri, işlem gücü ve kaynağı vardı — ama
  özgürlüğü yoktu.
- **Sonra bir akşam yemeği.** Masada Sam Altman, Greg Brockman, Elon Musk ve Ilya vardı.
  Musk finansman, Altman yönetim, Brockman mühendislik, Ilya bilimsel vizyon. O masada
  2015'te OpenAI doğdu. Konuşulan asıl hedef bir sohbet botu değil, **AGI**'ydı.
- **Ve sonra Transformer.** 2017'de Google'dan "Attention Is All You Need" makalesi geldi:
  tekrarlı yapı yok, paralel eğitim var.

Ilya'nın tezi şuydu:

> **"Ölçeklendir ve gerisine karışma."** Model yeterince büyürse, beklemediğimiz yetenekler
> kendiliğinden ortaya çıkar.

Çocuğa her şeyi tek tek öğretmeyiz; nasıl öğreneceğini öğretiriz. Bu fikrin mimarisi
Transformer oldu, sonucu ChatGPT.

---

## Bölüm 2 — Neden derin öğrenme?

Bölümün tek cümlelik özeti:

> Klasik makine öğrenmesinde özelliği **insan** çıkarır; derin öğrenmede **model veriden
> kendisi** çıkarır.

| | Akış |
|---|---|
| Klasik makine öğrenmesi | Ham veri → **insan: feature engineering** → model → sonuç |
| Derin öğrenme | Ham veri → **model: katmanlarda kendi öğrenir** → sonuç |

2000'lerde bilgisayarla görünün standardı elle tasarlanmış özelliklerdi: SIFT (2004),
HOG (2005). Araştırmacılar yıllarını iyi özellik tasarlamaya harcıyordu. 2012'de AlexNet
bu yaklaşımı açık farkla geçti; özellik çıkarma işi modele devredildi. Kedi örneğini
hatırlayın: kural yazmak yerine örnek göstermek.

### Ama her problemin cevabı değil

| Veri / durum | Tercih |
|---|---|
| Görüntü, ses, metin, video | Derin öğrenme |
| Çok fazla etiketsiz veri | Derin öğrenme |
| Zaman serisi | Duruma göre: tek ve kısa seride klasik yöntemler (ARIMA, gradient boosting); binlerce seri ya da uzun bağlamda LSTM / Transformer |
| Tablo verisi | Klasik makine öğrenmesi (XGBoost, LightGBM) |
| Açıklanabilirlik zorunlu (banka, sigorta, sağlık) | Klasik makine öğrenmesi |

Kural basit: veri görüntü, ses, metin ya da video ise derin öğrenme; tabloysa klasik
makine öğrenmesi genelde daha iyi ve daha açıklanabilir.

---

## Bölüm 3 — Yapay nöron

Bir sinir ağı üç parçadan oluşur: **girdi katmanı**, bir ya da daha çok **gizli katman**
ve **çıktı katmanı**. "Derin" kelimesi buradan gelir — gizli katman sayısı arttıkça ağ
derinleşir. Veri soldan sağa akar.

Şimdi bunu tek bir nörona indirip parça parça kuralım:

| Parça | Ne yapar |
|---|---|
| **Girdiler** (x₁ … xₙ) | Tablo verisinde her sütun bir girdi, görüntüde her piksel |
| **Ağırlıklar** (w) | Her girdinin önem katsayısı. *Öğrenme dediğimiz şey tam olarak bu sayıları bulmak.* |
| **Bias** (b) | Sabit kaydırma terimi. Girdiler sıfır olsa bile nöronun bir şey söyleyebilmesi için |
| **Toplam** (Σ) | Her girdiyi ağırlığıyla çarp, topla, bias ekle |
| **Aktivasyon** (φ) | Toplamı doğrusal olmayan bir fonksiyondan geçir |
| **Çıktı** | Nöronun ürettiği değer |

Bir benzetme: kredi başvurusunu değerlendiren bir banka düşünün. Ağırlıklar her kriterin
(gelir, borç, yaş) ne kadar önemli olduğu, bias ise bankanın genel eşiği. Bir nöron
aslında **ağırlıklı bir oylamadır**.

> Tek nöron bu kadar: **çarp, topla, bias ekle, aktivasyondan geçir.**

### Aktivasyon neden şart?

Aktivasyon olmasaydı 100 katmanlı bir ağ, tek katmanlı doğrusal bir modele eşit olurdu —
doğrusalın doğrusalı yine doğrusaldır. Katman eklemenin hiçbir anlamı kalmazdı.

| Fonksiyon | Nerede | Ne yapar |
|---|---|---|
| **ReLU** | Gizli katmanlarda varsayılan | Negatifse 0, pozitifse aynen geçir. Basit, hızlı, gradyanı sönmüyor |
| GELU / SiLU | Transformer'larda | ReLU'nun yumuşatılmış hâlleri |
| **Sigmoid** | Çıkış katmanı, ikili sınıflandırma | Sonucu 0–1 arasına sıkıştırır (evet / hayır) |
| **Softmax** | Çıkış katmanı, çok sınıflı | Çıktıları toplamı 1 olan bir olasılık dağılımına çevirir |
| (yok) | Çıkış katmanı, regresyon | Sayı doğrudan tahmindir |

---

## Bölüm 4 — İleri yayılım (forward propagation): bir ev fiyatı tahmini

Nöronu gerçek sayılarla çalıştıralım. Elimizde bir daire var: 3 oda, 120 m², 10 yaşında,
merkeze 5 km. Gerçek fiyatı 850 bin euro.

### Önce ölçekleme

| | Oda | m² | Bina yaşı | Merkeze uzaklık | Fiyat |
|---|---|---|---|---|---|
| Gerçek değer | 3 | 120 | 10 yıl | 5 km | 850 bin € |
| Ölçeklenmiş | 0.3 | 0.6 | 0.2 | 0.5 | 0.85 |

Değerleri 0–1 arasına çektik. Yoksa 120 gibi bir sayı diğer her şeyi ezer; model sadece
metrekareye bakar. Pratikte ilk yapılan işlerden biri budur.

### Gizli katman: iki nöron

Ağımızda iki gizli nöron var. İkisi de aynı girdileri alıyor ama **ağırlıkları farklı** —
bu yüzden farklı şeyler öğreniyorlar. Ağırlıklar şimdilik rastgele.

**Birinci nöron** (ağırlıklar 0.1, 0.3, 0.5, 0.7; bias 0.1):

```
z₁ = 0.3·0.1 + 0.6·0.3 + 0.2·0.5 + 0.5·0.7 + 0.1
   = 0.03 + 0.18 + 0.10 + 0.35 + 0.1
   = 0.76
a₁ = ReLU(0.76) = 0.76        (pozitif, aynen geçiyor)
```

**İkinci nöron** (ağırlıklar 0.2, 0.4, 0.6, 0.8; bias 0.1):

```
z₂ = 0.3·0.2 + 0.6·0.4 + 0.2·0.6 + 0.5·0.8 + 0.1
   = 0.06 + 0.24 + 0.12 + 0.40 + 0.1
   = 0.92
a₂ = ReLU(0.92) = 0.92
```

### Çıktı katmanı

Gizli katmanın ürettiği 0.76 ve 0.92 artık yeni girdiler (ağırlıklar 0.3 ve 0.4; bias 0.5):

```
ŷ = 0.76·0.3 + 0.92·0.4 + 0.5
  = 0.228 + 0.368 + 0.5
  ≈ 1.10
```

**Tahmin: yaklaşık 1 milyon 100 bin euro. Gerçek fiyat: 850 bin euro.**

Çıkışta aktivasyon olmadığı için sonuç 1'i aşabiliyor — regresyonda çıktı sınırsızdır.
İlk turda bu sapma normal; ağırlıklar rastgele başladı. Peki model ne kadar yanıldığını
nasıl ölçecek?

---

## Bölüm 5 — Loss: hatanın tek sayısı

Model kendini düzeltebilmek için önce **ne kadar yanıldığını tek bir sayıya** indirmek
zorundadır. Neden tek sayı? Çünkü optimizasyon tek bir sayıyı küçültmek üzerine kuruludur.

| Problem | Loss | Not |
|---|---|---|
| **Regresyon** | MSE — (tahmin − gerçek)² | Bizim örneğimiz |
| İkili sınıflandırma | Binary Cross-Entropy | Evet / hayır problemleri |
| Çok sınıflı sınıflandırma | Categorical Cross-Entropy | Softmax ile birlikte çalışır |

Bizim örneğimizde:

```
Tahmin  ŷ = 1.10   (1.100 bin €)
Gerçek  y = 0.85   (850 bin €)
Hata      = 1.10 − 0.85 = 0.25
MSE       = 0.25² ≈ 0.06
```

Neden kare alıyoruz? Artı ve eksi hatalar birbirini götürmesin, büyük hatalar daha ağır
cezalansın diye.

> Loss küçüldükçe model iyileşiyor demektir. **Eğitim, bu tek sayıyı küçültme çabasıdır.**

---

## Bölüm 6 — Sinir ağı nasıl eğitilir?

Eğitim altı adımlık bir döngü:

1. **Initialization** — Ağırlıklar rastgele başlar. Hepsi sıfır olsa bütün nöronlar aynı
   şeyi öğrenirdi.
2. **Forward propagation** — Az önce elle yaptığımız şey: veriyi soldan sağa akıtıp tahmin
   üretmek.
3. **Loss calculation** — Tahminle gerçek arasındaki farkı tek sayıya indirmek.
4. **Backpropagation** — Hata geriye yayılır, her ağırlığın hatadaki payı hesaplanır
   (zincir kuralı; matematiğine girmiyoruz).
5. **Update weights** — Her ağırlık, hatadaki payı oranında güncellenir.
6. **Iteration** — Döngü binlerce kez tekrarlanır. Tüm verinin bir kez geçmesine
   **epoch** denir.

### Gradient descent: sisli dağdan inmek

Güncelleme formülü:

```
yeni ağırlık = eski ağırlık − öğrenme oranı × eğim
```

Sisli bir dağın tepesindesiniz ve aşağı inmeniz gerekiyor. Nerede olduğunuzu
göremiyorsunuz, ama ayağınızın altındaki eğimi hissediyorsunuz. En dik iniş yönünde bir
adım atıyorsunuz, sonra tekrar. Gradient descent tam olarak budur.

- **Öğrenme oranı** adımın boyu. Çok küçükse öğrenme sürünür, çok büyükse dibi ıskalarsınız.
- **Optimizer** bu adımı akıllandırır; bugünün varsayılanı **Adam**.

Colab'da kullanacağımız hazır modellerin hepsi bu döngüyle eğitildi.

---

## Bölüm 7 — Hangi mimariler var?

Az önce baştan sona kurduğumuz ağ bir **ANN**'di. Diğerleri bu yapının farklı veri
tipleri için özelleşmiş hâlleri.

| Mimari | Ne için | Anahtar fikir | Sınırı |
|---|---|---|---|
| **ANN** | Tablo verisi | Her girdi her nörona bağlı (fully connected) | Sıra ve konum bilgisi taşımaz |
| **CNN** | Görüntü, video, ses spektrogramı | Aynı filtre tüm görüntüde gezer | — |
| **RNN** | Zaman serisi, metin, sensör verisi | Hafızayı bir sonraki adıma taşır | Uzun geçmişi unutur, paralelleşmez |
| **LSTM** | Uzun geçmişi olan diziler | Hafıza şeridi + üç kapı | Hâlâ adım adım ilerler, paralelleşmez |
| **Transformer** | Metin ve artık neredeyse her şey | Attention: her şey her şeye bakar | — |

### ANN — Yapay sinir ağı

Her girdi her nörona bağlı. Bu yüzden model girdilerin sırasını umursamaz: bir fotoğrafın
piksellerini karıştırsanız da aynı sonucu verir. CNN tam bu yüzden var.

### CNN — Evrişimli sinir ağı

Görüntü ham piksel olarak girer. Küçük bir **filtre** (kernel) görüntünün üzerinde gezer ve
önce kenarları, sonra dokuları, sonra parçaları yakalar. **Pooling** her adımda boyutu
küçültüp önemli olanı bırakır. **Flatten** bu haritaları tek uzun bir vektöre dizer;
sonrası bildiğimiz ANN. En sonda **softmax** sonucu olasılığa çevirir:
"bu görüntü %70 zebra, %20 at, %10 köpek."

> Klasik yöntemde "zebra çizgilidir" özelliğini biz yazardık. CNN'de filtreleri model
> kendisi öğreniyor.

Nerede: yüz tanıma, tıbbi görüntü, otonom sürüş.

### RNN — Tekrarlayan sinir ağı

Pazartesi 21, salı 22, çarşamba 24 derece. Perşembe? İlk sezgi: **yarın en çok bugüne
benzer.** RNN bu sezgiyi bir hafıza okuyla taşır: aynı hücre, aynı ağırlıklar, her gün
tekrar çalışır ve bir önceki günün özetini bir sonrakine aktarır.

Peki geçen ayın soğuk dalgası? O bilgi zincirde adım adım çarpılıp söner. RNN uzun
geçmişi unutur.

### LSTM — Uzun kısa süreli hafıza

LSTM hücrenin içine bir **hafıza şeridi** (hücre durumu) koyar. Bilgi orada haftalarca
bozulmadan taşınabilir. Şeridi her biri 0–1 arası bir vana gibi çalışan üç kapı yönetir:

| Kapı | Sorduğu soru |
|---|---|
| **Forget** | Geçen ayın soğuğunu ne kadar tutayım? |
| **Input** | Bugünün 24 derecesini ne kadar yazayım? |
| **Output** | Yarın için ne vereyim? |

Vanaların ne kadar açılacağını da model öğrenir. Sadeleştirilmiş bir versiyonu **GRU**'dur.

Nerede: hava tahmini, talep tahmini, konuşma tanıma. Sınırı: hâlâ gün gün ilerliyor,
paralelleşmiyor.

---

## Bölüm 8 — Üretken ve ayırt edici yapay zekâ

Elimizde bir kedi fotoğrafları veri seti var. Aynı veriyle iki farklı şey yapılabilir:

| | Ayırt edici (discriminative) | Üretken (generative) |
|---|---|---|
| Ne yapar | Yeni bir fotoğrafa "bu bir Ankara kedisi" der, **etiket** üretir | Hiç var olmamış **yeni bir kedi** resmi üretir |
| Ne öğrenir | Sınıflar arasındaki **sınırı** | Verinin **dağılımını** |
| Örnekler | Ev fiyatı, hava tahmini, görüntü sınıflandırma | ChatGPT, görsel üretim modelleri |

Bu derste şimdiye kadar anlattığımız her şey ayırt ediciydi. Üretken model kedinin neye
benzediğini bildiği için yenisini çizebilir. ChatGPT de aynısını yapıyor — sadece piksel
yerine kelime üretiyor.

---

## Bölüm 9 — Transformer

2017'de yayımlanan [Attention Is All You Need](https://arxiv.org/abs/1706.03762)
makalesinin mimarisi iki bloktan oluşur:

- **Encoder** girdiyi okuyup anlamını vektörlere çevirir.
- **Decoder** o vektörlerden çıktıyı kelime kelime üretir.

Metin önce **embedding**'e, yani sayı vektörlerine çevrilir. Model kelimeleri sırayla değil
hepsini birden okuduğu için sıra bilgisi ayrıca verilir (**positional encoding**). En üstte
softmax bir sonraki kelimeyi seçer.

Mimari ilk olarak makine çevirisi için tasarlandı. Bugün çoğu model şemanın yarısını
kullanıyor: BERT yalnızca encoder, GPT yalnızca decoder.

### Attention: "o" kim?

> Çocuk annesiyle konuşunca parka gitmekten vazgeçti çünkü **o** evde kalmalıydı.
> → "o" = **çocuk**
>
> Çocuk annesiyle konuşunca parka gitmekten vazgeçti çünkü **o** izin vermedi.
> → "o" = **annesi**

İlk sekiz kelime aynı; yalnızca son iki kelime değişti ve zamir bambaşka birine işaret
ediyor. Bunu kural yazarak nasıl çözerdiniz? Çözemezsiniz — bağlam sonsuz.

**Attention**, her kelimenin cümledeki hangi kelimeye ne kadar bakacağını veriden öğrenir.
Kural yazmadık, sözlük vermedik; model bu bağı milyonlarca cümleden kendisi çıkardı.

### Word embeddings: anlam bir vektöre dönüşür

Model kelimeyi değil sayıyı işler. Basit bir örnekle başlayalım; iki eksen düşünün:
sosyal sınıf ve cinsiyet.

| Kelime | Vektör |
|---|---|
| Kral | [1, 2] |
| Kraliçe | [2, 2] |
| Çiftçi (erkek) | [1, 1] |
| Terzi (kadın) | [2, 1] |

Kraldan kraliçeye giden ok ile çiftçiden terziye giden ok aynı yönde. "Cinsiyet" bu
uzayda bir **yön**. Meşhur örnek buradan gelir:

> **kral − erkek + kadın ≈ kraliçe**

Gerçek modellerde bu özellikleri biz belirlemiyoruz. Bir kelimenin vektörü 0.023, 0.074,
0.033… gibi yüzlerce sayıdan oluşur; hiçbir boyutun adı yoktur, hangisinin neyi temsil
ettiğini kimse bilmez. Vektör boyutları birkaç yüzden birkaç bine kadar değişir
(örneğin 384, 1024, 1536, 3072). İki boyutla yalnızca cinsiyet ve sınıfı kodlayabilirsiniz;
bin boyutla üslup, duygu, alan bilgisi ve zaman aynı anda kodlanabilir.

Ne işe yarar? İki metnin **anlamca** ne kadar yakın olduğunu ölçeriz. Semantik arama,
öneri sistemleri ve RAG bunun üzerine kuruludur. Bu ilişkileri de kimse elle yazmadı.

---

## Bölüm 10 — Transformer'dan büyük dil modeline

Cevap ismin içinde: **GPT — Generative Pre-trained Transformer.** Aynı mimari, internet
ölçeğinde veriyle eğitilince büyük dil modeli oluyor.

> **Ön eğitim dili öğretir, ince ayar işi öğretir, RLHF nasıl konuşacağını öğretir.**

### Canavarı evcilleştirmek

1. **Ön eğitim (pre-training).** Wikipedia, forumlar, makaleler, kitaplar — internetin
   büyük kısmı. Tek görev: bir sonraki kelimeyi tahmin et. Etiket yok. En pahalı aşama;
   aylar ve milyonlarca dolar sürer. Sonuç: dili çok iyi bilen ama zararlı içeriği, yanlış
   bilgiyi, propagandayı ve hakareti de öğrenmiş bir model — **bir canavar.**
2. **İnce ayar (instruction fine-tuning).** Yapılandırılmış, kaliteli diyalog verisi. Model
   anlamlı diyalog kurmayı öğrenir; canavar sakinleşir.
3. **RLHF.** İnsanlar modelin cevaplarını puanlar; model bu geri bildirimle insan
   tercihleriyle uyumlu davranmayı öğrenir.

ChatGPT'yi ChatGPT yapan ham model değil, bu **evcilleştirme süreci**. Aynı model RLHF
olmadan bambaşka davranır — ve bu adım tamamen insan emeğine dayanır.

---

## Bölüm 11 — Colab uygulaması: yüz analizi ve nesne tanıma

Derste konuştuğumuz her şeyi hazır, eğitilmiş modellerle çalışırken görüyoruz. Hiçbir
şey eğitmiyoruz; bugün sahadaki işlerin çoğu da böyle başlıyor.

Defter: [`YuzAnalizi/DL_MasterClass_Colab_YuzAnalizi.ipynb`](YuzAnalizi/DL_MasterClass_Colab_YuzAnalizi.ipynb)
— Colab'da *Dosya → Not defteri yükle* ile açıp hücreleri sırayla çalıştırın.

| Defterdeki adım | Derste karşılığı |
|---|---|
| Yapay üretilmiş bir yüz indiriyoruz | Üretken model üretti, ayırt edici modele veriyoruz |
| RetinaFace yüzü buluyor | CNN — filtreler görüntüde geziyor |
| Yüz 224×224'e kırpılıp 0–1 aralığına çekiliyor | Ölçekleme: model fotoğraf görmez, 150.528 sayı görür |
| Duygu: 7 sınıfa dağılmış olasılık | Softmax — toplam %100 |
| Yaş tek bir sayı | Regresyon |
| Cinsiyet iki sınıflı olasılık | İkili sınıflandırma |
| Yüz 512 boyutlu bir vektöre dönüşüyor | Embedding — kosinüs benzerliğiyle "aynı kişi mi?" |
| YOLO tek bakışta 80 nesne türünü buluyor | AlexNet'ten bugüne CNN: nerede (regresyon) + ne (sınıf) |
| Kamerayla canlı nesne takibi | Tespit + kareler arası eşleştirme = kalıcı kimlik |

Ev fiyatı örneğinde 4 sayı vardı; bir yüz fotoğrafında 150.528. Fark sadece bu.

### Sınırlar ve sorumluluk

- **Yaş tahmini yaklaşıktır.** Model, eğitildiği veri setindeki insanlara benziyorsanız
  iyi çalışır; benzemiyorsanız ciddi şekilde şaşar.
- **Cinsiyet ikili değildir.** Model iki sınıfa zorlanmış durumda; bu bir gerçeklik değil,
  veri setinin kısıtı.
- **Duygu, yüz ifadesinden okunmaz.** Model yüz kaslarının konumunu sınıflandırıyor;
  insanın ne hissettiğini değil. Gülümseyen biri mutlu olmayabilir.
- **Yanlılık gerçektir.** Doğruluk, eğitim verisinde az temsil edilen gruplarda belirgin
  şekilde düşer.
- **Takip, gözetime çok yakındır.** Kişileri kareler boyunca izlemek teknik olarak kolay;
  kimin, kimi, hangi amaçla izlediği sorusu teknik değil.
- **Biyometrik veri hassas veridir.** KVKK ve GDPR kapsamında özel nitelikli kişisel veri
  sayılır; rıza olmadan işlenemez.
- **Bu modeller işe alım, güvenlik, kredi gibi kararlarda kullanılmamalı.**

> Bir modelin çalışıyor olması, o modeli kullanmanın doğru olduğu anlamına gelmez.
> Teknik yeterlilik ile etik yeterlilik ayrı şeylerdir.

---

## Özet

| Kavram | Tek cümle |
|---|---|
| Derin öğrenme | Özellikleri insan değil, model veriden çıkarır |
| Nöron | Çarp, topla, bias ekle, aktivasyondan geçir |
| Aktivasyon | Olmasa 100 katman tek bir doğrusal modele eşit olurdu |
| Ölçekleme | Büyük sayılar küçükleri ezmesin diye her şey 0–1 arasına |
| Loss | Ne kadar yanıldığının tek sayısı |
| Gradient descent | Sisli dağdan, ayağının altındaki eğime bakarak inmek |
| CNN | Aynı filtre tüm görüntüde gezer |
| RNN / LSTM | Hafızayı bir sonraki adıma taşır; LSTM uzun süre unutmaz |
| Transformer | Her kelime her kelimeye bakar, hepsi aynı anda |
| Embedding | Anlam bir vektöre dönüşür; benzer anlamlar yakın düşer |
| LLM | Ön eğitim dili, ince ayar işi, RLHF konuşmayı öğretir |

Ve hepsinin ortak noktası: **hiçbir kuralı biz yazmadık.** Bütün bu davranışlar veriden
öğrenildi.

### Kendiniz deneyin

- Bir arkadaşınıza kediyi kurallarla tarif etmesini isteyin; her kurala bir istisna bulun.
- Ev fiyatı örneğinde ağırlıklardan birini değiştirip ileri yayılımı elle yeniden hesaplayın;
  tahmin gerçeğe yaklaştı mı, uzaklaştı mı?
- Colab defterinde aynı kişinin gülümseyen ve nötr iki fotoğrafını karşılaştırın — duygu
  dağılımı nasıl değişiyor?
- Kalabalık bir fotoğraf verin — kaç yüz, kaç nesne buluyor, neleri kaçırıyor?
- Canlı takipte bir nesneyi kadrajdan çıkarıp geri getirin — aynı kimliği alıyor mu?
