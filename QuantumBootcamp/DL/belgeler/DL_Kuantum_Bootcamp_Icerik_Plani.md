# Deep Learning — Kuantum Bootcamp Konuk Oturumu
## İçerik Planı — **v2 (hata denetiminden geçti)**

**Süre:** 120 dk · **Dil:** Türkçe + İngilizce teknik terim · **Seviye:** Sezgi ağırlıklı, formül minimum
**Format:** Mevcut kuantum bootcamp sunumuyla aynı — sol üstte başlık, ortada tek büyük fikir cümlesi, altında büyük görsel, yanda vaka kutusu

> **v1'e göre değişenler:** 6 gerçek hata düzeltildi, 4 yanıltıcı sadeleştirme güvenli hâle getirildi, ara eklendi, optimizer bölümü eklendi, Slayt 7 ↔ 16 çelişkisi giderildi. Ayrıntılı liste dokümanın sonunda.

---

## ZAMAN PLANI (düzeltilmiş — ara ve Q&A tamponu eklendi)

| Dakika | Bölüm | Slayt |
|---|---|---|
| 0–5 | Açılış | 1–2 |
| 5–18 | Neden Deep Learning? | 3–7 |
| 18–42 | Nasıl öğreniyor? | 8–16 |
| **42–52** | **☕ ARA** | — |
| 52–75 | Hangi algoritmalar var? | 17–24 |
| 75–97 | Colab uygulaması | 25–27 |
| 97–105 | Kuantum köprüsü | 28–29 |
| 105–112 | Ödev + özet | 30–31 |
| 112–120 | Q&A tamponu | — |

---

# BÖLÜM 0 — AÇILIŞ

### Slayt 1 — Kapak
**Başlık:** Deep Learning
**Alt:** Kuantum Bootcamp · Konuk Oturum
**Görsel:** Mevcut sunumdaki kapsam çubuğu, "Yapay Zeka & Makine Öğrenmesi" satırı vurgulu
**Not:** Kendini 30 saniyede tanıt.

### Slayt 2 — Bugünün akışı
**Ana mesaj:** Bugün üç soruya cevap arayacağız: **Deep Learning nedir, nasıl öğrenir, hangi mimariler var?**
**Görsel:** Yatay akış şeması + ara işareti
**Not:** Beklentiyi netleştir — matematik türetmeyeceğiz, sezgi kuracağız. Arayı burada duyur.

---

# BÖLÜM 1 — NEDEN DEEP LEARNING? (13 dk)

### Slayt 3 — Paradigma farkı
**Ana mesaj:** Klasik makine öğrenmesinde özelliği **insan çıkarır**; derin öğrenmede modelin kendisi **veriden çıkarır**.
**Görsel:** İki paralel boru hattı — üstte "Ham veri → *insan* feature engineering → model", altta "Ham veri → *model kendi katmanlarında öğreniyor*"
**Not:** Oturumun tek cümlelik özeti. Katılımcılar ML modülünü zaten gördü.

### Slayt 4 — Kural yazmanın duvarı *(interaktif, 2 dk)*
**Ana mesaj:** Bir kediyi tarif etmeye çalışın — **her kuralın bir istisnası çıkar.**
**Görsel:** Kedi ızgarası; kurallar ve karşı örnekler (sivri kulak → Scottish Fold, tüylü → Sphynx)

**Vaka kutusu — ✅ v2'de düzeltildi:**
> 2000'lerde bilgisayarla görünün standardı **elle tasarlanmış feature'lardı** — SIFT (2004), HOG (2005). Araştırmacılar yıllarını "iyi feature" tasarlamaya harcıyordu. 2012'de AlexNet, ImageNet yarışmasında top-5 hatasını %26'dan %15'e düşürerek bu yaklaşımı açık farkla geçti.

**⚠️ v1'de hata vardı:** "1960'lardan beri SIFT, HOG" yazıyordu. SIFT 1999/2004, HOG 2005 — 1960'larda bunlar yoktu. Tarih verirken dikkat.

### Slayt 5 — DL'i ateşleyen üçlü
**Ana mesaj:** Fikir on yıllardır vardı; patlamayı **veri + hesaplama gücü + algoritma** üçünün aynı anda olgunlaşması getirdi.
**Görsel:** Üç dişli çark — VERİ (internet, ImageNet 2009), DONANIM (GPU/CUDA), ALGORİTMA (ReLU 2010, dropout 2012)
**Doğru tarih:** Backpropagation 1986'da (Rumelhart, Hinton, Williams) popülerleşti → 2012 AlexNet. Yaklaşık 25 yıllık bekleyiş.

**Not — kuantum paraleli, ama dikkatli kur:**
Bu kitleye söyleyeceğin şey: *"DL'de algoritma 1986'da hazırdı, donanım 25 yıl sonra yetişti. Kuantumda da Shor algoritması 1994'ten beri var, donanım henüz yetişmedi."*

> **⚠️ Ama analojiyi zorlama.** Aradaki fark şu: DL'in beklediği şey **nicelikti** — daha hızlı çip, daha çok veri. Kuantumun beklediği şey **nitelik** — dekoherans ve hata düzeltme, yani çözülmesi gereken fiziksel bir problem. Bunu eklersen analoji hem güzel hem dürüst olur. Eklemezsen fazla iyimser durur ve alanı bilen biri itiraz edebilir.

### Slayt 6 — Vaka: AlphaFold ⭐ *(en çok düzeltme alan slayt)*

**Ana mesaj — ✅ v2'de düzeltildi:**
> 50 yıllık protein **yapı tahmini** problemi, onlarca yıllık deneysel veriyle eğitilen bir sinir ağıyla **büyük ölçüde çözüldü.**

**Vaka kutusu — doğrulanmış rakamlar:**
- 200 milyondan fazla protein yapısı tahmin edildi
- 190 ülkede **3 milyondan fazla** araştırmacı veritabanını kullanıyor
- 35.000'den fazla makalede atıf
- **2024 Nobel Kimya Ödülü** — ödülün yarısı David Baker'a (computational protein design), diğer yarısı Demis Hassabis ve John Jumper'a **"protein structure prediction"** için

**⚠️ v1'de üç hata vardı — üçü de sunumda söylersen düzeltilebilir:**

| v1'de yazan | Sorun | v2 |
|---|---|---|
| "protein **katlanma** problemi çözüldü" | *Folding* ≠ *structure prediction*. AlphaFold statik yapıyı tahmin ediyor; katlanmanın **dinamik süreci** (yollar, ara durumlar) çözülmedi. Nobel komitesi bile ödülü açıkça "structure prediction" için verdi. | "**yapı tahmini** problemi büyük ölçüde çözüldü" |
| "**deneysel yöntemle değil** bir sinir ağıyla" | Yanıltıcı. AlphaFold, PDB'de on yıllarca deneysel yöntemle biriktirilmiş yapılarla eğitildi. Deneysel yöntemin yerine geçmedi, **ürününü kullandı.** | "onlarca yıllık **deneysel veriyle eğitilen** bir sinir ağı" |
| "yüz milyonlarca **yıl** sürecek iş" | DeepMind'ın ifadesi "hundreds of millions of years of **PhD time**" — doktora-insan-yılı, takvim yılı değil. | "yüz milyonlarca **doktora-yılına denk** iş gücü" |

**Bu kitle için bağlantı:** Protein yapısı ve moleküler modelleme, kuantum kimyasının klasik problem alanı. DL ve kuantum bilişim aynı problemlere farklı yollardan saldırıyor — rakip değil, tamamlayıcı.

**Soru gelirse hazır ol:** "AlphaFold her şeyi çözdü mü?" → Hayır. Düzensiz proteinler (intrinsically disordered), konformasyonel değişimler ve tek mutasyonun etkisi hâlâ zayıf alanlar.

### Slayt 7 — DL ne zaman *yanlış* seçim? *(v2'de önemli güncelleme)*

**Ana mesaj:** Derin öğrenme her problemin cevabı değil — ama **"tablo verisinde DL kullanma" tavsiyesi 2026'da artık geçerliliğini yitirdi.**

**Görsel — güncel karar tablosu:**

| Durum | 2020'deki tavsiye | 2026 gerçeği |
|---|---|---|
| Küçük–orta tablo verisi | XGBoost / LightGBM | **TabPFN** (Transformer tabanlı) benchmark'larda öne geçti |
| Büyük tablo verisi | XGBoost | XGBoost hâlâ üstün |
| Açıklanabilirlik zorunlu (regülasyon) | Lineer model / karar ağacı | Değişmedi |
| Görüntü, ses, metin, video | Deep Learning | Değişmedi |
| Çok fazla etiketsiz veri | Deep Learning | Değişmedi |

**⚠️ v1'de eskimiş bilgi vardı:** "Az veri ve tablo verisi → klasik ML" yazıyordu. 2025'te *Nature*'da yayımlanan TabPFN (tabular foundation model), küçük–orta ölçekli tablo verisinde ayarlanmış XGBoost'u geçiyor. Büyük veri setlerinde XGBoost hâlâ önde. Yani doğru cevap "**veri boyutuna bağlı**."

**Not — bu aslında hikayeni güçlendiriyor:** Tablo verisi, klasik ML'in 20 yıl elinde tuttuğu son kaleydi. Oraya da bir Transformer girdi. Bu, Slayt 24'teki "Transformer her yeri yutuyor" temasının kanıtı olarak kullanılabilir. Sadece "açıklanabilirlik" maddesini vurgula — orada klasik yöntemler hâlâ tartışmasız.

---

# BÖLÜM 2 — NASIL ÖĞRENİYOR? (24 dk)

### Slayt 8 — Yapay nöron
**Ana mesaj:** Tek bir nöron aslında **ağırlıklı bir oylamadır** — girdileri önem katsayılarıyla toplar, bir eşikten geçirir.
**Görsel:** x₁,x₂,x₃ → ×w → Σ +b → aktivasyon → çıktı
**Not:** Kredi başvurusu benzetmesi. Öğrenme dediğimiz şey **bu ağırlıkları bulmak.**

### Slayt 9 — Aktivasyon fonksiyonu neden şart?
**Ana mesaj:** Aktivasyon olmadan, 100 katmanlı bir ağ **tek katmanlı bir doğrusal modele eşittir.**
**Görsel:** Solda düz çizgiyle ayrılamayan iç içe iki spiral, sağda eğrilerle ayrılmış hâli
**Yan kutu:**
- **ReLU** — gizli katmanların uzun süredir varsayılanı
- **GELU / SiLU** — modern Transformer'larda bugünün varsayılanı *(v2'de eklendi — Colab'da karşılaşabilirsin)*
- **Sigmoid** — ikili sınıflandırma çıkışı (0–1)
- **Softmax** — çok sınıflı çıkış (olasılıklar toplamı 1)

**Not:** "Doğrusalın doğrusalı yine doğrusaldır" — tek cümlelik gerekçe, bu kadarı yeterli.

### Slayt 10 — Derinlik ne demek?
**Ana mesaj:** Katmanlar üst üste bindikçe model **basit desenlerden karmaşık kavramlara** doğru bir hiyerarşi kurar.
**Görsel:** Kenarlar → dokular → parçalar → nesne
**Not:** Bu görselleştirmeler CNN'ler üzerinde gösterildi (Zeiler & Fergus, 2014). Her mimaride bu kadar temiz bir hiyerarşi çıkmaz — "tipik olarak" diyerek anlat.

### Slayt 11 — Loss: hatanın tek sayısı
**Ana mesaj:** Model kendini iyileştirebilmek için önce **ne kadar yanıldığını tek bir sayıya indirgemek** zorundadır.
**Yan kutu:** Regresyon → MSE/MAE · İkili → Binary Cross-Entropy · Çok sınıflı → Categorical Cross-Entropy
**Not:** Softmax + cross-entropy ikilisini burada Slayt 9'a geri bağla — birlikte çalışırlar.

### Slayt 12 — Gradient descent
**Ana mesaj:** Öğrenme, **sisli bir dağda yokuş aşağı adım adım inmektir.**
**Görsel:** 3B loss yüzeyi + learning rate karşılaştırması
**Oturumun tek formülü:** `w ← w − α · ∂L/∂w`
*yeni ağırlık = eski ağırlık − öğrenme oranı × eğim*
**Not:** **Bu slaytı işaretle — Slayt 28'de kuantuma bağlarken buraya döneceğiz.**

### Slayt 13 — Optimizer: SGD'den Adam'a *(✅ v2'de eklendi)*
**Ana mesaj:** Gradient descent'in kendisi ham hâliyle yavaştır — **optimizer'lar aynı formüle momentum ve uyarlanabilir adım ekler.**
**Görsel:** Aynı loss yüzeyinde SGD (zikzaklı) vs Adam (düzgün) yolları
**Yan kutu:** SGD → temel · Momentum → ivme kazanır, yerel çukurları aşar · RMSprop → her parametreye ayrı adım · **Adam** → momentum + RMSprop, pratikte varsayılan
**Not:** **Bu slayt v1'de eksikti.** Colab'da `optimizer='adam'` yazacaksın; katılımcı "bu ne?" diye sorarsa cevabın hazır olmalı. Detaya girme, "Adam bugünün varsayılanı, iki iyi fikri birleştiriyor" yeterli.

### Slayt 14 — Backpropagation
**Ana mesaj:** Backpropagation, hatanın **çıkıştan girişe geriye dağıtılıp her ağırlığın suç payının hesaplanmasıdır.**
**Görsel:** İleri mavi oklar (tahmin), geri kırmızı oklar (hata)
**Not:** Takım benzetmesi. Zincir kuralına girme, adı geçsin. **Bu slaytı da işaretle — Slayt 28'de geri döneceğiz.**

### Slayt 15 — Üç ayar düğmesi
**Ana mesaj:** **Epoch, batch size ve learning rate** — pratikte en çok oynayacağınız üç düğme.
**Yan kutu:** Epoch → tüm veriyi kaç kez gördü · Batch size → kaç örnekte bir güncelleme · Learning rate → adım büyüklüğü (en kritik)

### Slayt 16 — Overfitting: ezber mi, öğrenme mi?
**Ana mesaj:** Eğitim hatası düşerken doğrulama hatası yükseliyorsa, model öğrenmiyor — **ezberliyor.**
**Görsel:** Train/validation loss eğrisi, ayrışma noktası işaretli
**Yan kutu:** Dropout · Early stopping · Data augmentation · Regularization · Daha fazla veri
**Not:** Çıkmış soru ezberleyen öğrenci benzetmesi. Colab'da bu ayrışmayı canlı göstereceksin.

---

## ☕ ARA — 10 dk *(✅ v2'de eklendi)*

**⚠️ v1'de ara yoktu.** 120 dakika kesintisiz anlatım gerçekçi değil; dikkat 45–50 dakikada belirgin düşer. Arayı Bölüm 2'nin sonuna koydum: teori bitmiş, uygulama başlamamış — doğal kesme noktası.

---

# BÖLÜM 3 — HANGİ ALGORİTMALAR VAR? (23 dk)

### Slayt 17 — Karar haritası ⭐ *(herkes fotoğrafını çeker)*

**Ana mesaj:** Mimariyi seçen şey problem değil, **verinin şeklidir.**

| Verin nasıl? | Mimari |
|---|---|
| Tablo / satır-sütun | MLP — *ama önce XGBoost ve TabPFN'i dene (bkz. Slayt 7)* |
| Görüntü, uzamsal desen | CNN |
| Sıralı, zaman serisi | RNN / LSTM / GRU |
| Metin, uzun bağlam | Transformer |
| Etiketsiz, sıkıştırma, anomali | Autoencoder |
| Yeni içerik üretmek | GAN / Diffusion |

**⚠️ v1'de çelişki vardı:** Slayt 7 "tablo verisinde DL kullanma" diyor, bu tablo "tablo → MLP" diyordu. Katılımcı haklı olarak kafası karışırdı. v2'de tabloya not eklendi — **sunarken bu satırda açıkça durup "burada DL ilk tercih değil, ama nasıl yapıldığını göreceğiz" de.**

### Slayt 18 — MLP / ANN
**Ana mesaj:** En temel mimari: **her nöron bir sonraki katmandaki her nörona bağlı.**
**Kullanım:** Tablo verisi, churn tahmini, kredi skorlama, risk modelleme
**Not:** Parametre sayısı hızla patlar — CNN'in var oluş sebebi bu.

### Slayt 19 — CNN
**Ana mesaj:** CNN, görüntüyü piksel piksel değil, **küçük filtrelerle tarayarak** desen arar.
**Görsel:** 3×3 filtre görüntü üzerinde kayarken; kenar tespit filtresi öncesi/sonrası
**Yan kutu:** Conv → Pooling → Flatten → Dense
**Kullanım:** Görüntü sınıflandırma, medikal görüntüleme, nesne tespiti, malzeme mikroyapı analizi

**Ana fikir — ✅ v2'de ifade düzeltildi:** **Parametre paylaşımı.** Aynı filtre görüntünün her yerinde geçerlidir, bu yüzden model deseni nerede olursa olsun yakalayabilir.

**⚠️ v1'de yanıltıcı ifade vardı:** "Kedinin sol üstte veya sağ altta olması fark etmez" yazıyordu. Teknik olarak konvolüsyon *equivariant*'tır (girdi kayarsa çıktı da kayar), *invariant* değil. Kısmi invariance pooling'den gelir ve tam değildir — CNN'ler kaydırmaya beklenenden daha hassastır. Yukarıdaki ifade hem doğru hem anlaşılır.

### Slayt 20 — RNN / LSTM
**Ana mesaj:** Sıralı veride sıra bilgisi anlam taşır — RNN, **önceki adımı hatırlayarak** ilerler.
**Görsel:** Açılmış RNN zinciri; LSTM hafıza hücresi ve kapılar
**Yan kutu:** RNN → vanishing gradient, kısa hafıza · LSTM (1997) → kapılarla uzun vadeli hafıza · GRU (2014) → daha az kapı, daha hızlı
**Kullanım:** Zaman serisi, sensör verisi, enerji/talep tahmini, sinyal analizi
**Not:** "Bugün hava çok..." cümlesini tamamlamak için önceki kelimeleri hatırlaman gerekir. Kuantum donanımındaki kalibrasyon/sensör zaman serileri de bu kategoride.

### Slayt 21 — Transformer & Attention ⭐
**Ana mesaj:** Attention, modelin **tüm girdiye aynı anda bakıp neyin önemli olduğuna karar vermesini** sağlar.
**Görsel:** Attention haritası — "Hayvan yolu geçmedi çünkü **o** çok yorgundu" → "o" hangi kelimeye bağlanıyor?
**Yan kutu:** RNN sırayla okur → uzun bağlamı zor tutar. Transformer **eğitimde tüm diziyi paralel işler** → GPU'da ölçeklenir. Bugünkü tüm LLM'lerin temeli.

**⚠️ v1'de eksik nüans:** "Transformer paralel okur" yazıyordu. Doğrusu: **eğitimde** paralel işler; metin *üretirken* token token, yani sırayla ilerler. Soru gelirse bu ayrım önemli.

**Not:** 2017 "Attention Is All You Need".

### Slayt 22 — Autoencoder
**Ana mesaj:** Veriyi önce sıkıştırıp sonra geri açmayı öğrenen ağ, farkında olmadan **verinin özünü öğrenir.**
**Görsel:** Kum saati — Encoder → bottleneck → Decoder
**Kullanım:** Anomali tespiti, gürültü temizleme, boyut indirgeme
**Bu kitle için bağlantı:** Kuantum donanımında **gürültü ve hata tespiti** bu kalıba oturur — normal davranışı öğren, sapma olduğunda yeniden üretim hatası fırlasın.

### Slayt 23 — Üretken modeller: GAN → Diffusion
**Ana mesaj:** Üretken modeller ayırt etmeyi değil, **verinin dağılımını öğrenip yeni örnek üretmeyi** hedefler.
**Görsel:** Solda GAN düellosu, sağda diffusion'ın gürültüden görüntüye adımları
**Yan kutu:** GAN — hızlı ama eğitimi kararsız (mode collapse) · Diffusion — daha kararlı ve kaliteli, bugünkü görüntü/video üreticilerinin temeli
**Kullanım:** Görüntü üretimi, **moleküler tasarım (de novo drug design)**, veri artırma
**Not:** AlphaFold 3 de yapı tahmininde diffusion tabanlı bir modül kullanıyor — Slayt 6'ya geri bağla. Güzel bir kapanış halkası.

### Slayt 24 — 2026 gerçeği: her şey Transformer'a mı dönüyor?

**Ana mesaj:** Transformer görüntüye, zaman serisine ve artık tablo verisine de girdi — ama **CNN ve RNN'i öğrenmek hâlâ gerekli.**

**Görsel — ✅ v2'de tarihler düzeltildi:**

| Yıl | Kilometre taşı |
|---|---|
| 1986 | Backpropagation popülerleşiyor |
| **1997** | **LSTM** (Hochreiter & Schmidhuber) |
| 2012 | AlexNet — CNN çağı başlıyor |
| 2014 | seq2seq ile LSTM yaygınlaşıyor |
| 2017 | Transformer |
| 2020 | ViT — Transformer görüntüye giriyor |
| 2025 | TabPFN — Transformer tablo verisine giriyor |

**⚠️ v1'de tarih hatası vardı:** "2015 LSTM" yazıyordu. LSTM **1997**'de yayımlandı (Neural Computation). 2014–2015 yaygınlaşma dönemi, icat tarihi değil. Sunumda yanlış tarih vermek en kolay yakalanan hata türü.

**Yan kutu — CNN/RNN neden hâlâ gerekli:**
- Transformer çok veri ve çok hesaplama ister; sınırlı veride CNN daha iyi
- Edge/gömülü cihazlarda CNN hâlâ standart
- Kavramlar birbirinin üzerine kurulu — konvolüsyonu bilmeden ViT'i anlayamazsın

---

# BÖLÜM 4 — COLAB UYGULAMASI (22 dk)

### Slayt 25–27 — *(içerik sonra netleşecek)*
Demoyu sen ekrandan göstereceksin; katılımcılar izleyecek.

---

# BÖLÜM 5 — KUANTUM KÖPRÜSÜ (8 dk)

> **Bu bölümü kasten iddiasız kurguladım.** "Kuantum şunu hızlandırır" demiyoruz; sadece *öğrenme döngüsünün yapısal benzerliğini* gösteriyoruz.

### Slayt 28 — Parametreli kuantum devresi = eğitilebilir katman

**Ana mesaj:** Parametreli bir kuantum devresi de bir sinir ağı katmanı gibi çalışır: **parametreleri ayarlanır, hata ölçülür, parametreler güncellenir.**

| Sinir ağı | Parametreli kuantum devresi (PQC) |
|---|---|
| Ağırlıklar (w) | Kapı açıları (θ) |
| Forward pass | Devreyi çalıştır, ölçüm al |
| Loss hesapla | Expectation value'dan maliyet |
| Backpropagation ile gradyan | Parameter-shift rule ile gradyan |
| `w ← w − α·∂L/∂w` | `θ ← θ − α·∂L/∂θ` |

**Not:** Slayt 12'ye geri dön — **aynı güncelleme kuralı.** Mesaj: "Bugün öğrendiğin optimizasyon döngüsü kuantum tarafında da var; sadece gradyanı hesaplama yöntemi farklı."

> **⚠️ v2'de eklenen kritik nüans — soru gelirse buna ihtiyacın olacak.**
> Tablodaki son iki satır **eşdeğer değil, sadece benzer.** İki fark var:
>
> **1. Maliyet yapısı.** Backpropagation tek bir geri geçişte *tüm* parametrelerin gradyanını verir. Parameter-shift rule ise her parametre için ayrı devre çalıştırması ister (parametre başına iki çalıştırma). Yani maliyet parametre sayısıyla doğrusal büyür. Bu, QML'in ölçeklenme darboğazının kalbi.
>
> **2. Barren plateaus.** Devre büyüdükçe gradyanlar üstel olarak sıfıra yaklaşabiliyor — model "düz bir ovada" kalıp öğrenemiyor. QML'in en bilinen açık problemi. Adını bilmen yeterli; biri sorarsa "evet, barren plateau problemi bu alanın temel açık sorularından biri" demek seni güvende tutar.
>
> Bunları slayta yazma, konuşma notunda kalsın. Ama biri "o zaman kuantum sinir ağı yapalım gitsin" derse cevabın hazır olur.

### Slayt 29 — Hibrit mimari ve bugünkü gerçek durum
**Ana mesaj:** Bugünün yaklaşımı klasiği kuantumla değiştirmek değil, **klasik ağın içine kuantum bir katman yerleştirmek.**
**Görsel:** Klasik katmanlar → kuantum katman → klasik katmanlar
**Yan kutu — dürüst durum tespiti:**
- Bu alan bugün **araştırma aşamasında**, üretimde değil
- Mevcut donanımda kübit sayısı, gürültü ve barren plateau sınırlayıcı
- Slayt 5'i hatırlayın: DL de donanımın yetişmesini uzun süre bekledi

**Not:** Mevcut kuantum sunumunun 5. slaytındaki HSBC mesajıyla ("bugünden hazırlanmak") aynı çizgi.

---

# BÖLÜM 6 — KAPANIŞ

### Slayt 30 — Ödev
*(içerik Colab kararından sonra netleşecek)*

### Slayt 31 — Özet + kaynaklar
**Üç cümlelik özet:**
1. DL, özelliği insandan alıp modele veren bir paradigma değişimidir
2. Öğrenme = tahmin et → hatayı ölç → ağırlıkları düzelt döngüsüdür
3. Mimariyi problem değil verinin şekli belirler

**Kaynaklar:** Miuul Deep Learning to AI Agent programı · TensorFlow/Keras dokümantasyonu · 3Blue1Brown Neural Networks serisi · Deep Learning Book (Goodfellow, Bengio, Courville) · PennyLane QML dokümantasyonu

---
---

# 📋 DENETİM RAPORU — v1'de bulunan sorunlar

## A. Gerçek hatalar (yanlış bilgi)

| # | Slayt | Hata | Düzeltme |
|---|---|---|---|
| 1 | 6 | "protein **katlanma** problemi çözüldü" | *Folding* ≠ *structure prediction*. Nobel bile "structure prediction" için verildi. → "**yapı tahmini** problemi büyük ölçüde çözüldü" |
| 2 | 6 | "**deneysel yöntemle değil** sinir ağıyla" | AlphaFold onlarca yıllık deneysel PDB verisiyle eğitildi → "deneysel veriyle eğitilen sinir ağı" |
| 3 | 6 | "yüz milyonlarca **yıl** sürecek iş" | Orijinal ifade "hundreds of millions of years of **PhD time**" → "yüz milyonlarca **doktora-yılı**" |
| 4 | 4 | "**1960'lardan** beri SIFT, HOG" | SIFT 1999/2004, HOG 2005 → "2000'lerde" |
| 5 | 24 | "**2015** LSTM" | LSTM **1997** (Neural Computation). 2014 yaygınlaşma yılı |
| 6 | 7 | "Tablo verisi → XGBoost" | 2026'da eskimiş. TabPFN küçük–orta tablo verisinde XGBoost'u geçiyor (Nature 2025); XGBoost büyük veride hâlâ üstün |

## B. Yanıltıcı sadeleştirmeler (soru gelirse zorlanırsın)

| # | Slayt | Sorun | Düzeltme |
|---|---|---|---|
| 7 | 19 | "kedinin nerede olduğu fark etmez" | Konvolüsyon *equivariant*, *invariant* değil → "aynı filtre her yerde geçerli, deseni nerede olursa olsun yakalar" |
| 8 | 21 | "Transformer paralel okur" | Eğitimde paralel; üretimde sırayla → "**eğitimde** tüm diziyi paralel işler" |
| 9 | 28 | Parameter-shift ≈ backprop | Eşdeğer değil: maliyet parametre sayısıyla doğrusal büyür + barren plateaus. Konuşma notuna eklendi |
| 10 | 5 | DL/kuantum tarihsel analojisi | DL **nicelik** bekledi (hız, veri); kuantum **nitelik** bekliyor (hata düzeltme). Farkı söyle |

## C. Akış ve yapı sorunları

| # | Sorun | Çözüm |
|---|---|---|
| 11 | **Optimizer hiç anlatılmıyordu** ama Colab'da `optimizer='adam'` yazacaksın | Slayt 13 eklendi |
| 12 | **Slayt 7 ↔ 17 çelişkisi** — biri "tabloda DL kullanma", diğeri "tablo → MLP" diyordu | Karar haritasına açıklayıcı not eklendi |
| 13 | **Ara yoktu** — 120 dk kesintisiz | 42. dakikaya 10 dk ara eklendi |
| 14 | **Q&A ve gecikme tamponu yoktu** | Son 8 dk tampon olarak ayrıldı |
| 15 | Softmax (9) ve cross-entropy (11) ayrı slaytlarda, bağ kurulmuyordu | Slayt 11 notuna geri bağlantı eklendi |
| 16 | Slayt sayısı 30 → 31 (optimizer eklendi), toplam süre yeniden dengelendi | Zaman planı güncellendi |

---

## SUNUM SONRASI YAPILACAKLAR
- [ ] Colab notebook içeriği (Bölüm 4)
- [ ] Ödev + çözüm (Slayt 30)
- [ ] Görsellerin üretimi/temini
- [ ] pptx üretimi (mevcut sunumun tasarımıyla)
