"""Kapanış görseli: klasik yol vs Claude + Roboflow (MCP)."""
import os
from PIL import Image, ImageDraw, ImageFont

DIZIN = "/sessions/peaceful-lucid-dijkstra/mnt/cnn2/resimler"
FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
K = 2

ZEMIN, KOYU, GRI, ACIK = (245,245,245), (51,51,51), (125,125,125), (203,203,203)
KIRMIZI, KIRMIZI_A = (176,62,52), (250,233,229)
YESIL,  YESIL_A  = (46,124,80),  (228,244,233)
MOR,    MOR_A    = (126,87,168), (238,231,246)
MAVI,   MAVI_A   = (52,108,176), (226,238,250)
ZEYTIN = (140,130,40)

f_bas = ImageFont.truetype(FB, 27*K)
f_alt = ImageFont.truetype(FR, 16*K)
f_kb  = ImageFont.truetype(FB, 18*K)
f_et  = ImageFont.truetype(FB, 14*K)
f_not = ImageFont.truetype(FR, 14*K)
f_kck = ImageFont.truetype(FR, 13*K)
f_mono= ImageFont.truetype(FR, 13*K)


def sar(d, metin, font, en):
    satirlar, aktif = [], ""
    for k in metin.split():
        dn = (aktif + " " + k).strip()
        if d.textlength(dn, font=font) <= en: aktif = dn
        else: satirlar.append(aktif); aktif = k
    if aktif: satirlar.append(aktif)
    return satirlar


def ok(d, x0, y, x1, renk=GRI, kal=3*K):
    d.line([(x0,y),(x1-8*K,y)], fill=renk, width=kal)
    d.polygon([(x1,y),(x1-10*K,y-6*K),(x1-10*K,y+6*K)], fill=renk)


W, Y = 1180*K, 600*K
im = Image.new("RGB", (W, Y), ZEMIN)
d = ImageDraw.Draw(im)

d.text((42*K, 24*K), "Bundan sonrası: yazarak", font=f_bas, fill=KOYU)
d.text((42*K, 62*K),
       "Claude'u Roboflow'a bağladığınızda bu işlerin çoğunu konuşarak yaptırabilirsiniz.",
       font=f_alt, fill=GRI)

# ── SOL: klasik yol ──────────────────────────────────────────────────────
sx, sy, sw = 42*K, 116*K, 470*K
d.rectangle((sx, sy, sx+sw, sy+330*K), fill=KIRMIZI_A, outline=KIRMIZI, width=2)
d.rectangle((sx, sy, sx+6*K, sy+330*K), fill=KIRMIZI)
d.text((sx+20*K, sy+16*K), "KLASİK YOL", font=f_kb, fill=KIRMIZI)

adimlar = [
    ("1", "Veri setini ara", "Kaggle, Universe, GitHub... saatlerce tarama"),
    ("2", "İndir ve incele", "Format doğru mu, sınıflar tutuyor mu"),
    ("3", "Kod yaz", "Yükleme, dönüştürme, eğitim betiği"),
    ("4", "Eğit ve bekle", "Hata varsa baştan"),
    ("5", "Sonucu değerlendir", "Grafikleri okuyup neyi değiştireceğine karar ver"),
]
yy = sy + 54*K
for no, bas, alt in adimlar:
    d.ellipse((sx+22*K, yy, sx+44*K, yy+22*K), fill=KIRMIZI)
    d.text((sx+29*K, yy+3*K), no, font=f_kck, fill=(255,255,255))
    d.text((sx+56*K, yy), bas, font=f_et, fill=KOYU)
    d.text((sx+56*K, yy+20*K), alt, font=f_kck, fill=(95,95,95))
    yy += 54*K

# ── SAĞ: Claude + Roboflow ───────────────────────────────────────────────
cx = 668*K
d.rectangle((cx, sy, cx+sw, sy+330*K), fill=YESIL_A, outline=YESIL, width=2)
d.rectangle((cx, sy, cx+6*K, sy+330*K), fill=YESIL)
d.text((cx+20*K, sy+16*K), "CLAUDE  +  ROBOFLOW", font=f_kb, fill=YESIL)

konusma = [
    ("sen", "Çöp türlerini kutuyla bulan hazır bir model bul"),
    ("claude", "Universe'de 5742 görüntülük bir veri seti var. "
               "Modelini test ettim: metal %98 güvenle bulundu."),
    ("sen", "Bu veriyle kendi modelimi eğit"),
    ("claude", "Eğitim başlatıldı. İlerlemeyi izliyorum, "
               "bitince sonuçları özetlerim."),
]
yy = sy + 54*K
for kim, metin in konusma:
    kimin = (kim == "sen")
    renk  = MAVI if kimin else MOR
    dolgu = MAVI_A if kimin else MOR_A
    satirlar = sar(d, metin, f_mono, sw - 110*K)
    h = 22*K + len(satirlar)*20*K
    bx = cx + (20*K if kimin else 46*K)
    bw = sw - 66*K - (26*K if not kimin else 0)
    d.rounded_rectangle((bx, yy, bx+bw, yy+h), radius=8*K, fill=dolgu, outline=renk)
    d.text((bx+12*K, yy+6*K), "Sen" if kimin else "Claude", font=f_kck, fill=renk)
    for i, sat in enumerate(satirlar):
        d.text((bx+12*K, yy+24*K+i*20*K), sat, font=f_mono, fill=(55,55,55))
    yy += h + 12*K

ok(d, sx+sw+18*K, sy+165*K, cx-18*K, YESIL, 4)

# ── alt bant ─────────────────────────────────────────────────────────────
yb = 470*K
d.line([(42*K, yb), (W-42*K, yb)], fill=ACIK, width=2)
d.text((42*K, yb+18*K), "Bu atölyede kullandığımız veri setini böyle bulduk.",
       font=f_et, fill=KOYU)
d.text((42*K, yb+46*K),
       "Roboflow'un Claude bağlantısı 67 araç sunuyor: veri seti arama, etiketleme "
       "işi açma, otomatik etiketleme,", font=f_not, fill=(70,70,70))
d.text((42*K, yb+70*K),
       "model eğitme, eğitim takibi, sonuç değerlendirme ve hazır modelle tahmin.",
       font=f_not, fill=(70,70,70))
d.text((42*K, yb+102*K),
       "→ Kodu bilmek hâlâ gerekli — ne istediğinizi bilmiyorsanız ne isteyeceğinizi "
       "de bilemezsiniz.", font=f_not, fill=ZEYTIN)

im.resize((W//K, Y//K), Image.LANCZOS).save(os.path.join(DIZIN, "atolye_kapanis.png"))
print("atolye_kapanis.png", os.path.getsize(os.path.join(DIZIN,"atolye_kapanis.png"))//1024, "KB")
