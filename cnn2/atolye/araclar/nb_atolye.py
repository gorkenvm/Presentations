"""atolye_yolo.ipynb üreticisi."""
import ast, base64, json, mimetypes, os

CIKTI = "/sessions/peaceful-lucid-dijkstra/mnt/cnn2/atolye/atolye_yolo.ipynb"
RESIM_DIZIN = "/sessions/peaceful-lucid-dijkstra/mnt/cnn2/atolye/resimler"
REPO = ("https://colab.research.google.com/github/gorkenvm/Presentations/"
        "blob/main/cnn2/atolye/atolye_yolo.ipynb")

hucreler = []


def gorsel(dosya, genislik=900):
    yol = os.path.join(RESIM_DIZIN, dosya)
    tur = mimetypes.guess_type(yol)[0] or "image/png"
    b64 = base64.b64encode(open(yol, "rb").read()).decode()
    return f'<img src="data:{tur};base64,{b64}" width="{genislik}">'


def md(metin):
    hucreler.append({"cell_type": "markdown", "metadata": {},
                     "source": metin.strip().splitlines(True)})


def code(kaynak):
    # !pip / %magic satırları Python değil; doğrulamadan önce maskele
    kontrol = "\n".join("pass" if satir.lstrip().startswith(("!", "%")) else satir
                        for satir in kaynak.splitlines())
    ast.parse(kontrol)
    hucreler.append({"cell_type": "code", "metadata": {}, "execution_count": None,
                     "outputs": [], "source": kaynak.strip().splitlines(True)})


# ══════════════════════════════════════════════════════════════════
md(f"""
# Atölye — Nesne Tespiti, Takip ve Sayma

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)]({REPO})

Dün **sınıflandırma** yaptık: bir fotoğrafa bakıp "bu ne?" diye sorduk.
Bugün soruyu değiştiriyoruz: **"ne var, nerede, kaç tane?"**

Akış tek bir mantıkla ilerliyor — her adım bir öncekinin cevaplayamadığı soruyu çözüyor:

| Adım | Cevapladığı soru |
|---|---|
| **Tespit** | Bu karede ne var ve nerede? |
| **Takip** | Bu, az önceki nesnenin aynısı mı? |
| **Sayma** | Şu çizgiden kaç tane geçti? |

> **Başlamadan:** Menüden **Çalışma zamanı → Çalışma zamanı türünü değiştir → T4 GPU**.
> GPU olmadan fotoğraflar çalışır ama videolar çok yavaşlar.
""")

md(f"""
---
## Önce dünü hatırlayalım

{gorsel("cnn_mimari.gif", 900)}

<sub>Girdiden çıktıya: **Conv → ReLU → Pooling** bloğu tekrarlanır, sonra
**Flatten → Dense → Softmax**. Solda görüntü girer, sağda tek bir olasılık dağılımı çıkar.</sub>

Dün bu yapının **gövdesini** hazır aldık, **kafasını** kendi sınıflarımıza göre değiştirdik.
İki kavramı konuşmuştuk:

- **Transfer learning** — hazır modelin öğrendiğini kendi problemimize taşımak
- **Fine tuning** — o modeli kendi verimizle ince ayara çekmek

Bugün aynı fikri kullanacağız ama bu kez **eğitim bile yapmayacağız** — hazır modeli
doğrudan çalıştıracağız.

> Yukarıdaki şemaya son bir kez bakın: çıktı **tek bir olasılık dağılımı**.
> Bugünkü dersin tamamı, bu tek çıktının neden yetmediği üzerine.
""")

md("""
---
## Bugün kullanacağımız model: YOLO

**YOLO = You Only Look Once** — "sadece bir kez bak". İsim, fikrin kendisi.

2015'ten önceki tespit yöntemleri görüntüye **defalarca** bakıyordu: önce "burada bir
şey olabilir" diye binlerce aday bölge çıkarılıyor, sonra her biri ayrı ayrı sinir
ağından geçiriliyordu. Doğruydu ama tek bir fotoğraf dakikalar sürüyordu.

YOLO'nun fikri şu: **görüntüyü bir kere ağdan geçir, bütün kutuları ve sınıfları
aynı anda tahmin et.** Ağ görüntüyü bir ızgaraya böler, her hücre "benim bölgemde
bir nesne var mı, varsa kutusu nerede ve ne" sorusuna aynı geçişte cevap verir.

Sonuç: dakikalar yerine **milisaniyeler**. Gerçek zamanlı tespit böyle mümkün oldu.

### Hangi veriyle eğitildi: COCO

| | |
|---|---|
| **Ad** | COCO — *Common Objects in Context* |
| **Boyut** | ~330.000 görüntü, 1.5 milyondan fazla etiketlenmiş nesne |
| **Sınıf** | **80 tane** — person, car, dog, bottle, laptop, banana... |
| **Özelliği** | Nesneler stüdyoda değil, **doğal ortamlarında** ve çoğu zaman üst üste |

Dün kullandığımız ImageNet'ten farkı önemli: ImageNet'te her fotoğrafta genelde tek
bir nesne vardı ve sadece **etiketi** verilmişti. COCO'da ise her nesnenin etrafına
**kutu çizilmiş**. Model bu yüzden "nerede" sorusunu cevaplayabiliyor.

> Bu 80 sınıf bugün karşımıza tekrar çıkacak — 8. bölümde listeye bakıp içinde
> **olmayan** şeyleri konuşacağız.

### YOLO ile neler yapılır?

Aynı aileden, aynı kullanımla:

| Görev | Ne verir | Model adı |
|---|---|---|
| **Tespit** (detect) | Kutu + sınıf | `yolo26n.pt` |
| **Segmentasyon** (segment) | Piksel piksel maske | `yolo11n-seg.pt` |
| **Poz** (pose) | İskelet noktaları — omuz, dirsek, diz | `yolo11n-pose.pt` |
| **Sınıflandırma** (classify) | Tek etiket (dünkü gibi) | `yolo11n-cls.pt` |
| **Döndürülmüş kutu** (obb) | Eğik kutu — uydu, belge | `yolo11n-obb.pt` |

Bugün **tespit** ile başlayıp üzerine **takip** ve **sayma** ekleyeceğiz.

### Model boyutları

Dosya adının sonundaki harf boyutu söyler: **n**ano → **s**mall → **m**edium →
**l**arge → **x**large. Büyüdükçe daha doğru, daha yavaş. Biz `n` kullanacağız —
derste hız lazım, üstelik fark çoğu iş için küçük.

> **Sürüm notu:** YOLO 2015'ten beri geliştiriliyor. v3 (2018) uzun süre standarttı,
> bugün kullanılmıyor. Güncel sürüm **YOLO26**; kullanımı v8 ile neredeyse aynı,
> o yüzden eski öğreticiler hâlâ işinize yarar.
""")

md("""
---
## 0. Kurulum ve veri
""")

code(r"""
!pip install -q ultralytics

import os, zipfile, urllib.request
import numpy as np
import matplotlib.pyplot as plt
import cv2
import torch
from ultralytics import YOLO

print("Torch:", torch.__version__, "| GPU:", torch.cuda.is_available())
if not torch.cuda.is_available():
    print("  → GPU yok. Fotoğraflar çalışır, videolar yavaş olur.")
""")

code(r"""
# Atölye görselleri ve videoları — GitHub'dan
URL = ("https://raw.githubusercontent.com/gorkenvm/Presentations/main/"
       "cnn2/atolye/veri/gorseller.zip")

zip_yolu = "/content/gorseller.zip"
if not os.path.exists(zip_yolu):
    urllib.request.urlretrieve(URL, zip_yolu)
with zipfile.ZipFile(zip_yolu) as z:
    z.extractall("/content")

GORUNTU_DIZIN = "/content/atolye/goruntuler"    # cok nesneli sahneler
VIDEO_DIZIN   = "/content/atolye/video"
COP_DIZIN     = "/content/atolye/cop"           # dunku dersten cop fotograflari

print("Görüntüler:", sorted(os.listdir(GORUNTU_DIZIN)))
print("Videolar  :", sorted(os.listdir(VIDEO_DIZIN)))
print("Çöp       :", sorted(os.listdir(COP_DIZIN)))
""")

code(r"""
# --- yardımcılar ---

def goster(gorsel_bgr, baslik="", genislik=11):
    # OpenCV BGR görüntüsünü notebook'ta gösterir
    rgb = cv2.cvtColor(gorsel_bgr, cv2.COLOR_BGR2RGB)
    oran = rgb.shape[0] / rgb.shape[1]
    plt.figure(figsize=(genislik, genislik * oran))
    plt.imshow(rgb)
    plt.title(baslik, fontsize=12)
    plt.axis("off")
    plt.show()


def model_yukle(tercihler=("yolo26n.pt", "yolo11n.pt", "yolov8n.pt")):
    # Sürüm farklarına karşı: ilk indirilebileni kullan.
    # Sondaki harf model boyutu: n=nano (en hızlı), s=small, m=medium, l=large, x=xlarge.
    # Büyüdükçe daha doğru ama daha yavaş. Derste n kullanıyoruz.
    for ad in tercihler:
        try:
            m = YOLO(ad)
            print("Model:", ad)
            return m
        except Exception as e:
            print(f"  {ad} yüklenemedi ({type(e).__name__}), sıradakine geçiliyor")
    raise RuntimeError("Hiçbir model yüklenemedi")


model = model_yukle()
print("Tanıdığı sınıf sayısı:", len(model.names))
""")

# ══════════════════════════════════════════════════════════════════
md("""
---
# 1. Dünkü model neden yetmiyor?

Dün eğittiğimiz gibi bir sınıflandırıcı alalım ve içinde **birden çok nesne olan**
bir fotoğrafı verelim.
""")

code(r"""
from tensorflow.keras.applications.mobilenet_v2 import (
    MobileNetV2, preprocess_input, decode_predictions)
from tensorflow.keras.utils import load_img, img_to_array

siniflandirici = MobileNetV2(weights="imagenet")     # dünkü gövdenin tam hali

FOTO = os.path.join(GORUNTU_DIZIN, "traffic.jpg")

img = load_img(FOTO, target_size=(224, 224))
x = preprocess_input(np.expand_dims(img_to_array(img), 0))
tahmin = decode_predictions(siniflandirici.predict(x, verbose=0), top=3)[0]

goster(cv2.imread(FOTO), "Sınıflandırıcıya verdiğimiz fotoğraf")

print("Sınıflandırıcının cevabı:")
for _, ad, olasilik in tahmin:
    print(f"  {ad:22s} {olasilik:.3f}")
""")

md(f"""
Model **tek bir cevap** verdi. Oysa fotoğrafta onlarca araç, yaya ve trafik ışığı var.

**Model yanlış mı söyledi?** Hayır. Sorduğumuz soru yanlıştı.

{gorsel("tespit_vs_siniflandirma.png", 980)}
""")

# ══════════════════════════════════════════════════════════════════
md("""
---
# 2. Aynı fotoğraf, bu kez tespit

Üç satır. Aynı fotoğraf.
""")

code(r"""
# model(...)  -> tahmin yapar, sonuç listesi döner (her görüntü için bir eleman)
#   verbose=False : her çağrıda konsola log basmasın
#   conf=0.25     : varsayılan güven eşiği (aşağıda değiştireceğiz)
#   iou=0.7       : varsayılan NMS eşiği
#   imgsz=640     : modelin baktığı çözünürlük
#   device=0      : GPU kullan (varsayılan otomatik seçer)
sonuclar = model(FOTO, verbose=False)

# .plot() -> kutuları çizilmiş görüntüyü BGR dizi olarak döndürür
goster(sonuclar[0].plot(), "YOLO ile nesne tespiti")

print(f"Bulunan nesne sayısı: {len(sonuclar[0].boxes)}")
""")

code(r"""
# Ne bulduğuna sınıf sınıf bakalım
from collections import Counter

# .boxes.cls -> her kutunun sınıf numarası (tensor). int().tolist() ile Python listesine çeviriyoruz
sinif_idler = sonuclar[0].boxes.cls.int().tolist()

# model.names -> {0: 'person', 1: 'bicycle', ...} sözlüğü
sayim = Counter(model.names[i] for i in sinif_idler)

for ad, adet in sayim.most_common():
    print(f"  {ad:16s} {adet}")
""")

md("""
Az önce tek cevap veren fotoğraf, şimdi her nesneyi ayrı ayrı veriyor — **üstelik yeriyle**.

Diğer fotoğraflara da bakalım.
""")

code(r"""
from glob import glob

yollar = sorted(glob(os.path.join(GORUNTU_DIZIN, "*.jpg")))[:6]

# Modele liste verirsek hepsini tek seferde işler — tek tek çağırmaktan hızlıdır
toplu = model(yollar, verbose=False)

plt.figure(figsize=(16, 9))
for i, (yol, sonuc) in enumerate(zip(yollar, toplu)):
    plt.subplot(2, 3, i + 1)
    plt.imshow(cv2.cvtColor(sonuc.plot(), cv2.COLOR_BGR2RGB))
    plt.title(f"{os.path.basename(yol)} — {len(sonuc.boxes)} nesne", fontsize=10)
    plt.axis("off")
plt.tight_layout()
plt.show()
""")

# ══════════════════════════════════════════════════════════════════
md(f"""
---
# 3. Çıktının anatomisi

Ekranda gördüğümüz renkli kutuların altında ne var?

{gorsel("anatomi.png", 980)}
""")

code(r"""
kutular = sonuclar[0].boxes    # bu görüntüde bulunan bütün kutular

# kutu.cls  -> sınıf numarası      kutu.conf -> güven (0-1)
# kutu.xyxy -> [x1, y1, x2, y2]    kutu.xywh -> [merkez_x, merkez_y, en, boy]
# kutu.id   -> takip numarası (sadece track() kullanılırsa dolu)
print(f"{'sınıf':14s} {'güven':>7s}   kutu (x1, y1, x2, y2)")
print("-" * 58)
for kutu in kutular[:8]:
    ad  = model.names[int(kutu.cls)]
    gvn = float(kutu.conf)
    x1, y1, x2, y2 = [int(v) for v in kutu.xyxy[0]]
    print(f"{ad:14s} {gvn:7.3f}   ({x1:4d}, {y1:4d}, {x2:4d}, {y2:4d})")

print(f"\nToplam {len(kutular)} kutu.")
""")

md("""
## 3.1 Güven eşiği ile oynayalım

`conf` parametresi, "şu olasılığın altındakileri bana gösterme" demek.
Aynı fotoğrafı üç farklı eşikle çalıştıralım.
""")

code(r"""
# conf = güven eşiği. Modelin bu olasılığın altındaki tahminlerini gösterme.
esikler = [0.10, 0.25, 0.60]

plt.figure(figsize=(17, 6))
for i, esik in enumerate(esikler):
    s = model(FOTO, conf=esik, verbose=False)[0]
    plt.subplot(1, 3, i + 1)
    plt.imshow(cv2.cvtColor(s.plot(), cv2.COLOR_BGR2RGB))
    plt.title(f"conf = {esik}  →  {len(s.boxes)} nesne", fontsize=12)
    plt.axis("off")
plt.tight_layout()
plt.show()
""")

md("""
Eşik düştükçe kutu sayısı artıyor — ama artan kutuların bir kısmı **yanlış**.
Eşik yükseldikçe sonuç temizleniyor — ama bu sefer gerçek nesneleri **kaçırıyoruz**.

> "Doğru" eşik diye bir şey yok. Güvenlik kamerasında hiçbir şeyi kaçırmak istemezsin,
> eşiği düşürürsün. Otomatik bir sayım sisteminde yanlış saymak istemezsin, yükseltirsin.

## 3.2 NMS: aynı nesneye kaç kutu?

Model aslında **yüzlerce** aday kutu üretir; aynı arabanın üstüne onlarca kutu düşer.
NMS (Non-Maximum Suppression) üst üste binenleri temizler.

`iou` parametresi "ne kadar üst üste binerlerse aynı sayılsın" eşiğidir.
Yükseltirsek NMS gevşer ve kopyalar kalmaya başlar.
""")

md("""
> **NMS hakkında kısa not:** Yukarıdaki şemanın üçüncü kutusu NMS'i anlatıyor —
> model yüzlerce aday kutu üretir, üst üste binenlerden en güvenlisi tutulur.
> Bunu kodda göstermeye çalışmadık çünkü **yeni nesil YOLO'lar zaten neredeyse hiç
> kopya kutu üretmiyor**; YOLO26 NMS'i tamamen kaldırdı. Kavramı bilmek gerekiyor
> (eski modellerde ve kendi modelinizi eğitirken karşınıza çıkar) ama artık
> çalışırken görmek zor.

## 3.2 Asıl fark yaratan parametre: `imgsz`

Model fotoğrafı olduğu gibi işlemez; önce **sabit bir boyuta küçültür**. Varsayılan 640.
Küçük ve uzaktaki nesneler bu küçültmede kaybolabilir.
""")

code(r"""
# imgsz = modelin baktığı çözünürlük. Büyütmek küçük nesneleri kurtarır ama yavaşlatır.
boyutlar = [320, 640, 1280]

plt.figure(figsize=(17, 6))
for i, boyut in enumerate(boyutlar):
    s = model(FOTO, imgsz=boyut, conf=0.25, verbose=False)[0]
    plt.subplot(1, 3, i + 1)
    plt.imshow(cv2.cvtColor(s.plot(), cv2.COLOR_BGR2RGB))
    plt.title(f"imgsz = {boyut}  ->  {len(s.boxes)} nesne", fontsize=12)
    plt.axis("off")
plt.tight_layout()
plt.show()
""")

md("""
Fark burada net görünüyor. `imgsz=320`'de uzaktaki küçük araçlar kayboluyor,
`1280`'de geri geliyor — ama işlem süresi de o oranda artıyor.

> **Pratik kural:** Nesneleriniz küçük ve uzaksa `imgsz` artırın. Yakın ve büyükse
> artırmanın faydası yok, sadece yavaşlarsınız.
""")

# ══════════════════════════════════════════════════════════════════
md("""
---
# 4. Videoya geçelim

Video, arka arkaya dizilmiş fotoğraflardan başka bir şey değil. Modele **her kareyi
ayrı ayrı** vereceğiz.
""")

code(r"""
from IPython.display import HTML
from base64 import b64encode

VIDEO = os.path.join(VIDEO_DIZIN, "car_flow.mp4")


def video_goster(yol, genislik=720):
    # Tarayıcıda oynatilabilmesi icin H.264'e cevirip gomer
    duzeltilmis = yol.replace(".mp4", "_h264.mp4")
    os.system(f'ffmpeg -y -loglevel error -i "{yol}" -vcodec libx264 '
              f'-pix_fmt yuv420p "{duzeltilmis}"')
    veri = open(duzeltilmis, "rb").read()
    src = "data:video/mp4;base64," + b64encode(veri).decode()
    return HTML(f'<video width={genislik} controls loop>'
                f'<source src="{src}" type="video/mp4"></video>')


video_goster(VIDEO)
""")

code(r"""
def videoyu_isle(giris, cikis, islem, max_kare=None):
    # Videoyu kare kare isler. islem(kare, i) -> cizilmis kare
    cap = cv2.VideoCapture(giris)
    assert cap.isOpened(), f"Video açılamadı: {giris}"

    en  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    boy = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS) or 25

    # mp4v: OpenCV'nin yazabildiği codec. Tarayıcı bunu oynatamaz,
    # o yüzden video_goster() sonradan H.264'e çeviriyor.
    yazici = cv2.VideoWriter(cikis, cv2.VideoWriter_fourcc(*"mp4v"), fps, (en, boy))

    i = 0
    while True:
        ok, kare = cap.read()
        if not ok or (max_kare and i >= max_kare):
            break
        yazici.write(islem(kare, i))
        i += 1

    cap.release()
    yazici.release()
    print(f"{i} kare işlendi → {cikis}")
    return cikis


# Her kareyi ayrı ayrı tespit et
model_tespit = model_yukle()

def sadece_tespit(kare, i):
    return model_tespit(kare, verbose=False)[0].plot()

videoyu_isle(VIDEO, "/content/01_tespit.mp4", sadece_tespit)
video_goster("/content/01_tespit.mp4")
""")

md("""
İşe yarıyor. Ama bir sorun var.

> **Sorun:** Model her kareye **sıfırdan** bakıyor. 5. karedeki kırmızı arabanın,
> 4. karedeki kırmızı arabayla aynı araba olduğunu bilmiyor. Onun için her kare
> yepyeni bir dünya.

Bu yüzden "kaç araba geçti?" sorusunu **tespit tek başına cevaplayamaz.**
""")

# ══════════════════════════════════════════════════════════════════
md("""
---
# 5. Takip — nesnelere kimlik vermek

`track()`, tespitin üstüne bir katman ekler: her nesneye bir **ID** atar ve
kareler arasında onu izler.
""")

code(r"""
model_takip = model_yukle()

def takip_et(kare, i):
    # track() = predict() + kimlik atama
    #   persist=True     : kareler arası hafızayı koru (BU OLMAZSA ID'ler her karede sıfırlanır)
    #   tracker=...      : "botsort.yaml" (varsayılan) veya "bytetrack.yaml"
    #   classes=[2, 7]   : sadece belirli sınıfları takip et
    return model_takip.track(kare, persist=True, verbose=False)[0].plot()

videoyu_isle(VIDEO, "/content/02_takip.mp4", takip_et)
video_goster("/content/02_takip.mp4")
""")

md("""
Kutuların üstünde artık `id:3`, `id:7` gibi numaralar var. Aynı araba boyunca
**aynı numara** kalıyor.

Şimdi izlerini de çizelim — her nesnenin nereden gelip nereye gittiği görünsün.
""")

code(r"""
from collections import defaultdict

model_iz = model_yukle()
izler = defaultdict(list)

def iz_ciz(kare, i):
    sonuc = model_iz.track(kare, persist=True, verbose=False)[0]
    cizim = sonuc.plot()

    # İlk karelerde henüz ID atanmamış olabilir — None kontrolü şart
    if sonuc.boxes.id is not None:
        merkezler = sonuc.boxes.xywh.cpu()
        idler = sonuc.boxes.id.int().cpu().tolist()

        for (x, y, w, h), nesne_id in zip(merkezler, idler):
            iz = izler[nesne_id]
            iz.append((float(x), float(y)))
            if len(iz) > 40:                       # son 40 kare yeter
                iz.pop(0)
            if len(iz) > 1:
                nokta = np.array(iz, np.int32).reshape((-1, 1, 2))
                cv2.polylines(cizim, [nokta], False, (60, 200, 90), 3)
    return cizim

videoyu_isle(VIDEO, "/content/03_iz.mp4", iz_ciz)
video_goster("/content/03_iz.mp4")
""")

md("""
> **Neden ayrı bir problem?** Tespit "şu anda ne var" sorusunu cevaplar.
> Takip "bu, az önceki miydi" sorusunu cevaplar. İkincisi için modelin
> **hafızaya** ihtiyacı var — `persist=True` tam da bunu sağlıyor.
""")

# ══════════════════════════════════════════════════════════════════
md("""
---
# 6. Sayma — çizgiden kaç tane geçti?

Artık her nesnenin kimliği olduğuna göre sayabiliriz: bir **bölge** çizip
oradan geçen ID'leri sayacağız.
""")

code(r"""
from ultralytics import solutions

VIDEO2 = os.path.join(VIDEO_DIZIN, "people.m4v")

# Videonun ilk karesine bakıp bölgeyi nereye koyacağımıza karar verelim
cap = cv2.VideoCapture(VIDEO2)
ok, ilk_kare = cap.read()
cap.release()
print("Video boyutu:", ilk_kare.shape[1], "x", ilk_kare.shape[0])
goster(ilk_kare, "people.m4v — ilk kare", genislik=8)
""")

code(r"""
# Sayım bölgesi: dikey bir kapı. Koordinatlar yukarıdaki kareye göre.
bolge = [(360, 140), (360, 390), (410, 390), (410, 140)]

onizleme = ilk_kare.copy()
cv2.polylines(onizleme, [np.array(bolge, np.int32)], True, (0, 0, 255), 3)
goster(onizleme, "Sayım bölgesi", genislik=8)
""")

code(r"""
sayaci = solutions.ObjectCounter(
    region=bolge,           # sayım bölgesi: 2 nokta = çizgi, 3+ nokta = poligon
    model="yolo11n.pt",     # hangi model sayacak (yolo26n.pt de olur)
    classes=[0],            # sadece bu sınıflar sayılsın. 0=person, 2=car, 7=truck
    show=False,             # True olsaydı ayrı bir pencere açmaya çalışırdı — Colab'da işe yaramaz
    verbose=False,          # her kare için konsola satır basmasın
    conf=0.25,              # güven eşiği, predict'teki ile aynı anlamda
    tracker="botsort.yaml", # takip algoritması; "bytetrack.yaml" daha hızlı, biraz daha kaba
)

son_sonuc = {}

def say(kare, i):
    r = sayaci(kare)
    son_sonuc["r"] = r          # toplamları sonra yazdırmak için sakla
    return r.plot_im

videoyu_isle(VIDEO2, "/content/04_sayim.mp4", say, max_kare=400)

r = son_sonuc["r"]
print(f"Bölgeye giren : {r.in_count}")
print(f"Bölgeden çıkan: {r.out_count}")
print(f"Sınıf bazında : {r.classwise_count}")

video_goster("/content/04_sayim.mp4")
""")

md("""
Sol üstteki sayaç, bölgeden **giren** ve **çıkan** kişileri ayrı ayrı tutuyor.

Bu, mağaza girişinde müşteri sayan, kavşakta araç sayan, fabrikada ürün sayan
sistemlerin tam olarak yaptığı iş.
""")

# ══════════════════════════════════════════════════════════════════
md("""
---
# 7. Kendi görüntünüzle deneyin

Üç yol var. Hangisi kolayınıza gelirse.
""")

md("""
**a) İnternetten bir görsel adresi**
""")

code(r"""
GORSEL_URL = "https://ultralytics.com/images/bus.jpg"   # kendi linkinizi yazın

s = model(GORSEL_URL, verbose=False)[0]
goster(s.plot(), f"{len(s.boxes)} nesne bulundu")
""")

md("""
**b) Bilgisayardan / telefondan dosya yükleme**
""")

code(r"""
from google.colab import files

yuklenen = files.upload()          # dosya seçme penceresi açılır

# Aynı fotoğrafta parametrelerle oynayabilmek için hepsi burada:
AYAR = dict(
    conf=0.25,        # güven eşiği — düşür: daha çok kutu, çoğu yanlış
    iou=0.70,         # NMS eşiği — yükselt: kopya kutular kalır
    imgsz=640,        # bakılan çözünürlük — büyüt: küçük nesneler görünür, yavaşlar
    max_det=300,      # en fazla kaç nesne döndürülsün
    # classes=[0],    # sadece belirli sınıfları göster (0=person, 2=car, 39=bottle)
    # agnostic_nms=True,  # farklı sınıfların üst üste binen kutularını da temizle
    # half=True,      # yarı hassasiyet — GPU'da hızlandırır
)

for ad in yuklenen:
    s = model(ad, verbose=False, **AYAR)[0]
    goster(s.plot(), f"{ad} — {len(s.boxes)} nesne  (conf={AYAR['conf']})")
""")

md("""
**c) Webcam ile canlı yayın**

Kamera açık kalır, her kare modele gider ve kutular **anlık** olarak görüntünün üstüne
çizilir. Durdurmak için görüntüye tıklayın.

> Tarayıcı kamera izni ister. Çalışmazsa yukarıdaki iki yöntem duruyor.
""")

code(r"""
# Colab'da canlı kamera: JavaScript kareyi tarayıcıdan alır, Python işler,
# sonucu şeffaf bir katman olarak videonun üstüne geri çizer.
from IPython.display import display, Javascript
from google.colab.output import eval_js
from base64 import b64decode, b64encode
import PIL.Image, io

KAMERA_JS = '''
var video = null, div = null, stream = null, tuval = null, katmanImg = null;
var bekleyen = null, kapat = false;

function domuTemizle() {
  if (div !== null) {
    stream.getVideoTracks()[0].stop();
    video.remove(); div.remove();
    video = null; div = null; stream = null; katmanImg = null; tuval = null;
  }
}

function kareDongusu() {
  if (!kapat) window.requestAnimationFrame(kareDongusu);
  if (bekleyen) { bekleyen(tuval.toDataURL("image/jpeg", 0.8)); bekleyen = null; }
}

async function kameraKur() {
  if (div !== null) return stream;
  div = document.createElement("div");
  div.style.cssText = "border:2px solid #333;padding:4px;max-width:640px;position:relative";
  document.body.appendChild(div);

  var bilgi = document.createElement("div");
  bilgi.innerHTML = "<b style='color:#c33'>Durdurmak icin goruntuye tiklayin</b>";
  div.appendChild(bilgi);

  video = document.createElement("video");
  video.style.display = "block";
  video.width = 640;
  video.setAttribute("playsinline", "");
  video.onclick = function() { kapat = true; };
  stream = await navigator.mediaDevices.getUserMedia({video: true});
  div.appendChild(video);
  video.srcObject = stream;
  await video.play();

  tuval = document.createElement("canvas");
  tuval.width = 640; tuval.height = 480;
  window.requestAnimationFrame(kareDongusu);

  katmanImg = document.createElement("img");
  katmanImg.style.cssText = "position:absolute;z-index:2;left:4px;top:" +
                            (bilgi.offsetHeight + 4) + "px;pointer-events:none";
  div.appendChild(katmanImg);

  google.colab.output.setIframeHeight(document.documentElement.scrollHeight, true);
  return "hazir";
}

async function kareAl(katman) {
  if (kapat) { domuTemizle(); kapat = false; return ""; }
  var hazir = new Promise(function(cz) { bekleyen = cz; });
  if (katman != "") { katmanImg.src = katman; }
  tuval.getContext("2d").drawImage(video, 0, 0, 640, 480);
  var sonuc = await hazir;
  return {"img": sonuc};
}
'''


def js_goruntu_al(js_cevap):
    # JS'ten gelen base64 JPEG -> OpenCV BGR dizisi
    ham = b64decode(js_cevap.split(",")[1])
    return cv2.imdecode(np.frombuffer(ham, dtype=np.uint8), flags=1)


def katman_to_bytes(katman_rgba):
    # RGBA overlay -> tarayiciya gonderilecek base64 PNG
    tampon = io.BytesIO()
    PIL.Image.fromarray(katman_rgba, "RGBA").save(tampon, format="png")
    return "data:image/png;base64," + b64encode(tampon.getvalue()).decode()


def kare_al(katman=""):
    return eval_js('kareAl("' + katman + '")')
""")

code(r"""
# Canli tespit dongusu. Goruntuye tiklayinca durur.
model_canli = model_yukle()

display(Javascript(KAMERA_JS))
eval_js("kameraKur()")

katman = ""
kare_sayisi = 0

try:
    while True:
        veri = kare_al(katman)
        if not veri:                       # kullanici tikladi -> cik
            break

        kare = js_goruntu_al(veri["img"])

        # conf=0.4  : canli yayinda esigi biraz yuksek tutmak goruntuyu sakinlestirir
        # imgsz=480 : kucuk tutmak akiciligi artirir
        sonuc = model_canli(kare, conf=0.4, imgsz=480, verbose=False)[0]

        # Seffaf katman: sadece kutular cizilir, arka plan video kalir
        katman_rgba = np.zeros((480, 640, 4), dtype=np.uint8)
        for kutu in sonuc.boxes:
            x1, y1, x2, y2 = [int(v) for v in kutu.xyxy[0]]
            ad  = model_canli.names[int(kutu.cls)]
            gvn = float(kutu.conf)
            cv2.rectangle(katman_rgba, (x1, y1), (x2, y2), (60, 230, 90, 255), 2)
            cv2.putText(katman_rgba, ad + " " + str(round(gvn, 2)),
                        (x1, max(y1 - 6, 12)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (60, 230, 90, 255), 2)

        # Cizilen piksellerin alfasini ac, geri kalani seffaf birak
        katman_rgba[:, :, 3] = (katman_rgba[:, :, :3].max(axis=2) > 0).astype(np.uint8) * 255

        katman = katman_to_bytes(katman_rgba)
        kare_sayisi += 1

except Exception as hata:
    print("Dongu sonlandi:", type(hata).__name__, hata)

print("Canli yayin durdu.", kare_sayisi, "kare islendi.")
""")

# ══════════════════════════════════════════════════════════════════
md("""
---
# 8. Model neyi bulamaz?

YOLO'nun tanıdığı sınıflar **COCO** veri setinden geliyor. Bakalım neler varmış.
""")

code(r"""
isimler = list(model.names.values())
print(f"Toplam {len(isimler)} sınıf:\n")
for i in range(0, len(isimler), 8):
    print("  " + "  ".join(f"{a:14s}" for a in isimler[i:i+8]))
""")

code(r"""
# Dün sınıflandırdığımız çöp türleri bu listede var mı?
dunku_siniflar = ["cardboard", "glass", "metal", "paper", "plastic", "trash"]

print("Dünkü sınıflar COCO'da var mı?\n")
for s in dunku_siniflar:
    durum = "VAR" if s in isimler else "YOK"
    print(f"  {s:12s} {durum}")
""")

md("""
Hiçbiri yok.

> **Demek ki:** Hazır bir tespit modeli sadece **kendisine öğretilmiş** nesneleri bulur.
> Sizin probleminizdeki nesneleri bulmasını istiyorsanız iki yolunuz var:
>
> 1. Birinin o nesneleri etiketleyip eğittiği bir modeli kullanmak
> 2. Kendi verinizi etiketleyip kendiniz eğitmek

Aşağıda birinci yolu göreceğiz.
""")

# ══════════════════════════════════════════════════════════════════
md("""
---
# 9. Dünkü 6 sınıf, bu kez kutu ile

Roboflow Universe, insanların etiketleyip paylaştığı veri setlerinin ve eğitilmiş
modellerin bulunduğu bir depo. Orada **dünkü dersimizin tam olarak aynı sınıflarını**
içeren, tespit için etiketlenmiş bir veri seti var:

**`trash-classification-fg7fz`** — 5742 görüntü
`cardboard, glass, metal, paper, plastic, trash, vinyl`

Bu modeli **eğitmeden**, tek bir API çağrısıyla çalıştırabiliriz.

> Ücretsiz bir Roboflow hesabı ve API anahtarı gerekiyor:
> [app.roboflow.com](https://app.roboflow.com) → Settings → API Keys
""")

code(r"""
!pip install -q inference-sdk

from inference_sdk import InferenceHTTPClient

ROBOFLOW_API_KEY = ""          # <- kendi anahtariniz: app.roboflow.com > Settings > API Keys
MODEL_ID = "trash-classification-fg7fz/2"   # veri seti / surum numarasi

istemci = InferenceHTTPClient(api_url="https://detect.roboflow.com",
                              api_key=ROBOFLOW_API_KEY)

# Dunku dersten gelen cop fotograflarinin hepsini tek tek modele soralim
cop_yollari = sorted(glob(os.path.join(COP_DIZIN, "*.jpg")))
print(len(cop_yollari), "fotograf bulundu\n")

SINIF_RENK = {                 # her sinifa ayri renk (BGR)
    "cardboard": (60, 160, 220), "glass": (200, 160, 60), "metal": (150, 150, 150),
    "paper":     (90, 200, 90),  "plastic": (200, 90, 200), "trash": (80, 80, 200),
}

sekil = plt.figure(figsize=(17, 10))
ozet = []

for i, yol in enumerate(cop_yollari):
    cevap = istemci.infer(yol, model_id=MODEL_ID)
    tahminler = cevap["predictions"]

    gorsel = cv2.imread(yol)
    dosya_adi = os.path.basename(yol)
    gercek = "".join(c for c in dosya_adi if not c.isdigit()).replace(".jpg", "")

    for p in tahminler:
        # Roboflow merkez + genislik/yukseklik verir; kose koordinatina cevirelim
        x1 = int(p["x"] - p["width"] / 2)
        y1 = int(p["y"] - p["height"] / 2)
        x2 = int(p["x"] + p["width"] / 2)
        y2 = int(p["y"] + p["height"] / 2)

        renk = SINIF_RENK.get(p["class"], (60, 200, 90))
        cv2.rectangle(gorsel, (x1, y1), (x2, y2), renk, 3)

        etiket = p["class"] + " " + str(round(p["confidence"], 2))
        (tw, th), _ = cv2.getTextSize(etiket, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
        cv2.rectangle(gorsel, (x1, max(y1 - th - 10, 0)), (x1 + tw + 8, y1), renk, -1)
        cv2.putText(gorsel, etiket, (x1 + 4, max(y1 - 6, th)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        ozet.append({
            "dosya": dosya_adi, "gercek": gercek, "tahmin": p["class"],
            "guven": p["confidence"],
            "kutu": (x1, y1, x2, y2),
            "boyut": (int(p["width"]), int(p["height"])),
        })

    plt.subplot(2, 3, i + 1)
    plt.imshow(cv2.cvtColor(gorsel, cv2.COLOR_BGR2RGB))
    plt.title(dosya_adi + "  ->  " + str(len(tahminler)) + " nesne", fontsize=11)
    plt.axis("off")

plt.suptitle("Roboflow cop tespit modeli — dunku 6 sinif, bu kez kutu ile", fontsize=14)
plt.tight_layout()
plt.show()
""")

code(r"""
# Bulunanlarin dokumu
print(f"{'dosya':22s} {'gercek':11s} {'tahmin':11s} {'guven':>7s}   kutu (x1,y1,x2,y2)")
print("-" * 78)

dogru = 0
for s in ozet:
    isaret = "+" if s["tahmin"] == s["gercek"] else "-"
    dogru += (s["tahmin"] == s["gercek"])
    print(f"{s['dosya']:22s} {s['gercek']:11s} {s['tahmin']:11s} "
          f"{s['guven']:7.3f}   {s['kutu']}  {isaret}")

print(f"\n{dogru} / {len(ozet)} tahmin dosya adiyla ortusuyor")
print("(dosya adi kaba bir olcut — bazi fotograflarda birden fazla nesne olabilir)")
""")

md("""
Dikkat edin: **hiçbir eğitim yapmadık.** Birisi 5742 görüntüyü etiketlemiş, eğitmiş
ve paylaşmış. Biz sadece kullandık.

Kutuların yanındaki sayı modelin güveni. Dünkü sınıflandırıcı da benzer sayılar
veriyordu — fark şu: bu sefer **nesnenin nerede olduğunu da** biliyoruz.

## 9.1 Peki kendimiz eğitseydik ne kadar sürerdi?

Bu, atölyede en çok gelen soru. Somut cevap:

| Senaryo | Süre (T4 GPU) |
|---|---|
| 5742 görüntü, 30 epoch, 640px — **ciddi bir model** | 1,5 – 2,5 saat |
| 5742 görüntü, 10 epoch, 640px — kabul edilebilir | 30 – 50 dk |
| 500 görüntü, 10 epoch, 416px — **gösterim amaçlı** | 4 – 8 dk |

Yani **derste tam eğitim yapmak mümkün değil.** Ama kodun kendisi şaşırtıcı derecede
kısa — asıl iş veriyi hazırlamakta.

> **Önemli:** Dün kullandığımız çöp veri setiyle **bunu yapamayız.** O veri
> *sınıflandırma* için etiketlenmişti: her fotoğrafın bir etiketi vardı ama
> **kutusu yoktu**. Tespit modeli eğitmek için her nesnenin etrafına kutu çizilmiş
> olması gerekir. İşte Roboflow'un yaptığı iş tam olarak bu.
""")

code(r"""
# --- Kendi tespit modelinizi egitmek: kod bu kadar ---
# Derste CALISTIRMIYORUZ (uzun surer). Evde deneyin.

EGITIM_KODU = '''
# 1) Veri setini Roboflow'dan YOLO formatinda indir
from roboflow import Roboflow
rf = Roboflow(api_key="SIZIN_ANAHTARINIZ")
proje = rf.workspace("trashclassification").project("trash-classification-fg7fz")
veri = proje.version(2).download("yolov11")     # klasor + data.yaml olusturur

# 2) Egit — tek satir
from ultralytics import YOLO
model = YOLO("yolo11n.pt")          # hazir agirliklardan basla (transfer learning!)
sonuc = model.train(
    data=veri.location + "/data.yaml",
    epochs=30,          # dusur: daha hizli, daha kaba
    imgsz=640,          # dusur: cok daha hizli
    batch=16,
    patience=10,        # 10 epoch iyilesme yoksa dur
    project="cop_tespit",
)

# 3) Kullan
en_iyi = YOLO("cop_tespit/train/weights/best.pt")
en_iyi.predict("test.jpg", save=True)
'''

print(EGITIM_KODU)
""")

md("""
`model.train()` satırındaki mantık **dünküyle birebir aynı**: hazır ağırlıklardan
başlıyoruz, kendi verimizle ince ayar yapıyoruz. Sadece bu kez çıktı etiket değil,
kutu.

**Kendi nesneniz için yol haritası:**

1. **Topla** — 200-500 fotoğraf. Çeşitlilik sayıdan önemli: farklı açı, ışık, arka plan.
2. **Etiketle** — her nesnenin etrafına kutu çiz. Fotoğraf başına yarım-bir dakika.
3. **Eğit** — yukarıdaki kod. Küçük veriyle 10-20 dakika.
4. **Bak ve düzelt** — modelin kaçırdığı örnekleri veri setine ekle, tekrar eğit.

> Etiketleme, işin en sıkıcı ama en belirleyici kısmıdır. Model kalitesi neredeyse
> tamamen etiket kalitesine bağlıdır.
""")

# ══════════════════════════════════════════════════════════════════
md(f"""
---
## 9.2 Bundan sonrası: yazarak

{gorsel("kapanis.png", 980)}
""")

md("""
Bugün yaptığımız her şey — veri seti bulmak, modeli çalıştırmak, sonuçlara bakmak —
artık **konuşarak** da yapılabiliyor. Roboflow'un Claude bağlantısı 67 araç sunuyor:
Universe'de arama, etiketleme işi açma, otomatik ön etiketleme, model eğitme, eğitimi
izleme, sonuçları değerlendirme, hazır modelle tahmin.

> Bu atölyede kullandığımız çöp tespit veri setini de böyle bulduk.

**Ama şunu net söyleyeyim:** bu, kod bilmeyi gereksiz kılmıyor. Tam tersi —
`conf` nedir, NMS ne yapar, neden `imgsz` artırınca küçük nesneler görünür,
etiketlemenin neden en kritik iş olduğunu bilmiyorsanız, ne isteyeceğinizi de
bilemezsiniz. Bugün öğrendikleriniz o yüzden değerli.

---
# 10. Toparlayalım

| | Ne yapar | Ne yapamaz |
|---|---|---|
| **Sınıflandırma** | Resmin tamamına tek etiket | Kaç tane, nerede |
| **Tespit** | Her nesneye kutu + etiket | Bu, az önceki mi |
| **Takip** | Nesnelere kimlik verir | Kendi başına saymaz |
| **Sayma** | Bölgeden geçenleri sayar | Öğretilmemiş nesneyi bulamaz |

**Aklınızda kalsın:**

- `conf` ve `iou` sonucu doğrudan değiştirir — "doğru" değer probleme göre değişir.
- Hazır model sadece öğretildiği sınıfları bulur. COCO'da 80 sınıf var, sizinki
  muhtemelen yok.
- Kendi nesnenizi bulmak istiyorsanız iş etiketlemeden geçiyor.

**Bundan sonra deneyebilecekleriniz:**

- `yolo26n.pt` yerine `yolo26s.pt` veya `yolo26m.pt` — daha yavaş, daha doğru
- `model.track(..., tracker="botsort.yaml")` — farklı takip algoritması
- Segmentasyon modeli (`-seg` ekli) — kutu yerine piksel maskesi
- Poz tahmini (`-pose` ekli) — insan iskeleti
- Kendi veri setinizi etiketleyip eğitmek
""")

md("""
---
---

# Bonus — Köpek duygusu tespiti

> Bir öğrencinin sorusu üzerine eklendi: *"Saldırgan bir köpeği tespit edebilir miyiz?"*

Aynı yöntem, tamamen farklı bir problem. Roboflow Universe'de köpek duygusu için
etiketlenmiş **17.872 görüntülük** bir veri seti var — dört sınıf: `angry`, `happy`,
`relaxed`, `sad`.

**Neden bu model?** Aynı konuda üç model daha denedim; bu hem en çok veriye sahip
(17.872'ye karşı 1.765 ve 75) hem de test ettiğimde sınıfları gerçekten ayırt etti.
""")

code(r"""
# Test icin veri setinin kendi goruntulerini kullaniyoruz (herkese acik URL'ler)
KOPEK_MODEL = "dog-emotion-ovhny/2"

kopek_gorselleri = [
    # (URL, veri setindeki gercek etiket)
    ("https://source.roboflow.com/yAhbdfctUiTr4NpZ9RBEM1xoAWq2/QrsajeXFBd3vi0fJMH4Y/original.jpg", "angry"),
    ("https://source.roboflow.com/yAhbdfctUiTr4NpZ9RBEM1xoAWq2/9XJxrNqgxuQWRUH0U3XB/original.jpg", "angry"),
    ("https://source.roboflow.com/yAhbdfctUiTr4NpZ9RBEM1xoAWq2/g0ldy3URJdCkMWUaHylj/original.jpg", "angry"),
    ("https://source.roboflow.com/yAhbdfctUiTr4NpZ9RBEM1xoAWq2/atsUgfq2kIH9uWNlHQj2/original.jpg", "relaxed"),
    ("https://source.roboflow.com/yAhbdfctUiTr4NpZ9RBEM1xoAWq2/XSQaWPBOY1vX237WtYzl/original.jpg", "relaxed"),
    ("https://source.roboflow.com/yAhbdfctUiTr4NpZ9RBEM1xoAWq2/CDQzlmQ3inCYm1SQ30lR/original.jpg", "relaxed"),
]

# Duygu basina renk (BGR) — kirmizi = dikkat
DUYGU_RENK = {"angry": (60, 60, 220), "sad": (180, 120, 60),
              "happy": (80, 200, 80), "relaxed": (200, 160, 60)}

plt.figure(figsize=(17, 10))

for i, (url, gercek) in enumerate(kopek_gorselleri):
    # NOT: infer() confidence parametresi almaz. Esigi degistirmek isterseniz
    # yapilandirmayi istemciye verirsiniz:
    #   from inference_sdk import InferenceConfiguration
    #   istemci_dusuk = istemci.with_configuration(
    #       InferenceConfiguration(confidence_threshold=0.15))
    # Varsayilan esik bu model icin yeterli calisiyor.
    cevap = istemci.infer(url, model_id=KOPEK_MODEL)

    ham = urllib.request.urlopen(url).read()
    gorsel = cv2.imdecode(np.frombuffer(ham, np.uint8), cv2.IMREAD_COLOR)

    if cevap["predictions"]:
        p = max(cevap["predictions"], key=lambda t: t["confidence"])
        x1 = int(p["x"] - p["width"] / 2);  y1 = int(p["y"] - p["height"] / 2)
        x2 = int(p["x"] + p["width"] / 2);  y2 = int(p["y"] + p["height"] / 2)
        renk = DUYGU_RENK.get(p["class"], (120, 120, 120))
        cv2.rectangle(gorsel, (x1, y1), (x2, y2), renk, 4)
        baslik = p["class"] + " " + str(round(p["confidence"], 2)) + "   (gercek: " + gercek + ")"
        dogru_mu = (p["class"] == gercek)
    else:
        baslik = "tespit yok   (gercek: " + gercek + ")"
        dogru_mu = False

    plt.subplot(2, 3, i + 1)
    plt.imshow(cv2.cvtColor(gorsel, cv2.COLOR_BGR2RGB))
    plt.title(baslik, fontsize=11, color="green" if dogru_mu else "red")
    plt.axis("off")

plt.suptitle("Kopek duygu tespiti — dog-emotion-ovhny/2", fontsize=14)
plt.tight_layout()
plt.show()
""")

md("""
## Kendi köpek fotoğrafınızla deneyin
""")

code(r"""
# Kendi fotografinizi yukleyin
yuklenen = files.upload()

for ad in yuklenen:
    cevap = istemci.infer(ad, model_id=KOPEK_MODEL)
    gorsel = cv2.imread(ad)

    print(ad, "->", len(cevap["predictions"]), "tespit")
    for p in sorted(cevap["predictions"], key=lambda t: -t["confidence"]):
        print(f"   {p['class']:9s} {p['confidence']:.3f}")
        x1 = int(p["x"] - p["width"] / 2);  y1 = int(p["y"] - p["height"] / 2)
        x2 = int(p["x"] + p["width"] / 2);  y2 = int(p["y"] + p["height"] / 2)
        renk = DUYGU_RENK.get(p["class"], (120, 120, 120))
        cv2.rectangle(gorsel, (x1, y1), (x2, y2), renk, 4)
        cv2.putText(gorsel, p["class"] + " " + str(round(p["confidence"], 2)),
                    (x1, max(y1 - 8, 16)), cv2.FONT_HERSHEY_SIMPLEX, 0.8, renk, 2)

    goster(gorsel, ad)
""")

md("""
## Bu modelin sınırları — dürüst konuşalım

Amaç "ısırmak üzere olan köpeği tespit etmek" ise, bu modelin **o iş için yeterli
olmadığını** bilerek kullanmak gerekir. Nedenleri:

**1. Model duyguyu değil, etiketi öğrendi.**
Birileri fotoğraflara bakıp "bu kızgın" demiş. Model o insanların kararını taklit
ediyor. Köpeğin gerçek niyetini değil.

**2. Fotoğraf, davranışın tamamı değil.**
Köpek uzmanları saldırganlığı **duruştan, kuyruktan, tüylerden, hareketten ve sesten**
okur. Tek karelik bir fotoğrafta bunların çoğu yok. Dişini gösteren bir köpek
oynuyor da olabilir.

**3. Sınıflar bulanık.**
`angry` ile `sad` arasındaki sınırı etiketleyen kişi çizmiş. Başka biri farklı çizerdi.

**4. Hata bedeli çok yüksek.**
Çöp sınıflandırırken yanlış tahmin canını yakmaz. Burada **yanlış negatif** — saldırgan
köpeği kaçırmak — birinin yaralanması demektir. Böyle bir sistemde `conf` eşiğini
düşürmek ve her uyarıyı bir insana doğrulatmak gerekir.

> **Söylenecek doğru cümle:** "Bu model fotoğraftaki köpeğin ifadesini dört kategoriden
> birine sokuyor." **Söylenmemesi gereken:** "Bu model saldırgan köpekleri tespit eder."

**Ciddi bir sistem için ne gerekirdi?**

| Eksik | Ne yapılmalı |
|---|---|
| Tek kare yetmiyor | Video ve **takip** — duruş zaman içinde nasıl değişiyor |
| Vücut dili yok | Poz tahmini (`-pose` modelleri): kuyruk, kulak, baş pozisyonu |
| Uzman etiketi yok | Veteriner/davranış uzmanı etiketlemesi |
| Ses yok | Hırlama sesi, çok güçlü bir sinyal |
| Bağlam yok | Köpek kime bakıyor, mesafe ne, tasmalı mı |

> Bu tam da dersin başındaki fikre bağlanıyor: **model sadece kendisine gösterileni
> öğrenir.** Ona tek kare fotoğraf gösterirseniz, tek kare fotoğraftan çıkarılabilecek
> kadarını öğrenir.
""")

# ══════════════════════════════════════════════════════════════════
nb = {"cells": hucreler,
      "metadata": {"accelerator": "GPU",
                   "colab": {"provenance": [], "gpuType": "T4", "toc_visible": True},
                   "kernelspec": {"display_name": "Python 3", "name": "python3"},
                   "language_info": {"name": "python"}},
      "nbformat": 4, "nbformat_minor": 0}

with open(CIKTI, "w", encoding="utf-8") as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print(f"{CIKTI} — {len(hucreler)} hücre "
      f"({sum(h['cell_type']=='code' for h in hucreler)} kod), "
      f"{os.path.getsize(CIKTI)//1024} KB")
