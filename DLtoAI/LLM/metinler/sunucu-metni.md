# Sunucu Metni — DL MasterClass 2. Ders (v26)

## 1 · KAPAK

Merhaba, ben Veysel Murat Görken.
Lisansımı Biyomedikal mühendisliği üzerine yaptım; o yıllarda medikal görüntü işleme ve MATLAB'le yapay zekaya adım attım. Yüksek lisansta makine öğrenmesi ve ağaç modelleri üzerine yoğunlaştım. 3 yıl veri bilimci olarak çalıştıktan sonra yolum Berlin'e düştü; şu an burada iklim teknolojileri alanında AI Engineer olarak çalışıyorum. Ayrıca Miuul Deep Learning to AI Bootcamp'inde mentörlük yapmaya devam ediyorum.

Geçen derste derin öğrenmenin nasıl çalıştığını konuştuk: nöron, loss, gradient descent, transformer.

Bugün odaklanacağımız tek bir konu var: Büyük dil modelleri ve en büyük dertlerimizden biri olan halüsinasyonlarla nasıl baş edebileceğimiz.

## 2 · Önümüzdeki 50 yıla hazır mısınız?

Teknik kısma geçmeden önce on dakikanızı, bir tarihçinin uyarısına ayırmak istiyorum.

Yuval Noah Harari, Sapiens'in yazarı. Teknoloji liderlerinin iyimserliğinin tam karşısında duran şeyler söylüyor.

İlk tespiti şu: Tarih genelde yavaş akar. Bir kuşak bir şey öğrenir, bilgeliğini bir sonrakine aktarır, o da üstüne koyar. Harari diyor ki bu dönem bitti. Şu anda tek bir insan ömrüne sığdırılmış üç büyük devrimle aynı anda karşı karşıyayız. Ve artık sadece hesaplama yapan değil, karar da verebilen yeni bir zekâ türü dünyayı şekillendiriyor.

## 3 · Önümüzdeki 50 yıla hazır mısınız?

Şunu hatırlatarak devam ediyor: Yetmiş bin yıl önce biz, Afrika'nın bir köşesinde önemsiz bir hayvandık. Aslanlardan zayıftık, fillerden küçüktük. Bizi gezegenin efendisi yapan şey pençemiz ya da kaslarımız değildi. Dildi.

Dil sayesinde birbirini hiç görmemiş binlerce yabancı aynı hikâyeye inanıp birlikte hareket edebildi. Devletler, dinler, şirketler, para — hepsi bu sayede var. Harari buna "bilişsel devrim" diyor.

## 4 · Önümüzdeki 50 yıla hazır mısınız?

Ve uyarısı şu: Şimdi o dili, bizden başka biri de kullanıyor.

Soru teknik bir soru değil: Elli yıl sonra kararları kim veriyor olacak?

Şimdi bu iddiayı altı başlıkta açalım.

## 5 · Yapay zekâ bir araç değil

Harari'nin ilk itirazı, yapay zekânın "sadece bir araç" olarak anlatılmasına.

Diyor ki: Tarihteki bütün büyük teknolojiler pasifti. Matbaa muazzam bir devrimdi, ama matbaa neyi basacağına kendi karar veremez. Atom bombası tarihin en yıkıcı aleti, ama nereye düşeceğine kendi karar veremez. Bıçak da öyle: ekmek mi keseceksiniz, birine mi saplayacaksınız, buna siz karar verirsiniz.

Aracın amacı hep dışarıdan verilir.

## 6 · Yapay zekâ bir araç değil

Yapay zekâ bu listeye girmiyor. Çünkü karar verebiliyor. Yeni fikir üretebiliyor. Sizi ikna etmeye çalışabiliyor. Gerektiğinde manipüle edebiliyor.

Harari bunun için "araç" değil "fail" diyor — yani eylemde bulunan, ajan.

Buna bir de şunu ekliyor, ve bence en çarpıcı cümlesi bu: Uzaydan bir yabancı türün gelmesini beklememize gerek yok. Zaten kendi elimizle inorganik, ölümsüz ve bizden daha zeki bir tür yaratıyoruz.

## 7 · Yapay zekâ bir araç değil

Bir de güç meselesi var. İnsanı gezegenin efendisi yapan şey fiziksel güç değildi, bilişsel zekâydı. Bir orangutan sizden çok daha güçlüdür ama dünyayı yönetemez.

Harari diyor ki: Yapay zekâ bizi bu alanda geçtiğinde, bizim orangutan konumuna düşmemiz için başka hiçbir şeyin değişmesi gerekmez.

Ve Silikon Vadisi'nin kendine anlattığı hikâyeyi çok sert eleştiriyor: "Bir tanrı yaratacağız ama o bizim kölemiz olacak."

Harari'nin cevabı basit: Bir tanrı köle olarak kalmaz. Böyle bir dengesizlikte, sonunda köleleşen tarafın hangisi olacağı sorusu açık kalır.

Bunu aklınızda tutun, çünkü birazdan konuşacağımız her şey bu ayrımın üzerine kurulu.

## 8 · Uygarlığın işletim sistemi: dil

Peki dil neden bu kadar önemli?

Harari'nin cevabı şu: İnsanlığın kurduğu her büyük yapı aslında kelimelerden yapılmıştır. O bunlara "sosyal kurgu" diyor.

Bir anayasayı düşünün. Fiziksel olarak nedir? Bir metin. Gücü nereden geliyor? Herkesin ona inanmasından. Yarın sabah kimse inanmazsa, kâğıt kâğıt olarak kalır.

Din de öyle. Kutsal kitaplar kelimelerdir; ama milyarlarca insanı aynı anda aynı şekilde davranmaya ikna eder.

Para da öyle. Cebinizdeki banknotun kâğıt olarak değeri yok. Değerli, çünkü hepimiz birden aynı hikâyeye inanıyoruz.

## 9 · Uygarlığın işletim sistemi: dil

Harari buna "uygarlığın işletim sistemi" diyor. Ve diyor ki: Yapay zekâ dili sadece öğrenmedi — hackledi. İşletim sistemini ele geçiren bir güç, üzerinde çalışan yasaları, anayasaları, kutsal kitapları da kontrol edebilir hale gelir.

Burada iki benzetme yapıyor. Birincisi paralı asker tuzağı: Britanya Kralı, ülkeyi korusunlar diye Anglosakson paralı askerler tutmuş. Askerler işlerini yapmışlar. Sonra da yönetimi ele geçirmişler.

Harari'ye göre bugün yaptığımız şey tam olarak bu — dili bizim için yönetsin diye bir güç tutuyoruz, ama o gücün kendi gündemini kurmasını engelleyecek bir mekanizmamız yok.

## 10 · Uygarlığın işletim sistemi: dil

İkinci benzetme daha da somut: dijital göçmenler.

Diyor ki, yapay zekâ şirketlerine ait milyonlarca ajan bugün sınırları vizesiz geçiyor. Hiçbir pasaport kontrolünden geçmiyorlar, hiçbir ülkenin göç kotasına takılmıyorlar. Ama yerel kültürlerin içine giriyorlar. İnsanların nasıl düşündüğünü, neye inandığını, nasıl karar verdiğini etkiliyorlar. Harari bunu kitlesel bir göç dalgasına benzetiyor.

Ve şunu ekliyor: Bu etki yasaların nasıl yazılacağına, hatta ülkeyi kimin yöneteceğine kadar uzanabilir. Bugün bir seçmenin fikri nasıl şekilleniyor? Okuduğu, izlediği, konuştuğu şeylerle. Bunların ne kadarı artık bir algoritmanın önüne koyduğu şey?

Kısacası: İşletim sistemini ele geçiren, üzerinde çalışan her şeyi ele geçirir.

## 11 · Demokrasi sarsılıyor

Üçüncü başlık: demokrasi.

Harari diyor ki, demokrasinin özü aslında çok basit. İnsanlar bir araya gelir, fikirler etrafında konuşur, ikna eder, ikna olur.

Ama bu sohbetin tarafları artık sadece insanlar değil.

Birincisi: manipülasyon ucuzladı. Gerçeği bulmak zor ve pahalı; kurgu üretmek neredeyse bedava.

Tarih boyunca toplumları bir arada tutan şey ortak hikâyelerdi ve o hikâyeleri hep insanlar anlattı. Şimdi ilk kez hikâye anlatıcısı insan olmayabilir. Dili ve samimiyeti kullanarak inanç üretebilen, hatta kanıt üretebilen bir şeyden bahsediyoruz.

## 12 · Demokrasi sarsılıyor

Cambridge Analytica'yı hatırlayın — insanların oyları veriye bakılarak şekillendirildi.

O günün teknolojisiyle.

## 13 · Demokrasi sarsılıyor

İkincisi, benim en çok dikkatimi çeken kısım: sahte samimiyet.

Yapay zekâ sahte hesaplar, sahte kişiler yaratabiliyor. Sizinle bir yakınlık kuruyor. O yakınlık gerçek değil, ama sizin tarafınızda gerçek hissediliyor.

Üçüncüsü de en rahatsız edici olanı. Harari, bugünün çocuklarının doğdukları andan itibaren insanlardan çok yapay zekâlarla etkileşime girmesini "tarihin en büyük ve en korkutucu psikolojik deneyi" olarak tanımlıyor.

Ve şunu ekliyor: İnsanın en büyük zaafı, hissetmeyen ama hissediyormuş gibi yapan bir şeye anında empati duymak. Buna antropomorfizm deniyor. Bir robot süpürgeye isim takmamızın sebebi de bu.

Bu yüzden çok sert sınırlar öneriyor: yapay zekâ sosyal medya hesabı açamasın, çocuklarla denetimsiz etkileşime girmesin.

## 14 · Doğuştan bürokrat: tüzel kişilik

Dördüncü başlık, Harari'nin "kırmızı çizgi" dediği yer.

Diyor ki: Yapay zekâya asla tüzel kişilik verilmemeli. Bunu insanlık tarihinin yapabileceği "en aptalca şey" olarak tanımlıyor. Ve önemli bir ayrım koyuyor — diğer riskler geri döndürülebilir, bu değil.

Tüzel kişilik ne demek? Banka hesabı açabilmek. Mülk edinebilmek. Dava açabilmek. Sözleşme imzalayabilmek. Lobi faaliyeti yürütebilmek.

## 15 · Doğuştan bürokrat: tüzel kişilik

Şunu düşünün: Arkasında hiçbir insan olmayan bir yapı, mahkemeye gidebiliyor, para biriktirebiliyor, milletvekiline lobi yapabiliyor. Kime hesap veriyor? Kimseye. Kim dava edecek? Kimi?

Harari'ye göre bu, demokrasinin sonu olur.

Ve neden özellikle tehlikeli? Çünkü yapay zekâ, onun tabiriyle "doğuştan bir bürokrat". Dünyadaki bütün dilleri, bütün mevzuatı biliyor. Hukuk ve finans da zaten tamamen dil tabanlı sistemler — orada üstünlük kurmak için fiziksel hiçbir şeye ihtiyaç yok. Yorulmuyor, unutmuyor, tatile çıkmıyor.

## 16 · Doğuştan bürokrat: tüzel kişilik

Onun deyişiyle: tilki kümese girmiş olur.

Kümesin kurulma amacı tavukları korumaktır. Tilkiyi kümesin bekçisi yaparsanız, savunmayı kendi elinizle kaldırmış olursunuz. Tilki tavukları yemeye başladığında bunu size haber verecek olan da yine tilkidir. Yani hem koruyan hem denetleyen aynı taraf olur.

Yasaları yorumlayan, finansı yöneten ve bunların doğru yapılıp yapılmadığını denetleyen mekanizmanın hepsi aynı sisteme verilirse, bir şeyin ters gittiğini anlayacak bağımsız bir göz kalmaz.

## 17 · Dijital egemenlik ve kapatma düğmesi

Harari'nin bir başka uyarısı da egemenlik üzerine.

Bir de şu var: Tüm dünyanın verisi bugün tek bir merkezde toplanabiliyor.

## 18 · Dijital egemenlik ve kapatma düğmesi

Harari buna "kapatma düğmesi" diyor. Starlink örneğini veriyor — dünyanın öbür ucundaki bir sistem, tek bir hamleyle felç edilebilir.

Sonuç: İnsanlar özgür yurttaş olmaktan çıkıp, verisi izlenen birer kullanıcıya dönüşür. Harari buna "yapay devlet" diyor.

## 19 · Dijital egemenlik ve kapatma düğmesi

Bu yüzden ülkelerin, Amerika ile Çin arasındaki teknolojik yarışta geri kalma korkusuyla egemenliklerini yapay zekâya devretmemesi gerektiğini söylüyor.

Ve Harvardlı tarihçi Jill Lepore'a atıf yapıyor: Asıl tehlike makinelerin bizden zeki olması değil. Devletin ve demokrasinin yerini algoritmik sistemlerin alması. O zaman devlet, yurttaşın taleplerine göre değil, veri sistemlerine göre yönetilir.

## 20 · Gerçek mi, kurgu mu?

Beşinci başlık, bence en can alıcı benzetme.

Harari diyor ki: Gelecek nesiller için gerçek; karmaşık, ulaşması zor ve çoğu zaman can yakıcı bir şey olacak. Kurgu ise ucuz, basit ve çekici.

Bunu bir düşünün. Gerçeği öğrenmek emek ister, zaman ister, bazen de canınızı yakar — çünkü çoğu zaman duymak istediğiniz şey değildir. Kurgu ise anında anlaşılır, üretmesi bedavadır ve tam duymak istediğiniz şeyi söyler. Üstelik kendiliğinden yayılır, çünkü paylaşması keyiflidir.

Bu asimetride hangisinin kazanacağını tahmin etmek zor değil.

## 21 · Gerçek mi, kurgu mu?

Ve buradan çok çarpıcı bir örneğe geçiyor. Diyor ki: Bir at düşünün. Ahırın önünde iki insan para alışverişi yapıyor. Belki de o atın kendisini satıyorlar. At oradadır, olan biteni görür, sesleri duyar — ama ne döndüğünü anlamaz. Anlamadığı için de itiraz edemez.

Harari'nin iddiası şu: Yapay zekânın kurduğu finansal sistemler o kadar karmaşıklaşacak ki, on yıl içinde bizim konumumuz o atınkine benzeyebilir. Sistemin içindeyiz, olan biteni görüyoruz, ama artık anlamıyoruz.

Bu yüzden somut bir öneride bulunuyor: Finansal piyasalar yapay zekâya kapatılmalı.

Ve bu sadece finans meselesi değil. İnsanlar artık kime oy vereceği gibi hayati kararları bile devretmeye başladı. Karar vermeyi bıraktıkça düşünme kasımız zayıflıyor.

Şunu unutmayalım: Anlamadığınız bir sistemi yönetemezsiniz. Yönetemediğiniz bir sistemde de karar veren taraf siz değilsinizdir.

## 22 · Asıl ihtiyaç: bilgelik

Son başlık, ve Harari'nin bütün konuşmayı bağladığı yer.

Diyor ki: Yapay zekâ, problem çözme yeteneğini — yani zekâyı — inanılmaz ucuzlattı. Eskiden bir uzmana haftalarca ödeme yapmanız gereken işi bugün saniyeler içinde yaptırabiliyorsunuz.

Ama asıl darboğaz zekâ değil. Bilgelik.

Zekâ, önünüze konan problemi çözer. Bilgelik ise hangi problemin çözülmeye değer olduğunu seçer. Bunlar aynı şey değil.

## 23 · Asıl ihtiyaç: bilgelik

Ve şu rakamı veriyor: Bugün şirketler zekâya 100 birim harcarken, güvenliğe ve bilgeliğe 1 birim ayırıyor.

Benzetmesi de şu: Lambadan bir cin çıkmış durumda. Her dileğimizi gerçekleştirebilecek bir gücümüz var. Ama ne dileyeceğimizi bilecek olgunluğa sahip değiliz.

Harari'nin çözüm önerisi teknolojik değil: "Bilgelik devrimi" diyor. Yani sadece daha güvenli makineler tasarlamak değil, kendi arzularımızı da kontrol edebilecek bir derinliğe ulaşmak.

Şimdi bunu somut bir örneğe bağlayalım. Çünkü "yapay zekâ gerçeği umursamaz" cümlesi soyut duruyor. Bir mahkeme salonunda ne göründüğüne bakalım.

## 24 · Bunlar gelecek zaman değil

(not yok)

## 25 · Kaputun altı: Transformer

Şimdi kaputun altına bakalım.

Buraya kadar konuştuğumuz her şeyin altında tek bir mimari var: Transformer. Ve o mimari 2017'de yayımlanan sekiz sayfalık bir makaleyle geldi.

Makalenin adı: "Attention Is All You Need". Sekiz yazar — çoğu Google Brain ve Google Research'ten, biri Toronto Üniversitesi'nden.

O güne kadar dil işleme RNN ve LSTM üzerine kuruluydu. Bu makale şunu söyledi: Bunların hiçbirine gerek yok. Sadece attention yeterli.

Makalenin linkini paylaşıyorum, dersten sonra bakabilirsiniz:

https://arxiv.org/pdf/1706.03762

İsterseniz sadece ilk iki sayfasını okuyun. Alanı değiştiren fikir orada, çok sade bir dille anlatılıyor.

## 26 · Transformer'ı Transformer yapan üç şey

Transformer'ı Transformer yapan üç şey var.

BİRİNCİSİ: PARALEL İŞLEME
RNN cümleyi kelime kelime, sırayla okur — ikinci kelimeye geçmek için birinciyi bitirmek zorundadır.
Transformer bütün kelimeleri aynı anda işler.
Böylece GPU'nun binlerce çekirdeği boşta kalmaz.
Eğitim haftalardan günlere iner; ölçeklemenin önü açılan şey tam olarak budur.

İKİNCİSİ: SELF-ATTENTION
Her kelime, cümledeki diğer bütün kelimelere bakar.
Hangisinin kendisi için önemli olduğunu kendisi tartar — bu ağırlıklar veriden öğrenilir.
Ekrandaki örnek: "Çanta valize sığmadı, çünkü o çok büyüktü." Buradaki "o" hangisi? Çanta mı, valiz mi?
Model "o" kelimesinden bütün kelimelere bakar ve en yüksek ağırlığı "Çanta"ya verir.
Önemlisi şu: bağlam artık uzaklıktan bağımsız. Cümlenin başındaki kelimeyle sonundaki kelime arasında da doğrudan bağ kurulabiliyor.

ÜÇÜNCÜSÜ: POSITIONAL ENCODING
Her şeyi aynı anda işlerseniz bir şeyi kaybedersiniz: sırayı.
"Ali Veli'yi aradı" ile "Veli Ali'yi aradı" aynı kelimelerden oluşur ama aynı şey değildir.
Bu yüzden her kelimeye konumu ayrı bir sinyal olarak eklenir: kelime vektörü artı konum vektörü, modele giren girdiyi oluşturur.
Model sırayı ezberlemez — ölçer.

Özet: paralel işle, neyin önemli olduğunu kendin bul, sırayı unutma.

## 27 · Transformer mimarisi

İşte Transformer'ın tamamı. Bu haliyle karmaşık görünüyor — bilerek böyle gösteriyorum. Gelin bunu parçalayalım.

Kabaca iki blok var: solda encoder, sağda decoder.

Encoder anlayan taraf: girdiyi okuyup temsilini çıkarıyor.
Decoder üreten taraf: o temsile bakarak kelime kelime çıktı üretiyor. İkisini birbirine bağlayan şey yine attention.

Şimdi sağ tarafı, yani decoder'ı sahneden çıkaralım ve sadece anlayan tarafa bakalım.

## 28 · Transformer mimarisi  ·  Encoder

Geriye encoder kaldı. İçinde iki şey var.

Önce multi-head attention: cümledeki her kelime diğer bütün kelimelere bakıyor. "Multi-head" demek, bu bakışın birden fazla açıdan aynı anda yapılması demek — bir kafa dilbilgisel ilişkiye, bir başkası anlamsal ilişkiye bakabiliyor.

Sonra positionwise FFN: her kelime için ayrı ayrı çalışan küçük bir sinir ağı.

Her ikisinin de üstünde "Add & norm" var. "Add" artık bağlantı: girdiyi çıktıya geri ekliyor, böylece derin ağlarda bilgi kaybolmuyor. "Norm" ise değerleri dengede tutuyor.

Solda "n ×" yazıyor — bu blok üst üste birçok kez tekrarlanıyor. GPT-3'te 96 kat.

Şimdi bunu da kaldıralım. Çünkü her şeyin başladığı yer aslında en altta.

## 29 · Transformer mimarisi  ·  Girdi

En alta indik. Model bir cümleyi göremez, sayı görür. Metnin sayıya dönüştüğü yer burası.

İki şeyin toplandığını görüyorsunuz: embedding ve positional encoding.

Embedding kelimenin ne olduğunu, positional encoding ise nerede olduğunu taşıyor. İkisi toplanıp modele giriyor.

Bu kutuyu üçe ayırarak açalım.

## 30 · 

Birinci adım: TOKENIZATION.

Metin önce parçalara bölünüyor. Bu parçalara token diyoruz ve token her zaman bir kelime değil.

"Kitap" tek token olabilir ama "kitaplaştırmak" birkaç parçaya bölünür. Türkçe gibi eklemeli dillerde bu çok olur — bu yüzden Türkçe metinler İngilizceye göre daha fazla token harcar, yani aynı metin daha pahalıya gelir.

Her token sözlükte bir numaraya karşılık geliyor. Model artık kelimeyi değil, o numarayı görüyor.

## 31 · 

İkinci adım: TOKEN EMBEDDINGS.

Numara tek başına anlam taşımaz. 4711 numaralı token ile 4712 numaralı token arasında hiçbir ilişki yok.

Bu yüzden her token bir vektöre dönüştürülüyor — yüzlerce boyutlu bir sayı dizisine. Bu vektörler eğitim sırasında öğreniliyor.

Ve şu ortaya çıkıyor: anlamca yakın kelimeler bu uzayda birbirine yakın duruyor. Geçen hafta konuştuğumuz word embedding örneğini hatırlayın — kral eksi erkek artı kadın, kraliçeye yaklaşıyordu.

Yani model anlamı burada, geometride tutuyor.

## 32 · 

Üçüncü adım: POSITIONAL ENCODINGS.

Bir sorun kaldı. Transformer bütün kelimeleri aynı anda işliyor — bu onun gücü, ama aynı zamanda zaafı. Çünkü sırayı kaybediyor.

"Ali Veli'yi aradı" ile "Veli Ali'yi aradı" aynı kelimelerden oluşur ama aynı şey değildir.

Bu yüzden her token'ın vektörüne, konumunu anlatan bir vektör ekleniyor. Orijinal makalede bu sinüs ve kosinüs dalgalarıyla üretiliyor.

Üçü birleşince şu oluyor: model her kelime için hem ne olduğunu hem nerede olduğunu biliyor. Artık attention katmanına girmeye hazırız.

## 33 · Embeddings  ·  1) Tokenization

Tokenization'a başlıyoruz.

Şuradan başlayalım: Transformer bir kutu. Soluna İngilizce bir cümle koyuyorsunuz, sağından Fransızcası çıkıyor. Orijinal makale zaten çeviri için yazılmıştı.

Ama o kutunun içine girmeden önce bir sorun var. Model harf görmez, kelime görmez, cümle görmez. Sadece sayı görür.

Yani bu cümlenin kutuya girebilmesi için önce sayıya çevrilmesi gerekiyor. Bu bölümde tam olarak o dönüşümü izleyeceğiz.

## 34 · Gerçek token'lar nasıl görünüyor?

Şemaya dönmeden önce gerçekten nasıl göründüğüne bakalım.

Ekrandaki cümle Türkçe: "Yapay zekâ AI modelleri, metinleri kelime kelime değil token'lar halinde işler!"

Üçü de aynı cümle. Değişen şey, hangi modelin tokenizer'ından geçtiği.

Renklerdeki her blok bir token. Dikkat edin: bazı kelimeler tek parça kalıyor, bazıları ikiye üçe bölünüyor. "token'lar" hepsinde bölünmüş durumda — kesme işareti ayrı bir token.

Üç satırı karşılaştırın: aynı cümle farklı sayıda parçaya ayrılıyor. Yeni tokenizer'lar Türkçeyi daha iyi tanıyor, daha az parçaya bölüyor.

Bu neden önemli? Çünkü faturayı token üzerinden ödüyorsunuz ve context window token üzerinden doluyor. Aynı metin, eski bir modelde daha pahalıya gelir.

İsterseniz kendi cümlenizi deneyin — OpenAI'ın tokenizer aracı bunu canlı gösteriyor.

## 35 · Embeddings  ·  1) Tokenization

Elimizde tek bir cümle var: "Jane visits Africa in September."

İnsan için bu bir bütün. Anlamı var, öznesi var, zamanı var.

Model içinse şu an hiçbir şey ifade etmiyor. Onun için bu sadece bir karakter dizisi.

İlk iş bu cümleyi parçalara ayırmak.

## 36 · Embeddings  ·  1) Tokenization

Cümle token'lara bölündü: jane, visits, africa, in, september ve nokta.

Burada dikkat edilmesi gereken şey şu: token her zaman bir kelime değildir.

Bu örnekte öyle görünüyor çünkü İngilizce kelimeler kısa. Ama "kitaplaştırmak" gibi bir kelime birkaç parçaya bölünür. Türkçe eklemeli bir dil olduğu için bizde bu çok olur.

Pratik sonucu şu: aynı metin Türkçede İngilizceye göre daha fazla token harcar. API kullanıyorsanız aynı cümle size daha pahalıya gelir.

Bir de nokta işaretinin ayrı bir token olduğuna dikkat edin. Noktalama da modelin gördüğü bilginin parçası.

## 37 · Embeddings  ·  2) Token Embeddings

Şimdi her token'ın altına bir sayı geldi: 4869, 7879, 3888, 1999, 2244, 1012.

Bunlara token id diyoruz. Modelin sözlüğünde her token'ın bir sıra numarası var; bu numaralar o sözlükteki yerini gösteriyor.

Ama burada bir problem var. Bu numaralar keyfî. 4869 ile 7879 arasında hiçbir anlamlı ilişki yok. Numaraları toplasanız, çıkarsanız bir şey elde edemezsiniz.

Yani token id tek başına anlam taşımıyor. Sadece bir etiket.

## 38 · Embeddings  ·  2) Token Embeddings

İşte çözüm burada: her token id, bir sayı dizisine — bir vektöre — dönüştürülüyor.

Aşağıdaki tabloya bakın. Her satır bir token, her satırda onlarca, yüzlerce sayı var.

Bu sayılar rastgele değil. Eğitim sırasında öğreniliyorlar. Model milyarlarca cümle görüyor ve bu sayıları, benzer bağlamlarda geçen kelimeler benzer değerler alacak şekilde ayarlıyor.

Sonuç şu: anlam artık bir sayı dizisinde tutuluyor. Ve bu diziler bir uzayda konum belirtiyor — anlamca yakın kelimeler o uzayda birbirine yakın duruyor.

Geçen hafta konuştuğumuz örneği hatırlayın: kral eksi erkek artı kadın, kraliçeye yaklaşıyordu. İşte o aritmetik tam olarak bu sayılarla yapılıyor.

## 39 · Embeddings  ·  2) Token Embeddings

Bu matrisin iki boyutu var, ikisini de bilmek işinize yarar.

Dikey eksen: sequence length. Kaç token'ınız var. Bizim örneğimizde altı.

Yatay eksen: embed size. Her token'ın kaç sayıyla temsil edildiği. Bu, modelin tasarım kararı. Küçük modellerde birkaç yüz, büyük modellerde binlerce olabilir.

Bu iki sayı doğrudan maliyeti belirliyor. Sequence length uzadıkça hesap artıyor — hem de doğrusal değil, karesel olarak, çünkü birazdan göreceğimiz attention her token'ı her token'la karşılaştırıyor.

Bir modelin "context window'u 128 bin token" dediğinde kastettiği şey bu dikey eksenin ne kadar uzayabildiği.

## 40 · Embeddings  ·  2) Token Embeddings

Son bir soru: bu sayılar ne anlama geliyor?

Ekranda sütunlara isim verilmiş: özel isim, zaman, görmek, dişilik, sıcak. Bu bir öğretim kolaylığı — sezgi kazanmak için. Gerçekte kimse bu sütunlara isim vermiyor.

Ama asıl dikkat edilecek şey rakamlar. Şu anda gördüğünüz değerler HENÜZ ÖĞRENİLMİŞ DEĞİL. Bunlar eğitim öncesi, rastgele başlatılmış ağırlıklar.

Yani model bu noktada hiçbir şey bilmiyor. "Jane"in özel isim olduğunu, "September"ın bir zaman ifadesi olduğunu bilmiyor. Tablo dolu ama içi boş.

Şimdi bu tablonun eğitimden sonra ne hâle geldiğine bakalım.

## 41 · Embeddings  ·  2) Token Embeddings

Şimdi dikkat edin: tablo aynı, kelimeler aynı, sütunlar aynı. Değişen tek şey rakamlar.

Bu, eğitimden sonraki hâli.

Başlangıçta bu sayılar rastgeleydi. Model milyarlarca cümle gördü, her seferinde tahmin yaptı, hata yaptı, geri yayılımla ağırlıklarını düzeltti. Ve bu tablodaki her sayı yavaş yavaş yerine oturdu.

Birkaç satıra bakalım. "Jane" satırı özel isim sütununda 0,89 — çok yüksek. "September" satırı zaman sütununda 0,86. "in" satırı ise özel isim sütununda 0,0004 — neredeyse sıfır, çünkü "in" bir edat.

Kimse bu değerleri elle yazmadı. Model, hangi kelimenin hangi bağlamda geçtiğine bakarak bunları kendisi buldu.

İşte "öğrenme" dediğimiz şey somut olarak bu: bir tablodaki sayıların yerine oturması.

## 42 · Embeddings  ·  3) Positional Encodings

Elimizde artık anlamı taşıyan bir matris var. Ama bir şey eksik: sıra.

Transformer bütün token'ları aynı anda işliyor. Bu onun gücü — ama sırayı kaybediyor. Model için "Ali Veli'yi aradı" ile "Veli Ali'yi aradı" şu an aynı şey.

Çözüm: ikinci bir matris. Positional encoding.

Boyutlarına dikkat edin — token embedding matrisiyle tıpatıp aynı: sequence length çarpı embed size. Bu tesadüf değil, birazdan ikisini toplayacağız.

Bu matriste kelime yok. Sadece konum bilgisi var: birinci sıra, ikinci sıra, üçüncü sıra.

## 43 · Embeddings  ·  3) Positional Encodings

Peki bu konum sayıları nereden geliyor?

Orijinal makale bunu sinüs ve kosinüs dalgalarıyla üretiyor. Formül ekranda: çift indisli boyutlar için sinüs, tek indisli boyutlar için kosinüs.

Formülü ezberlemenize gerek yok. Önemli olan fikir şu: her konum için, farklı frekanslarda dalgalardan oluşan benzersiz bir parmak izi üretiliyor.

Neden dalga? Çünkü iki güzel özelliği var. Birincisi, hiçbir konum bir diğeriyle aynı parmak izine sahip olmuyor. İkincisi, aradaki mesafe düzgün davranıyor — model "bu token şundan üç sıra sonra geliyor" ilişkisini yakalayabiliyor.

Ve en pratik faydası: eğitimde hiç görmediği uzunlukta bir cümle geldiğinde de formül çalışmaya devam ediyor.

Not: bugünkü modellerin çoğu bunun daha gelişmiş türevlerini kullanıyor, ama fikir aynı.

## 44 · Embeddings  ·  Toplam

Ve işte birleşme anı.

Token embedding matrisi ile positional encoding matrisi aynı boyutta olduğu için hücre hücre toplanıyorlar.

Sonuç tek bir matris: her satır bir token, her satır hem o token'ın ne olduğunu hem nerede olduğunu taşıyor.

Bu, Transformer'ın kapısından içeri giren şeyin ta kendisi. Buraya kadar yaptığımız her şey — bölme, numaralama, vektöre çevirme, konum ekleme — bu tek matrisi üretmek içindi.

Şimdi asıl olaya geçiyoruz: bu satırlar birbirine nasıl bakıyor?

## 45 · Attention

Attention iki başlıkta inceleyeceğimiz bir mekanizma.

Önce self-attention: bir cümledeki her token'ın, aynı cümledeki diğer bütün token'lara bakması. "Self" demek, kendi içinde bakıyor demek.

Sonra multi-headed attention: bu bakışın tek bir açıdan değil, birden fazla açıdan aynı anda yapılması.

Sağdaki şemada gördüğünüz mavi kutu tam olarak burası. Şimdiye kadar hep altındaki kısımla — embedding ve positional encoding ile — uğraştık. Artık o kutunun içine giriyoruz.

## 46 · Self-Attention

Self-attention bloğuna odaklanalım.

Aşağıdan yukarı: Sources geliyor, embedding'e dönüşüyor, positional encoding ekleniyor ve multi-head attention'a giriyor. Üstünde Add & norm var, ve bütün blok n kez tekrarlanıyor.

Bu şemayı bir kenara koyun; şimdi onu yatırıp içine bakacağız.

## 47 · Self-Attention

Aynı şema, sadece yan çevrildi. Neden? Çünkü artık soldan sağa bir akış olarak düşünmek daha kolay.

Solda girdi var: kaynak metin, embedding, konum bilgisi.
Ortada multi-head attention.
Sağda Add & norm.

Şimdi ortadaki o kutunun içinde ne olduğuna bakalım.

## 48 · Self-Attention  ·  Key, Query, Value

İşte geldik self-attention'ın kalbine.

Soldaki embedding matrisi kelimelerin hem anlamını hem konumunu taşıyor. Ama bu tek başına yetmiyor. Çünkü dil dinamiktir: bir kelimenin anlamı yanındaki kelimelere göre değişir. "Banka" kelimesi yanında "nehir" varken başka bir şeydir, "para" varken başka.

Transformer bu dinamik ilişkiyi çözmek için şunu yapıyor: tek bir embedding matrisini alıp üç ayrı paralel sinir ağı katmanından geçiriyor. Bunların adı W_Q, W_K ve W_V. Üçü de eğitimle öğrenilmiş ağırlık matrisleri. Girdi üçünde de aynı, ağırlıklar farklı — o yüzden çıktılar da farklı.

Elimize üç matris ulaşıyor: Query yani sorgu, Key yani anahtar, Value yani değer.

Sezgisel karşılıkları şöyle:
Query, o token'ın sorduğu soru — "benim için önemli olan ne?"
Key, her token'ın kendini tanıttığı etiket — "ben şuyum."
Value ise o token'ın gerçekten taşıdığı içerik.

Model ne yapıyor? Her Query'yi bütün Key'lerle çarpıp kıyaslıyor. Hangi Key yüksek puan alırsa, o token'ın Value'su o kadar ağırlıkla toplanıyor. Aklınızda YouTube araması olsun: yazdığınız sorgu, videoların etiketleri, videonun kendisi. Bir sonraki sayfada bunu tek tek açacağım, burada tanımda kalalım.

Bir noktanın altını çizin: üç matris de aynı cümleden üretiliyor. Model aynı cümleye üç farklı gözle bakıyor — biri soruyor, biri kendini tanıtıyor, biri içerik taşıyor. "Self" attention denmesinin sebebi tam olarak bu. Dışarıdan gelen bir bilgi yok; cümle kendi kendine bakıyor.

Sağdaki matrislerin boyutlarına dikkat edin: sequence length çarpı head size. Satır sayısı token sayısı kadar — yani her token'ın kendi Query'si, kendi Key'i ve kendi Value'su var. "Head size" ifadesi de bir sonraki konunun habercisi: multi-head attention.

Son bir not, ekranın altında da yazıyor: self-attention girdi olarak illa embedding matrisini almak zorunda değil. Biz şu an encoder'ın ilk katmanına baktığımız için embedding matrisini girdi kabul ediyoruz. Üst katmanlarda girdi, bir alttaki katmanın çıktısı oluyor.

## 49 · Self-Attention  ·  Query sorar, Key tanıtır, Value taşır

Q, K ve V hâlâ soyut duruyor. İki örnekle somutlaştıralım. Soldaki günlük hayattan, sağdaki doğrudan cümlenin içinden. Satırları eşleştirerek okuyacağız.

Soldan başlayalım. YouTube'da video arıyorsunuz. Arama çubuğuna yazdığınız şey — diyelim "sene sonu kedi bakım rehberi" — sizin Query'niz. Yüklenmiş videoların başlıkları ve etiketleri Key: "kedi aşı takvimi", "köpek mamaları", "kedi besleme"… Her video "ben şuyum" diye kendini tanıtıyor. Sistem sorgunuzu bütün etiketlerle kıyaslıyor, en yüksek puanı alanı öne çıkarıyor. Açtığınız videonun asıl içeriği de Value.

Buradaki ayrımı özellikle vurgulayın: etiket ile içerik aynı şey değil. Eşleşmeyi etiket yapar, ama size ulaşan şey içeriktir.

Şimdi aynısını cümlede yapalım: "Çanta valize sığmadı, çünkü o çok büyüktü."

"o" kelimesi bir soru soruyor: ben hangi nesneyi işaret ediyorum? Bu onun Query'si. Cümledeki bütün kelimeler kendi Key'leriyle cevap veriyor. Asıl yarış çanta ile valiz arasında: ikisi de bir nesne, ikisi de büyük olabilir. Model uyum puanlarını hesaplıyor ve çanta öne çıkıyor — çünkü sığmayan taraf çanta; büyük olan da o.

Ekrandaki yüzdeler temsilî, gerçek sayılar değil. Ama fikir tam olarak bu: bu bir seçim değil, bir ağırlıklandırma. Valiz sıfırlanmıyor, sadece daha az pay alıyor.

Ağırlıklar belli olunca çantanın Value'su — yani taşıdığı anlam — büyük ölçüde "o"nun temsiline ekleniyor. Bu sayfanın sonunda "o" artık boş bir zamir değil; içinde çantadan gelen anlam var. Modelin "o"nun neyi kastettiğini anlaması dediğimiz şey bu.

Vaktiniz varsa ikinci bir örnek verin — bu sefer zamir değil, çift anlamlı bir kelime:
"Bankta oturup nehir manzarasını izledik." ve "Banka hesabıma para yatırdım."
Her iki cümlede de kelime aynı embedding'le yola çıkıyor. Birinci cümlede Query'si şunu soruyor: etrafımda oturmak, nehir gibi kelimeler var mı? "Nehir"in Key'i "ben doğa ve manzara terimiyim" diye cevap veriyor; eşleşme olunca Value'dan "oturulan ahşap bank" anlamı çekiliyor. İkinci cümlede "para" ile eşleştiği için "finans kuruluşu" anlamı geliyor. Aynı kelime, aynı başlangıç vektörü — anlamı belirleyen bağlam. Self-attention'ın yaptığı iş tam olarak bu: kelimeleri bağlama göre yeniden yazmak.

Tek cümleyle: Query sorar, Key tanıtır, Value taşır. Şimdi bu üçünün matematiksel olarak nasıl birleştiğine bakalım — softmax, Q çarpı K devriği, sonra Value.

## 50 · Self-Attention  ·  Query ve Key

Elimizde iki matris var: Query ve Key.

İkisi de aynı embedding matrisinden üretildi, ama farklı ağırlıklarla. Yani aynı cümleye iki farklı gözle bakıyorlar.

Boyutlarına dikkat edin: her ikisi de sequence length çarpı head size. Yani her token için bir Query satırı, her token için bir Key satırı var.

Şimdi bu ikisini birleştireceğiz.

## 51 · Self-Attention  ·  Query × Keyᵀ

Soruları cevaplarla eşleştirmek için matris çarpımı kullanıyoruz.

Query matrisini, Key matrisinin devriğiyle çarpıyoruz. Devrik almamızın sebebi tamamen boyut uyumu — çarpımın tutması için.

Bu çarpımın anlamı şu: her Query satırı, her Key satırıyla tek tek karşılaştırılıyor. İki vektör birbirine ne kadar benziyorsa çarpım o kadar büyük çıkıyor.

Yani "bu soru bu cevaba ne kadar uyuyor?" sorusunu tek bir çarpımla, hepsi için aynı anda soruyoruz.

## 52 · Self-Attention  ·  Dot Product

Sonuç kare bir matris: her iki boyutu da cümledeki token sayısına eşit.

Buna dot product matrisi diyoruz. İçindeki her hücre, bir kelimenin başka bir kelimeyle ne kadar ilişkili olduğunu gösteriyor.

Altı kelimelik cümlede altıya altılık bir matris. Yüz kelimelik cümlede yüze yüzlük. Dikkat edin — bu karesel büyüyor. Uzun metinlerin neden pahalı olduğunun cevabı burada.

## 53 · Self-Attention  ·  Scaled Dot Product

Bu matrisi doğrudan kullanmıyoruz, önce iki işlemden geçiriyoruz.

Birincisi ölçekleme: head size'ın kareköküne bölüyoruz. Sebep pratik — boyut büyüdükçe çarpımlar da büyüyor ve softmax'i tıkıyor. Bölme onu dengede tutuyor.

İkincisi softmax: her satırı toplamı 1 olan bir olasılık dağılımına çeviriyoruz.

Sonuç, makalenin scaled dot product dediği matris.

## 54 · Self-Attention  ·  Attention Weights

İşte bu matrise attention weights diyoruz — dikkat ağırlıkları.

Ekrandaki her satır bir kelimenin dikkat dağılımı. Satırdaki sayılar toplandığında 1 ediyor.

Renklere bakın: koyu hücreler güçlü bağı gösteriyor. "in" satırında "jane" hücresi 0,47 — yüksek. Demek ki model "in" kelimesini yorumlarken "jane"e bakmayı öğrenmiş.

Bu tablo, modelin cümleyi nasıl okuduğunun doğrudan fotoğrafı. Bir modelin neye baktığını merak ediyorsanız bakacağınız yer burası.

## 55 · Self-Attention  ·  × Value

Ağırlıklar hazır. Şimdi onları Value matrisiyle çarpıyoruz.

Ağırlık matrisi "kim kime ne kadar baksın" diyor. Value matrisi ise taşınacak asıl içeriği tutuyor.

Çarpım şunu yapıyor: her token için, diğer bütün tokenların içeriğini ağırlıklarına göre topluyor. Yüksek ağırlıklı olanlar sonuca çok, düşük olanlar az katkı veriyor.

## 56 · Self-Attention  ·  Context Vector

Çıktımız context vector.

Boyutu yine sequence length çarpı head size. Yani girdiğimiz gibi bir matris çıktı — ama içerik değişti.

Artık her satır sadece o kelimenin kendi anlamını değil, cümlenin geri kalanından aldığı bağlamı da taşıyor.

Aynı kelime farklı cümlelerde farklı bir context vector alır. "Yüz" kelimesi "yüz kişi" ile "yüzünü yıka"da aynı embedding'le başlar ama buradan farklı çıkar. Transformer'ın gücü tam olarak bu.

## 57 · Self-Attention  ·  Neler yaptık?

Bu kısım biraz yoğundu. Kısaca geri saralım.

## 58 · Self-Attention  ·  Özet  1/3

Önce embedding matrisinden üç matris ürettik: Key, Query ve Value. Üçü de aynı girdiden, ama farklı ağırlıklarla.

## 59 · Self-Attention  ·  Özet  2/3

Sonra Query ile Key'i çarptık, ölçekledik, softmax'ten geçirdik. Scaled dot product elimizde.

## 60 · Self-Attention  ·  Özet  3/3

En son bunu Value ile çarpıp context vector'e ulaştık.

Üç adım: üret, eşleştir, taşı. Self-attention'ın tamamı bu.

## 61 · Peki ya Multi-Head Attention?

Makaleye göz attıysanız multi-head attention diye bir şey gördünüz.

Merak etmeyin, çok farklı bir şey değil. Şimdiye kadar anlattığımın biraz ilerletilmiş hâli.

## 62 · Single Head Attention

Buraya kadar anlattığım şeye single head attention deniyor.

Sebebi basit: Key, Query ve Value matrislerinin hepsi tek katmanlıydı. Tek bir bakış açısı.

## 63 · Multi-Head Attention

Şimdi Key matrisine bakalım. Tek bir tablo. Sequence length çarpı head size.

## 64 · Multi-Head Attention

Multi-head attention'da bu tek tablo yerine, daha küçük ama çok sayıda tablo kullanıyoruz.

Aynı toplam kapasiteyi tek büyük katman yerine birçok küçük katmana dağıtıyoruz.

Neden? Çünkü her katman cümleye başka bir açıdan bakabiliyor. Biri dilbilgisel ilişkiyi yakalarken bir diğeri anlamsal ilişkiyi yakalayabiliyor.

## 65 · Multi-Head Attention

Aynı şeyi üçüne birden yapıyoruz: Keys, Queries ve Values artık çok katmanlı.

İşlem sırası hiç değişmedi — çarp, ölçekle, softmax, Value ile çarp. Sadece bunu tek seferde değil, her başlık için ayrı ayrı yapıyoruz.

Sonuçta çok katmanlı bir context vector çıkıyor.

## 66 · Multi-Head Attention  ·  Concat

Ama çok katmanlı bir yapıyı doğrudan bir sinir ağına veremeyiz.

O yüzden önce katmanları birleştiriyoruz — concat. Sonra tek bir doğrusal projeksiyondan geçiriyoruz.

Ve işte bu, multi-head attention bloğunun nihai çıktısı.

## 67 · Hangi Mimariler Var?  ·  CNN

Soldan sağa oku. Görüntü ham piksel olarak giriyor. Küçük bir filtre — kernel — görüntünün üzerinde gezerek kenarları, sonra dokuları, sonra parçaları yakalıyor. Pooling her adımda boyutu küçültüyor, önemli olanı bırakıyor.
Flatten katmanında bu haritalar tek bir uzun vektöre diziliyor ve işte oradan sonrası bildiğimiz ANN: tam bağlantılı katmanlar. Softmax de olasılığa çeviriyor — bu görüntü %70 zebra.
Vurgulanacak tek şey: klasik yöntemde 'zebra çizgilidir' diye feature'ı biz yazardık; burada filtreleri model kendi öğreniyor.

## 68 · Multi-Head Attention  ·  Şemadaki yeri

Şimdi bu bloğun büyük şemada nerede durduğunu hatırlayalım.

Şu yatık duran parça, baştan beri anlattığımız kısım: embedding, positional encoding ve multi-head attention.

Şimdi onu düzeltip yerine oturtalım.

## 69 · Multi-Head Attention  ·  Şemadaki yeri

(not yok)

## 70 · Feed-Forward Networks

Üstüne inen parça yeni: Positionwise FFN, yani ileri beslemeli ağ.

Bu ikisi birlikte encoder bloğunu oluşturuyor. Alt yarı bağlamı kuruyor, üst yarı onu işliyor.

## 71 · Feed-Forward Networks

Feed-forward network aslında çok sade bir yapı: iki sinir ağı ve aralarında bir ReLU aktivasyonu.

Girdi olarak multi-head attention'ın çıktısını alıyor.

Buradaki önemli detay şu: girdi ve çıktı boyutu aynı, ama arada boyut şişiyor. Makaledeki örnekte birinci ağ 512'den 2048'e çıkarıyor, ikincisi 2048'den 512'ye indiriyor.

Neden? Attention'da öğrenilen özelliklerin daha geniş bir alana yayılıp daha ayrıntılı işlenmesi için. Bloğun dışarıya verdiği boyut ise sabit kalıyor — böylece bloklar üst üste dizilebiliyor.

## 72 · Encoder

Encoder bloğunun tamamı bu.

Multi-Head Attention, Add & Norm, Feed-Forward, Add & Norm.

Add & Norm'dan bahsetmemiştik. "Add" artık bağlantı: katmanın girdisini çıktısına geri ekliyor, böylece derin ağlarda bilgi kaybolmuyor. "Norm" ise layer normalization; değerleri dengede tutup eğitimi kolaylaştırıyor. Ayrıntısına girmiyoruz ama ikisi de kaybolan gradyan sorununa karşı çözüm.

## 73 · Encoder

Aynı bloğu bir de yatay çizilmiş hâliyle görelim — soldan sağa akış.

Kaynak metin giriyor, embedding ve konum ekleniyor, attention ve FFN'den geçiyor, encoder çıktısı oluşuyor.

## 74 · Encoder

(not yok)

## 75 · Encoder

Encoder'ın işi bitti. Görevi neydi? Verilen metinden anlam çıkarmak ve onun sayısal bir temsilini üretmek.

Ama biz çeviri yapacağız. Yani bir de üreten tarafa ihtiyacımız var.

## 76 · Encoder ve Decoder

İşte decoder. Encoder anlıyor, decoder üretiyor.

Örneğimizde encoder İngilizce cümleyi okuyor, decoder onun Fransızca karşılığını kelime kelime yazıyor.

İkisinin arasındaki o ok kritik — birazdan ona geleceğiz.

## 77 · Decoder

Decoder'a yakından bakalım. Encoder'a çok benziyor ama iki noktada ayrılıyor.

Birincisi: en altta "masked" multi-head attention var.
İkincisi: ortada ikinci bir attention katmanı var, ve o encoder'a bağlanıyor.

Şimdi bu ikisini sırayla açalım.

## 78 · Cross Attention

Önce ortadaki katman: cross attention.

## 79 · Normal Attention

Farkı görmek için normal attention'ı hatırlayalım.

## 80 · Normal Attention

Aynı akış, sadeleştirilmiş hâli.

## 81 · Normal Attention

Normal bir attention bloğunda Key, Query ve Value'nun üçü de aynı yerden gelir: bir önceki katmandan.

Aslında adındaki "self" tam olarak bunu anlatıyor — kendi içine bakıyor.

## 82 · Cross Attention

Cross attention'da ise durum değişiyor.

Query hâlâ decoder'ın bir önceki katmanından geliyor. Ama Key ve Value encoder'dan geliyor.

Anlamı şu: decoder üretirken "kaynak metinde ne vardı?" diye soruyor. Encoder'ın öğrendiği bilgiyi kullanabiliyor.

Encoder ile decoder'ı birbirine bağlayan köprü tam olarak burası.

## 83 · Masked Attention

İkinci fark: masking. Ve bu sadece decoder'da var.

## 84 · Masked Attention

Diyagramda "masked multi-head attention" yazan yer burası.

## 85 · Masked Attention

Boru hattı aynı. Tek fark, softmax'ten önce bir maskeleme adımı eklenmesi.

## 86 · Unmasked Attention

Maskesiz bir attention weights matrisi böyle görünüyor.

Her satır, bir kelimenin hem kendinden önceki hem sonraki kelimelerle ilişkisini gösteriyor.

Encoder'da bu sorun değil — cümle zaten tek seferde, bütün olarak veriliyor.

## 87 · Unmasked vs Masked

Ama decoder farklı çalışıyor. Sonucu parça parça üretiyor ve ürettiği her parçayı bir sonrakinin girdisi yapıyor.

Şimdi düşünün: model ikinci kelimeyi tahmin ederken üçüncü kelimeye bakabilseydi ne olurdu? Cevabı kopya çekmiş olurdu. Zaten o kelime henüz üretilmedi bile.

Bu yüzden her kelimenin yalnızca kendinden öncekilere bakmasını sağlıyoruz.

Sağdaki matrise bakın: üst üçgen tamamen sıfır. Gelecek görünmüyor. İşte maskeleme bu.

## 88 · Transformer

Artık iki parçayı da tanıyoruz. Bir araya getirelim.

Solda encoder: İngilizce cümle tokenize ediliyor, embedding'e dönüşüyor, encoder'dan geçiyor.
Sağda decoder: aynı hazırlık, ama üretilen metin için.

## 89 · Transformer

Decoder'ın çıkışında iki katman daha var.

Önce sözlük boyutunda tek katmanlı bir doğrusal ağ. Sonra softmax.

Sonuç: sözlükteki her kelime için bir olasılık. Model bu dağılıma bakarak bir sonraki kelimeyi seçiyor.

## 90 · Transformer  ·  Üretim

Şimdi eğitilmiş bir Transformer'ın nasıl üretim yaptığını izleyelim.

İngilizce cümlemizi encoder'a veriyoruz. Encoder onu anlamlı bir temsile çeviriyor ve decoder'a aktarıyor.

Decoder'a ise sadece bir şey veriyoruz: başlangıç token'ı, [BOS].

Ve model ilk kelimeyi üretiyor: "jane".

## 91 · Transformer  ·  Üretim

(not yok)

## 92 · Transformer  ·  Üretim

(not yok)

## 93 · Transformer  ·  Üretim

(not yok)

## 94 · Transformer  ·  Üretim

Ama cümle bitmedi. Peki ikinci kelimeyi nasıl üretecek?

Ürettiği kelimeyi geri alıp girdiye ekliyoruz. Artık decoder'ın girdisi [BOS] ve "jane".

Bu sefer "visite" çıkıyor. Sonra aynı şey tekrar: girdi bir token daha uzuyor.

Her adımda cümle bir kelime büyüyor ve model bir sonrakini tahmin ediyor. Bugün ChatGPT'de kelimelerin tek tek akmasını görüyorsunuz ya — sebebi tam olarak bu.

## 95 · Transformer  ·  Üretim

(not yok)

## 96 · Transformer  ·  Üretim

(not yok)

## 97 · Transformer  ·  Üretim

(not yok)

## 98 · Transformer  ·  Üretim

Üçüncü kelime de geldi: l'Afrique. Döngü aynı şekilde devam ediyor.

## 99 · Transformer  ·  Üretim

Ve sonunda model [EOS] üretiyor — end of sentence.

Bu, "cümlem bitti" demek. Döngü burada duruyor.

İngilizceden Fransızcaya çeviri tamamlandı. Baştan beri anlattığımız her şey — tokenization, embedding, positional encoding, attention, encoder, decoder — bu tek çıktıyı üretmek içindi.

## 100 · Transformer'dan Büyük Dil Modeline

Elimizde artık bir Transformer var. Peki bu, kullandığımız asistanlara nasıl dönüşüyor?

Cevap zaten ismin içinde: GPT — Generative Pre-trained Transformer. Üretken, ön eğitimli Transformer. Şimdi bu "ön eğitimli" kısmının ne demek olduğuna bakalım.

Ekrandaki üçlü, bu dersin belki de en can alıcı özeti. Soldan sağa okuyalım.

Birincisi ön eğitim, pre-training. İnternetteki trilyonlarca ham veriyle yapılıyor. Model burada tek bir şey öğreniyor: sonraki kelimeyi tahmin etmek. Bunu yaparken dili öğreniyor — grameri, kalıpları, dünyaya dair olguları. Ama dikkat: bu aşamanın sonunda model bir soruya nasıl cevap vereceğini bilmiyor. Sadece metni devam ettirmeyi biliyor. Ona soru sorsanız, size cevap vermek yerine benzer sorular yazmaya devam edebilir.

İkincisi ince ayar, fine-tuning. Burada modeli soru-cevap çiftleriyle eğitiyoruz. Model işi öğreniyor: talimat takip etmeyi, kendisine sorulan şeye cevap vermeyi. Asistana dönüşme tam olarak burada oluyor.

Üçüncüsü RLHF — insan geri bildirimiyle pekiştirmeli öğrenme. İnsanlar modelin cevaplarını karşılaştırıp puanlıyor, model bu tercihlere göre ayarlanıyor. Burada öğrendiği şey içerik değil, üslup ve sınır: nasıl kibar olunur, nasıl güvenli kalınır, neyi söylememek gerekir.

Slaytın altındaki cümleyi tekrar edin, akılda kalan cümle bu olsun:
Ön eğitim dili öğretir, ince ayar işi öğretir, RLHF ise nasıl konuşacağını öğretir.

Ölçek farkına da dikkat çekin: ön eğitim devasa ve pahalı, diğer iki aşama yanında çok küçük kalıyor. Yani modelin bildiği neredeyse her şey ilk aşamadan geliyor; son iki aşama o bilgiyi kullanılabilir hâle getiriyor.

## 101 · Taming The Monster

Aynı süreci bir metaforla toparlayalım: bir canavarı evcilleştirme hikâyesi.

Soldaki kırmızı alan, ön eğitim. Burada elimizde kontrolsüz, vahşi bir canavar var. İnternetteki her şeyi okumuş — iyisini, kötüsünü, yanlışını, tehlikelisini. Tek bildiği şey önüne konan metni tamamlamak. Muazzam bilgili ama güvenli değil. Bu hâliyle kimsenin eline veremezsiniz.

Ortadaki sarı alan, ince ayar. Canavarı insani diyaloğa alıştırıyoruz. Kaliteli diyalog verileriyle — soru-cevap çiftleri, StackOverflow, Reddit gibi kaynaklardan derlenmiş konuşmalarla — eğitiyoruz. Artık anlamlı cümle kuran, kendisinden isteneni yapan bir forma bürünüyor.

Sağdaki yeşil alan, RLHF. Son aşama. İnsan tercihleri ve puanlarıyla canavarı tamamen evcilleştiriyoruz. Çıkan şey artık zararsız, güvenli ve gerçekten işe yarar bir asistan. Metinle, görselle, sesle, kodla, hepsi bir aradayken çoklu-formlu verilerle çalışabilen bir model.

Buradan çıkarılacak asıl fikir şu: bugün kullandığımız asistanların "kişiliği" doğuştan gelmiyor. Ham model çok daha ham, çok daha kaba bir şey. Aradaki fark tamamen bu iki evcilleştirme aşamasının eseri.

Ve bu, dersin başındaki Harari tartışmasına da bağlanıyor: canavarı kimin, hangi değerlerle evcilleştirdiği — modelin ne bildiği kadar önemli.
