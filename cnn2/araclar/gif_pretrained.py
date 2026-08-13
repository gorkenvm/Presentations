"""Pretrained model sayfası ve VGG'nin 3×3 fikri için iki statik görsel."""
import os

from PIL import Image, ImageDraw, ImageFont

DIZIN = "/sessions/peaceful-lucid-dijkstra/mnt/cnn2/resimler"
FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
K = 2

ZEMIN, KOYU, GRI, ACIK = (245,245,245), (51,51,51), (128,128,128), (205,205,205)
KIRMIZI, KIRMIZI_A = (176,62,52), (250,232,228)
YESIL,   YESIL_A   = (46,124,80),  (228,244,232)
MOR,     MOR_A     = (110,80,160), (236,230,246)
MAVI,    MAVI_A    = (52,108,176), (226,238,250)
ZEYTIN = (140,130,40)

f_bas  = ImageFont.truetype(FB, 27*K)
f_alt  = ImageFont.truetype(FR, 16*K)
f_kbas = ImageFont.truetype(FB, 18*K)
f_et   = ImageFont.truetype(FB, 15*K)
f_not  = ImageFont.truetype(FR, 15*K)
f_kck  = ImageFont.truetype(FR, 13*K)
f_h    = ImageFont.truetype(FB, 14*K)


def orta(d, kutu, s, font, renk):
    x0,y0,x1,y1 = kutu
    l,t,r,b = d.textbbox((0,0), s, font=font)
    d.text((x0+(x1-x0-(r-l))/2-l, y0+(y1-y0-(b-t))/2-t), s, font=font, fill=renk)


def ok(d, x0, y, x1, renk=GRI, kalinlik=3):
    d.line([(x0,y),(x1-10*K,y)], fill=renk, width=kalinlik)
    d.polygon([(x1,y),(x1-11*K,y-6*K),(x1-11*K,y+6*K)], fill=renk)


# ══════════════════════════════════════════════════════════════════════
# 1) pretrained.png
# ══════════════════════════════════════════════════════════════════════
W, Y = 1180*K, 540*K
im = Image.new("RGB", (W, Y), ZEMIN); d = ImageDraw.Draw(im)
d.text((42*K, 26*K), "Pretrained model: başkasının eğittiği ağırlıkları ödünç almak",
       font=f_bas, fill=KOYU)
d.text((42*K, 64*K), "Aynı problem iki yoldan çözülür — fark, nereden başladığınız.",
       font=f_alt, fill=GRI)

kw, kh, ky = 500*K, 190*K, 110*K
for i,(x,renk,acik,bas,satirlar) in enumerate([
    (42*K, KIRMIZI, KIRMIZI_A, "A · SIFIRDAN EĞİTMEK",
     ["ImageNet: 1.2 milyon görüntü, 1000 sınıf",
      "Günler–haftalar süren GPU eğitimi",
      "Az veriniz varsa ezberler (overfitting)",
      "Ağırlıklar rastgeleden başlar"]),
    (638*K, YESIL, YESIL_A, "B · PRETRAINED KULLANMAK",
     ["Hazır ağırlıkları indir — saniyeler",
      "Son katmanı kendi sınıflarınla değiştir",
      "500 görüntüyle bile iyi sonuç",
      "Ağırlıklar 'görmeyi' zaten biliyor"]),
]):
    d.rectangle((x, ky, x+kw, ky+kh), fill=acik, outline=renk, width=2)
    d.rectangle((x, ky, x+6*K, ky+kh), fill=renk)
    d.text((x+20*K, ky+14*K), bas, font=f_kbas, fill=renk)
    for j,s in enumerate(satirlar):
        d.text((x+20*K, ky+50*K+j*28*K), "•  "+s, font=f_not, fill=(60,60,60))

ok(d, 556*K, ky+kh//2, 626*K, YESIL, 4)

# neden ise yariyor seridi
sy = 340*K
d.text((42*K, sy-30*K), "Neden işe yarıyor? Katmanlar sırayla genelden özele gider:",
       font=f_et, fill=KOYU)
kutular = [("İlk katmanlar", "kenar, renk, yön", MAVI, MAVI_A),
           ("Orta katmanlar", "doku, desen", MOR, MOR_A),
           ("Üst katmanlar", "parça: göz, tekerlek", MOR, MOR_A),
           ("Son katmanlar", "nesnenin kendisi", KIRMIZI, KIRMIZI_A)]
bx, bw = 42*K, 250*K
for i,(bas,alt,renk,acik) in enumerate(kutular):
    x = bx + i*(bw+30*K)
    d.rectangle((x, sy, x+bw, sy+66*K), fill=acik, outline=renk)
    d.text((x+16*K, sy+12*K), bas, font=f_h, fill=renk)
    d.text((x+16*K, sy+36*K), alt, font=f_kck, fill=(80,80,80))
    if i < 3:
        ok(d, x+bw+4*K, sy+33*K, x+bw+26*K, ACIK, 2)

d.text((42*K, 434*K),
       "Kedi de olsa çöp de olsa kenar kenardır — ilk katmanlar her görüntü için "
       "aynı şeyi öğrenir.", font=f_not, fill=GRI)
d.text((42*K, 460*K),
       "→ Bu yüzden ImageNet'te öğrenilen ilk katmanlar sizin probleminize "
       "olduğu gibi devredilebilir.", font=f_not, fill=ZEYTIN)
d.text((42*K, 492*K),
       "Devredilmeyen kısım son katmandır: o 1000 ImageNet sınıfına göre "
       "ayarlanmıştır, onu siz değiştirirsiniz.", font=f_not, fill=GRI)

im.resize((W//K, Y//K), Image.LANCZOS).save(os.path.join(DIZIN, "pretrained.png"))
print("pretrained.png", os.path.getsize(os.path.join(DIZIN,"pretrained.png"))//1024, "KB")


# ══════════════════════════════════════════════════════════════════════
# 2) vgg_3x3.png  —  iki 3×3 = bir 5×5
# ══════════════════════════════════════════════════════════════════════
W, Y = 1180*K, 480*K
im = Image.new("RGB", (W, Y), ZEMIN); d = ImageDraw.Draw(im)
d.text((42*K, 26*K), "VGG'nin fikri: iki 3×3, bir 5×5 eder", font=f_bas, fill=KOYU)
d.text((42*K, 64*K), "Aynı görüş alanı (receptive field), daha az parametre, "
                     "arada fazladan bir ReLU.", font=f_alt, fill=GRI)

hh = 26*K
def kare_izgara(d, x, y, n, renk, acik, etiket):
    for r in range(n):
        for c in range(n):
            d.rectangle((x+c*hh, y+r*hh, x+(c+1)*hh, y+(r+1)*hh),
                        fill=acik, outline=renk)
    d.text((x, y+n*hh+8*K), etiket, font=f_kck, fill=GRI)

# A — tek 5x5
ay = 130*K
d.text((42*K, ay-28*K), "A ·  Tek 5×5 filtre", font=f_kbas, fill=KIRMIZI)
kare_izgara(d, 42*K, ay, 5, KIRMIZI, KIRMIZI_A, "5×5 girdi bölgesi")
ok(d, 190*K, ay+65*K, 250*K)
d.text((196*K, ay+34*K), "5×5 conv", font=f_kck, fill=GRI)
kare_izgara(d, 262*K, ay+52*K, 1, KIRMIZI, KIRMIZI_A, "1 hücre")
d.text((42*K, ay+186*K), "Parametre:  5·5·C·C  =  25C²", font=f_et, fill=KIRMIZI)
d.text((42*K, ay+212*K), "Aktivasyon (ReLU) sayısı:  1", font=f_not, fill=GRI)

# B — iki 3x3
by = 130*K
bx = 620*K
d.text((bx, by-28*K), "B ·  Üst üste iki 3×3 filtre", font=f_kbas, fill=YESIL)
kare_izgara(d, bx, by, 5, YESIL, YESIL_A, "5×5 girdi bölgesi")
ok(d, bx+148*K, by+65*K, bx+204*K)
d.text((bx+150*K, by+34*K), "3×3 conv", font=f_kck, fill=GRI)
kare_izgara(d, bx+216*K, by+26*K, 3, YESIL, YESIL_A, "3×3 ara harita")
ok(d, bx+306*K, by+65*K, bx+362*K)
d.text((bx+308*K, by+34*K), "3×3 conv", font=f_kck, fill=GRI)
kare_izgara(d, bx+374*K, by+52*K, 1, YESIL, YESIL_A, "1 hücre")
d.text((bx, by+186*K), "Parametre:  2 · 3·3·C·C  =  18C²   (%28 daha az)",
       font=f_et, fill=YESIL)
d.text((bx, by+212*K), "Aktivasyon (ReLU) sayısı:  2  →  daha fazla "
                       "doğrusal olmayanlık", font=f_not, fill=GRI)

yb = 396*K
d.line([(42*K, yb), (W-42*K, yb)], fill=ACIK, width=2)
d.text((42*K, yb+18*K),
       "Ama VGG yine de ağır: 138M parametrenin ~103M'i tek bir katmanda "
       "(7×7×512 → 4096 tam bağlantı).", font=f_not, fill=KOYU)
d.text((42*K, yb+46*K),
       "→ Ağırlık evrişimde değil, sondaki Dense katmanlarında birikiyor. "
       "Sonraki mimariler tam da bunu çözmeye çalışacak.", font=f_not, fill=ZEYTIN)

im.resize((W//K, Y//K), Image.LANCZOS).save(os.path.join(DIZIN, "vgg_3x3.png"))
print("vgg_3x3.png", os.path.getsize(os.path.join(DIZIN,"vgg_3x3.png"))//1024, "KB")
