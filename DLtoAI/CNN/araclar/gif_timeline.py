"""CNN mimarileri zaman çizelgesi (content.md, Chapter 4 ve sonrası).

Kompakt sürüm: kutuda tek satırlık tanıtım. Modellerin ayrıntılı
"neden önemliydi / bugün ne durumda" anlatımı konuşmacı notlarında.
"""
import colorsys
import os

from PIL import Image, ImageDraw, ImageFont

DIZIN = "/sessions/peaceful-lucid-dijkstra/mnt/cnn2/resimler"
FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
K = 2

ZEMIN, KOYU, GRI, ACIK = (245,245,245), (51,51,51), (125,125,125), (205,205,205)
YESIL, TURUNCU, SOLUK = (46,132,72), (196,124,30), (150,150,150)

f_bas  = ImageFont.truetype(FB, 28*K)
f_alt  = ImageFont.truetype(FR, 16*K)
f_lane = ImageFont.truetype(FB, 18*K)
f_ad   = ImageFont.truetype(FB, 17*K)
f_yil  = ImageFont.truetype(FB, 15*K)
f_not  = ImageFont.truetype(FR, 13*K)
f_sim  = ImageFont.truetype(FB, 20*K)
f_efs  = ImageFont.truetype(FR, 14*K)

SIMGE = {2: ("●", YESIL), 1: ("◐", TURUNCU), 0: ("○", SOLUK)}

SINIF = [
    ("1998", "LeNet-5", 0, "İlk CNN; el yazısı rakam tanıma"),
    ("2012", "AlexNet", 0, "GPU + ReLU + dropout; CNN çığırını açtı"),
    ("2014", "VGG-16 / VGG-19", 1, "Sadece 3×3 filtre; basit ama çok ağır (138M)"),
    ("2014", "GoogLeNet (Inception v1)", 1, "Inception bloğu; 1×1 ile boyut indirgeme"),
    ("2015", "ResNet", 2, "Kısayol bağlantısı; çok derin ağlar mümkün oldu"),
    ("2016", "Inception-ResNet v2", 0, "Inception + kısayol; güçlü ama hantal"),
    ("2016", "Xception", 1, "Depthwise separable evrişim"),
    ("2017", "DenseNet", 1, "Her katman kendinden öncekilerin hepsine bağlı"),
    ("2017", "MobileNet", 2, "Mobil/gömülü cihaz; az parametre"),
    ("2018", "MobileNetV2", 2, "Ters residual; transfer learning'de çok sık"),
    ("2019", "EfficientNet", 2, "Derinlik + genişlik + çözünürlük birlikte ölçeklenir"),
    ("2022", "ConvNeXt", 2, "Modern CNN; Vision Transformer ile yarışıyor"),
]

TESPIT = [
    ("klasik", "Sliding Window", 0, "Pencereyi tek tek gezdir; çok yavaş"),
    ("2014", "R-CNN", 0, "~2000 bölge önerisi, her birine ayrı CNN"),
    ("2015", "Fast R-CNN", 0, "Tek CNN geçişi + ROI pooling"),
    ("2015", "Faster R-CNN", 1, "Bölge önerisi de ağın içinde (RPN)"),
    ("2016", "YOLO v1", 0, "Tek geçişte tespit; anlık tespitin başlangıcı"),
    ("2016", "SSD", 1, "Çok ölçekli tek geçiş"),
    ("2017", "Mask R-CNN", 2, "Tespit + piksel maskesi (instance segmentation)"),
    ("2017", "RetinaNet", 1, "Focal loss; sınıf dengesizliğine çözüm"),
    ("2018", "YOLOv3", 0, "Darknet-53; uzun süre fiili standart"),
    ("2023", "YOLOv8", 2, "Ultralytics; sahada hâlâ çok yaygın"),
    ("2026", "YOLO26", 2, "NMS'siz uçtan uca; güncel sürüm"),
]

KAPSAM_DISI = {"ConvNeXt", "YOLO26"}


def renk(i, n, s=0.30, v=1.0):
    r, g, b = colorsys.hsv_to_rgb((i / n * 0.92 + 0.02) % 1.0, s, v)
    return int(r * 255), int(g * 255), int(b * 255)


def koyu_ton(i, n):
    r, g, b = colorsys.hsv_to_rgb((i / n * 0.92 + 0.02) % 1.0, 0.75, 0.62)
    return int(r * 255), int(g * 255), int(b * 255)


SATIR = 62 * K
KUTU_G = 430 * K
BAS = 168 * K


def serit(d, x0, kayitlar, baslik, altbaslik):
    d.text((x0, 118 * K), baslik, font=f_lane, fill=KOYU)
    d.text((x0, 142 * K), altbaslik, font=f_efs, fill=GRI)
    eksen = x0 + 56 * K
    d.line([(eksen, BAS + 10 * K), (eksen, BAS + (len(kayitlar) - 1) * SATIR + 40 * K)],
           fill=ACIK, width=2)

    n = len(kayitlar)
    for i, (yil, ad, durum, notu) in enumerate(kayitlar):
        y = BAS + i * SATIR
        ac, ko = renk(i, n), koyu_ton(i, n)
        kapsam = ad in KAPSAM_DISI

        d.text((x0, y + 12 * K), yil, font=f_yil, fill=GRI)
        d.ellipse((eksen - 6 * K, y + 18 * K, eksen + 6 * K, y + 30 * K),
                  fill=ko, outline=ZEMIN, width=2)

        kx = eksen + 22 * K
        kutu = (kx, y, kx + KUTU_G, y + 48 * K)
        if kapsam:
            d.rectangle(kutu, fill=ZEMIN, outline=ko, width=2)
            for xx in range(int(kx), int(kx + KUTU_G), 12 * K):
                d.line([(xx, y), (min(xx + 6 * K, kx + KUTU_G), y)], fill=ko, width=3)
        else:
            d.rectangle(kutu, fill=ac, outline=ko)
            d.rectangle((kx, y, kx + 5 * K, y + 48 * K), fill=ko)

        d.text((kx + 14 * K, y + 7 * K), ad, font=f_ad, fill=ko)
        d.text((kx + 14 * K, y + 28 * K), notu, font=f_not, fill=(70, 70, 70))

        sim, srenk = SIMGE[durum]
        d.text((kx + KUTU_G + 14 * K, y + 12 * K), sim, font=f_sim, fill=srenk)
        if kapsam:
            d.text((kx + KUTU_G + 40 * K, y + 16 * K), "ders dışı",
                   font=f_efs, fill=SOLUK)


W = 1300 * K
Y = BAS + 12 * SATIR + 96 * K
im = Image.new("RGB", (W, Y), ZEMIN)
d = ImageDraw.Draw(im)

d.text((42 * K, 26 * K), "CNN Mimarileri — Zaman Çizelgesi", font=f_bas, fill=KOYU)
d.text((42 * K, 66 * K),
       "Simge bugünkü kullanım durumunu gösterir; kutu rengi sadece ayırt etmek için.",
       font=f_alt, fill=GRI)

ex = 42 * K
for durum, metin in [(2, "bugün yaygın kullanılıyor"),
                     (1, "niş / belirli durumlarda"),
                     (0, "tarihsel — artık tercih edilmiyor")]:
    sim, srenk = SIMGE[durum]
    d.text((ex, 88 * K), sim, font=f_sim, fill=srenk)
    d.text((ex + 24 * K, 92 * K), metin, font=f_efs, fill=GRI)
    ex += (24 + len(metin) * 7 + 34) * K

serit(d, 42 * K, SINIF, "SINIFLANDIRMA  (backbone)", "Görüntüde ne var? — Chapter 4")
serit(d, 660 * K, TESPIT, "NESNE TESPİTİ", "Ne var, nerede? — Chapter 6")

im = im.resize((W // K, Y // K), Image.LANCZOS)
yol = os.path.join(DIZIN, "timeline.png")
im.save(yol)
print("timeline.png", os.path.getsize(yol) // 1024, "KB", im.size)
