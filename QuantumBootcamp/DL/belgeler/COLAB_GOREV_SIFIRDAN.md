# Görev: Sıfırdan bir Colab defteri yaz — "Yüz Analizi"

Var olan defteri **düzeltme, kullanma veya referans alma**. Baştan, temiz bir
`.ipynb` yaz.

---

## 1. Bağlam

Bu defter, **Miuul Kuantum Bootcamp** için hazırlanan 2 saatlik bir
**"Deep Learning Master Class"** sunumunun uygulama bölümü. Sunum bitiminde
öğrencilerle birlikte canlı çalıştırılacak, yaklaşık **15 dakika** sürecek.

Eğitmen: Veysel Murat Görken (Data Scientist / AI Engineer).
Dinleyici: derin öğrenmeye yeni başlayan bootcamp öğrencileri. Python bilgileri
temel düzeyde; matematik türetmesi yapılmayacak.

Sunumda işlenen ve defterde **karşılığını görmeleri gereken** kavramlar:

| Sunumda gördükleri | Defterde görecekleri |
|---|---|
| CNN — filtreler görüntünün üzerinde gezer | Yüzü bulan model bir CNN |
| Softmax — olasılık dağılımı | Duygu tahmini 7 sınıfa dağılmış olasılık |
| Embedding — anlam bir vektöre dönüşür | Yüz de N boyutlu bir vektöre dönüşüyor |
| Ölçekleme / normalizasyon | Görüntü sabit boyuta getirilip normalize ediliyor |
| Üretken vs ayırt edici modeller | Üretilmiş bir yüzü, ayırt edici bir modele veriyoruz |

Defter, eğitmenin çalışma arkadaşının projesindeki **"Yüz Analizi"** sekmesinin
Python karşılığı olacak: <https://github.com/grknc/generative-ai-workshop>
(orada modeller tarayıcıda `face-api.js` ile çalışıyor; burada Colab'da çalışacak).

---

## 2. Teknik ortam ve kısıtlar

- **Google Colab**, ücretsiz katman, **CPU** runtime. GPU gerektirmeyecek.
- Colab bugün **Python 3.12** kullanıyor.
- **Google Drive kullanılmayacak.** Defter her seferinde
  *Dosya → Not defteri yükle* ile yüklenip çalıştırılacak.
- **Hiçbir model eğitilmeyecek.** Yalnızca hazır/önceden eğitilmiş modeller
  kullanılacak.
- Kurulum + ilk model indirmesi dahil **toplam süre 2–3 dakikayı geçmemeli.**
- Hücreler **yukarıdan aşağı sırayla** çalıştırıldığında hatasız akmalı.
- Tüm metin, değişken adları, çıktı etiketleri ve yorumlar **Türkçe** olacak.
  (Model çıktıları İngilizce geliyorsa Türkçeye çevrilerek gösterilecek:
  `angry → kızgın`, `happy → mutlu`, `Man → Erkek`, `Woman → Kadın` gibi.)

### 2.1 Bilinen tuzak — kütüphane seçimini bu belirliyor

Önceki denemede `deepface` kullanıldı ve **çalışmadı**:

- `pip install deepface`, bağımlılık olarak `opencv-python`'ı çekiyor ve pip en
  yeni sürümü alıyor: **OpenCV 5.0**.
- OpenCV 5.0'da `cv2.CascadeClassifier` çekirdek `objdetect` modülünden
  **kaldırıldı**; `deepface` hâlâ 4.x API'sini kullanıyor.
- Sonuç: `AttributeError: module 'cv2' has no attribute 'CascadeClassifier'`
- Sürüm sabitleme (`opencv-python-headless<5`), tüm opencv paketlerini kaldırıp
  yeniden kurma ve runtime'ı yeniden başlatma denendi — **hiçbiri işe yaramadı**;
  `cv2.__version__` hâlâ `5.0.0` dönüyor.

Bu yüzden **kütüphane seçimi sana ait.** `deepface` kullanacaksan bu sorunu
gerçekten çözdüğünü göstermelisin (sürüm sabitleme + `sys.path` / `cv2.__file__`
doğrulaması ile). Aksi hâlde OpenCV'ye bağımlı olmayan bir yığın seç. Makul
alternatifler:

- `facenet-pytorch` (MTCNN yüz tespiti + InceptionResnetV1 embedding)
- `insightface`
- `transformers` üzerinden Hugging Face'teki hazır yüz duygu / yaş / cinsiyet
  sınıflandırma modelleri
- `mediapipe` (yüz tespiti için)

Hangisini seçersen seç, **bugünkü Colab'da gerçekten çalıştığını doğrula** ve
kullandığın tüm paketleri sürümüyle sabitle.

---

## 3. Defterin içeriği

Aşağıdaki akış istenen pedagojik sırayı veriyor. Bölüm başlıklarını koru,
içindeki teknik uygulamayı seçtiğin kütüphaneye göre yaz.

**Başlık hücresi (markdown)**
Defterin adı, "Kuantum Bootcamp · Veysel Murat Görken", yukarıdaki
sunum ↔ defter eşleme tablosu, ve "hiçbir şey eğitmiyoruz" notu.

**0 · Kurulum**
Tek hücrede tüm kurulum. Sürümler sabitlenmiş olmalı. Kurulumdan sonra
runtime'ın yeniden başlatılması gerekiyorsa bunu hücrenin kendisi yapmalı
(`IPython.Application.instance().kernel.do_shutdown(True)`) ve tekrar
çalıştırıldığında döngüye girmemeli. Ardından bir **doğrulama hücresi**:
kütüphane sürümlerini yazdırsın ve kritik fonksiyonun varlığını kontrol etsin.

**1 · Bir yüz bulalım**
Demo için **yapay üretilmiş** bir yüz indir
(`https://thispersondoesnotexist.com/random-person.jpeg`, `User-Agent` başlığı
gerekiyor). Görseli göster. Bağlantı çalışmazsa kullanıcıyı kendi fotoğrafını
yükleyeceği bölüme yönlendiren bir `try/except` olsun.
Konuşma notu: "Bu fotoğrafı üretken bir model üretti; şimdi onu ayırt edici bir
modele vereceğiz."

**2 · Adım 1 — Yüzü bul (face detection)**
Fotoğrafta yüzün nerede olduğunu bul. Orijinal görüntünün üzerine tespit
kutusunu çiz (matplotlib), yanına kırpılmış + ölçeklenmiş yüzü göster.
Modele giren dizinin **boyutunu ve değer aralığını** yazdır — sunumdaki
"model fotoğraf görmez, sayı görür" mesajını buraya bağla.

**3 · Adım 2 — Duygu analizi**
Duygu tahminini **7 sınıfa dağılmış olasılık** olarak al ve **yatay bar grafik**
ile göster. Olasılıkların toplamının 1 olduğunu açıkça yazdır — sunumdaki
softmax slaydının karşılığı bu.

**4 · Adım 3 — Yaş ve cinsiyet**
Tahmin edilen yaş ve cinsiyeti (olasılıkla birlikte) yazdır. Yaşın regresyon,
cinsiyetin sınıflandırma olduğunu markdown'da bir cümleyle belirt.

**5 · Kendi fotoğrafını dene**
`from google.colab import files` ile yükleme. Yüklenen fotoğraf için 2–4.
adımların hepsini tek seferde çalıştıran bir fonksiyon yaz, sonuçları tek
figürde göster. Yüz bulunamazsa anlaşılır bir Türkçe uyarı versin, hata
fırlatmasın.

**6 · Bonus — Yüz de bir vektör**
Yüzü bir **embedding vektörüne** çevir. Vektörün boyutunu ve ilk birkaç
elemanını yazdır. Sonra **iki farklı yüzü** karşılaştır: kosinüs benzerliğini
hesapla ve "aynı kişi mi?" sorusuna eşik değeriyle cevap ver. Sunumdaki
embedding slaydının karşılığı bu — "anlam bir sayı dizisine dönüşüyor".

**7 · Sınırlar ve sorumluluk**
Kod değil, markdown. Kısa ve net: bu modeller eğitim verisindeki
dengesizlikleri taşır; yaş tahmini kaba bir tahmindir; duygu tahmini yüz
ifadesini okur, kişinin gerçek duygusunu değil; rıza olmadan yüz verisi
işlemek GDPR/KVKK kapsamındadır; işe alım, güvenlik, kredi gibi kararlarda
kullanılmamalı.

**Özet**
Defterde görülenleri sunumdaki kavramlarla eşleyen kısa bir kapanış.

---

## 4. Biçim ve üslup

- Her kod hücresinden **önce** onu açıklayan bir markdown hücresi olsun.
- Markdown'larda yer yer `> **Konuşma notu:**` ile eğitmene sunum sırasında
  söyleyeceği cümleyi hazırla.
- Kod hücreleri kısa ve okunur olsun; canlı derste ekrana yansıtılacak.
  Uzun blokları fonksiyonlara böl, fonksiyon adları Türkçe olsun
  (`yuzleri_bul`, `duygu_analiz_et`, `resim_yukle` gibi).
- Grafiklerde renk paleti sunumla uyumlu olsun: altın `#C08A2E`,
  lacivert `#15263F`, turkuaz `#148F77`.
- Uyarı ve log gürültüsünü bastır (`warnings.filterwarnings("ignore")`,
  `TF_CPP_MIN_LOG_LEVEL`).
- Çıktı: tek bir `.ipynb` dosyası, `nbformat 4`.

---

## 5. Kabul kriteri

1. **Tamamen temiz** bir Colab runtime'ında (Çalışma zamanı → Çalışma zamanını
   sil) defter baştan sona, hücre hücre, **hiç hata vermeden** çalışıyor.
2. Kurulumdan doğrulama hücresine kadar geçen süre 3 dakikanın altında.
3. Her bölüm en az bir **görsel çıktı** üretiyor (fotoğraf, kutu, bar grafik).
4. Hiçbir hücre Google Drive'a erişmiyor, hiçbir hücre eğitim yapmıyor.
5. Bir sonraki çalıştırmada kırılmaması için **tüm pip paketleri sürümüyle
   sabitlenmiş**.
6. Teslimle birlikte, defteri hangi tarihte hangi Colab Python sürümünde
   çalıştırıp doğruladığını yaz.
