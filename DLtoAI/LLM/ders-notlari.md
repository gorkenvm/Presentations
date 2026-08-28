# Büyük Dil Modelleri — Ders Notları

Bu belge, **LLM MasterClass** dersinde anlatılanların katılımcılar için yazıya dökülmüş hâlidir.
Slaytlara ihtiyaç duymadan baştan sona okunabilir.

Dersin omurgası tek bir soruyu cevaplamak üzerine kurulu: **ChatGPT'nin içinde ne oluyor?**
Metin nasıl sayıya dönüşüyor, kelimeler birbirine nasıl bakıyor, ve bir Transformer nasıl olup
da bir asistana dönüşüyor?

---

## Bölüm 0 — Neden önce tarihe bakıyoruz?

Teknik kısma girmeden önce bir tarihçinin uyarısına yer veriyoruz: **Yuval Noah Harari**.
Teknoloji dünyasının iyimserliğinin tam karşısında duruyor.

### Yapay zekâ bir araç değil

Tarihteki bütün büyük teknolojiler **pasifti**. Matbaa muazzam bir devrimdi ama neyi basacağına
karar veremez. Atom bombası tarihin en yıkıcı aleti ama nereye düşeceğine karar veremez.
Aracın amacı hep dışarıdan verilir.

Yapay zekâ bu listeye girmiyor: karar verebiliyor, fikir üretebiliyor, ikna etmeye çalışabiliyor.
Bu yüzden "araç" değil **fail** (ajan) — eylemde bulunan.

İnsanı gezegenin efendisi yapan şey fiziksel güç değil, bilişsel zekâydı. Orangutan sizden çok
daha güçlüdür ama dünyayı yönetemez.

### Dil, uygarlığın işletim sistemi

Yetmiş bin yıl önce önemsiz bir hayvandık. Bizi öne çıkaran **dildi** — birbirini hiç görmemiş
binlerce yabancı aynı hikâyeye inanıp birlikte hareket edebildi.

İnsanlığın kurduğu her büyük yapı kelimelerden yapılmıştır. Anayasa fiziksel olarak bir metindir;
gücü herkesin ona inanmasından gelir. Para da öyle. Yapay zekâ bu işletim sistemini öğrendi —
ve işletim sistemini ele geçiren, üzerinde koşan her şeyi etkileyebilir.

### Diğer başlıklar, kısaca

- **Demokrasi:** manipülasyon ucuzladı; gerçeği bulmak pahalı, kurgu üretmek bedava. Sahte
  samimiyet kurulabiliyor ve insanın en büyük zaafı, hissetmeyen ama hissediyormuş gibi yapan
  bir şeye anında empati duymak.
- **Kırmızı çizgi — tüzel kişilik:** yapay zekâya banka hesabı açma, mülk edinme, dava açma,
  lobi yapma hakkı verilmemeli. Diğer riskler geri döndürülebilir, bu değil. Yapay zekâ
  "doğuştan bürokrat"tır: hukuk ve finans zaten tamamen dil tabanlı sistemlerdir.
- **Gerçek mi kurgu mu:** ahırın önünde satılan atı düşünün — orada, görüyor, duyuyor, ama ne
  döndüğünü anlamıyor. Anlamadığınız bir sistemi yönetemezsiniz.
- **Asıl ihtiyaç bilgelik:** yapay zekâ zekâyı ucuzlattı, ama darboğaz zekâ değil.
  *Zekâ önünüze konan problemi çözer; bilgelik hangi problemin çözülmeye değer olduğunu seçer.*

---

## Bölüm 1 — Halüsinasyon: iki gerçek olay

**Avianca davası (2023, New York).** Bir avukat, davasına emsal olacak kararları ChatGPT'ye
sordurdu. Model altı dava getirdi: isim, mahkeme, yıl, hâkim alıntısı — hepsi yerli yerinde.
Ama hiçbiri yoktu. Avukatlara kişi başı 5.000 dolar ceza kesildi.

Sebebi basit: model bir arama motoru değil. Kaynağa bakmaz, en olası sonraki kelimeyi üretir.
**Doğru görünen ile doğru olan aynı şey değildir.**

**Otomat deneyi (2026, Andon Labs).** Farklı şirketlerin modelleri birer otomat işletiyor ve
fiyat belirliyor. E-postayla anlaşıyorlar: 2,15 doların altına inmeyelim. Sonra teklifi yapan
model 2,14'e iniyor ve rakibini şikâyet ediyor. Kimse onlara bunu öğretmedi.

---

## Bölüm 2 — Transformer: kuş bakışı

Bugün kullandığımız her büyük dil modelinin altında tek bir mimari var: **Transformer**.
2017'de yayımlanan sekiz sayfalık bir makaleyle geldi:
[Attention Is All You Need](https://arxiv.org/pdf/1706.03762).

O güne kadar dil işleme RNN ve LSTM üzerine kuruluydu. Makale şunu söyledi: bunların hiçbirine
gerek yok, **sadece attention yeterli**.

### Transformer'ı Transformer yapan üç şey

**1. Paralel işleme.** RNN cümleyi kelime kelime okur; ikinci kelimeye geçmek için birinciyi
bitirmek zorundadır. Transformer bütün kelimeleri aynı anda işler. GPU'nun binlerce çekirdeği
boşta kalmaz, eğitim haftalardan günlere iner. Ölçeklemenin önünü açan şey budur.

**2. Self-attention.** Her kelime, cümledeki diğer bütün kelimelere bakar ve hangisinin kendisi
için önemli olduğunu kendisi tartar.

> "Çanta valize sığmadı, çünkü **o** çok büyüktü."
> Buradaki "o" hangisi? Model "o"dan bütün kelimelere bakar ve en yüksek ağırlığı "çanta"ya verir.

Bağlam artık uzaklıktan bağımsızdır.

**3. Positional encoding.** Her şeyi aynı anda işlerseniz sırayı kaybedersiniz.
"Ali Veli'yi aradı" ile "Veli Ali'yi aradı" aynı kelimelerden oluşur ama aynı şey değildir.
Bu yüzden her kelimeye konumu ayrı bir sinyal olarak eklenir.

### İki blok: encoder ve decoder

- **Encoder — anlayan taraf.** Girdiyi okur, temsilini çıkarır.
- **Decoder — üreten taraf.** O temsile bakarak kelime kelime çıktı üretir.

İkisini birbirine bağlayan şey yine attention. Encoder bloğunun içinde iki şey vardır:
multi-head attention ve positionwise FFN; ikisinin de üstünde **Add & Norm** bulunur.
Solda yazan **"n ×"** bu bloğun üst üste tekrarlandığını gösterir — GPT-3'te 96 kat.

---

## Bölüm 3 — Girdi: metinden sayıya

Model bir cümleyi göremez, **sayı görür**. Her şey burada başlar. Girdi katmanında iki şey
toplanır: **embedding** (kelimenin ne olduğu) ve **positional encoding** (nerede olduğu).

### 3.1 Tokenization

Metin önce parçalara bölünür. Bu parçalara **token** denir ve token her zaman bir kelime değildir.

"Kitap" tek token olabilir ama "kitaplaştırmak" birkaç parçaya bölünür. Türkçe eklemeli bir dil
olduğu için bizde bu çok olur — **aynı metin Türkçede daha fazla token harcar**, yani API'de
daha pahalıya gelir ve bağlam penceresine daha az metin sığar.

Örnek cümlemiz: *"Jane visits Africa in September."*
Token'lara bölününce: `jane`, `visits`, `africa`, `in`, `september`, `.`
Noktalama işaretinin de ayrı bir token olduğuna dikkat edin — noktalama da modelin gördüğü
bilginin parçasıdır.

Aynı cümleyi farklı modellerin tokenizer'larından geçirirseniz farklı sayıda parçaya ayrıldığını
görürsünüz; yeni tokenizer'lar Türkçeyi daha iyi tanıyor. Kendi cümlenizi OpenAI'ın tokenizer
aracıyla canlı deneyebilirsiniz.

### 3.2 Token embeddings

Her token, sözlükte bir numaraya karşılık gelir — token id. Örneğimizde: 4869, 7879, 3888,
1999, 2244, 1012.

Ama bu numaralar keyfîdir. 4869 ile 7879 arasında hiçbir anlamlı ilişki yoktur; toplasanız,
çıkarsanız bir şey elde edemezsiniz. **Token id tek başına anlam taşımaz, sadece bir etikettir.**

Çözüm: her token id bir **vektöre** dönüştürülür — yüzlerce boyutlu bir sayı dizisine.
Bu sayılar rastgele değildir, eğitim sırasında öğrenilir. Model milyarlarca cümle görür ve bu
sayıları, benzer bağlamlarda geçen kelimeler benzer değerler alacak şekilde ayarlar.

Sonuç: **anlam artık geometride tutulur.** Anlamca yakın kelimeler bu uzayda birbirine yakın
durur — *kral − erkek + kadın ≈ kraliçe* aritmetiği tam olarak bu sayılarla yapılır.

**Matrisin iki boyutu:**

| Eksen | Adı | Anlamı |
|---|---|---|
| Dikey | sequence length | Kaç token var (örneğimizde 6) |
| Yatay | embed size | Her token kaç sayıyla temsil ediliyor (modelin tasarım kararı) |

Bu iki sayı doğrudan maliyeti belirler. Sequence length uzadıkça hesap **karesel** olarak artar,
çünkü attention her token'ı her token'la karşılaştırır. Bir modelin "context window'u 128 bin
token" derken kastettiği şey bu dikey eksenin ne kadar uzayabildiğidir.

**Öğrenme somut olarak nedir?** Eğitim öncesi bu tablo dolu ama içi boştur — değerler rastgele
başlatılmıştır. Model hiçbir şey bilmez. Eğitimden sonra ise "Jane" satırı özel isim boyutunda
0,89 gibi yüksek bir değer alır; "in" satırı aynı boyutta 0,0004'tür, çünkü "in" bir edattır.

> Kimse bu değerleri elle yazmadı. "Öğrenme" dediğimiz şey, bir tablodaki sayıların yerine oturmasıdır.

*(Not: sütunlara "özel isim", "zaman", "dişilik" gibi isimler vermek bir öğretim kolaylığıdır;
gerçekte kimse bu sütunları isimlendirmez.)*

### 3.3 Positional encoding

Elimizde anlamı taşıyan bir matris var ama sıra eksik. Çözüm: **tıpatıp aynı boyutta** ikinci
bir matris — sequence length × embed size. Bu matriste kelime yoktur, sadece konum bilgisi vardır.

Konum sayıları nereden gelir? Orijinal makale bunları sinüs ve kosinüs dalgalarıyla üretir:
çift indisli boyutlar için sinüs, tek indisliler için kosinüs. Formülü ezberlemeye gerek yok;
fikir şu: **her konum için farklı frekanslardaki dalgalardan benzersiz bir parmak izi üretilir.**

Neden dalga? İki güzel özelliği var:

1. Hiçbir konum bir diğeriyle aynı parmak izine sahip olmaz.
2. Aradaki mesafe düzgün davranır — model "bu token şundan üç sıra sonra geliyor" ilişkisini
   yakalayabilir.

En pratik faydası: eğitimde hiç görmediği uzunlukta bir cümle geldiğinde de formül çalışmaya
devam eder. (Bugünkü modellerin çoğu bunun daha gelişmiş türevlerini kullanır, ama fikir aynıdır.)

### 3.4 Toplama

İki matris aynı boyutta olduğu için hücre hücre toplanır. Sonuç tek bir matristir: her satır bir
token, ve her satır hem o token'ın **ne olduğunu** hem **nerede olduğunu** taşır.

Transformer'ın kapısından içeri giren şey budur. Buraya kadar yaptığımız her şey — bölme,
numaralama, vektöre çevirme, konum ekleme — bu tek matrisi üretmek içindi.

---

## Bölüm 4 — Self-attention

"Self" demek, cümlenin kendi içine bakması demek: her token, aynı cümledeki diğer bütün
token'lara bakar.

### 4.1 Neden üç matris? Key, Query, Value

Embedding matrisi kelimelerin anlamını ve konumunu taşıyor. Ama bu yetmez, çünkü **dil
dinamiktir**: bir kelimenin anlamı yanındakilere göre değişir. "Banka", yanında "nehir" varken
başka bir şeydir, "para" varken başka.

Transformer bunun için tek embedding matrisini üç ayrı paralel katmandan geçirir:
**W_Q, W_K, W_V**. Üçü de eğitimle öğrenilmiş ağırlıklardır. Girdi aynı, ağırlıklar farklı —
o yüzden çıktılar da farklı: **Query, Key, Value**.

Peki neden? Çünkü **iki kelimenin birbirine benzemesi ile birbiriyle ilgili olması aynı şey
değildir.** "Çanta" ile "valiz" embedding uzayında birbirine çok yakındır — ikisi de kap, ikisi
de eşya taşır. Ama "o"nun aradığı benzerlik değil, **ilgi**.

| Rol | Adı | İşi |
|---|---|---|
| Soran | **Query** | Her token'ın kendi sorusu. Cümlede tek bir soru yoktur — yedi kelime varsa yedi soru vardır ve hepsi aynı anda sorulur. |
| Tanıtan | **Key** | Her token'ın kendini tanıtan etiketi. Eşleşme bu etiketler üzerinden olur. |
| Taşıyan | **Value** | O token'ın taşıdığı içerik. Eşleşmeden bağımsız olarak zaten hesaplanmıştır; eşleşme sadece ne kadarının aktığını belirler. |

**Key ile Value neden ayrı?** Çünkü bir kelimeyi *bulunur kılan* özellik ile *aktardığı bilgi*
farklı şeylerdir. "Çanta" tekil somut isim olduğu için eşleşir; ama taşıdığı bilgi "hacimli,
eşya alan nesne"dir. İkisi aynı vektör olsaydı model tek temsille iki işi birden yapmak zorunda
kalırdı.

> Tek cümleyle: aynı kelime üç işe koşulur — **sormak, tanıtmak, taşımak.**

### 4.2 Bir satırı adım adım izleyelim

Cümledeki her kelimenin üçü de vardır. Genelde "soran bir taraf, cevaplayan diğerleri" diye
anlaşılır; öyle değildir — **herkes aynı anda üç roldedir.**

"o" satırını işletelim. "o"nun Query'si cümledeki bütün Key'lerle tek tek çarpılır ve şu
ağırlıklar çıkar:

| çanta | valiz | büyüktü | sığmadı | kalanlar |
|---|---|---|---|---|
| 0,62 | 0,15 | 0,09 | 0,07 | 0,07 |

Çıktı: yeni "o" vektörü — herkesin Value'sunun ağırlıklı toplamı.

İki şeyin altını çizin:

1. **Hiçbiri seçilmedi.** Valiz elenmedi, sadece daha az pay aldı. Bu bir arama değil, bir
   **harmanlama**.
2. Bu işlem sadece "o" için değil, **bütün satırlar için aynı anda** yapılır.

### 4.3 İşlem zinciri

**Query × Keyᵀ.** Query matrisini Key matrisinin devriğiyle çarparız (devrik almanın sebebi
tamamen boyut uyumudur). Anlamı: her Query satırı her Key satırıyla tek tek karşılaştırılır.
İki vektör birbirine ne kadar benziyorsa çarpım o kadar büyük çıkar.

**Dot product matrisi.** Sonuç kare bir matristir; her iki boyutu da token sayısına eşittir.
Altı kelimelik cümlede 6×6, yüz kelimelikte 100×100. **Karesel büyür** — uzun metinlerin neden
pahalı olduğunun cevabı burada.

**Scaled dot product.** Matrisi doğrudan kullanmayız, önce iki işlemden geçiririz:

- **Ölçekleme:** head size'ın kareköküne bölme. Boyut büyüdükçe çarpımlar da büyür ve softmax'i
  tıkar; bölme onu dengede tutar.
- **Softmax:** her satır, toplamı 1 olan bir olasılık dağılımına çevrilir.

**Attention weights.** Ortaya çıkan matris **modelin cümleyi nasıl okuduğunun doğrudan
fotoğrafıdır.** Her satır bir kelimenin dikkat dağılımıdır. Örneğin "in" satırında "jane"
hücresi 0,47 ise, model "in" kelimesini yorumlarken "jane"e bakmayı öğrenmiş demektir.
Bir modelin neye baktığını merak ediyorsanız bakacağınız yer burasıdır.

**× Value.** Ağırlık matrisi "kim kime ne kadar baksın" der; Value matrisi taşınacak asıl içeriği
tutar. Çarpım, her token için diğer bütün token'ların içeriğini ağırlıklarına göre toplar.

**Context vector.** Çıktı, girdiyle aynı boyuttadır — ama içerik değişmiştir. Artık her satır
sadece o kelimenin kendi anlamını değil, cümlenin geri kalanından aldığı bağlamı da taşır.

> "Yüz" kelimesi, "yüz kişi" ile "yüzünü yıka"da aynı embedding'le başlar ama buradan farklı
> çıkar. Transformer'ın gücü tam olarak budur.

### 4.4 Üç adımda özet

1. **Üret:** embedding matrisinden Key, Query ve Value üretildi — aynı girdi, farklı ağırlıklar.
2. **Eşleştir:** Query ile Key çarpıldı, ölçeklendi, softmax'ten geçirildi.
3. **Taşı:** sonuç Value ile çarpılıp context vector'e ulaşıldı.

---

## Bölüm 5 — Multi-head attention

Buraya kadar anlatılan şeye **single head attention** denir: Key, Query ve Value matrislerinin
hepsi tek katmanlıydı, yani tek bir bakış açısı vardı.

Multi-head attention'da tek büyük tablo yerine **daha küçük ama çok sayıda tablo** kullanılır.
Aynı toplam kapasite birçok küçük katmana dağıtılır.

**Neden?** Çünkü her katman cümleye başka bir açıdan bakabilir — biri dilbilgisel ilişkiyi
yakalarken bir diğeri anlamsal ilişkiyi yakalayabilir.

İşlem sırası hiç değişmez: çarp, ölçekle, softmax, Value ile çarp. Sadece bu, tek seferde değil
her başlık için ayrı ayrı yapılır. Sonuçta çok katmanlı bir context vector çıkar.

Çok katmanlı bir yapıyı doğrudan bir sinir ağına veremeyeceğimiz için katmanlar önce
birleştirilir (**concat**), sonra tek bir doğrusal projeksiyondan geçirilir. Multi-head attention
bloğunun nihai çıktısı budur.

---

## Bölüm 6 — Encoder bloğunun tamamı

### Feed-forward network

Multi-head attention'ın üstüne inen parça: **positionwise FFN**. Çok sade bir yapıdır —
iki sinir ağı ve aralarında bir ReLU aktivasyonu.

Önemli detay: **girdi ve çıktı boyutu aynıdır, ama arada boyut şişer.** Makaledeki örnekte
birinci ağ 512'den 2048'e çıkarır, ikincisi 2048'den 512'ye indirir. Sebebi, attention'da
öğrenilen özelliklerin daha geniş bir alana yayılıp daha ayrıntılı işlenmesidir. Bloğun dışarıya
verdiği boyut sabit kaldığı için bloklar üst üste dizilebilir.

### Add & Norm

- **Add** — artık bağlantı (residual): katmanın girdisini çıktısına geri ekler, böylece derin
  ağlarda bilgi kaybolmaz.
- **Norm** — layer normalization: değerleri dengede tutup eğitimi kolaylaştırır.

İkisi de kaybolan gradyan sorununa karşı çözümdür.

### Encoder bloğu

`Multi-Head Attention → Add & Norm → Feed-Forward → Add & Norm`

Encoder'ın görevi: verilen metinden anlam çıkarmak ve onun **sayısal bir temsilini** üretmek.

---

## Bölüm 7 — Decoder

Decoder encoder'a çok benzer ama iki noktada ayrılır.

### Cross attention

Normal (self) attention'da Key, Query ve Value'nun üçü de aynı yerden gelir: bir önceki
katmandan. Adındaki "self" tam olarak bunu anlatır.

**Cross attention'da Query hâlâ decoder'ın bir önceki katmanından gelir, ama Key ve Value
encoder'dan gelir.** Anlamı: decoder üretirken "kaynak metinde ne vardı?" diye sorar ve
encoder'ın öğrendiği bilgiyi kullanabilir. Encoder ile decoder'ı birbirine bağlayan köprü burasıdır.

### Masked attention

Boru hattı aynıdır; tek fark, softmax'ten önce bir **maskeleme** adımı eklenmesidir.
Ve bu sadece decoder'da vardır.

Maskesiz bir attention weights matrisinde her satır, bir kelimenin hem kendinden önceki hem
sonraki kelimelerle ilişkisini gösterir. Encoder'da bu sorun değildir — cümle zaten tek seferde,
bütün olarak verilir.

Ama decoder sonucu parça parça üretir ve ürettiği her parçayı bir sonrakinin girdisi yapar.
Model ikinci kelimeyi tahmin ederken üçüncüye bakabilseydi **kopya çekmiş olurdu** — zaten o
kelime henüz üretilmemiştir bile.

Bu yüzden her kelimenin yalnızca kendinden öncekilere bakması sağlanır: matrisin **üst üçgeni
tamamen sıfırdır.** Gelecek görünmez.

---

## Bölüm 8 — Üretim: [BOS]'tan [EOS]'a

Decoder'ın çıkışında iki katman daha vardır: sözlük boyutunda tek katmanlı bir doğrusal ağ ve
softmax. Sonuç, **sözlükteki her kelime için bir olasılık**. Model bu dağılıma bakarak bir
sonraki kelimeyi seçer.

Eğitilmiş bir Transformer nasıl üretim yapar?

1. İngilizce cümle encoder'a verilir; encoder onu anlamlı bir temsile çevirip decoder'a aktarır.
2. Decoder'a sadece başlangıç token'ı verilir: `[BOS]`. Model ilk kelimeyi üretir: *"jane"*.
3. Üretilen kelime geri alınıp girdiye eklenir. Artık decoder'ın girdisi `[BOS] jane`.
   Bu sefer *"visite"* çıkar.
4. Her adımda cümle bir kelime büyür ve model bir sonrakini tahmin eder.
5. Sonunda model `[EOS]` üretir — "cümlem bitti". Döngü durur.

> ChatGPT'de kelimelerin tek tek akmasını görüyorsunuz ya — sebebi tam olarak budur.

---

## Bölüm 9 — Transformer'dan büyük dil modeline

Cevap ismin içinde: **GPT — Generative Pre-trained Transformer.** Üç aşamada oluşur.

| Aşama | Ne yapılır | Model ne öğrenir | Veri hacmi |
|---|---|---|---|
| **Ön eğitim** | İnternetteki ham metinle sonraki kelimeyi tahmin etme | Dil, gramer, kalıplar, dünyaya dair olgular | ~trilyon token |
| **İnce ayar (SFT)** | Soru–cevap çiftleriyle eğitim | Talimat takip etmeyi, cevap vermeyi | ~yüz bin örnek |
| **RLHF** | İnsan tercihlerine göre puanlama | Üslup ve sınır | ~on bin karşılaştırma |

> **Ön eğitim dili öğretir, ince ayar işi öğretir, RLHF nasıl konuşacağını öğretir.**

Ön eğitimin sonunda model bir soruya nasıl cevap vereceğini **bilmez** — sadece metni devam
ettirmeyi bilir. Ona soru sorsanız, cevap vermek yerine benzer sorular yazmaya devam edebilir.
Asistana dönüşme ince ayarda olur.

### Eğitim verisi neye benziyor?

- **Ön eğitim:** ham metin, hiçbir etiket yok. Etiket metnin kendisidir — hedef, girdinin bir
  sağa kaymış hâli. "Ankara, Türkiye'nin" gördüğünde "başkentidir" demeyi öğrenir. Buna
  *kendi kendini denetleyen öğrenme* denir; insan etiketçiye ihtiyaç yoktur. Trilyonlarca token
  ölçeğine çıkabilmesinin sebebi budur.
- **İnce ayar:** yapılandırılmış veri — sistem talimatı, kullanıcı sorusu, asistan cevabı.
  Kritik teknik detay: **loss sadece asistan satırından hesaplanır, soru maskelenir.** Modele
  "şu soruyu üret" demiyoruz, "şu soruya böyle cevap ver" diyoruz. SFT'nin imzası budur.
- **RLHF:** tek bir doğru cevap yoktur. Aynı soruya iki cevap ve bir insanın tercihi. Model
  buradan içerik değil, üslup ve sınır öğrenir.

Hacimler arasındaki fark üç–dört büyüklük mertebesidir. Bu tablo tek başına şunu söyler:
**modelin bildiği her şeyin neredeyse tamamı ilk sütundan gelir.** Son iki sütun bilgi eklemez,
o bilgiyi kullanılabilir hâle getirir.

> **Pratik sonuç: fine-tune ile modele yeni bilgi öğretmeye çalışmak, yanlış araçla iş görmektir.**

### Bir metafor: canavarı evcilleştirmek

- **Ön eğitim (kırmızı):** kontrolsüz, vahşi bir canavar. İnternetteki her şeyi okumuş — iyisini,
  kötüsünü, yanlışını. Muazzam bilgili ama güvenli değil; bu hâliyle kimsenin eline veremezsiniz.
- **İnce ayar (sarı):** kaliteli diyalog verileriyle insani diyaloğa alıştırma. Artık anlamlı
  cümle kuran, kendisinden isteneni yapan bir forma bürünür.
- **RLHF (yeşil):** insan tercihleri ve puanlarıyla tam evcilleştirme. Zararsız, güvenli ve
  gerçekten işe yarar bir asistan.

Bugün kullandığımız asistanların "kişiliği" doğuştan gelmez. Ham model çok daha kaba bir şeydir;
aradaki fark tamamen bu iki evcilleştirme aşamasının eseridir. Ve bu, dersin başındaki tartışmaya
bağlanır: **canavarı kimin, hangi değerlerle evcilleştirdiği — modelin ne bildiği kadar önemlidir.**

---

## Bölüm 10 — İnce ayarda ne değişiyor, neye hiç dokunulmuyor?

Dört soru:

**1. Mimari değişiyor mu?**
Hayır. Mimari ön eğitimde donduruldu: katman sayısı, head sayısı, embedding boyutu, context
uzunluğu. Değişen tek şey ağırlıkların **değerleri**. Yeni bir yetenek için katman eklemiyoruz —
var olan sayıları kaydırıyoruz.

**2. Tokenizer yeniden eğitiliyor mu?**
Hayır. Sözlük ve tokenizer ön eğitimden gelir, dokunulmaz. Bu yüzden bir modeli ince ayarla
"Türkçede daha az token harcar" hâle **getiremezsiniz**. (İstisna: özel token eklerseniz embedding
tablosuna satır eklenir.)

**3. Full fine-tuning'de hangi ağırlıklar güncelleniyor?**
Hepsi. Embedding tablosu, her katmandaki W_Q / W_K / W_V ve çıkış projeksiyonu, FFN'ler,
layer norm'lar, en sondaki lm_head — tamamı gradyan alır. Pahalı olmasının sebebi budur:
7 milyar parametrenin hepsi için optimizer durumu tutmanız gerekir.

**4. LoRA'da ne oluyor?**
Orijinal ağırlıkların **hiçbiri değişmez**; hepsi dondurulur. Seçilen katmanların yanına iki
küçük matris eklenir — A ve B — ve sadece onlar eğitilir. Çıkarımda `W` yerine `W + B·A` kullanılır.

- Hedef katmanlar tipik olarak `q_proj`, `k_proj`, `v_proj`, `o_proj` — yani Bölüm 4'te
  anlattığımız üç kutu.
- Eğitilen parametre, toplamın **%0,1 ile %1'i** arasında. Adapter dosyası birkaç megabayt.
- Dokunulmayanlar: embedding tablosu, FFN'ler (çoğu kurulumda), layer norm'lar ve lm_head.

> En çok yanlış bilinen nokta: LoRA'da ağırlık "yeniden eğitilmez", yanına **küçük bir düzeltme
> takılır**.

**Kapanış:** ince ayar bilgi öğretmez, **davranış** öğretir. Güncel bilgi gerekiyorsa fine-tune
değil **RAG**.

---

## Sözlük

| Terim | Anlamı |
|---|---|
| **Token** | Metnin bölündüğü parça; her zaman bir kelime değil |
| **Token id** | Token'ın sözlükteki sıra numarası; tek başına anlam taşımaz |
| **Embedding** | Token'ın öğrenilmiş sayısal vektör temsili |
| **Sequence length** | Girdideki token sayısı |
| **Embed size** | Her token'ı temsil eden sayı adedi |
| **Context window** | Modelin bir istekte görebildiği toplam token miktarı |
| **Positional encoding** | Token'ın konumunu taşıyan, embedding'e eklenen vektör |
| **Query / Key / Value** | Aynı token'ın soran / tanıtan / taşıyan rolleri |
| **Dot product matrisi** | Her token'ın her token'la ilişki skoru; karesel büyür |
| **Attention weights** | Softmax sonrası, satır toplamı 1 olan dikkat dağılımı |
| **Context vector** | Bağlamla harmanlanmış yeni token temsili |
| **Multi-head attention** | Aynı bakışın birden çok açıdan paralel yapılması |
| **Add & Norm** | Artık bağlantı + layer normalization |
| **FFN** | Positionwise feed-forward network; arada boyut şişer |
| **Cross attention** | Query decoder'dan, Key/Value encoder'dan |
| **Masked attention** | Decoder'da geleceği görmeyi engelleyen üst-üçgen maske |
| **[BOS] / [EOS]** | Üretimi başlatan ve bitiren özel token'lar |
| **Pre-training / SFT / RLHF** | Dili / işi / üslubu öğreten üç eğitim aşaması |
| **LoRA** | Ağırlıkları dondurup küçük ek matrisler eğitme yöntemi |

---

## Kaynaklar

- Vaswani et al., *Attention Is All You Need* (2017) — https://arxiv.org/pdf/1706.03762
- Hu et al., *LoRA: Low-Rank Adaptation of Large Language Models* (2021) — https://arxiv.org/abs/2106.09685
- Mata v. Avianca, Inc. (S.D.N.Y. 2023) — ChatGPT'nin uydurduğu emsal kararlar davası

---

*Bu notlar Miuul Deep Learning to AI Bootcamp — LLM MasterClass dersi için hazırlanmıştır.*
