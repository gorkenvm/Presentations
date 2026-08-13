"""CNN mimarisi: katman katman ilerleyen animasyonlu GIF üretir."""
import zlib
from PIL import Image, ImageDraw, ImageFont

SRC = "/sessions/peaceful-lucid-dijkstra/mnt/cnn2/resimler/cnnarchitecture.paint"
PNG_OUT = "/sessions/peaceful-lucid-dijkstra/mnt/cnn2/resimler/cnn_mimari.png"
GIF_OUT = "/sessions/peaceful-lucid-dijkstra/mnt/cnn2/resimler/cnn_mimari.gif"

W, H = 1109, 449
FONT_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_R = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def heif_unci_oku(path):
    """Windows Paint'in kaydettiği sıkıştırılmamış (deflate + BGRA) HEIF dosyasını okur."""
    data = open(path, "rb").read()
    mdat = data[565 + 8:]                      # mdat kutusunun içeriği
    ham = zlib.decompressobj(-15).decompress(mdat)   # ham deflate
    im = Image.frombytes("RGBA", (W, H), ham)
    b, g, r, a = im.split()                    # bileşen sırası BGRA
    return Image.merge("RGBA", (r, g, b, a)).convert("RGB")


# --- Aşamalar: (bitiş_x, vurgu_kutusu(x0,y0,x1,y1) veya None, başlık, açıklama) ---
ASAMALAR = [
    (190, (25, 20, 185, 300), "1 · Girdi (Input)",
     "Görüntü bir piksel matrisidir:  yükseklik × genişlik × kanal  (224×224×3)"),
    (312, (192, 60, 310, 300), "2 · Convolution + ReLU",
     "Filtre (kernel) görüntü üzerinde gezer → öznitelik haritası (feature map) çıkar"),
    (640, (315, 60, 635, 300), "3 · Pooling  (+ tekrarlanan bloklar)",
     "Boyut küçülür, önemli bilgi kalır. Conv → ReLU → Pooling bloğu üst üste tekrarlanır"),
    (700, (655, 55, 700, 300), "4 · Flatten",
     "Matrisler tek boyutlu bir vektöre serilir → yapay sinir ağının istediği format"),
    (918, (700, 5, 915, 330), "5 · Fully Connected (Dense)",
     "Çıkarılan öznitelikler birleştirilir, karar burada verilir"),
    (W, (918, 40, 1065, 300), "6 · Softmax → Çıktı",
     "Her sınıf için olasılık:  Zebra 0.7 · Horse 0.2 · Dog 0.1"),
]

BANT = 78          # alt açıklama bandının yüksekliği
GOVDE = 438        # orijinal görselin alt siyah çizgisi kırpılır
RENK = (196, 62, 42)

taban = heif_unci_oku(SRC)
taban.save(PNG_OUT)
taban = taban.crop((0, 0, W, GOVDE))
solmus = Image.blend(taban, Image.new("RGB", taban.size, "white"), 0.82)

f_bas = ImageFont.truetype(FONT_B, 26)
f_ack = ImageFont.truetype(FONT_R, 20)

kareler = []
for i, (x_son, kutu, baslik, aciklama) in enumerate(ASAMALAR):
    kare = Image.new("RGB", (W, GOVDE + BANT), "white")
    kare.paste(solmus, (0, 0))
    kare.paste(taban.crop((0, 0, x_son, GOVDE)), (0, 0))   # açığa çıkan kısım
    d = ImageDraw.Draw(kare)

    if kutu:
        d.rectangle(kutu, outline=RENK, width=3)

    # ilerleme çubuğu
    y = GOVDE + 4
    d.rectangle([0, y, W, y + 5], fill=(226, 226, 226))
    d.rectangle([0, y, int(W * (i + 1) / len(ASAMALAR)), y + 5], fill=RENK)

    d.text((22, GOVDE + 18), baslik, font=f_bas, fill=RENK)
    d.text((22, GOVDE + 50), aciklama, font=f_ack, fill=(45, 45, 45))
    kareler.append(kare.convert("P", palette=Image.ADAPTIVE, colors=96))

kareler = [k.resize((900, int(900*(GOVDE+BANT)/W))) for k in kareler]
kareler[0].save(GIF_OUT, save_all=True, append_images=kareler[1:],
                duration=[2300] * (len(kareler) - 1) + [3600], loop=0, optimize=True)

import os
print("PNG:", os.path.getsize(PNG_OUT) // 1024, "KB")
print("GIF:", os.path.getsize(GIF_OUT) // 1024, "KB", len(kareler), "kare")
