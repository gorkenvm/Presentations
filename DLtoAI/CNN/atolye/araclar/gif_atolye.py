"""Atölye görselleri: sınıflandırma vs tespit, ve tespit çıktısının anatomisi."""
import os
from PIL import Image, ImageDraw, ImageFont

DIZIN = "/sessions/peaceful-lucid-dijkstra/mnt/cnn2/resimler"
FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
K = 2

ZEMIN, KOYU, GRI, ACIK = (245,245,245), (51,51,51), (125,125,125), (203,203,203)
KIRMIZI, KIRMIZI_A = (176,62,52), (250,232,228)
YESIL,  YESIL_A  = (46,124,80),  (226,244,232)
MAVI,   MAVI_A   = (52,108,176), (224,238,250)
MOR,    MOR_A    = (126,87,168), (238,231,246)
TURUNCU = (196,124,30)
ZEYTIN = (140,130,40)

f_bas = ImageFont.truetype(FB, 27*K)
f_alt = ImageFont.truetype(FR, 16*K)
f_kb  = ImageFont.truetype(FB, 18*K)
f_et  = ImageFont.truetype(FB, 14*K)
f_not = ImageFont.truetype(FR, 15*K)
f_kck = ImageFont.truetype(FR, 12*K)
f_mono= ImageFont.truetype(FB, 13*K)


def orta_x(d, x0, x1, y, s, font, renk):
    l,t,r,b = d.textbbox((0,0), s, font=font)
    d.text((x0 + (x1-x0-(r-l))/2 - l, y), s, font=font, fill=renk)

def ok(d, x0, y, x1, renk=GRI, kal=3*K):
    d.line([(x0,y),(x1-8*K,y)], fill=renk, width=kal)
    d.polygon([(x1,y),(x1-10*K,y-6*K),(x1-10*K,y+6*K)], fill=renk)


# ══════════════════════════════════════════════════════════════════════
# 1) Sınıflandırma vs Tespit
# ══════════════════════════════════════════════════════════════════════
W, Y = 1180*K, 520*K
im = Image.new("RGB", (W, Y), ZEMIN); d = ImageDraw.Draw(im)
d.text((42*K, 24*K), "Aynı fotoğraf, iki farklı soru", font=f_bas, fill=KOYU)
d.text((42*K, 60*K), "Dün birinciyi sorduk. Bugün ikinciyi soracağız.", font=f_alt, fill=GRI)

# temsili sahne: yol + 3 araba + 1 yaya
def sahne(d, x, y, en, boy, kutular=False):
    d.rectangle((x, y, x+en, y+boy), fill=(228,232,236), outline=ACIK, width=2)
    d.rectangle((x, y+boy*0.62, x+en, y+boy), fill=(214,218,222))     # yol
    nesneler = [(0.10, 0.66, 0.20, 0.16, "car"), (0.36, 0.70, 0.24, 0.18, "car"),
                (0.68, 0.64, 0.18, 0.14, "car"), (0.56, 0.40, 0.05, 0.24, "person")]
    for fx, fy, fw, fh, ad in nesneler:
        bx, by = x + en*fx, y + boy*fy
        bw, bh = en*fw, boy*fh
        renk = MAVI if ad == "car" else MOR
        d.rounded_rectangle((bx, by, bx+bw, by+bh), radius=5*K,
                            fill=MAVI_A if ad=="car" else MOR_A, outline=renk)
        if kutular:
            d.rectangle((bx-4*K, by-4*K, bx+bw+4*K, by+bh+4*K), outline=YESIL, width=3)
            d.rectangle((bx-4*K, by-22*K, bx+bw+4*K, by-4*K), fill=YESIL)
            d.text((bx-1*K, by-20*K), ad, font=f_kck, fill=(255,255,255))

sy = 120*K
d.text((42*K, sy-28*K), "SINIFLANDIRMA  —  \"bu resim ne?\"", font=f_kb, fill=KIRMIZI)
sahne(d, 42*K, sy, 380*K, 210*K, kutular=False)
d.text((42*K, sy+228*K), "Çıktı: tek bir etiket + olasılık", font=f_not, fill=(65,65,65))
d.rounded_rectangle((42*K, sy+256*K, 300*K, sy+296*K), radius=6*K,
                    fill=KIRMIZI_A, outline=KIRMIZI)
d.text((58*K, sy+266*K), "car        0.62", font=f_mono, fill=KIRMIZI)
d.text((42*K, sy+312*K), "Kaç tane? Nerede? Yaya var mı?", font=f_not, fill=KIRMIZI)
d.text((42*K, sy+336*K), "Bu sorulara cevap veremez.", font=f_not, fill=KIRMIZI)

ok(d, 460*K, sy+105*K, 540*K)

d.text((580*K, sy-28*K), "NESNE TESPİTİ  —  \"ne var, nerede, kaç tane?\"", font=f_kb, fill=YESIL)
sahne(d, 580*K, sy, 380*K, 210*K, kutular=True)
d.text((580*K, sy+228*K), "Çıktı: her nesne için kutu + etiket + olasılık", font=f_not, fill=(65,65,65))
kx = 580*K
for i, (s, r) in enumerate([("car     0.91   [ 78, 260, 155, 300]", MAVI),
                            ("car     0.88   [180, 268, 272, 306]", MAVI),
                            ("person  0.84   [312, 204, 330, 254]", MOR)]):
    d.rounded_rectangle((kx, sy+256*K+i*30*K, kx+430*K, sy+282*K+i*30*K),
                        radius=5*K, fill=YESIL_A, outline=(200,224,208))
    d.text((kx+12*K, sy+261*K+i*30*K), s, font=f_mono, fill=r)

d.text((580*K, sy+352*K), "4 nesne, her birinin yeri belli.", font=f_not, fill=YESIL)

im.resize((W//K, Y//K), Image.LANCZOS).save(os.path.join(DIZIN, "atolye_tespit_vs_siniflandirma.png"))
print("atolye_tespit_vs_siniflandirma.png",
      os.path.getsize(os.path.join(DIZIN,"atolye_tespit_vs_siniflandirma.png"))//1024, "KB")


# ══════════════════════════════════════════════════════════════════════
# 2) Çıktının anatomisi: kutu, confidence, NMS
# ══════════════════════════════════════════════════════════════════════
W, Y = 1180*K, 560*K
im = Image.new("RGB", (W, Y), ZEMIN); d = ImageDraw.Draw(im)
d.text((42*K, 24*K), "Tespit çıktısının anatomisi", font=f_bas, fill=KOYU)
d.text((42*K, 60*K), "Üç kavram: kutu koordinatları, güven eşiği ve NMS.", font=f_alt, fill=GRI)

# --- A: kutu koordinatlari ---
ax, ay = 42*K, 130*K
d.text((ax, ay-28*K), "1 · Kutu nedir?", font=f_kb, fill=MAVI)
d.rectangle((ax, ay, ax+300*K, ay+180*K), fill=(232,236,240), outline=ACIK)
bx0, by0, bx1, by1 = ax+70*K, ay+45*K, ax+220*K, ay+150*K
d.rounded_rectangle((bx0, by0, bx1, by1), radius=6*K, fill=MAVI_A, outline=MAVI, width=3)
d.rectangle((bx0, by0-22*K, bx0+96*K, by0-2*K), fill=MAVI)
d.text((bx0+5*K, by0-20*K), "car 0.91", font=f_kck, fill=(255,255,255))
for px, py, et in [(bx0, by0, "(x1, y1)"), (bx1, by1, "(x2, y2)")]:
    d.ellipse((px-5*K, py-5*K, px+5*K, py+5*K), fill=KIRMIZI)
d.text((ax+4*K, by0-46*K), "(x1, y1)", font=f_kck, fill=KIRMIZI)
d.text((bx1-8*K, by1+8*K), "(x2, y2)", font=f_kck, fill=KIRMIZI)
d.text((ax, ay+196*K), "Sol üst ve sağ alt köşe —", font=f_kck, fill=(70,70,70))
d.text((ax, ay+216*K), "piksel cinsinden.", font=f_kck, fill=(70,70,70))

# --- B: confidence esigi ---
cx = 400*K
d.text((cx, ay-28*K), "2 · Güven eşiği (conf)", font=f_kb, fill=TURUNCU)
d.rectangle((cx, ay, cx+300*K, ay+180*K), fill=(255,255,255), outline=ACIK)
degerler = [("car",    0.91, YESIL),
            ("car",    0.88, YESIL),
            ("person", 0.84, YESIL),
            ("truck",  0.41, TURUNCU),
            ("bus",    0.19, GRI)]
for i, (ad, v, r) in enumerate(degerler):
    yy = ay + 18*K + i*30*K
    d.text((cx+14*K, yy), f"{ad:8s}", font=f_mono, fill=(60,60,60))
    d.rectangle((cx+96*K, yy+2*K, cx+96*K+int(170*K*v), yy+16*K), fill=r)
    d.text((cx+276*K, yy), f"{v:.2f}", font=f_kck, fill=(90,90,90))
esik_x = cx + 96*K + int(170*K*0.5)
d.line([(esik_x, ay+10*K), (esik_x, ay+168*K)], fill=KIRMIZI, width=3)
d.text((esik_x-30*K, ay+170*K), "conf=0.50", font=f_kck, fill=KIRMIZI)
d.text((cx, ay+196*K), "Eşiğin solundakiler atılır.", font=f_kck, fill=(70,70,70))
d.text((cx, ay+216*K), "Yükseltirsen kutu azalır.", font=f_kck, fill=(70,70,70))

# --- C: NMS ---
nx = 758*K
d.text((nx, ay-28*K), "3 · NMS (iou)", font=f_kb, fill=YESIL)
d.rectangle((nx, ay, nx+380*K, ay+180*K), fill=(232,236,240), outline=ACIK)
d.text((nx+16*K, ay+8*K), "NMS'siz", font=f_kck, fill=KIRMIZI)
for i,(dx,dy) in enumerate([(0,0),(8*K,6*K),(-7*K,9*K),(4*K,-6*K)]):
    d.rectangle((nx+40*K+dx, ay+50*K+dy, nx+150*K+dx, ay+140*K+dy),
                outline=KIRMIZI, width=2)
d.text((nx+40*K, ay+150*K), "aynı arabaya 4 kutu", font=f_kck, fill=KIRMIZI)
ok(d, nx+170*K, ay+95*K, nx+210*K)
d.text((nx+230*K, ay+8*K), "NMS'li", font=f_kck, fill=YESIL)
d.rectangle((nx+240*K, ay+50*K, nx+350*K, ay+140*K), outline=YESIL, width=4)
d.text((nx+240*K, ay+150*K), "tek kutu kalır", font=f_kck, fill=YESIL)
d.text((nx, ay+196*K), "Üst üste binen kutulardan en", font=f_kck, fill=(70,70,70))
d.text((nx, ay+216*K), "güvenli olanı tutar, ötekini atar.", font=f_kck, fill=(70,70,70))

yb = 420*K
d.line([(42*K, yb), (W-42*K, yb)], fill=ACIK, width=2)
d.text((42*K, yb+20*K),
       "Model aslında yüzlerce aday kutu üretir. Gördüğümüz temiz sonuç, bu iki "
       "süzgeçten geçmiş halidir.", font=f_not, fill=(65,65,65))
d.text((42*K, yb+50*K),
       "conf düşük → çok kutu, çok yanlış      |      conf yüksek → az kutu, "
       "kaçırılan nesne", font=f_et, fill=KOYU)
d.text((42*K, yb+82*K),
       "→ \"Doğru\" eşik diye bir şey yok; neyi kaçırmayı göze aldığına bağlı.",
       font=f_not, fill=ZEYTIN)

im.resize((W//K, Y//K), Image.LANCZOS).save(os.path.join(DIZIN, "atolye_anatomi.png"))
print("atolye_anatomi.png", os.path.getsize(os.path.join(DIZIN,"atolye_anatomi.png"))//1024, "KB")
