"""Tek sayfalık 'görüntü = sayı matrisi' görseli: piksel, gri tonlama, renkli."""
from PIL import Image, ImageDraw, ImageFont
import os

DIZIN = "/sessions/peaceful-lucid-dijkstra/mnt/cnn2/resimler"
FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
K = 2                                    # 2× çiz, sonra küçült → kenarlar yumuşasın

ZEMIN, KOYU, GRI, ACIK = (245,245,245), (51,51,51), (130,130,130), (207,207,207)
ZEYTIN = (140,130,40)
f_bas  = ImageFont.truetype(FB, 27*K)
f_alt  = ImageFont.truetype(FR, 16*K)
f_et   = ImageFont.truetype(FB, 15*K)
f_h    = ImageFont.truetype(FB, 13*K)
f_not  = ImageFont.truetype(FR, 15*K)

# 6×6 gri tonlamalı örnek
GRI6 = [[ 30, 30, 30, 30, 30, 30],
        [ 30,210,210,210,210, 30],
        [ 30,210, 40, 40,210, 30],
        [ 30,210,210,210,210, 30],
        [ 30,210, 40, 40,210, 30],
        [ 30, 30, 30, 30, 30, 30]]

# 4×4 renkli örnek (RGB)
KIR, YES, MAV, SAR = (220,40,40), (40,180,60), (50,90,200), (240,200,50)
RENK4 = [[KIR,KIR,YES,YES],
         [KIR,KIR,YES,YES],
         [MAV,MAV,SAR,SAR],
         [MAV,MAV,SAR,SAR]]


def orta(d, kutu, s, font, renk):
    x0,y0,x1,y1 = kutu
    l,t,r,b = d.textbbox((0,0), s, font=font)
    d.text((x0+(x1-x0-(r-l))/2-l, y0+(y1-y0-(b-t))/2-t), s, font=font, fill=renk)


def kutucuk(d, x, y, h, dolgu, metin, yazi_renk):
    d.rectangle((x, y, x+h, y+h), fill=dolgu, outline=ACIK)
    if metin is not None:
        orta(d, (x, y, x+h, y+h), metin, f_h, yazi_renk)


W, Y = 1180*K, 620*K
im = Image.new("RGB", (W, Y), ZEMIN)
d = ImageDraw.Draw(im)
d.text((42*K, 26*K), "Görüntü = sayı matrisi", font=f_bas, fill=KOYU)
d.text((42*K, 62*K), "Bilgisayar resmi görmez; piksel değerlerini görür. "
                     "0 = siyah, 255 = beyaz.", font=f_alt, fill=GRI)

gy, h = 140*K, 42*K

# ── SOL: gri tonlamalı ────────────────────────────────────────────────────
gx = 42*K
d.text((gx, gy-26*K), "GRİ TONLAMALI  6×6×1", font=f_et, fill=KOYU)
for r in range(6):
    for c in range(6):
        v = GRI6[r][c]
        kutucuk(d, gx+c*h, gy+r*h, h, (v,v,v), str(v),
                (255,255,255) if v < 128 else (40,40,40))
d.text((gx, gy+6*h+16*K), "Piksel başına tek sayı.", font=f_not, fill=GRI)

# ── ORTA: renkli ──────────────────────────────────────────────────────────
rx = gx + 6*h + 70*K
d.text((rx, gy-26*K), "RENKLİ  4×4×3", font=f_et, fill=KOYU)
for r in range(4):
    for c in range(4):
        kutucuk(d, rx+c*h, gy+r*h, h, RENK4[r][c], None, None)
d.text((rx, gy+4*h+16*K), "Piksel başına üç sayı.", font=f_not, fill=GRI)

# ── SAĞ: üç kanal matrisi ─────────────────────────────────────────────────
kh = 30*K
kx0 = rx + 4*h + 50*K
for k, (ad, renk) in enumerate([("R (kırmızı)", (192,60,60)),
                                ("G (yeşil)", (40,150,70)),
                                ("B (mavi)", (50,90,200))]):
    kx = kx0 + k*(4*kh + 32*K)
    d.text((kx, gy-26*K), ad, font=f_et, fill=renk)
    for r in range(4):
        for c in range(4):
            kutucuk(d, kx+c*kh, gy+r*kh, kh, (252,252,252),
                    str(RENK4[r][c][k]), renk)
d.text((kx0, gy+4*kh+16*K),
       "Aynı görüntü, üç ayrı matris.", font=f_not, fill=GRI)

# ── alt bant ──────────────────────────────────────────────────────────────
yb = 470*K
d.line([(42*K, yb), (W-42*K, yb)], fill=ACIK, width=2)
d.text((42*K, yb+18*K),
       "Bir CNN'in girdisi her zaman  yükseklik × genişlik × kanal  şeklinde "
       "bir sayı bloğudur.", font=f_not, fill=KOYU)
d.text((42*K, yb+46*K),
       "Gri tonlamalı: 224×224×1          Renkli: 224×224×3",
       font=f_et, fill=KOYU)
d.text((42*K, yb+78*K),
       "→ Bu yüzden evrişim filtresi de girdiyle aynı derinlikte olmak zorunda.",
       font=f_not, fill=ZEYTIN)

im = im.resize((W//K, Y//K), Image.LANCZOS)
yol = os.path.join(DIZIN, "piksel.png")
im.save(yol)
print("piksel.png", os.path.getsize(yol)//1024, "KB", im.size)
