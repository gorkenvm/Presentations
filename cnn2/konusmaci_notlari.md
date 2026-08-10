# Konuşmacı Notları — CNN Mimarileri

> Bu dosya **sadece anlatıcı içindir**. Colab defteri katılımcılarda açık olacağı için
> konuşma metni oraya konmadı. Bunu ikinci ekranda / telefonda açık tut.

Defterdeki akış tek bir örnek üzerinden ilerliyor, kopmuyor:

```
6×6×3  →  [Conv: 4 filtre, 3×3×3]  →  4×4×4  →  [MaxPool 2×2]  →  2×2×4  →  [Flatten]  →  16
```

---

# BÖLÜM A — Önceki dersin özeti

## 1. CNN Mimarisi

**Aç:** "Bir görüntüyü sınıflandırmak istiyoruz. Ama 224×224×3 = 150 bin sayı. Bunu doğrudan
bir sinir ağına verirsek parametre patlar. CNN'in yaptığı şey: önce görüntüyü *özetlemek*,
sonra özet üzerinden karar vermek."

GIF oynarken sırayla söyle — her aşamada tek cümle:

| Aşama | Söylenecek |
|---|---|
| Girdi | "Görüntü bizim için bir sayı matrisi. Piksel değerleri." |
| Convolution + ReLU | "Filtre gezer, öznitelik çıkarır. Kenar, köşe, doku." |
| Pooling | "Küçült ama önemliyi kaybetme. Bu blok üst üste tekrar eder." |
| Flatten | "Matrisleri tek sıraya ser — sinir ağı böyle istiyor." |
| Fully Connected | "Kararı burada veriyoruz." |
| Softmax | "Çıktı olasılık: zebra 0.7." |

**Soru at:** "Neden doğrudan Dense katmanına vermiyoruz?"
Beklenen cevap: parametre sayısı + konum bağımsızlığı (aynı kedi sol üstte de olsa tanınmalı).

## 1.1 Piksel / gri tonlama / renkli

Hızlı geç, tek cümle: "Bilgisayar resmi görmez, sayı görür."

Vurgulanacak tek şey: **renkli görüntü üç ayrı matristir**. Bir sonraki bölümde
"filtre neden 3 kanallı" sorusunun cevabı burada.

## 2. Convolution

### Bir filtre = tek bir 3B çekirdek

Bu GIF'te **girdi 5×5×3** — ana akıştaki 6×6 değil. Bilerek küçük tutuldu, tek bir
hücrenin nasıl hesaplandığını göstermek için. Katılımcı sorarsa: "Burada tek bir çıktı
hücresine odaklanıyoruz, birazdan asıl örneğe döneceğiz."

**En kritik cümle:** "Filtre 3 kanallı. Her kanal kendi dilimiyle çarpılıyor, üç sonuç
**toplanıyor**, bias ekleniyor. Sonuç **tek bir sayı**. Yani derinlik kayboluyor."

**Sık yapılan hata:** Katılımcılar "3 kanal girdi → 3 kanal çıktı" sanıyor. Değil.
Bir filtre → bir harita.

### Kaç filtre = kaç çıktı kanalı

"Çıktının derinliğini girdinin derinliği belirlemiyor — **filtre sayısı** belirliyor."
`Conv2D(4, (3,3))` → buradaki 4, filtre sayısı.

### Filtre ağırlıkları

Sorulacak soru bu: **"Bu filtredeki sayıları kim yazıyor?"**

- Başlangıçta **rastgele**. Keras varsayılanı `glorot_uniform`; ReLU ile `he_normal` da yaygın.
- Sıfırla başlatılmaz — tüm filtreler aynı olur, hepsi aynı gradyanı alır, hiçbiri
  farklılaşmaz ("simetri kırılmaz").
- **Eğitimin amacı tam da bu ağırlıkları bulmak.** Binlerce adım sonra bazı filtreler
  kenar bulmayı, bazıları doku bulmayı "keşfeder". Kimse onlara kenar dedektörü ol demedi.

Vurgu: "Klasik görüntü işlemede Sobel filtresini biz yazardık. Burada ağ kendi Sobel'ini
buluyor — ve bizim aklımıza gelmeyecek 200 tane daha."

### Stride — YAN YOL

Bunu söyle: **"Şimdi ana akıştan bir dakika ayrılıyoruz."** Stride ve padding, conv
katmanının ayarları; ana örneğimizde ikisi de varsayılan.

Özel durum: 6×6'da stride 2 → son sütun ve satır hiç taranmıyor. `padding='valid'`
taşan kısmı sessizce atar. "Boyutlarınız bölünmüyorsa veri kaybediyorsunuz, uyarı almazsınız."

### Padding — YAN YOL

Neden: kenar bilgisi, segmentasyonda aynı boyut zorunluluğu, derin ağlarda birikimli kayıp.

Özel durum: sıfır dolgu kenarda **yapay kenar** yaratır — GIF'te ilk sütundaki −16/−24
gerçek bir kenar değil.

**Ana akışa dönerken açıkça söyle:** "Örneğimizde stride 1, padding yok. Yani hâlâ 4×4×4."

## 3. Pooling

"Conv'dan çıkan 4 kanallı 4×4 bloğu aldık. Pooling **her kanala ayrı ayrı** uygulanır."

**En kritik cümle:** "Pooling kanal sayısına dokunmaz. 4 girdi, 4 çıktı. Kanal sayısını
değiştiren tek şey conv katmanındaki filtre sayısıdır."

**Özel durum — sık atlanan:** `MaxPooling2D`'de stride varsayılanı **pencere boyutuna
eşittir** (2×2 → stride 2). `Conv2D`'de ise **1**. İki katmanın varsayılanı farklı.

**Soru at:** "Boyut küçülünce bilgi kaybediyor muyuz?"
Cevap: evet, kasıtlı. Amaç konum hassasiyetini azaltmak; nesne 2 piksel kaysa da aynı
sonucu istiyoruz. Kayıp değil, soyutlama.

## 4. Flatten

**Kritik ve sık yanlış bilinen:** Sıralama **kanal kanal değil**. TensorFlow/Keras
`channels_last` düzeninde sıra (satır, sütun, kanal).

- Doğru: `6 9 9 9 | 7 9 8 9 | 5 8 9 8 | 9 9 8 9`
- Yaygın yanlış: `6 7 5 9 | 9 9 8 9 | ...`

"Flatten'ın ağırlığı yoktur, hiçbir şey öğrenmez. Sadece şekil değiştirir."

---

# BÖLÜM B — Asıl konu

## 5. Pretrained modeller

**Aç:** "Elinizde 500 fotoğraf var. Sıfırdan bir CNN eğitseniz ezberler. Ama birisi
1.2 milyon görüntüyle haftalarca eğitim yapmış ve ağırlıkları paylaşmış."

**Neden işe yarıyor — asıl anlatılacak fikir bu:**
İlk katmanlar **kenar ve renk** öğrenir. Kedi fotoğrafında da çöp fotoğrafında da kenar
kenardır. O yüzden ilk katmanlar devredilebilir. Son katmanlar ise ImageNet'in 1000
sınıfına göre ayarlanmıştır — devredilmez, onu siz değiştirirsiniz.

**Dürüst ol:** ImageNet günlük nesnelerden oluşur. Tıbbi görüntü veya uydu fotoğrafında
kazanç azalır. Yine de sıfırdan iyidir.

## 6. Zaman çizelgesi

Çizelgedeki kutular kasten kısa. **Ayrıntıyı sen anlat** — aşağıda her model için
"neden önemliydi / bugün ne durumda" var. Hepsini anlatma; ● işaretli olanlara ve
soru gelenlere odaklan.

### Sınıflandırma (backbone)

| Model | Neden önemliydi | Bugün |
|---|---|---|
| **LeNet-5** (1998) | Evrişim + pooling fikrini ilk kez birleştirdi; banka çeklerindeki rakamları okudu | 7 katman, 32×32 gri girdi. Gerçek fotoğraflar için fazla küçük |
| **AlexNet** (2012) | ReLU, dropout ve GPU eğitimi. ImageNet'i büyük farkla kazandı | 11×11 filtreler ve şişkin Dense katmanlar israf |
| **VGG** (2014) | Tek kural: her yerde 3×3. Mimariyi okunabilir yaptı | 138M parametre pahalı. Öznitelik çıkarıcı olarak yaşıyor |
| **GoogLeNet** (2014) | Aynı katmanda 1×1, 3×3, 5×5 paralel; 1×1 hesabı ucuzlatır | Kurması karmaşık. Fikirleri her yerde yaşıyor |
| **ResNet** (2015) ● | Kısayol bağlantısı; derin ağ ilk kez eğitilebildi | Hâlâ en güvenli başlangıç noktası |
| **Inception-ResNet v2** (2016) | Inception + kısayol birleşimi | Doğruluğu iyi ama hantal |
| **Xception** (2016) | Evrişimi ikiye böldü: önce her kanal ayrı, sonra kanallar arası | Bu fikir MobileNet'in temeli oldu; modelin kendisi seyrek |
| **DenseNet** (2017) | Her katman kendinden öncekilerin hepsine bağlı | Az parametre ama çok bellek. Tıbbi görüntülemede tercih ediliyor |
| **MobileNet** (2017) ● | Telefon/gömülü cihaz için tasarlanmış ilk ciddi CNN | Hız veya boyut kısıtı olan her yerde ilk seçenek |
| **MobileNetV2** (2018) ● | Blokları ters çevirdi: önce genişlet, işle, sonra daralt | Transfer learning'in fiili standardı |
| **EfficientNet** (2019) ● | Derinlik, genişlik ve çözünürlüğü birlikte ve oranlı büyüttü | Aynı doğruluk daha az hesapla; B0–B7 arası seçim |
| **ConvNeXt** (2022) ● | ResNet'i Transformer'lardan öğrenilenlerle yeniledi | Modern CNN'lerin en güçlüsü — *ders kapsamı dışı* |

### Nesne tespiti

| Model | Neden önemliydi | Bugün |
|---|---|---|
| **Sliding Window** | Pencereyi tek tek gezdirip her konumu sınıflandırma fikri | Binlerce pencere = binlerce hesap. Kullanılamaz |
| **R-CNN** (2014) | Her yeri taramak yerine ~2000 aday bölge seç | Her bölgeye ayrı CNN; tek görüntü dakikalar sürüyor |
| **Fast R-CNN** (2015) | CNN'i bir kez çalıştır, bölgeleri ortak haritadan kes; ~100 kat hız | Bölge önerileri hâlâ ağın dışında |
| **Faster R-CNN** (2015) | Bölge önerisi de ağın içine girdi (RPN); uçtan uca tek ağ | Doğru ama iki aşamalı, yavaş. Hassas işlerde |
| **YOLO v1** (2016) | Tek bakışta hem kutu hem sınıf; anlık tespiti başlattı | Küçük nesnelerde zayıf; sonraki sürümler geçti |
| **SSD** (2016) | Farklı ölçeklerdeki haritalardan tespit | Basit ve hızlı; doğrulukta YOLO'nun gerisinde |
| **Mask R-CNN** (2017) ● | Kutunun yanına piksel maskesi: nesnenin şekli de var | Instance segmentation'ın referans modeli |
| **RetinaNet** (2017) | Focal loss: kolay arka plan örnekleri eğitimi boğmasın | Focal loss her yerde; model olarak yerini bıraktı |
| **YOLOv3** (2018) | Çok ölçekli tahmin, güçlü omurga | Sonrakiler hem hızlı hem doğru. Eski projelerde çıkar |
| **YOLOv8** (2023) ● | Tespit + segmentasyon + sınıflandırma tek pakette | Sahada en yaygın. **Bu derste bunu kullanacağız** |
| **YOLO26** (2026) ● | NMS adımını kaldırdı, uçtan uca tek geçiş | Güncel sürüm — *ders kapsamı dışı*, API benzer |

## 7. AlexNet

Anlatım sırası: **önce ne değişti, sonra neden bıraktık.**

"2012'den önce görüntü sınıflandırmada elle tasarlanmış öznitelikler kullanılıyordu.
AlexNet ImageNet'i kazandı ve ikinciyle arasındaki fark o kadar açıktı ki bütün alan
bir yılda yön değiştirdi."

Beş yenilik — hızlı say: ReLU, GPU, dropout, veri artırma, örtüşen pooling.

**ReLU'yu vurgula:** "Ondan önce sigmoid kullanılıyordu. Sigmoid derin ağlarda öğrenmeyi
yavaşlatıyor. ReLU basit: negatifse sıfır, pozitifse aynen geçir. Eğitim birkaç kat hızlandı."

**Neden bıraktık:** 11×11 filtreler ve devasa Dense katmanlar. Aynı işi çok daha küçük
ağlar yapıyor.

## 8. VGG — "iki 3×3, bir 5×5 eder"

**Bu, defterde görsel olarak değil metin olarak var. Anlatırken tahtaya çiz.**

Şöyle kur:

1. "Bir 5×5 filtre, girdide 5×5'lik bir alana bakar. Buna **görüş alanı** diyoruz."
2. "Şimdi iki tane 3×3 filtreyi üst üste koyalım. İkinci filtrenin gördüğü her hücre,
   birinci filtrenin 3×3'lük bir alanından geliyor. Yani ikinci filtre dolaylı olarak
   girdide **5×5**'lik bir alan görüyor."
3. "Aynı görüş alanı. Peki parametre?"
   - Tek 5×5 filtre: 5 × 5 = **25** ağırlık (kanal başına)
   - İki adet 3×3: 3 × 3 + 3 × 3 = **18** ağırlık
   - **%28 daha az.**
4. "Üstelik bir kazanç daha var: iki filtre arasında **fazladan bir ReLU** var.
   Model daha karmaşık şeyler öğrenebiliyor."

Bir cümlelik özet: **"Küçük filtreyi üst üste koymak, büyük filtreden hem ucuz hem güçlü."**

**Sonra bedeli göster:** VGG-16'nın 138M parametresinin **~103 milyonu** tek bir katmanda:
`7×7×512 → 4096` tam bağlantı. Hesabı canlı yap: 7×7×512 = 25088, çarpı 4096 ≈ 102.8 milyon.

"Yani ağırlığın dörtte üçü evrişimde değil, en sondaki Dense katmanında. Bütün o güzel
3×3 tasarımı bir kenara, fatura burada."

**Köprü sorusu:** "Bu Dense katmanlarını atıp yerine Global Average Pooling koysak ne olur?"
(GoogLeNet'in yaptığı tam olarak bu — sormak istersen.)

## 9. ResNet

Bu bölümü **soru ile aç, cevabı sonra ver.**

**Soru:** "VGG bize derinleş dedi. Peki 16 yerine 56 katman yapsak daha mı iyi olur?"
Katılımcıların çoğu "evet" der. "Hayır" de ve grafiği göster.

**Grafiği anlat:** "56 katmanlı ağ, 20 katmanlıdan **daha kötü**. Ve dikkat — bu
**eğitim** hatası, test değil. Yani ezberleme problemi değil. Ağ eğitim verisini bile
öğrenemiyor. Bu tuhaf: 56 katmanlı ağ, teorik olarak 20 katmanlı ağı taklit edip
kalan 36 katmanı boş geçebilirdi. Ama optimizasyon bunu bulamıyor."

**Sonra çözümü ver:**
"Fikir çok basit. Katmanların çıktısına, katmanlara hiç girmemiş **girdiyi de ekliyoruz**.

`çıktı = F(x) + x`

Ne değişti? Ağ artık sıfırdan bir çıktı üretmek zorunda değil. Girdiye **ne ekleyeceğini**
öğreniyor. Ve eğer eklenecek bir şey yoksa `F(x) = 0` yapıp girdiyi olduğu gibi geçirebiliyor.

Yani **fazladan katman artık zarar veremiyor.** En kötü ihtimalle hiçbir şey yapmıyor."

**Sonuç:** 152 katman eğitilebildi, ImageNet 2015 kazanıldı. Karşılaştırma tablosunu göster:
ResNet-50, VGG-16'dan 3 kat derin ama 5 kat az parametreli (25.6M / 138M) ve daha doğru.

**Sorulursa — bottleneck bloğu:** Derin sürümlerde blok içinde 1×1 → 3×3 → 1×1 var.
İlk 1×1 kanal sayısını düşürür (mesela 256 → 64), pahalı 3×3 küçük veride çalışır,
son 1×1 kanalı geri açar. Aynı işi çok daha ucuza yapmanın yolu.

**Kapanış cümlesi:** "Bu kısayol fikri bugün neredeyse her modern mimaride var —
Transformer'larda bile. 2015'in en etkili tek fikri diyebiliriz."

**Düşünelim sorusu:** "Fazladan katman zarar veremiyorsa neden 1000 katmanlı ResNet
yapmıyoruz?" Cevap: getiri hızla azalır, bellek ve süre artar; belli bir noktadan sonra
katman eklemek ölçülebilir bir kazanç vermiyor.

---

## 10. Transfer Learning ve Fine Tuning

> Buradan itibaren okunmak üzere yazıldı. **Söyle** yazan yerler doğrudan
> söyleyebileceğin cümleler. **Yap** yazan yerler ne yapacağını anlatır.

### Bölüme giriş

**Söyle:**
"Şimdiye kadar mimarileri tanıdık. AlexNet, VGG, ResNet. Ama bunlar başkalarının
eğittiği modeller. Asıl soru şu: ben bunları kendi problemimde nasıl kullanacağım?
Bu bölüm onun cevabı."

"İki terim duyacaksınız. Transfer learning ve fine tuning. Aynı şey değiller, ama
aynı işin iki adımı. Transfer learning, hazır bir modelin bilgisini bizim
problemimize taşımak demek — bize bir başlangıç noktası verir. Fine tuning ise o
modeli bizim verimize göre özelleştirmek demek. Önce transfer edersiniz, sonra ince
ayar yaparsınız."

### 10.1 Gövde ve kafa

**Söyle:**
"Her sınıflandırma ağı ikiye ayrılır. Alt kısma gövde diyoruz, İngilizcesi backbone.
Bu kısım evrişim katmanlarından oluşur ve işi öznitelik çıkarmaktır — kenar, doku,
parça. Üst kısma kafa diyoruz, head. Bu kısım Dense katmanlarından oluşur ve işi
karar vermektir."

"Şimdi kritik nokta: gövdenin öğrendiği şey probleme özel değil. Kenar her yerde
kenardır. Ama kafa ImageNet'in bin sınıfına göre ayarlanmış. Bizim altı sınıfımızla
alakası yok."

"O yüzden yaptığımız şey çok basit: kafayı kesip atıyoruz, kendi kafamızı takıyoruz."

**Söyle:** "Keras'ta bunu yapan tek bir parametre var: `include_top=False`.
Modeli böyle çağırdığınızda sadece gövde iniyor."

### 10.2 Hangi stratejiyi seçeceğim

**Yap:** Karar matrisi görselini göster.

**Söyle:**
"Cevabı iki soru belirliyor. Birincisi: kaç görüntünüz var? İkincisi: veriniz
ImageNet'e benziyor mu?"

"Az veriniz varsa ve veriniz günlük nesnelerden oluşuyorsa — sol üst kutu — gövdeyi
hiç açmayın. Sadece kafayı eğitin. Buna feature extraction deniyor. En hızlısı, en
güvenlisi."

"Çok veriniz varsa son blokları da açabilirsiniz. Bu en yaygın kullanılan yol."

"Verileriniz röntgen ya da uydu görüntüsü gibi ImageNet'e hiç benzemiyorsa ve azsa —
en zor durum bu. Sadece son bloğu açın, veri artırma şart."

"Hem çok veriniz hem farklı alan varsa her şeyi açabilirsiniz. Ama yine sıfırdan
değil, hazır ağırlıktan başlayın."

### 10.3 İki aşamalı tarif

**Söyle:**
"Pratikte neredeyse her zaman şu sırayla ilerlenir. İki aşama var."

"Birinci aşama: gövdeyi tamamen donduruyorsunuz. Yeni kafayı takıyorsunuz. Normal
öğrenme oranıyla birkaç epoch eğitiyorsunuz. Burada sadece kafa öğreniyor."

"İkinci aşama: gövdenin son birkaç bloğunu açıyorsunuz. Öğrenme oranını yüz kat
düşürüyorsunuz. Modeli yeniden derliyorsunuz. Ve birkaç epoch daha eğitiyorsunuz."

**Söyle (vurgula):**
"Üçüncü adım olan yeniden derleme atlanırsa hiçbir değişiklik geçerli olmaz.
Katmanları açarsınız ama model eski haliyle eğitilmeye devam eder. Çok sık yapılan
bir hata."

### 10.4 Dört tuzak

**Söyle:**
"Şimdi dört tane tuzak anlatacağım. Bu dördünün ortak özelliği şu: hata mesajı
almazsınız. Kod çalışır, model eğitilir, sonuç kötü çıkar ve nedenini bulamazsınız."

**1 — Yanlış ön işleme.**
"Her hazır modelin kendine ait bir ön işleme fonksiyonu var. MobileNetV2 girdiyi
eksi bir ile artı bir arasına çeker. VGG16 ise resmi BGR'ye çevirip ImageNet
ortalamasını çıkarır. Yanlış olanı kullanırsanız model çöp üretir ama size bunu
söylemez. Her zaman modelin kendi `preprocess_input` fonksiyonunu kullanın."

**2 — Yüksek öğrenme oranı.**
"İnce ayar aşamasında normal öğrenme oranını kullanırsanız, açtığınız katmanlar ilk
birkaç adımda ImageNet'te öğrendiklerini siler. O zaman hazır ağırlıkla başlamanın
hiçbir anlamı kalmaz. Yüz kat düşürün."

**3 — Yanlış sıra.**
"Gövdeyi kafadan önce açarsanız şu olur: kafa henüz rastgele, yani anlamsız tahminler
yapıyor. Bu da büyük hata sinyalleri üretiyor. O sinyaller geri yayılıp gövdeyi
bozuyor. Önce kafa, sonra gövde."

**4 — BatchNormalization.**
"En sinsi olanı bu. BatchNormalization katmanları eğitim sırasında verinin ortalama
ve varyansını takip eder. Gövdeyi açtığınızda bu katmanlar da açılır ve bu
istatistikleri sizin küçük veri kümenize göre güncellemeye başlar. Bu da modelin
öğrendiğini bozar."

"Çözüm basit: katmanları açarken BatchNormalization'lara dokunmayın, donuk kalsınlar.
Birazdan kodda göreceksiniz."

---

## 11. Uygulama — Garbage Classification

> Bu bölümü hücre hücre ilerleyeceksin. Her başlıkta: önce söyleyeceğin, sonra
> çalıştıracağın hücre, sonra ekranda göreceğin şey var.

### Bölüme giriş

**Söyle:**
"Şimdi bu tarifi gerçekten çalıştıracağız. Elimizde çöp fotoğrafları var, altı sınıf:
karton, cam, metal, kağıt, plastik ve genel çöp. Toplam iki bin beş yüz yirmi yedi
görüntü."

"Aynı veriyi, aynı tarifi iki farklı gövdeyle deneyeceğiz. MobileNetV2 hafif bir
model, telefonlar için tasarlanmış. ResNet50 ise ondan on kat büyük. Sonunda ikisini
karşılaştıracağız."

**Yap:** Menüden Çalışma zamanı → Çalışma zamanı türünü değiştir → T4 GPU seçtir.
Bunu şimdi yaptır, sonra unutulur.

**Söyle:** "GPU seçmezseniz eğitim dakikalar değil saatler sürer."

### 11.1 Veriyi indir

**Söyle:**
"Veri setini GitHub'dan indiriyoruz. Drive'a bağlanmaya gerek yok, kimsenin bir şey
kurması gerekmiyor. Hücreyi çalıştırın, veri kendiliğinden inip açılıyor."

**Yap:** Hücreyi çalıştır.

**Ekranda ne olacak:** TensorFlow ve Keras sürümü, GPU bilgisi, sonra sınıf sınıf
görüntü sayıları ve toplam.

**Söyle:** "Sınıfların dengesiz olduğuna dikkat edin. Kağıt beş yüz doksan dört
görüntü, çöp ise sadece yüz otuz yedi. Bu modelin işini zorlaştıracak."

**Yap:** İkinci hücreyi çalıştır — altı rastgele örnek görüntü çıkar.

**Söyle:** "Fotoğraflar beyaz zeminde çekilmiş, temiz bir veri seti. Gerçek hayatta
bu kadar kolay olmaz."

### 11.2 Veri hazırlığı

**Söyle:**
"Burada iki şey yapıyoruz. Birincisi veriyi okuyoruz. İkincisi veri artırma
uyguluyoruz — görüntüleri çeviriyoruz, kaydırıyoruz, yakınlaştırıyoruz. Böylece iki
bin beş yüz görüntüden çok daha fazlasını görmüş oluyoruz."

**Söyle (vurgula):**
"Bir noktaya dikkatinizi çekmek istiyorum. Burada `rescale` kullanmıyoruz. Onun
yerine modelin kendi `preprocessing_function` fonksiyonunu veriyoruz. Az önce
anlattığım birinci tuzak tam olarak buydu."

**Söyle:** "Eğitim verisine artırma uyguluyoruz ama doğrulama verisine
uygulamıyoruz. Doğrulama verisi olduğu gibi kalmalı, yoksa neyi ölçtüğümüzü bilemeyiz."

**Yap:** Hücreyi çalıştır.

**Ekranda ne olacak:** "Found ... images belonging to 6 classes" iki kez — biri
eğitim biri doğrulama için. Sonra sınıf isimleri.

### 11.3 Gövdeyi tanıyalım

**Söyle:**
"Eğitime başlamadan önce elimizdeki gövdeye bakalım. Kaç katman var, kaç parametre
var, hangileri eğitilebilir?"

**Yap:** İlk hücreyi çalıştır.

**Ekranda ne olacak:** Katman sayısı yüz elli dört, parametre iki milyon iki yüz
elli yedi bin, on yedi mantıksal blok. Sonra son on bir katmanın listesi.

**Söyle:** "Yüz elli dört katman var ama bunların hepsi ağırlık taşımıyor. Aktivasyon
ve normalizasyon katmanları da sayılıyor."

**Yap:** İkinci hücreyi çalıştır — asıl gösterilecek şey bu.

**Ekranda ne olacak:** Üç satır:
```
1) İndirildiği hali        eğitilebilir: 2.223.872   donuk:     34.112
2) Tamamen dondurulmuş     eğitilebilir:         0   donuk:  2.257.984
3) Son 11 katman açık      eğitilebilir:   879.040   donuk:  1.378.944
```

**Söyle:**
"Bu üç satır, az önce anlattığım üç stratejinin tam karşılığı."

"İlk satır: model indirildiği hali. Her şey eğitilebilir."

"İkinci satır: hepsini dondurduk. Eğitilebilir parametre sıfır. Bu feature
extraction."

"Üçüncü satır: son on bir katmanı açtık. Sekiz yüz yetmiş dokuz bin parametre
eğitilebilir oldu. Bu da fine tuning."

**Söyle (vurgula):**
"Şimdi alttaki listeye bakın. Son on bir katmanı açtık ama içlerinden BN yazanlar
donuk kalmış. Bunlar BatchNormalization katmanları. Dördüncü tuzak buydu — onlara
kasten dokunmuyoruz."

### 11.4 Aşama 1

**Söyle:**
"Birinci aşamaya geçiyoruz. Gövde tamamen donuk. Sadece taktığımız yeni kafa
öğrenecek."

**Yap:** Hücreyi çalıştır.

**Ekranda ne olacak:** Önce parametre özeti — eğitilebilir yedi bin altı yüz seksen
altı. Sonra beş epoch eğitim.

**Söyle:**
"Şu sayıya bakın: yedi bin altı yüz seksen altı. İki buçuk milyon parametreli bir
modelde sadece yedi bin parametre eğitiyoruz. İşte bu yüzden az veriyle çalışabiliyor
ve bu yüzden bu kadar hızlı."

**Söyle (eğitim dönerken):**
"Doğruluk ilk epoch'ta bile yüksek çıkacak. Çünkü gövde zaten görmeyi biliyor, biz
sadece 'bu öznitelikler karton demek' eşlemesini öğretiyoruz."

### 11.5 Aşama 2

**Söyle:**
"İkinci aşama. Üç şey aynı anda yapılıyor, üçü de şart."

"Bir: son otuz katmanı açıyoruz — ama BatchNormalization'lar hariç."
"İki: öğrenme oranını binde birden yüz binde bire düşürüyoruz. Yüz kat."
"Üç: modeli yeniden derliyoruz."

**Yap:** Hücreyi çalıştır.

**Ekranda ne olacak:** Eğitilebilir parametre sayısı sıçrayacak. Sonra beş epoch daha.

**Söyle:**
"Eğitilebilir parametre yedi binden bir buçuk milyona çıktı. Artık gövde de
öğreniyor — ama çok küçük adımlarla, çünkü öğrenme oranını düşürdük."

### 11.6 Sonuçlar

**Yap:** Grafik hücresini çalıştır.

**Söyle:**
"Kırmızı kesikli çizgi ince ayarın başladığı yer. Orada doğruluğun bir sıçrama
yapmasını bekliyoruz. Çünkü gövde artık genel nesneler yerine çöp fotoğraflarına
özelleşiyor."

**Eğer doğrulama kaybı ince ayardan sonra yükseldiyse söyle:**
"Bakın, doğrulama kaybı yükselmeye başladı. Bu aşırı öğrenmenin işareti. Model
eğitim verisini ezberliyor. Çözüm: daha az katman açmak ya da öğrenme oranını daha
da düşürmek."

### 11.6b Tahminleri görelim

**Söyle:**
"Sayılar bir şey anlatır ama asıl ikna edici olan modeli iş başında görmektir.
Şimdi rastgele sekiz fotoğraf alıp modele soralım."

**Yap:** Tahmin hücresini çalıştır.

**Ekranda ne olacak:** İki sıra hâlinde sekiz fotoğraf. Her birinin üstünde modelin
tahmini, yüzde kaç emin olduğu ve gerçek sınıf. Doğrular yeşil, yanlışlar kırmızı.

**Söyle:**
"Yüzde değeri modelin kendine güveni. Dikkat edin — model yanlış cevaba da yüksek
güven verebilir. Emin olmak ile haklı olmak farklı şeyler."

**Yap:** Hücreyi bir daha çalıştır, farklı fotoğraflar gelir. İki üç kez tekrarla.

**Söyle:** "Her çalıştırdığımızda farklı örnekler geliyor. Birkaç kez deneyip modelin
genel olarak nerede iyi nerede kötü olduğunu görebilirsiniz."

### 11.6c Model nerede zorlanıyor

**Yap:** Sınıf başına doğruluk tablosunu çıkaran hücreyi çalıştır.

**Ekranda ne olacak:** Altı satırlık tablo — her sınıf için doğru bilinen sayısı ve oranı.

**Söyle:**
"Şimdi asıl öğretici kısım. Hangi sınıf en kötü?"

"Büyük ihtimalle `trash` çıkacak. Sebebi basit: elimizde ondan sadece yüz otuz yedi
görüntü var, kağıttan ise beş yüz doksan dört. Model az gördüğü sınıfı iyi öğrenemiyor."

"Bu, veri setinin dengesiz olmasının bedeli. Gerçek projelerde çok sık karşınıza çıkar.
Çözümü ya az olan sınıftan daha fazla veri toplamak, ya da eğitimde o sınıfa daha fazla
ağırlık vermek."

**Yap:** Yanlış bilinen örnekleri gösteren hücreyi çalıştır.

**Söyle:**
"Bunlar modelin yanıldığı örnekler. Bir bakın — siz olsanız doğru bilir miydiniz?"

"Çoğu zaman modelin karıştırdığı şeyler insanın da karıştırdığı şeylerdir. Cam mı
plastik mi, kağıt mı karton mu. Modelin hatası her zaman aptallık değildir; bazen
problem gerçekten zordur."

### 11.7 ResNet50 ile karşılaştırma

**Söyle:**
"Şimdi aynı tarifi ResNet50 ile çalıştıracağız. Kodda değişen tek şey gövde ve onun
ön işleme fonksiyonu. Geri kalan her şey birebir aynı."

**Yap:** Hücreyi çalıştır. Bu daha uzun sürecek.

**Söyle (beklerken):**
"ResNet50 yirmi üç buçuk milyon parametreli. MobileNetV2 iki buçuk milyondu. Yani on
kat büyük. Eğitim süresinin de o oranda uzadığını göreceksiniz."

**Yap:** Karşılaştırma tablosu hücresini çalıştır.

**Söyle:**
"Şimdi asıl soruyu soralım. ResNet50 on kat büyük. Doğruluk farkı bunu haklı
çıkarıyor mu?"

"Cevap genelde hayır. Küçük ve temiz bir veri setinde iki model de benzer sonuç
verir. Ama biri telefona sığar, diğeri sığmaz."

**Söyle (kapanış):**
"Bugün öğrendiğiniz en pratik şey bu: en büyük modeli seçmek her zaman doğru cevap
değil. Problemi çözen en küçük modeli seçin."

### Gelebilecek sorular

**"Neden epoch sayısı bu kadar az?"**
"Derste zamanı kısa tutmak için. Evde on beş, yirmi epoch deneyin. Defterde en üstte
`EPOK_1` ve `EPOK_2` değişkenleri var, oradan değiştirebilirsiniz."

**"Kaç katman açmalıyım?"**
"Kesin bir kural yok. Az veriyle az katman. Defterdeki `ACILACAK` değişkenini otuzdan
altmışa çıkarıp deneyin, doğrulama kaybını izleyin."

**"Kendi verimle nasıl yaparım?"**
"Klasör yapısı aynı olsun: her sınıf için bir klasör, içinde o sınıfın fotoğrafları.
`dir_path` değişkenini kendi klasörünüze çevirmeniz yeterli."

**"Model dosyasını nasıl kaydederim?"**
"`model.save('modelim.keras')` yeterli. Sonra `keras.models.load_model` ile geri
yüklersiniz."

---

## Zamanlama

| Bölüm | Süre |
|---|---|
| 1–4. Önceki ders özeti | 35 dk |
| 5. Pretrained modeller | 8 dk |
| 6. Zaman çizelgesi | 7 dk |
| 7. AlexNet | 6 dk |
| 8. VGG | 10 dk |
| 9. ResNet | 12 dk |
| 10. Transfer learning | 15 dk |
| 11. Uygulama | 25 dk (eğitim süreleri dahil) |

## Dersten önce mutlaka yap

1. Colab'ı GitHub'dan aç, T4 GPU seç.
2. **Bütün defteri baştan sona bir kez çalıştır.** Model ağırlıkları önbelleğe girsin,
   veri inmiş olsun, gerçek eğitim sürelerini gör.
3. Süreler uzunsa `EPOK_1` ve `EPOK_2` değerlerini düşür.
4. Çalıştırdıktan sonra çıktıları temizleyip öyle derse gir — dinleyici sonuçları
   önceden görmesin.

GIF'ler döngüde oynuyor; konuşurken başa dönmesi normal, bekletmeye çalışma.
