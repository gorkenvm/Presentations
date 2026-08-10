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

## Zamanlama

| Bölüm | Süre |
|---|---|
| 1–4. Önceki ders özeti | 35 dk |
| 5. Pretrained modeller | 8 dk |
| 6. Zaman çizelgesi | 7 dk |
| 7. AlexNet | 6 dk |
| 8. VGG | 10 dk |
| 9. ResNet | 12 dk |

GIF'ler döngüde oynuyor; konuşurken tekrar başa dönmesi normal, bekletmeye çalışma.
