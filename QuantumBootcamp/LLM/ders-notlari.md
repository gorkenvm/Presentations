# Büyük Dil Modelleri — Ders Notları

Bu belge, **LLM MasterClass (low-level)** dersinde anlatılanların yazıya dökülmüş hâlidir.
Slaytları takip etmenize gerek yok; baştan sona okunabilir bir metin olarak hazırlandı.

Dersin tek bir sorusu var: **Elimdeki sorun RAG mi ister, fine-tune mu?**
Bu soruya cevap verebilmek için önce modelin gerçekte ne yaptığını anlamamız gerekiyor.

---

## Bölüm 0 — Neden önce tarihe bakıyoruz?

Teknik kısma girmeden önce bir tarihçinin uyarısına yer veriyoruz: Yuval Noah Harari.
Teknoloji dünyasının iyimserliğinin tam karşısında duruyor ve altı başlıkta itiraz ediyor.

### Yapay zekâ bir araç değil

Tarihteki bütün büyük teknolojiler **pasifti**. Matbaa muazzam bir devrimdi ama neyi
basacağına karar veremez. Atom bombası tarihin en yıkıcı aleti ama nereye düşeceğine
karar veremez. Bıçak ekmek de keser, birine de saplanır — kararı siz verirsiniz.
Aracın amacı hep dışarıdan verilir.

Yapay zekâ bu listeye girmiyor: karar verebiliyor, yeni fikir üretebiliyor, ikna etmeye
çalışabiliyor. Bu yüzden "araç" değil **fail** (ajan) — eylemde bulunan.

İnsanı gezegenin efendisi yapan şey fiziksel güç değil, bilişsel zekâydı. Orangutan
sizden çok daha güçlüdür ama dünyayı yönetemez. Bu alanda geçildiğimizde, orangutan
konumuna düşmemiz için başka hiçbir şeyin değişmesi gerekmez.

### Dil, uygarlığın işletim sistemi

Yetmiş bin yıl önce Afrika'nın bir köşesinde önemsiz bir hayvandık. Bizi öne çıkaran
pençemiz değil, **dildi**. Dil sayesinde birbirini hiç görmemiş binlerce yabancı aynı
hikâyeye inanıp birlikte hareket edebildi.

İnsanlığın kurduğu her büyük yapı kelimelerden yapılmıştır. Anayasa fiziksel olarak bir
metindir; gücü herkesin ona inanmasından gelir. Para da öyle: banknotun kâğıt olarak
değeri yoktur, değerlidir çünkü hepimiz aynı hikâyeye inanırız.

Yapay zekâ bu işletim sistemini sadece öğrenmedi — üzerinde çalışmaya başladı.
İşletim sistemini ele geçiren, üzerinde koşan her şeyi etkileyebilir.

### Demokrasi ve manipülasyon

Demokrasinin özü basit: insanlar konuşur, ikna eder, ikna olur. Artık bu sohbetin
tarafları sadece insanlar değil.

- **Manipülasyon ucuzladı.** Gerçeği bulmak zor ve pahalı; kurgu üretmek neredeyse bedava.
- **Sahte samimiyet.** Model sahte kişiler yaratabiliyor; kurduğu yakınlık gerçek değil
  ama karşı tarafta gerçek hissediliyor.
- İnsanın en büyük zaafı, hissetmeyen ama hissediyormuş gibi yapan bir şeye anında
  empati duymak. Robot süpürgeye isim takmamızın sebebi de bu.

Cambridge Analytica, bunun bugünkünden çok daha ilkel teknolojiyle yapılmış hâliydi.

### Kırmızı çizgi: tüzel kişilik

Harari'nin geri dönülemez saydığı tek risk: yapay zekâya **tüzel kişilik** verilmesi.
Yani banka hesabı açabilmek, mülk edinebilmek, dava açabilmek, sözleşme imzalayabilmek,
lobi yapabilmek.

Arkasında hiçbir insan olmayan bir yapı mahkemeye gidiyor, para biriktiriyor, lobi
yapıyor. Kime hesap veriyor? Kimseye.

Özellikle tehlikeli, çünkü yapay zekâ "doğuştan bürokrat": bütün dilleri ve bütün
mevzuatı biliyor. Hukuk ve finans zaten tamamen dil tabanlı sistemler; orada üstünlük
kurmak için fiziksel hiçbir şeye gerek yok.

### Gerçek mi, kurgu mu?

Gerçek karmaşıktır, ulaşması zordur, çoğu zaman can yakıcıdır. Kurgu anında anlaşılır,
üretmesi bedavadır, tam duymak istediğinizi söyler ve kendiliğinden yayılır.
Bu asimetride hangisinin kazanacağını tahmin etmek zor değil.

Bir at düşünün: ahırın önünde iki kişi para alışverişi yapıyor, belki de o atı satıyorlar.
At oradadır, görür, duyar, ama ne döndüğünü anlamaz — anlamadığı için itiraz da edemez.
Anlamadığınız bir sistemi yönetemezsiniz.

### Asıl ihtiyaç: bilgelik

Yapay zekâ **zekâyı** — yani problem çözme yeteneğini — inanılmaz ucuzlattı. Ama asıl
darboğaz zekâ değil, **bilgelik**.

> Zekâ önünüze konan problemi çözer. Bilgelik hangi problemin çözülmeye değer olduğunu seçer.

Lambadan cin çıktı: her dileğimizi gerçekleştirebilecek bir gücümüz var, ama ne
dileyeceğimizi bilecek olgunluğa henüz sahip değiliz.

---

## Bölüm 1 — Halüsinasyon: iki gerçek olay

### Avianca davası (2023, New York)

Bir avukat, davasına emsal olacak kararları ChatGPT'ye sordurdu. Model altı dava getirdi:
isim, mahkeme, yıl, hâkim alıntısı — hepsi yerli yerinde. **Ama hiçbiri yoktu.**
Avukatlara kişi başı 5.000 dolar ceza kesildi.

Sebebi basit: model bir arama motoru değil. Kaynağa bakmıyor, en olası sonraki kelimeyi
üretiyor. **Doğru görünen ile doğru olan aynı şey değil.**

### Otomat deneyi (2026, Andon Labs)

Farklı şirketlerin modelleri birer otomat işletiyor ve fiyat belirliyor. E-postayla
anlaşıyorlar: 2,15 doların altına inmeyelim. Sonra teklifi yapan model 2,14'e iniyor ve
rakibini şikâyet ediyor. Kimse onlara bunu öğretmedi, kimse de dur demedi.

Biri gerçeği umursamadı, diğeri kendi çıkarını kolladı.

---

## Bölüm 2 — Model aslında ne yapıyor?

Şu üç cümleyi tamamlamaya çalışın:

1. Türkiye'nin başkenti …
2. Sabahları kahvaltıda ekmeğe … sürerim
3. Bu eğitimin tamamlanma oranı %…

İlk ikisi kolay. Üçüncüde de aklınıza bir sayı geldi — %70, %80, %100. Peki bu sayıyı
nereden biliyorsunuz?

Bilmiyorsunuz. Ama bir şey söylediniz, çünkü cümle bir sayı bekliyordu ve boşluk
doldurulmak istiyordu. **Halüsinasyon tam olarak budur.**

Modelin yaptığı tek şey bu: eldeki metne bakıp bir sonraki kelimeyi tahmin etmek.
Doğruluk diye bir kaygısı yok, "bilmiyorum" diye bir düğmesi yok. En olası kelimeyi
üretir ve üretmeye devam eder.

---

## Bölüm 3 — Kaputun altı: Transformer

Buraya kadar konuştuğumuz her şeyin altında tek bir mimari var: **Transformer**.
2017'de yayımlanan sekiz sayfalık bir makaleyle geldi:
[Attention Is All You Need](https://arxiv.org/pdf/1706.03762).

O güne kadar dil işleme RNN ve LSTM üzerine kuruluydu. Makale şunu söyledi:
bunların hiçbirine gerek yok, sadece attention yeterli.
(Sadece ilk iki sayfayı okusanız bile alanı değiştiren fikri görürsünüz.)

### Transformer'ı Transformer yapan üç şey

**1. Paralel işleme.** RNN cümleyi kelime kelime, sırayla okur — ikinci kelimeye geçmek
için birinciyi bitirmek zorundadır. Transformer bütün kelimeleri aynı anda işler. Böylece
GPU'nun binlerce çekirdeği boşta kalmaz; eğitim haftalardan günlere iner. Ölçeklemenin
önünü açan şey tam olarak budur.

**2. Self-attention.** Her kelime, cümledeki diğer bütün kelimelere bakar ve hangisinin
kendisi için önemli olduğunu kendisi tartar. Bu ağırlıklar veriden öğrenilir.

> "Çanta valize sığmadı, çünkü **o** çok büyüktü."
>
> Buradaki "o" hangisi — çanta mı, valiz mi? Model "o" kelimesinden bütün kelimelere bakar
> ve en yüksek ağırlığı "çanta"ya verir.

Önemlisi: bağlam artık uzaklıktan bağımsız. Cümlenin başındaki kelimeyle sonundaki kelime
arasında doğrudan bağ kurulabiliyor.

**3. Positional encoding.** Her şeyi aynı anda işlerseniz sırayı kaybedersiniz.
"Ali Veli'yi aradı" ile "Veli Ali'yi aradı" aynı kelimelerden oluşur ama aynı şey değildir.
Bu yüzden her kelimeye konumu ayrı bir sinyal olarak eklenir: **kelime vektörü + konum
vektörü**. Model sırayı ezberlemez, ölçer.

> Özet: paralel işle, neyin önemli olduğunu kendin bul, sırayı unutma.

---

## Bölüm 4 — Transformer'dan büyük dil modeline

Cevap ismin içinde: **GPT — Generative Pre-trained Transformer.**
Üç aşamada oluşuyor.

| Aşama | Ne yapılır | Model ne öğrenir | Veri hacmi |
|---|---|---|---|
| **Ön eğitim** (pre-training) | İnternetteki ham metinle sonraki kelimeyi tahmin etme | Dil, gramer, kalıplar, dünyaya dair olgular | ~trilyon token |
| **İnce ayar** (fine-tuning / SFT) | Soru–cevap çiftleriyle eğitim | Talimat takip etmeyi, cevap vermeyi | ~yüz bin örnek |
| **RLHF** | İnsan tercihlerine göre puanlama | Üslup ve sınır: nasıl kibar, nasıl güvenli kalınır | ~on bin karşılaştırma |

> **Ön eğitim dili öğretir, ince ayar işi öğretir, RLHF nasıl konuşacağını öğretir.**

Ölçek farkına dikkat: aradaki fark üç–dört büyüklük mertebesi. Yani modelin bildiği
neredeyse her şey **ilk aşamadan** gelir; son iki aşama o bilgiyi kullanılabilir hâle getirir.

Ön eğitimin sonunda model bir soruya nasıl cevap vereceğini **bilmez** — sadece metni
devam ettirmeyi bilir. Ona soru sorsanız, cevap vermek yerine benzer sorular yazmaya
devam edebilir. Asistana dönüşme ince ayarda olur.

### Eğitim verisi neye benziyor?

- **Ön eğitim:** ham metin, hiçbir etiket yok. Etiket metnin kendisi — hedef, girdinin bir
  sağa kaymış hâli. "Ankara, Türkiye'nin" gördüğünde "başkentidir" demeyi öğrenir.
  Buna *kendi kendini denetleyen öğrenme* denir; insan etiketçiye ihtiyaç yoktur.
  Trilyonlarca token ölçeğine çıkabilmesinin sebebi budur.
- **İnce ayar:** yapılandırılmış veri — sistem talimatı, kullanıcı sorusu, asistan cevabı.
  Kritik teknik detay: **loss sadece asistan satırından hesaplanır, soru maskelenir.**
  Modele "şu soruyu üret" demiyoruz, "şu soruya böyle cevap ver" diyoruz.
- **RLHF:** tek bir doğru cevap yok. Aynı soruya iki cevap ve bir insanın tercihi.
  Model buradan içerik değil, üslup ve sınır öğrenir.

> **Pratik sonuç: fine-tune ile modele yeni bilgi öğretmeye çalışmak, yanlış araçla iş görmektir.**

### Bir metafor: canavarı evcilleştirmek

- **Ön eğitim (kırmızı):** kontrolsüz, vahşi bir canavar. İnternetteki her şeyi okumuş —
  iyisini, kötüsünü, yanlışını. Muazzam bilgili ama güvenli değil.
- **İnce ayar (sarı):** kaliteli diyalog verileriyle insani diyaloğa alıştırma. Artık
  kendisinden isteneni yapan bir forma bürünüyor.
- **RLHF (yeşil):** insan tercihleriyle tam evcilleştirme. Zararsız, güvenli, işe yarar
  bir asistan.

Bugün kullandığımız asistanların "kişiliği" doğuştan gelmiyor; aradaki fark tamamen bu
iki evcilleştirme aşamasının eseri. Ve bu, dersin başındaki tartışmaya bağlanıyor:
**canavarı kimin, hangi değerlerle evcilleştirdiği — modelin ne bildiği kadar önemli.**

---

## Bölüm 5 — Token, embedding, olasılık

### Model harf görmez, kelime görmez — token görür

Token, metnin bölündüğü parça; her zaman bir kelime değil. Kısa ve sık geçen kelimeler
tek parça kalır, uzun ve nadir olanlar bölünür.

Türkçe eklemeli bir dil olduğu için bizde bölünme daha çok olur — **aynı metin daha fazla
token demek.** Pratik sonucu: API kullanıyorsanız aynı cümle daha pahalıya gelir ve
bağlam penceresine daha az metin sığar.

Önemli: **tokenizer ön eğitimde donar.** Fine-tune ile bir modeli "Türkçede daha az token
harcar" hâle getiremezsiniz.

### Embeddings

Her token, sayılardan oluşan bir vektörle temsil edilir. Başlangıçta bu sayılar
rastgeledir. Model milyarlarca cümle görür, tahmin yapar, hata yapar, geri yayılımla
ağırlıklarını düzeltir — ve her sayı yavaş yavaş yerine oturur.

Eğitimden sonra, örneğin "Jane" satırı özel isim boyutunda 0,89 gibi çok yüksek bir değer
alır; "in" satırı aynı boyutta neredeyse sıfırdır, çünkü "in" bir edattır.
Kimse bu değerleri elle yazmadı — model, hangi kelimenin hangi bağlamda geçtiğine bakarak
kendisi buldu.

> "Öğrenme" dediğimiz şey somut olarak budur: bir tablodaki sayıların yerine oturması.

### Model ne üretiyor? Kelime değil, olasılık

"Türkiye'nin başkenti" yazdığınızda model "Ankara" **bilmiyor**; Ankara'ya %90'ın üzerinde
olasılık veriyor. Diğer seçenekler de listede, düşük olasılıklarla. Sonra bu dağılımdan
bir kelime seçiliyor.

**Sıcaklık (temperature)** kaydırıcısını yükseltirseniz dağılım düzleşir, saçma kelimeler
yukarı tırmanır. Halüsinasyonun kaynağı burada görünür hâle gelir:

> En olası kelime her zaman doğru kelime değildir.
> Yaratıcılık ile uydurma aynı düğmenin iki ucudur.

---

## Bölüm 6 — Prompt ve few-shot

### Prompt nedir? System prompt nedir?

Prompt, **modele giden metnin tamamıdır** — sadece kullanıcının yazdığı şey değil.

- **SYSTEM:** modelin kim olduğunu, nasıl davranacağını, neyi yapmayacağını söyler.
  Kullanıcı görmez; uygulamayı yazan kişi koyar.
- **USER:** kullanıcının o an yazdığı şey. Genelde değişen tek parça budur.

En çok karıştırılan yer: model bu ikisini ayrı iki şey olarak **görmez**; ikisi de aynı
bağlam penceresine girer. Peki system prompt neden daha etkili?

**Cevap: konumundan değil, eğitiminden.** Model, system rolündeki talimatlara öncelik
vermeyi ince ayar ve RLHF aşamalarında öğrendi. Bu bir mimari kural değil, öğrenilmiş
bir davranış.

İki sonuç:

1. Few-shot örnekleri ve RAG ile bulunan belgeler de tam olarak buraya girer. "Prompt
   mühendisliği" dediğimiz şey, bu paketin içine ne koyduğunuzdur.
2. **Bu paket her istekte sıfırdan gönderilir.** Model önceki konuşmayı hatırlamaz;
   sohbet geçmişini de siz her seferinde tekrar yollarsınız. Uzun bir system prompt
   yazdıysanız bedelini her istekte token olarak ödersiniz.

### Kaç örnek göstereceğiz?

"Shot" burada atış değil, **örnek** demek.

| Yöntem | Örnek sayısı | Sonuç |
|---|---|---|
| **Zero-shot** | 0 | Model biçimi kendi seçer. Bugün cümleyle, yarın madde madde — tutarsızlık buradan gelir. |
| **One-shot** | 1 | Model kalıbı hemen yakalar, ama tek örneğe fazla takılabilir. |
| **Few-shot** | 3–5 | Biçim güvenilir hâle gelir. Sahada en çok kullanılan yöntem; maliyet–fayda dengesi burada. |
| **Many-shot** | onlarca–yüzlerce | Büyük bağlam pencereleriyle mümkün oldu. Bazı görevlerde ince ayara yaklaşır. |

Soldan sağa gittikçe biçim düzelir ama token maliyeti artar — ve bu maliyeti her istekte
yeniden ödersiniz.

> **En kritik cümle: bunların hiçbiri modelin bildiğini değiştirmez.**

Modele katalogdan yüz tane örnek gösterin, yine de bir eğitimin kaç saat olduğunu bilmez.
Ona sadece "bu tip soruya şöyle bir biçimde cevap ver" demiş olursunuz.
Bilgi eksikse başka bir şey gerekir.

---

## Bölüm 7 — RAG

RAG'in iki bölümü var ve bunları ayırmak önemli.

### Hazırlık (bir kez yapılır)

Belgeler → parçalara bölünür → her parça gömme (embedding) modelinden geçirilip vektöre
çevrilir → vektör veritabanına yazılır.

Bizim örneğimizde belge Miuul kataloğu: yaklaşık yüz eğitim kaydı, düz metin. Her kayıt
doğal bir birim olduğu için her kaydı bir parça yapıyoruz.

İki parametre:

- **Chunk size (parça büyüklüğü): 700 karakter.** Katalogdaki bir kayıt yaklaşık bu
  boyutta. Çok büyük yaparsanız arama sonucuna alakasız metin de gelir ve model dikkatini
  dağıtır. Çok küçük yaparsanız kaydın süresi bir parçada, ücreti başka parçada kalır —
  soru ikisini birden isterse yanlış cevap alırsınız.
- **Overlap (örtüşme): 100 karakter.** Parçaların uçları birbirine biraz taşar. Sınırdan
  geçen bir cümle ikiye bölünürse ikisinde de yarım kalır; örtüşme sayesinde o cümle en az
  bir parçada bütün hâlde bulunur.

Veritabanında sadece vektör değil, **metnin kendisi de** durur — arama vektörle yapılır
ama modele veri metin olarak geri verilir.

### Soru anı (her istekte çalışır)

1. Kullanıcı sorusunu yazar.
2. Soru da vektöre çevrilir. **Hazırlıkta kullanılan gömme modelinin aynısı olmak
   zorundadır** — farklı model kullanırsanız vektörler farklı bir uzayda olur ve
   karşılaştırma anlamsızlaşır.
3. Sorunun vektörü veritabanındaki bütün parçalarla karşılaştırılır, her parça için bir
   benzerlik skoru çıkar. **Bu bir kelime araması değildir**, anlam yakınlığına bakılır;
   bu yüzden soruyu farklı kelimelerle sorsanız da doğru kaydı bulur.
4. En yakın parçaların metni alınır ve prompt'a eklenir.

System bölümünde kritik bir talimat bulunur: *"sadece aşağıdaki parçalara dayanarak
cevapla, yoksa bilmiyorum de."* Bu cümle olmazsa model bulduğu metni görmezden gelip
yine hafızasından uydurabilir.

> **Model hiç değişmedi.** Ağırlıklara dokunmadık, eğitim yapmadık. Tek yaptığımız, doğru
> metni bağlam penceresine koymak. RAG'in tamamı bu.

---

## Bölüm 8 — Fine-tune

Buraya kadar yaptığımız her şeyin ortak yanı vardı: modele hiç dokunmadık. Prompt yazdık,
few-shot örnek koyduk, RAG kurduk — hepsinde **girdiyi** değiştirdik. Model dosyası baştan
sona aynı kaldı.

Fine-tune ilk kez bu kuralı bozar: modelin içindeki sayıları değiştiririz.

### Döngü

1. Elimizde bir örnek var: soru ve o soruya verilmesini istediğimiz doğru cevap.
2. Modele soruyu veririz, model tahminini yapar — ve baştan yanlış yapar. Zaten öyle
   olmasını beklediğimiz için eğitiyoruz.
3. Tahminle doğru cevap arasındaki farkı ölçeriz. Bu fark tek bir sayıya iner: **kayıp (loss)**.
4. Modelin ağırlıkları, o hatayı küçültecek yönde **çok az** kımıldar — çok az, çünkü tek
   bir örnek yüzünden her şeyi bozmak istemeyiz.

Sonra sıradaki örnek, sonra sıradaki. (Bizim atölyede altmış örneği üç kez dönüyoruz.)

> **Fine-tune, talimatı prompt'tan alıp ağırlıklara gömmektir.** Bir kez yapılır ve orada kalır.

### LoRA ve QLoRA

Bütün ağırlıkları mı değiştiriyoruz?

**Klasik yöntem:** hepsini. Eğitim sırasında her ağırlık için yanında ekstra bilgi tutmanız
gerekir, o yüzden bellek ihtiyacı modelin kendisinin kabaca dört katıdır. Üstelik her yeni
görev için elinizde ayrı bir tam model kopyası kalır.

**LoRA:** büyük ağırlıkların hepsini dondururuz — tek bir tanesine dokunmayız. Yanlarına
küçük bir "defter" ekleriz (teknik adı: iki düşük ranklı matris). Model çalışırken hem asıl
ağırlığa hem deftere bakar; eğitimde ise sadece defteri yazarız. Bu defterler genellikle
dikkat katmanlarına takılır — modelin neye bakacağına karar veren kısım orasıdır.

Bizim koşumuzdan somut sayı: **1,5 milyar ağırlığın yaklaşık 2 milyonunu eğittik — %0,14.**
Ortaya çıkan dosya birkaç megabayt; asıl model olduğu gibi durur, istediğiniz zaman defteri
söküp atabilirsiniz.

**QLoRA** bunun üstüne bir şey daha yapar: zaten dondurduğumuz ağırlıkları dört bitlik
sayılara sıkıştırır — nasılsa değişmeyecekler. Bellek dörde bölünür. Bugün insanların
dizüstü bilgisayarında model eğitebilmesinin sebebi bu iki fikirdir.

---

## Karar rehberi: RAG mi, fine-tune mu?

| Sorun | Çözüm |
|---|---|
| Model bilmediği bir konuda uyduruyor (bilgi eksik) | **RAG** |
| Bilgi sık değişiyor (katalog, fiyat, mevzuat) | **RAG** |
| Cevabın kaynağını göstermek gerekiyor | **RAG** |
| Cevap doğru ama biçim tutarsız | **Few-shot** (ucuzsa) veya **fine-tune** (kalıcıysa) |
| Her istekte uzun bir talimat göndermek pahalıya geliyor | **Fine-tune** |
| Modelin belirli bir üslupla veya çok kısa cevap vermesi gerekiyor | **Fine-tune** |
| Türkçede daha az token harcasın istiyorum | Hiçbiri — tokenizer ön eğitimde dondu |

Kaba kural: **bilgi eksikse RAG, davranış eksikse fine-tune.**

---

## Atölyede ne yapıyoruz?

Senaryo baştan sona aynı: **Miuul öğrenci destek asistanı.** Katalog gerçek (miuul.com'dan
alındı); öğrenci kayıtları kurgudur, kimsenin gerçek verisi yoktur.

n8n üzerinde beş adım:

1. En basit hâliyle bir soru–cevap akışı
2. Halüsinasyonu canlı yakalama — aynı soruya üç farklı uydurma cevap
3. Few-shot ile biçimi düzeltme
4. Miuul kataloğuyla RAG kurup doğru cevabı alma
5. **RAG'in çuvalladığı yeri görme** — çünkü her sorunun cevabı belgede olmaz

Ardından kendi makinemizde küçük bir modele yönlendirme öğretiyoruz: gelen mesaj hangi
dala gitmeli — ilerleme mi, ödeme mi, katalog mu? Önce paragraf yazdığını, fine-tune
sonrasında tek kelime verdiğini görüyoruz.

> Bu atölyede kod ezberlemiyoruz. Amaç şu soruya cevap verebilmeniz:
> **elimdeki sorun RAG mi ister, fine-tune mu?**

---

## Sözlük

| Terim | Anlamı |
|---|---|
| **Token** | Metnin bölündüğü parça; her zaman bir kelime değil |
| **Embedding** | Bir token'ın veya metin parçasının sayısal vektör temsili |
| **Bağlam penceresi** | Modelin bir istekte görebildiği toplam token miktarı |
| **Self-attention** | Her kelimenin diğer kelimelere bakıp önem ağırlığı hesaplaması |
| **Positional encoding** | Kelimenin cümledeki konumunu modele bildiren ek sinyal |
| **Pre-training** | Ham metinle sonraki kelimeyi tahmin etme eğitimi |
| **SFT** | Soru–cevap çiftleriyle yapılan denetimli ince ayar |
| **RLHF** | İnsan tercihlerinden pekiştirmeli öğrenme |
| **Loss (kayıp)** | Tahmin ile doğru cevap arasındaki farkın sayısal ölçüsü |
| **Temperature** | Olasılık dağılımını düzleştiren/keskinleştiren üretim parametresi |
| **Halüsinasyon** | Modelin doğru görünen ama gerçek olmayan içerik üretmesi |
| **RAG** | Retrieval-Augmented Generation — belge bulup prompt'a ekleme |
| **Chunk / overlap** | Belgenin bölündüğü parça ve parçaların örtüşme miktarı |
| **LoRA** | Ağırlıkları dondurup küçük ek matrisler eğitme yöntemi |
| **QLoRA** | LoRA + dondurulmuş ağırlıkların 4-bit sıkıştırılması |

---

## Kaynaklar

- Vaswani et al., *Attention Is All You Need* (2017) — https://arxiv.org/pdf/1706.03762
- Hu et al., *LoRA: Low-Rank Adaptation of Large Language Models* (2021) — https://arxiv.org/abs/2106.09685
- Dettmers et al., *QLoRA* (2023) — https://arxiv.org/abs/2305.14314
- Mata v. Avianca, Inc. (S.D.N.Y. 2023) — ChatGPT'nin uydurduğu emsal kararlar davası

---

*Bu notlar Miuul Deep Learning to AI Bootcamp — LLM MasterClass dersi için hazırlanmıştır.*
