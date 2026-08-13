# Atölye Konuşmacı Notları — Nesne Tespiti, Takip, Sayma

> **Söyle** yazan yerler doğrudan okuyabileceğin cümleler.
> **Yap** ne yapacağını, **Ekranda** ne göreceğini anlatır.
> Öğrenciler kod yazmayacak; sen göstereceksin, onlar tahmin edecek.

**Toplam süre: ~2 saat**

| Bölüm | Süre |
|---|---|
| 0. Kurulum + tekrar | 15 dk |
| 1. Kırılma anı | 15 dk |
| 2. İlk tespit | 15 dk |
| 3. Anatomi (conf, NMS) | 25 dk |
| 4-5. Video ve takip | 25 dk |
| 6. Sayma | 15 dk |
| 7. Kendi görüntün | 10 dk |
| 8-10. Sınırlar, Roboflow, kapanış | 15 dk |

---

## Dersten önce mutlaka yap

1. Colab'ı GitHub'dan aç, **T4 GPU** seç.
2. Baştan sona bir kez çalıştır — model ağırlıkları insin, videoların gerçek işlem
   süresini gör.
3. Roboflow API anahtarını 9. bölümdeki hücreye yapıştır ve **çalıştığını doğrula.**
4. Çıktıları temizleyip derse öyle gir.

**Zaman sıkışırsa atlanabilecekler:** 5. bölümdeki iz çizme hücresi, 7. bölümdeki
webcam. Sayma bölümü atlanmasın — dersin doruk noktası orası.

---

## 0. Açılış (15 dk)

**Söyle:**
"Dün bir model eğittik. Bir fotoğraf verdik, bize 'bu karton' dedi. Bugün o modelin
yapamadığı bir şeyi konuşacağız."

"Önce hızlıca dünü hatırlayalım. Transfer learning neydi?"

**Soru at ve cevap bekle:** "Hazır bir modelin gövdesini alıp kendi kafamızı takmak."

**Yap:** Dünkü CNN mimarisi şemasını (zebra) göster — animasyon dönerken konuş.

**Söyle:**
"Bu dünkü şemamız. Soldan görüntü giriyor, evrişim ve pooling katmanlarından geçiyor,
sağda tek bir olasılık dağılımı çıkıyor: zebra 0.7, at 0.2, köpek 0.1."

"Dün bu yapının **gövdesini** hazır aldık — o kısım görmeyi zaten biliyordu. **Kafasını**
kesip attık, kendi altı çöp sınıfımıza göre yenisini taktık. Buna **transfer learning**
dedik."

"Sonra gövdenin son katmanlarını da açıp kendi verimizle biraz oynattık. Buna da
**fine tuning** dedik — öğrenme oranını yüz kat düşürerek, çünkü yoksa modelin
öğrendiklerini silecektik."

**Vurgula — bugüne köprü:**
"Şimdi şemanın sağ ucuna bir daha bakın. Çıktı **tek bir olasılık dağılımı**.
Bugünkü dersin tamamı, bu tek çıktının neden yetmediği üzerine."

**Söyle:** "Bugün de hazır model kullanacağız. Ama bu sefer eğitim bile yapmayacağız —
model zaten hazır, biz sadece çalıştıracağız."

**Yap:** 0. bölümdeki iki hücreyi çalıştır (kurulum + veri indirme).

**Söyle (kurulum inerken):**
"Ultralytics diye bir kütüphane kuruyoruz. YOLO modellerini üç satırda çalıştırmamızı
sağlıyor. Eskiden bu iş kırk satır OpenCV koduydu."

---

## 1. Kırılma anı (15 dk)

> Bu bölüm bugünün en önemli 10 dakikası. Acele etme.

**Söyle:**
"Şimdi dünkü gibi bir sınıflandırıcı alıyorum. MobileNetV2, ImageNet'te eğitilmiş,
bin sınıf tanıyor. Ona bir trafik fotoğrafı vereceğim."

**Yap:** Fotoğrafı gösteren hücreyi çalıştır ama **tahmini henüz gösterme** —
fotoğraf ekrana gelsin.

**Söyle:** "Bu fotoğrafta ne var? Sayalım: arabalar, yayalar, trafik ışıkları."

**Soru at:** "Sizce model ne diyecek?"

**Yap:** Tahmini göster.

**Ekranda:** Tek bir sınıf ve olasılık.

**Söyle (asıl vurgu):**
"Model tek bir cevap verdi. Peki **model yanlış mı söyledi?**"

*(Bekle. Öğrenciler "hayır" diyecek.)*

"Hayır. Fotoğrafta gerçekten araba var. Model doğru söyledi. Sorun modelde değil —
**bizim sorduğumuz soruda.**"

"Sınıflandırma tek bir soruyu cevaplar: *bu resim ne?* Cevap tek etikettir.
Ama biz başka bir şey sormak istiyoruz: *ne var, nerede, kaç tane?*
Bu tamamen farklı bir problem ve adı **nesne tespiti**."

**Yap:** Karşılaştırma görselini göster.

**Söyle:** "Soldaki dünkü dünyamız, sağdaki bugünkü."

---

## 2. İlk tespit (15 dk)

**Söyle:** "Aynı fotoğraf. Bu sefer YOLO'ya veriyorum. Üç satır."

**Yap:** Tespit hücresini çalıştır.

**Ekranda:** Kutularla dolu fotoğraf, altında bulunan nesne sayısı.

**Söyle:** "Az önce tek cevap veren fotoğraf şimdi düzinelerce nesne veriyor.
Her birinin sınıfı ve **yeri** belli."

**Yap:** Sınıf sayımı hücresini çalıştır.

**Söyle:** "Kaç araba, kaç yaya — sayabiliyoruz artık. Dün bunu yapamıyorduk."

**Yap:** Altı fotoğraflı toplu hücreyi çalıştır.

**Söyle:** "Mutfak, hayvanat bahçesi, havaalanı, tenis kortu. Hepsinde çalışıyor.
Hiçbir eğitim yapmadık — model bunları zaten biliyordu."

---

## 3. Çıktının anatomisi (25 dk)

**Söyle:** "Şimdi biraz altına inelim. O renkli kutuların arkasında ne var?"

**Yap:** Anatomi görselini göster, sonra kutu koordinatlarını yazdıran hücreyi çalıştır.

**Ekranda:** Sınıf, güven, dört sayı.

**Söyle:**
"Her kutu dört sayıdan ibaret: sol üst köşe ve sağ alt köşe. Piksel cinsinden.
Yanındaki 0.91 ise modelin ne kadar emin olduğu."

### 3.1 Güven eşiği

**Söyle:** "Şimdi bir deney. `conf` diye bir parametre var — 'şu olasılığın altındakileri
bana gösterme' demek. Varsayılanı 0.25."

**Soru at (çalıştırmadan önce):**
"Eşiği 0.10'a düşürürsem ne olur? Ya 0.60'a çıkarırsam?"

*(Cevapları al. "Düşürünce daha çok kutu" cevabı gelecektir — doğru ama eksik.)*

**Yap:** Üç eşikli hücreyi çalıştır.

**Söyle:**
"Evet, düşürünce kutu arttı. Ama **artan kutulara bakın** — bazıları hiçbir şeyin
üstünde değil. Model 'burada %12 ihtimalle bir otobüs var' diyor ve yanılıyor."

"Yükseltince temizlendi. Ama bu sefer **gerçekten orada olan** bazı nesneleri kaçırdık."

**Vurgula:**
"Doğru eşik diye bir şey yok. Güvenlik kamerası yazıyorsanız hiçbir şeyi kaçırmak
istemezsiniz, eşiği düşürürsünüz — yanlış alarmlara katlanırsınız. Otomatik fatura
kesen bir sistem yazıyorsanız yanlış saymak istemezsiniz, yükseltirsiniz."

### 3.2 NMS

**Söyle:**
"Bir şey daha var. Model aslında yüzlerce aday kutu üretir. Aynı arabanın üstüne
onlarca kutu düşer. Biz onları görmüyoruz çünkü arada bir temizlik adımı var:
**NMS** — maksimum olmayanı bastırma."

"Mantığı basit: üst üste binen kutulardan en güvenli olanı tut, kalanları at.
`iou` parametresi de 'ne kadar üst üste binerlerse aynı sayılsın' eşiği."

**Yap:** `iou` hücresini çalıştır — sadece sayılar basar, üç görsel yok.

**Ekranda:** Üç satır, kutu sayıları birbirine çok yakın.

**Söyle (bu bir hata değil, dersin konusu):**
"Sayılar neredeyse aynı çıktı. Bu bir hata değil — göstermek istediğim şey tam da bu."

"Eski YOLO'lar, v3 v5 v8, aynı nesne için yüzlerce aday üretirdi. NMS olmasa görüntü
kutudan görünmezdi. Yeni nesil modeller ise eğitim sırasında 'her nesne için tek kutu
üret' diye öğretiliyor. YOLO26 bunu bir adım ileri götürüp NMS'i tamamen kaldırdı."

"Yani NMS'i öğrenmemiz gerekiyor çünkü hâlâ pek çok modelde var. Ama artık onu
çalışırken görmek zor. Bu, alanın ilerlediğinin işareti."

> Öğrenci "o zaman neden anlatıyoruz" derse: eski modellerle çalışırken, kendi
> modelini eğitirken ve literatürü okurken karşına çıkacak.

### 3.3 Asıl fark yaratan parametre: imgsz

**Söyle:**
"Şimdi gerçekten fark yaratan bir parametre göstereceğim. Model fotoğrafı olduğu gibi
işlemiyor — önce sabit bir boyuta küçültüyor. Varsayılan 640 piksel."

**Soru at:** "Peki uzaktaki küçük arabalar bu küçültmede ne oluyor?"

**Yap:** `imgsz` hücresini çalıştır.

**Ekranda:** Üç görsel — 320, 640, 1280. Nesne sayıları belirgin şekilde farklı.

**Söyle:**
"320'de uzaktaki küçük araçlar tamamen kayboldu. 1280'de geri geldiler. Model onları
'göremiyordu' çünkü küçültme sırasında birkaç piksele inmişlerdi."

"Bedeli süre. 1280 dört kat daha yavaş."

**Pratik kural olarak söyle:** "Nesneleriniz küçük ve uzaksa imgsz artırın.
Yakın ve büyükse artırmanın faydası yok, sadece yavaşlarsınız."

---

## 4-5. Video ve takip (25 dk)

**Söyle:** "Video, arka arkaya dizilmiş fotoğraflardan başka bir şey değil.
Modele her kareyi ayrı ayrı vereceğiz."

**Yap:** Ham videoyu göster, sonra tespit hücresini çalıştır.

> **Not:** Bu hücre biraz sürer. Beklerken konuş.

**Söyle (beklerken):**
"Şu anda model saniyede 25 kareyi tek tek işliyor. Her kare için sıfırdan
'burada ne var' diye bakıyor."

**Yap:** Sonuç videosunu oynat.

**Söyle:** "Çalışıyor. Ama şimdi size bir soru soracağım."

**Soru at (kritik an):**
"Şu kırmızı arabayı takip edin. Model, 5. karedeki kırmızı arabayla 4. karedekinin
**aynı araba** olduğunu biliyor mu?"

*(Bekle.)*

"Hayır. Bilmiyor. Model için her kare yepyeni bir dünya. Her seferinde sıfırdan
bakıyor ve 'burada bir araba var' diyor. Hangi araba olduğu umurunda değil."

"Peki 'bu yoldan kaç araba geçti?' diye sorsam? **Cevaplayamayız.** Çünkü aynı
arabayı 250 kere saymış oluruz."

**Söyle:** "İşte bu yüzden takip ayrı bir problem."

**Yap:** Takip hücresini çalıştır.

**Ekranda:** Kutuların üstünde `id:1`, `id:2` gibi numaralar.

**Söyle:**
"Şimdi her nesnenin bir kimliği var. Araba ekranda kaldığı sürece **aynı numara**
onda kalıyor. `persist=True` dediğimiz şey tam olarak bu — modele hafıza verdik."

**Yap:** İz çizme hücresini çalıştır.

**Söyle:** "Arkalarındaki yeşil çizgi, o nesnenin nereden gelip nereye gittiği.
Trafik analizinde, spor analizinde tam olarak bu kullanılıyor."

---

## 6. Sayma (15 dk)

**Söyle:** "Artık her nesnenin kimliği olduğuna göre sayabiliriz."

**Yap:** İlk kareyi ve bölge önizlemesini göster.

**Söyle:**
"Bir kapı çiziyorum. Buradan geçen kişileri sayacağız. Kimliği olduğu için
aynı kişiyi iki kere saymayacak."

**Yap:** Sayma hücresini çalıştır.

**Söyle (beklerken):**
"Bu, mağaza girişinde müşteri sayan, kavşakta araç sayan, fabrikada bantta ürün sayan
sistemlerin tam olarak yaptığı iş. Gördüğünüz gibi çok az kodla."

**Ekranda:** Videoda sol üstte giren/çıkan sayaçları, altında toplamlar.

**Söyle:** "Giren ve çıkan ayrı ayrı tutuluyor. Yönü de biliyor."

---

## 7. Kendi görüntün (10 dk)

**Söyle:** "Şimdi eğlenceli kısım. Kendi fotoğrafımızı verelim."

**Yap:** Sırayla URL, dosya yükleme, webcam.

**Dosya yükleme hücresinde:** Üstteki `AYAR` sözlüğünde `conf`, `iou`, `imgsz`,
`max_det` var. Aynı fotoğrafla `conf` değerini değiştirip birkaç kez çalıştır —
öğrenci parametrenin etkisini kendi fotoğrafında görsün.

**Webcam — canlı yayın:**
Kamera açılır ve kutular anlık olarak görüntünün üstüne çizilir. Durdurmak için
görüntüye tıkla.

**Söyle (kamera açıkken):**
"Şu anda modele saniyede birkaç kare gidiyor ve anında geri dönüyor. Elimi
oynatıyorum, kutu takip ediyor."

**Yap:** Kamerayı sınıfa çevir.

**Söyle:** "Hepiniz `person` olarak işaretlendiniz. Model sizi tek tek buldu."

**Yap:** Bir şişe, telefon veya çanta göster — COCO'da olan nesneler.

**Söyle:** "Şişe, telefon, çanta — hepsi COCO listesinde var, o yüzden buluyor.
Birazdan listede **olmayan** bir şeyi deneyeceğiz."

> Kamera izni takılırsa vakit kaybetme, dosya yüklemeye geç. Colab'da kamera
> bazen ilk denemede açılmaz — hücreyi bir kez daha çalıştırmak genelde çözer.

---

## 8-10. Sınırlar, Roboflow, kapanış (15 dk)

**Söyle:** "Son bir soru. Bu model her şeyi bulabilir mi?"

**Yap:** COCO sınıf listesini yazdır.

**Söyle:** "Seksen sınıf. İnsan, araba, şişe, köpek, laptop..."

**Soru at:** "Dün ne sınıflandırmıştık? Karton, cam, metal, kağıt, plastik, çöp.
Sizce bu listede var mı?"

**Yap:** Kontrol hücresini çalıştır.

**Ekranda:** Altısı da YOK.

**Söyle:**
"Hiçbiri yok. Yani dün eğittiğimiz modelin bildiği hiçbir şeyi bu model bilmiyor."

"Demek ki hazır bir tespit modeli sadece **kendisine öğretilmiş** nesneleri bulur.
Sizin probleminizdeki nesne muhtemelen o listede yok."

"Peki ne yapacağız? İki yol var. Ya birinin o nesneleri etiketleyip eğittiği bir
modeli bulacağız, ya da kendimiz etiketleyeceğiz."

**Yap:** Roboflow hücresini çalıştır.

**Söyle:**
"Roboflow Universe, insanların etiketleyip paylaştığı veri setlerinin deposu.
Orada dün kullandığımız sınıfların **tam olarak aynısını** içeren bir veri seti buldum.
5742 fotoğraf, birisi tek tek etiketlemiş."

**Ekranda:** Çöp nesnelerinin kutularla bulunmuş hali.

**Söyle (vurgula):**
"Dikkat edin — **hiçbir eğitim yapmadık.** Ne dün, ne bugün. Birisi o işi yapmış,
biz sadece çağırdık."

**Söyle (kapanış):**
"Bugün öğrendiğiniz şeyi tek cümleye indirirsem: modeller sadece kendilerine
gösterilen şeyi bulabilir. Geri kalan her şey — kutu çizmek, etiketlemek, veri
toplamak — işin sıkıcı ama belirleyici kısmı. Model kalitesi neredeyse tamamen
etiket kalitesine bağlıdır."

"Kendi nesnenizi bulmak istiyorsanız yolu şu: 200-500 fotoğraf toplayın,
etiketleyin, dünkü transfer learning mantığıyla eğitin, modelin kaçırdıklarını
veri setine ekleyip tekrarlayın."

---

## Gelebilecek sorular

**"YOLOv3 kullanmıyor muyuz? İnternette hep o var."**
"YOLOv3 2018 modeli, artık kullanılmıyor. Sonraki sürümler hem daha hızlı hem daha
doğru. Eski eğitim materyallerinde çok görürsünüz çünkü uzun süre standarttı."

**"n, s, m harfleri ne demek?"**
"Model boyutu. `n` nano — en küçük ve en hızlı. `s` small, `m` medium, sonra `l` ve `x`.
Büyüdükçe daha doğru ama daha yavaş. Biz `n` kullanıyoruz çünkü derste hız lazım."

**"Gerçek zamanlı çalışır mı?"**
"GPU'da evet, saniyede 30-100 kare. CPU'da zorlanır. Telefonda çalıştırmak için
özel sürümleri var."

**"Kaç fotoğrafla kendi modelimi eğitebilirim?"**
"Sınıf başına 100-200 fotoğrafla başlanabilir. Ama fotoğrafların çeşitli olması sayıdan
daha önemli — farklı açı, farklı ışık, farklı arka plan."

**"Etiketleme ne kadar sürer?"**
"Fotoğraf başına yarım-bir dakika. 500 fotoğraf yaklaşık bir günlük iş. Otomatik
ön etiketleme araçları bunu kısaltıyor ama yine de kontrol etmek gerekiyor."

**"Kutu yerine tam şeklini bulabilir mi?"**
"Evet, ona segmentasyon deniyor. Model adının sonuna `-seg` eklemek yeterli.
Kutu yerine piksel piksel maske veriyor."
