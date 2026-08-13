# Devir Teslim Notu — CNN Dersi ve YOLO Atölyesi

> Bu dosya, işi devralan kişi/ajan içindir. Kullanıcı: **VMG**, bir derin öğrenme
> bootcamp'inde eğitmen. Türkçe konuşuyor, Türkçe içerik üretiyoruz.

---

## 1. Durum özeti

İki teslimat var. Birincisi **bitti ve anlatıldı**, ikincisi **bugün anlatılacak**.

| Dosya | Durum |
|---|---|
| `cnn2_ders.ipynb` | ✅ Bitti, ders anlatıldı, öğrenciler beğendi. 88 hücre, 5.6 MB |
| `konusmaci_notlari.md` | ✅ O dersin konuşmacı notları |
| `atolye_yolo.ipynb` | ⚠️ Bugünkü atölye. 53 hücre, 733 KB. **3 hata düzeltildi ama Colab'da sınanmadı** |
| `atolye_konusmaci_notlari.md` | ⚠️ Atölye notları. Aşağıdaki 2 numaralı maddeye göre güncellenmeli |

---

## 2. ACİL — sırada ne var

Kullanıcı atölyeyi bugün anlatacak. Son turda üç hata bildirdi, üçünü de düzelttim
ama **Colab'da doğrulanmadı**. Sıradaki iş bunları doğrulatmak.

### 2.1 Düzeltilen ama sınanmayan üç şey

**a) `iou` bölümü kaldırıldı.**
Kullanıcı "üç eşikte de 21 kutu çıktı, göstermeye değmez" dedi. Haklı — yeni YOLO'lar
kopya kutu üretmiyor, YOLO26 NMS'siz. Kod hücresini sildim, yerine kısa bir markdown
notu koydum ("NMS'i bilmek gerek ama artık çalışırken görmek zor"). Görsel şemada
NMS anlatımı duruyor.

**b) Webcam canlı yayın hatası.**
Hata: `TypeError: Cannot read properties of undefined (reading 'getContext')`
Sebep: JS'te `var video, div, stream, tuval, katmanImg;` — hepsi **undefined**.
`kameraKur()` fonksiyonu `if (div !== null) return stream;` ile başlıyordu;
`undefined !== null` **true** olduğu için kurulum hiç çalışmadan çıkıyordu.
Düzeltme: `var video = null, div = null, stream = null, tuval = null, katmanImg = null;`
**Bu tek satırlık düzeltme Colab'da denenmedi.**

**c) 9. bölüm (Roboflow) "0 nesne bulundu".**
Sebep: `kitchen.jpg` bir mutfak sahnesi; Roboflow'daki çöp modeli **yakın çekim tek
nesne** fotoğraflarıyla eğitilmiş.
Düzeltme: `veri/atolye_gorseller.zip` içine dünkü Garbage veri setinden 6 fotoğraf
eklendi (`atolye/cop/` klasörü). 9. bölüm artık `COP_DIZIN/metal10.jpg` kullanıyor.
**Bu da denenmedi** — Roboflow modelinin bu fotoğraflarda çalışacağını doğrulayamadım.
Çalışmazsa `confidence` düşürmeyi veya başka bir fotoğrafı denemeyi öner.

### 2.2 Konuşmacı notları güncellenmeli

`atolye_konusmaci_notlari.md` içindeki **"### 3.2 NMS"** bölümü hâlâ silinen `iou`
hücresini anlatıyor. O bölüm ya kısaltılmalı ya da "kodda göstermiyoruz, sadece
şemadan anlatıyoruz" diye yeniden yazılmalı. Numaralandırma da kaydı: eski 3.3
(`imgsz`) artık defterde **3.2**.

---

## 3. Nasıl çalışıyor — üretim sistemi

**Defterler elle düzenlenmiyor.** Her biri bir Python üreteç betiğinden doğuyor.
Betikler `cnn2/araclar/` içinde:

| Betik | Ne üretir |
|---|---|
| `nb_kur.py` | `cnn2_ders.ipynb` |
| `nb_atolye.py` | `atolye_yolo.ipynb` |
| `gif_*.py` | `resimler/` içindeki şema ve animasyonlar |
| `mp4_gif.py` | Kullanıcının verdiği MP4'leri GIF'e çevirir |
| `cizim.py` | GIF betiklerinin ortak çizim yardımcıları |

**Çalıştırma:** Betiklerin içindeki yollar `/sessions/<oturum>/mnt/cnn2/...` biçiminde
sabit yazılmış. Yeni oturumda oturum adı değişir — betiklerin başındaki `DIZIN`,
`CIKTI`, `RESIM_DIZIN` sabitlerini güncellemen gerekir.

**Akış:** üreteci düzenle → çalıştır → defter yeniden yazılır. Deftere elle dokunma,
bir sonraki üretimde ezilir.

### 3.1 Üreteçte üç tuzak (hepsine takıldım)

**1. Kod hücresi içinde `\n`**
Kod hücreleri `code(r"""...""")` ile yazılıyor. **`r` şart.** Ham string olmazsa
Python `\n` kaçışlarını gerçek satır sonuna çevirir ve hücre bozulur.

**2. Kod hücresi içinde üç tırnak**
Hücre içindeki docstring'ler (`"""..."""`) dıştaki `r"""` stringini kapatır.
Fonksiyon açıklamalarını `#` yorum olarak yaz. JavaScript blokları için `'''...'''`
kullanılabilir ama o zaman **yama betiğinin** kendisi `'''` kullanamaz — bu yüzden
webcam bölümünü ayrı bir dosyaya yazıp okuttum.

**3. `!pip` satırları**
`code()` fonksiyonu `ast.parse` ile doğrulama yapıyor. `!pip` ve `%magic` Python değil;
doğrulamadan önce `pass` ile maskeleniyor. Bu mantık `nb_atolye.py` içinde var,
`nb_kur.py` içinde yok (orada magic kullanılmıyor).

---

## 4. Veri ve GitHub

Repo: **`gorkenvm/Presentations`**, klasör `cnn2/`.

**Görseller deftere base64 gömülü** — push edilmeden de çalışırlar. `nb_kur.py` içinde
`GOMULU = False` yapılırsa GitHub raw URL'e geçer (defter küçülür, push şart olur).

**Veri setleri zip olarak repoda:**

| Zip | İçerik |
|---|---|
| `veri/garbage_classification.zip` | 2527 görüntü, 6 sınıf, 43 MB — dünkü ders |
| `veri/atolye_gorseller.zip` | 10 çok nesneli fotoğraf + 2 video + 6 çöp fotoğrafı, 9 MB — atölye |

Defterler bu zip'leri `raw.githubusercontent.com`'dan indiriyor. **Push edilmeden
defterdeki indirme hücresi 404 verir.** Sıra önemli: önce push, sonra Colab.

**Push:** `cnn2/push.ps1` — PowerShell'den `.\push.ps1 -Message "..."`.
Repoyu `..\.gitrepo\Presentations` altına klonlar, klasörü oraya aynalar (robocopy
`/MIR`), commit'ler, push eder.

⚠️ **`04_cnn_course_materials` klasörü hariç tutuluyor** — içindeki `yolov3.weights`
237 MB, GitHub 100 MB üstünü reddeder ve *tüm* push başarısız olur. Script'te ayrıca
push öncesi 100 MB kontrolü var.

---

## 5. Sınanamayanlar — dürüst liste

Sandbox'ta doğrulayamadığım şeyler. Kullanıcıya her seferinde açıkça söyledim,
sen de söyle:

- **Ultralytics/YOLO hiç çalıştırılamadı.** Kurulum PyTorch + CUDA (3 GB) çekiyor,
  sandbox'a sığmadı. Bütün YOLO kodu dokümana bakarak yazıldı.
- **ImageNet/YOLO ağırlıkları indirilemiyor** — sandbox ağı `storage.googleapis.com`
  ve GitHub releases'e 403 veriyor.
- **Colab'a özgü her şey:** `google.colab.files`, `eval_js`, webcam JS köprüsü,
  `drive.mount`.
- **Roboflow hosted inference** bir kez çalıştı (`trash-classification-fg7fz/2`,
  dataset thumbnail'ında `paper 0.998`), ama **atölye zip'indeki çöp fotoğraflarında
  denenmedi.**

Doğrulanabilenler için sandbox'ta TensorFlow kuruldu ve **`cnn2_ders.ipynb`'nin
bütün kod hücreleri gerçek veriyle uçtan uca çalıştırıldı** — o defter sağlam.

---

## 6. Kullanıcının çalışma tarzı — bilmen gerekenler

- **Adım adım ilerliyor.** Bir bölüm bitir, göster, onay bekle. Toptan üretim istemiyor.
- **Kaynak materyaline sadık kalmak istiyor.** Elinde eski Colab defterleri var;
  "sana verdiğim colabtaki kodu kullanalım" dedi. Kendi kalıplarını koru
  (`ImageDataGenerator`, `flow_from_directory`, `Model(inputs=backbone.input, ...)`),
  modernleştirme dürtüsüne kapılma — ama **bozuk API'yi düzelt ve söyle.**
- **Görsellerde titiz.** Beğenmediğini açıkça söylüyor. İki kez geri dönüş oldu:
  timeline kutularını büyüttüm sonra geri aldı; VGG'nin "iki 3×3" şemasını
  anlaşılmaz buldu, defterden çıkarıp konuşmacı notlarına metin olarak taşıdım.
- **Jargondan rahatsız oluyor.** "Bu bilgilerin ne anlama geldiğini ben de bilmiyorum"
  dedi. Her terimi açıkla ya da kullanma.
- **Konuşmacı notlarını okuyarak anlatıyor.** Notlar **Söyle / Yap / Ekranda ne olacak**
  formatında, tırnak içinde doğrudan okunabilir cümleler halinde yazılıyor.
  Bu format işe yaradı, koru.
- **Zaman baskısı altında.** Uzun açıklama yerine hızlı ve kesin çıktı istiyor.
- **Kendi düzenlemelerini yapıyor.** Bir kod hücresini kendi eliyle değiştirip geri
  gönderdi; onu aynen aldım, çevresindeki metni ona göre güncelledim. **Kullanıcının
  yazdığına dokunma.**

---

## 7. Yapılmış işlerin tam listesi

### `cnn2_ders.ipynb` (bitti)

11 bölüm: CNN mimarisi → piksel/gri/renkli (canlı kodla) → convolution (stride,
padding) → pooling → flatten → pretrained modeller → zaman çizelgesi → AlexNet →
VGG → ResNet → transfer learning ve fine tuning → Garbage Classification uygulaması
(MobileNetV2 + ResNet50 karşılaştırması, tahmin görselleştirmesi, hata analizi).

**Düzelttiğim gerçek hatalar:**
- Kaynak defterde MobileNetV2'ye `rescale=1./255` ile `[0,1]` veri gidiyordu,
  model `[-1,1]` bekliyor → `preprocessing_function=preprocess_input`
- Fine tuning'de BatchNormalization katmanları açılıyordu → donuk bırakıldı
- Doğrulama akışında `shuffle=True` yüzünden sınıf bazlı doğruluk tablosu yanlış
  sayıyordu → `shuffle=False`

### `atolye_yolo.ipynb` (bugün)

10 bölüm: dünkü şema tekrarı → sınıflandırma neden yetmiyor (kırılma anı) → ilk
tespit → anatomi (`conf`, `imgsz`) → video → takip (ID + iz) → sayma (bölgeden geçen)
→ kendi görüntün (URL / dosya / canlı webcam) → COCO'da ne yok → Roboflow ile dünkü
6 sınıf, kutu ile.

**Kaynak defterde bulup düzelttiğim:** `object_counter.ObjectCounter()` +
`set_args(...)` API'si kaldırılmış → `solutions.ObjectCounter(region=..., model=...)`
ve `results.plot_im`.

---

## 8. İlk yapılacak

1. Kullanıcıya sor: atölyeyi Colab'da denedi mi, webcam ve Roboflow düzeltmeleri
   çalıştı mı?
2. Çalıştıysa `atolye_konusmaci_notlari.md`'deki 3.2 NMS bölümünü güncelle
   (madde 2.2).
3. Çalışmadıysa hata metnini iste, üreteçten düzelt, yeniden üret.
4. Push komutu: `cd C:\dev\presentations\DLtoAI\cnn2` ardından
   `.\push.ps1 -Message "..."`
