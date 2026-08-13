"""Ders GIF'leri için ortak çizim yardımcıları.

Görsel dil, kullanıcının verdiği conv_gif2 / conv_gif3 animasyonlarından alındı:
açık gri zemin, ince çerçeveli hücreler, kanal başına renk, altta özet satırı
ve zeytin rengi tek cümlelik çıkarım.
"""
import os

from PIL import Image, ImageDraw, ImageFont

DIZIN = "/sessions/peaceful-lucid-dijkstra/mnt/cnn2/resimler"
FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

ZEMIN = (245, 245, 245)
KOYU = (51, 51, 51)
GRI = (130, 130, 130)
ACIK = (207, 207, 207)
BEYAZ = (255, 255, 255)
VURGU = (192, 80, 77)
ZEYTIN = (140, 130, 40)

# conv_gif3'teki kanal renkleri
KANAL = [(176, 101, 29), (126, 87, 168), (46, 139, 139), (194, 24, 91)]
KANAL_A = [(250, 238, 224), (238, 231, 246), (225, 242, 242), (250, 228, 238)]

f_bas = ImageFont.truetype(FB, 25)
f_alt = ImageFont.truetype(FR, 16)
f_et = ImageFont.truetype(FB, 14)
f_h = ImageFont.truetype(FB, 17)
f_not = ImageFont.truetype(FR, 15)
f_notb = ImageFont.truetype(FB, 15)
f_sem = ImageFont.truetype(FB, 24)


def orta(d, kutu, s, font, renk):
    x0, y0, x1, y1 = kutu
    l, t, r, b = d.textbbox((0, 0), s, font=font)
    d.text((x0 + (x1 - x0 - (r - l)) / 2 - l, y0 + (y1 - y0 - (b - t)) / 2 - t),
           s, font=font, fill=renk)


def izgara(d, x0, y0, veri, h=40, dolgu=BEYAZ, kenar=ACIK, yazi=KOYU,
           vurgu=(), vurgu_renk=VURGU, vurgu_dolgu=None, kalin=()):
    """veri: 2B liste (None = boş hücre). vurgu/kalin: (r, c) kümeleri."""
    for r, satir in enumerate(veri):
        for c, v in enumerate(satir):
            k = (x0 + c * h, y0 + r * h, x0 + (c + 1) * h, y0 + (r + 1) * h)
            iv = (r, c) in vurgu
            d.rectangle(k, fill=(vurgu_dolgu or (250, 232, 230)) if iv else dolgu,
                        outline=vurgu_renk if iv else kenar)
            if v is not None:
                orta(d, k, str(v), f_h, vurgu_renk if iv else yazi)
    for r, c in kalin:
        d.rectangle((x0 + c * h, y0 + r * h, x0 + (c + 1) * h, y0 + (r + 1) * h),
                    outline=vurgu_renk, width=3)


def ok(d, x0, y, x1, renk=GRI):
    d.line([(x0, y), (x1 - 9, y)], fill=renk, width=2)
    d.polygon([(x1, y), (x1 - 10, y - 5), (x1 - 10, y + 5)], fill=renk)


def kaydet(ad, kareler, sureler, renk=200):
    """Tüm kareler tek palete indirgenir; yoksa PIL kareler arası farkı
    optimize edemez ve dosya birkaç kat büyür."""
    g, y = kareler[0].size
    m = Image.new("RGB", (g, y * len(kareler)))
    for i, k in enumerate(kareler):
        m.paste(k, (0, i * y))
    palet = m.quantize(colors=renk, method=Image.MEDIANCUT)
    p = [k.quantize(palette=palet, dither=Image.Dither.NONE) for k in kareler]
    yol = os.path.join(DIZIN, ad)
    p[0].save(yol, save_all=True, append_images=p[1:], duration=sureler,
              loop=0, optimize=True, disposal=1)
    print(f"{ad:22s} {len(p):2d} kare  {sum(sureler)/1000:5.1f} sn  "
          f"{os.path.getsize(yol)//1024:4d} KB  {kareler[0].size}")


def zemin(W, Y, baslik, altbasl):
    im = Image.new("RGB", (W, Y), ZEMIN)
    d = ImageDraw.Draw(im)
    d.text((42, 26), baslik, font=f_bas, fill=KOYU)
    d.text((42, 60), altbasl, font=f_alt, fill=GRI)
    return im, d


def dipnot(d, y, ozet, notlar):
    d.text((42, y), ozet, font=f_notb, fill=KOYU)
    for i, s in enumerate(notlar):
        d.text((42, y + 26 + i * 22), s, font=f_not,
               fill=ZEYTIN if s.startswith("→") else GRI)
