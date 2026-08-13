"""ResNet: çözdüğü sorun ve kısayol bağlantısı."""
import os

from PIL import Image, ImageDraw, ImageFont

DIZIN = "/sessions/peaceful-lucid-dijkstra/mnt/cnn2/resimler"
FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
K = 2

ZEMIN, KOYU, GRI, ACIK = (245,245,245), (51,51,51), (125,125,125), (205,205,205)
KIRMIZI, KIRMIZI_A = (176,62,52), (250,232,228)
YESIL,   YESIL_A   = (46,124,80),  (228,244,232)
MAVI,    MAVI_A    = (52,108,176), (226,238,250)
MOR,     MOR_A     = (110,80,160), (236,230,246)
ZEYTIN = (140,130,40)

f_bas  = ImageFont.truetype(FB, 27*K)
f_alt  = ImageFont.truetype(FR, 16*K)
f_kbas = ImageFont.truetype(FB, 18*K)
f_et   = ImageFont.truetype(FB, 15*K)
f_not  = ImageFont.truetype(FR, 15*K)
f_kck  = ImageFont.truetype(FR, 13*K)
f_sem  = ImageFont.truetype(FB, 26*K)


def orta(d, kutu, s, font, renk):
    x0,y0,x1,y1 = kutu
    l,t,r,b = d.textbbox((0,0), s, font=font)
    d.text((x0+(x1-x0-(r-l))/2-l, y0+(y1-y0-(b-t))/2-t), s, font=font, fill=renk)


def ok(d, x0, y0, x1, y1, renk=GRI, kal=3):
    d.line([(x0,y0),(x1,y1)], fill=renk, width=kal)
    if x1 > x0:
        d.polygon([(x1,y1),(x1-11*K,y1-6*K),(x1-11*K,y1+6*K)], fill=renk)
    else:
        d.polygon([(x1,y1),(x1-6*K,y1-11*K),(x1+6*K,y1-11*K)], fill=renk)


W, Y = 1180*K, 620*K
im = Image.new("RGB", (W, Y), ZEMIN); d = ImageDraw.Draw(im)
d.text((42*K, 26*K), "ResNet'in çözdüğü sorun", font=f_bas, fill=KOYU)
d.text((42*K, 64*K),
       "Katman eklemek modeli neden kötüleştiriyordu — ve tek bir okla nasıl düzeldi?",
       font=f_alt, fill=GRI)

# ══ SOL PANEL: sorun ══════════════════════════════════════════════════════
px, py, pw, ph = 42*K, 116*K, 500*K, 330*K
d.rectangle((px, py, px+pw, py+ph), fill=KIRMIZI_A, outline=KIRMIZI, width=2)
d.rectangle((px, py, px+6*K, py+ph), fill=KIRMIZI)
d.text((px+20*K, py+14*K), "SORUN  ·  2015 öncesi", font=f_kbas, fill=KIRMIZI)
d.text((px+20*K, py+44*K),
       "Katman ekledikçe model daha iyi olmalıydı. Olmadı.", font=f_not, fill=(60,60,60))

# basit egitim hatasi grafigi
gx, gy, gw, gh = px+56*K, py+82*K, 380*K, 146*K
d.rectangle((gx, gy, gx+gw, gy+gh), fill=(255,255,255), outline=ACIK)
d.text((gx-42*K, gy+50*K), "eğitim", font=f_kck, fill=GRI)
d.text((gx-42*K, gy+68*K), "hatası", font=f_kck, fill=GRI)
d.text((gx+gw-90*K, gy+gh+8*K), "eğitim adımı →", font=f_kck, fill=GRI)

def egri(son_hata):
    """Hata yukarıdan aşağı düşer; ekranda yukarı = daha çok hata."""
    n = []
    for i in range(41):
        hata = son_hata + (0.95 - son_hata) * (2.718 ** (-i / 9.0))
        n.append((gx + i*gw//40, gy + int(gh * (1 - hata))))
    return n

d.line(egri(0.45), fill=KIRMIZI, width=3)     # 56 katman — daha kötü, üstte
d.line(egri(0.12), fill=MAVI, width=3)        # 20 katman — daha iyi, altta
d.text((gx+gw-152*K, gy+int(gh*0.55)-30*K), "56 katman", font=f_et, fill=KIRMIZI)
d.text((gx+gw-152*K, gy+int(gh*0.88)-30*K), "20 katman", font=f_et, fill=MAVI)

d.text((px+20*K, py+ph-64*K),
       "Daha derin ağ, EĞİTİM verisinde bile daha kötüydü.", font=f_not, fill=KIRMIZI)
d.text((px+20*K, py+ph-38*K),
       "Yani ezberleme (overfitting) değil — ağ öğrenemiyordu.",
       font=f_not, fill=(60,60,60))

# ══ SAĞ PANEL: çözüm ══════════════════════════════════════════════════════
qx = 638*K
d.rectangle((qx, py, qx+pw, py+ph), fill=YESIL_A, outline=YESIL, width=2)
d.rectangle((qx, py, qx+6*K, py+ph), fill=YESIL)
d.text((qx+20*K, py+14*K), "ÇÖZÜM  ·  kısayol bağlantısı", font=f_kbas, fill=YESIL)

# blok semasi:  x → [conv] → [conv] → (+) → çıktı ,  x'ten (+)'a kavis
by = py+126*K
kw, kh = 118*K, 54*K
x0 = qx+34*K
d.text((x0, by+14*K), "x", font=f_sem, fill=KOYU)
d.text((x0-6*K, by+52*K), "girdi", font=f_kck, fill=GRI)

b1 = x0+40*K
d.rectangle((b1, by, b1+kw, by+kh), fill=MAVI_A, outline=MAVI)
orta(d, (b1, by, b1+kw, by+kh), "Conv + ReLU", f_et, MAVI)
b2 = b1+kw+30*K
d.rectangle((b2, by, b2+kw, by+kh), fill=MAVI_A, outline=MAVI)
orta(d, (b2, by, b2+kw, by+kh), "Conv", f_et, MAVI)

ok(d, x0+22*K, by+kh//2, b1-6*K, by+kh//2)
ok(d, b1+kw+4*K, by+kh//2, b2-6*K, by+kh//2)

# toplama dairesi
cx, cy = b2+kw+56*K, by+kh//2
ok(d, b2+kw+4*K, cy, cx-20*K, cy)
d.ellipse((cx-18*K, cy-18*K, cx+18*K, cy+18*K), fill=(255,255,255), outline=YESIL, width=3)
orta(d, (cx-18*K, cy-18*K, cx+18*K, cy+18*K), "+", f_sem, YESIL)
ok(d, cx+22*K, cy, cx+72*K, cy)
d.text((cx+80*K, cy-14*K), "ReLU", font=f_et, fill=KOYU)

# kisayol kavisi
ky = by - 54*K
d.line([(x0+10*K, by+6*K), (x0+10*K, ky), (cx, ky)], fill=YESIL, width=3)
ok(d, cx, ky, cx, cy-24*K, YESIL)
d.text((x0+60*K, ky-26*K), "kısayol: girdi olduğu gibi ileri taşınır",
       font=f_kck, fill=YESIL)

d.text((qx+20*K, py+ph-104*K), "çıktı  =  F(x)  +  x", font=f_kbas, fill=YESIL)
d.text((qx+20*K, py+ph-72*K),
       "Ağ sıfırdan çıktı üretmiyor; girdiye NE EKLEYECEĞİNİ öğreniyor.",
       font=f_not, fill=(60,60,60))
d.text((qx+20*K, py+ph-44*K),
       "Eklenecek bir şey yoksa F(x)=0 yapıp girdiyi aynen geçirebiliyor —",
       font=f_not, fill=(60,60,60))
d.text((qx+20*K, py+ph-20*K),
       "yani fazladan katman artık zarar veremiyor.", font=f_not, fill=(60,60,60))

# ══ alt bant ══════════════════════════════════════════════════════════════
yb = 476*K
d.line([(42*K, yb), (W-42*K, yb)], fill=ACIK, width=2)
d.text((42*K, yb+20*K), "Sonuç:", font=f_et, fill=KOYU)
d.text((130*K, yb+20*K),
       "152 katmanlı ağ ilk kez eğitilebildi ve ImageNet 2015'i kazandı.",
       font=f_not, fill=(60,60,60))
d.text((42*K, yb+52*K),
       "ResNet-50, VGG-16'dan 3 kat derin ama 5 kat az parametreli "
       "(25.6M / 138M) — ve daha doğru.", font=f_not, fill=(60,60,60))
d.text((42*K, yb+84*K),
       "→ Bu kısayol fikri bugün neredeyse her modern mimaride var: "
       "Transformer'larda bile.", font=f_not, fill=ZEYTIN)

im.resize((W//K, Y//K), Image.LANCZOS).save(os.path.join(DIZIN, "resnet.png"))
print("resnet.png", os.path.getsize(os.path.join(DIZIN, "resnet.png"))//1024, "KB")
