"""ResNet-50 mimarisi: uçtan uca akış + bottleneck bloğunun içi."""
import os

from PIL import Image, ImageDraw, ImageFont

DIZIN = "/sessions/peaceful-lucid-dijkstra/mnt/cnn2/resimler"
FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
K = 2

ZEMIN, KOYU, GRI, ACIK = (245,245,245), (51,51,51), (125,125,125), (200,200,200)
MAVI,  MAVI_A  = (52,108,176), (198,222,246)
KIRMIZI, KIRMIZI_A = (176,62,52), (250,214,208)
YESIL, YESIL_A = (46,124,80), (206,236,216)
TURUNCU, TURUNCU_A = (196,124,30), (252,232,204)
GRI_A = (228,228,228)
ZEYTIN = (140,130,40)

f_bas = ImageFont.truetype(FB, 26*K)
f_alt = ImageFont.truetype(FR, 15*K)
f_et  = ImageFont.truetype(FB, 13*K)
f_kck = ImageFont.truetype(FR, 11*K)
f_kb  = ImageFont.truetype(FB, 11*K)
f_not = ImageFont.truetype(FR, 14*K)
f_sem = ImageFont.truetype(FB, 22*K)


def orta_x(d, x0, x1, y, s, font, renk):
    l,t,r,b = d.textbbox((0,0), s, font=font)
    d.text((x0 + (x1-x0-(r-l))/2 - l, y), s, font=font, fill=renk)


def slab(d, x, orta_y, en, boy, dolgu, kenar, derinlik=9*K):
    """Basit 3B dilim: ön yüz + üst ve sağ eğik yüzler."""
    y0, y1 = orta_y - boy//2, orta_y + boy//2
    d.polygon([(x, y0), (x+derinlik, y0-derinlik),
               (x+en+derinlik, y0-derinlik), (x+en, y0)], fill=dolgu, outline=kenar)
    d.polygon([(x+en, y0), (x+en+derinlik, y0-derinlik),
               (x+en+derinlik, y1-derinlik), (x+en, y1)], fill=dolgu, outline=kenar)
    d.rectangle((x, y0, x+en, y1), fill=dolgu, outline=kenar)
    return x + en + derinlik


def ok(d, x0, y, x1, renk=GRI, kal=2*K):
    d.line([(x0,y),(x1-5*K,y)], fill=renk, width=kal)
    d.polygon([(x1,y),(x1-7*K,y-4*K),(x1-7*K,y+4*K)], fill=renk)


W, Y = 1180*K, 600*K
im = Image.new("RGB", (W, Y), ZEMIN)
d = ImageDraw.Draw(im)
d.text((42*K, 24*K), "ResNet-50 mimarisi", font=f_bas, fill=KOYU)
d.text((42*K, 60*K),
       "Derinleştikçe en × boy yarıya iner, kanal sayısı ikiye katlanır. "
       "Her aşamanın üzerinden bir kısayol atlar.", font=f_alt, fill=GRI)

# Etiketler sabit satırlarda ve şaşırtmalı (bir üstte bir altta) —
# dilimler dar, etiketler geniş; yan yana yazılırsa üst üste biniyor.
UST_A, UST_B = 100*K, 122*K
KAVIS_Y = 150*K
ORTA    = 262*K
ALT_A, ALT_B = 348*K, 372*K

x = 52*K
ADIMLAR = [
    (16*K, 150*K, GRI_A,     GRI,     "224×224×3",  "girdi",           False),
    (24*K,  98*K, MAVI_A,    MAVI,    "112×112×64", "Conv 7×7, s2",    False),
    (24*K,  66*K, KIRMIZI_A, KIRMIZI, "56×56×64",   "MaxPool 3×3, s2", False),
    (40*K,  66*K, MAVI_A,    MAVI,    "56×56×256",  "Stage 1  ×3",     True),
    (52*K,  48*K, MAVI_A,    MAVI,    "28×28×512",  "Stage 2  ×4",     True),
    (64*K,  34*K, MAVI_A,    MAVI,    "14×14×1024", "Stage 3  ×6",     True),
    (76*K,  24*K, MAVI_A,    MAVI,    "7×7×2048",   "Stage 4  ×3",     True),
    (76*K,  12*K, TURUNCU_A, TURUNCU, "1×1×2048",   "Global Avg Pool", False),
]

for i, (en, boy, dolgu, kenar, ust, alt, kisayol) in enumerate(ADIMLAR):
    if i:
        ok(d, x + 6*K, ORTA, x + 40*K)
        x += 48*K
    sol = x
    x = slab(d, x, ORTA, en, boy, dolgu, kenar)
    renk = KIRMIZI if dolgu is KIRMIZI_A else (TURUNCU if dolgu is TURUNCU_A else MAVI)
    orta_x(d, sol, x, UST_A if i % 2 == 0 else UST_B, ust, f_kb, KOYU)
    orta_x(d, sol, x, ALT_A if i % 2 == 0 else ALT_B, alt, f_et, renk)
    d.line([((sol+x)//2, (UST_A if i % 2 == 0 else UST_B) + 18*K),
            ((sol+x)//2, ORTA - boy//2 - 6*K)], fill=(225,225,225), width=1)
    if kisayol:
        d.arc((sol - 8*K, KAVIS_Y, x + 8*K, KAVIS_Y + 46*K), 180, 360,
              fill=YESIL, width=3)
        d.polygon([(x + 8*K, KAVIS_Y + 23*K), (x + 3*K, KAVIS_Y + 11*K),
                   (x + 13*K, KAVIS_Y + 11*K)], fill=YESIL)

ok(d, x + 6*K, ORTA, x + 44*K)
x += 52*K
d.rectangle((x, ORTA - 46*K, x + 22*K, ORTA + 46*K), fill=YESIL_A, outline=YESIL)
orta_x(d, x, x + 22*K, UST_A, "1000", f_kb, KOYU)
orta_x(d, x, x + 22*K, ALT_A, "FC + Softmax", f_et, YESIL)

d.text((52*K, 406*K),
       "Toplam 50 ağırlıklı katman:  1 (baştaki conv)  +  16 blok × 3 conv  +  1 (FC)",
       font=f_not, fill=(70,70,70))
d.text((52*K, 432*K),
       "→ Yeşil kavisler kısayol bağlantıları: her aşamanın girdisi, çıktısına eklenir.",
       font=f_not, fill=ZEYTIN)

# ── alt: bottleneck bloğunun içi ──────────────────────────────────────────
d.line([(42*K, 470*K), (W - 42*K, 470*K)], fill=ACIK, width=2)
d.text((42*K, 482*K), "Bir bloğun içi (bottleneck)", font=f_et, fill=KOYU)

by = 528*K
bx = 52*K
d.text((bx, by + 4*K), "x", font=f_sem, fill=KOYU)
bx += 34*K
for etiket, alt in [("1×1, 64", "kanalı düşür"),
                    ("3×3, 64", "asıl iş, ucuz"),
                    ("1×1, 256", "kanalı geri aç")]:
    ok(d, bx - 26*K, by + 16*K, bx - 6*K)
    d.rectangle((bx, by, bx + 108*K, by + 34*K), fill=MAVI_A, outline=MAVI)
    orta_x(d, bx, bx + 108*K, by + 8*K, etiket, f_et, MAVI)
    orta_x(d, bx, bx + 108*K, by + 40*K, alt, f_kck, GRI)
    bx += 134*K

ok(d, bx - 26*K, by + 16*K, bx - 6*K)
d.ellipse((bx, by, bx + 32*K, by + 32*K), fill=(255,255,255), outline=YESIL, width=3)
orta_x(d, bx, bx + 32*K, by + 3*K, "+", f_sem, YESIL)
ok(d, bx + 38*K, by + 16*K, bx + 70*K)
d.text((bx + 76*K, by + 6*K), "ReLU", font=f_et, fill=KOYU)

ky = by - 22*K
d.line([(64*K, by + 2*K), (64*K, ky), (bx + 16*K, ky)], fill=YESIL, width=3)
d.line([(bx + 16*K, ky), (bx + 16*K, by - 6*K)], fill=YESIL, width=3)
d.polygon([(bx + 16*K, by + 2*K), (bx + 10*K, by - 10*K), (bx + 22*K, by - 10*K)],
          fill=YESIL)

d.text((bx + 150*K, by + 2*K),
       "İlk 1×1 kanalı 256'dan 64'e indirir; pahalı 3×3", font=f_kck, fill=(80,80,80))
d.text((bx + 150*K, by + 22*K),
       "böylece küçük veride çalışır, son 1×1 geri açar.", font=f_kck, fill=(80,80,80))

im.resize((W//K, Y//K), Image.LANCZOS).save(os.path.join(DIZIN, "resnet_mimari.png"))
print("resnet_mimari.png",
      os.path.getsize(os.path.join(DIZIN, "resnet_mimari.png"))//1024, "KB")
