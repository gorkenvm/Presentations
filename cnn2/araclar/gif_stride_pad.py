"""Stride ve padding animasyonları.

Kullanıcının verdiği conv_gif2/conv_gif3 ile aynı görsel dil ve aynı boyut
zinciri: girdi 6×6, kernel 3×3 → çıktı 4×4 → pooling 2×2.
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
KIRMIZI = (192, 80, 77)
KIRMIZI_A = (247, 227, 226)
MOR = (126, 87, 168)
MOR_A = (235, 227, 245)
YESIL = (78, 138, 107)
YESIL_A = (228, 240, 233)
AMBER = (176, 137, 44)
ZEYTIN = (140, 130, 40)

f_bas = ImageFont.truetype(FB, 25)
f_alt = ImageFont.truetype(FR, 16)
f_et = ImageFont.truetype(FB, 15)
f_h = ImageFont.truetype(FB, 17)
f_not = ImageFont.truetype(FR, 15)
f_notb = ImageFont.truetype(FB, 15)
f_sem = ImageFont.truetype(FB, 26)

H = 40


def orta(d, kutu, s, font, renk):
    x0, y0, x1, y1 = kutu
    l, t, r, b = d.textbbox((0, 0), s, font=font)
    d.text((x0 + (x1 - x0 - (r - l)) / 2 - l, y0 + (y1 - y0 - (b - t)) / 2 - t),
           s, font=font, fill=renk)


def izgara(d, x0, y0, veri, dolgu=(255, 255, 255), kenar=ACIK, yazi=KOYU,
           pencere=None, pencere_renk=KIRMIZI, pad_hucre=(), bos=None):
    for r, satir in enumerate(veri):
        for c, v in enumerate(satir):
            k = (x0 + c * H, y0 + r * H, x0 + (c + 1) * H, y0 + (r + 1) * H)
            ic = pencere and (pencere[0] <= r < pencere[0] + 3
                              and pencere[1] <= c < pencere[1] + 3)
            pad = (r, c) in pad_hucre
            d.rectangle(k, fill=(KIRMIZI_A if ic else
                                 ((238, 238, 238) if pad else dolgu)),
                        outline=(pencere_renk if ic else
                                 ((200, 200, 200) if pad else kenar)))
            if v is None:
                continue
            orta(d, k, str(v), f_h, GRI if pad else (KOYU if ic else yazi))
    if pencere:
        r, c = pencere[0], pencere[1]
        d.rectangle((x0 + c * H, y0 + r * H, x0 + (c + 3) * H, y0 + (r + 3) * H),
                    outline=pencere_renk, width=3)


def kaydet(ad, kareler, sureler):
    g, y = kareler[0].size
    m = Image.new("RGB", (g, y * len(kareler)))
    for i, k in enumerate(kareler):
        m.paste(k, (0, i * y))
    palet = m.quantize(colors=200, method=Image.MEDIANCUT)
    p = [k.quantize(palette=palet, dither=Image.Dither.NONE) for k in kareler]
    yol = os.path.join(DIZIN, ad)
    p[0].save(yol, save_all=True, append_images=p[1:], duration=sureler,
              loop=0, optimize=True, disposal=1)
    print(f"{ad:20s} {len(p):2d} kare  {sum(sureler)/1000:4.1f} sn  "
          f"{os.path.getsize(yol)//1024:4d} KB  {kareler[0].size}")


# ── ortak veri: dikey kenarlı 6×6 görüntü, dikey kenar bulucu kernel ────────
G6 = [[8, 8, 8, 1, 1, 1] for _ in range(6)]
KERN = [[1, 0, -1], [1, 0, -1], [1, 0, -1]]


def konv(g, k, stride):
    n = len(g)
    cn = (n - 3) // stride + 1
    return [[sum(g[r * stride + i][c * stride + j] * k[i][j]
                 for i in range(3) for j in range(3))
             for c in range(cn)] for r in range(cn)], cn


def kare(baslik, altbasl, girdi, cikti, ozet, sonuc_notu, pencere=None,
         aktif=None, pad_hucre=(), yan=None, W=1200, not_satir=None):
    g_n, c_n = len(girdi), len(cikti)
    # ızgaralar ne kadar yer kaplarsa kapsın, altyazı üstüne binmesin
    y_ozet = 130 + max(g_n, c_n, 3) * H + 44
    Y = y_ozet + 26 + (not_satir or len(sonuc_notu)) * 22 + 26
    im = Image.new("RGB", (W, Y), ZEMIN)
    d = ImageDraw.Draw(im)
    d.text((42, 26), baslik, font=f_bas, fill=KOYU)
    d.text((42, 60), altbasl, font=f_alt, fill=GRI)

    gy = 130
    gx = 42
    kx = gx + g_n * H + 58
    cx = kx + 3 * H + 58
    ky = gy + (g_n - 3) * H // 2
    cy = gy + (g_n - c_n) * H // 2

    d.text((gx, gy - 26), f"GİRDİ  {g_n}×{g_n}", font=f_et, fill=KOYU)
    d.text((kx, ky - 26), "KERNEL 3×3", font=f_et, fill=MOR)
    d.text((cx, cy - 26), f"ÇIKTI  {c_n}×{c_n}", font=f_et, fill=YESIL)

    izgara(d, gx, gy, girdi, pencere=pencere, pad_hucre=pad_hucre)
    izgara(d, kx, ky, KERN, dolgu=MOR_A, kenar=(200, 190, 220), yazi=MOR)
    izgara(d, cx, cy, cikti, dolgu=YESIL_A, kenar=(200, 220, 208), yazi=YESIL)
    if aktif:
        r, c = aktif
        d.rectangle((cx + c * H, cy + r * H, cx + (c + 1) * H, cy + (r + 1) * H),
                    outline=KIRMIZI, width=3)

    orta(d, (kx - 48, ky, kx - 12, ky + 3 * H), "✳", f_sem, GRI)
    orta(d, (cx - 48, cy, cx - 12, cy + c_n * H), "=", f_sem, GRI)

    if yan:
        yx = cx + c_n * H + 58
        d.text((yx, gy - 26), yan[0], font=f_et, fill=GRI)
        for i, s in enumerate(yan[1:]):
            d.text((yx, gy + 6 + i * 24), s, font=f_not, fill=GRI)

    y = y_ozet
    d.text((42, y), ozet, font=f_notb, fill=KOYU)
    for i, s in enumerate(sonuc_notu):
        d.text((42, y + 26 + i * 22), s, font=f_not,
               fill=ZEYTIN if s.startswith("→") else GRI)
    return im


# ══════════════════════════════════════════════════════════════════════════
# 1) STRIDE
# ══════════════════════════════════════════════════════════════════════════
NOT_SATIR = 2


def stride_animasyon():
    t1, n1 = konv(G6, KERN, 1)
    t2, n2 = konv(G6, KERN, 2)
    kareler, sureler = [], []
    yan = ["KARŞILAŞTIRMA", "stride 1  →  çıktı 4×4",
           "stride 2  →  çıktı 2×2", "", "Filtre 2'şer atlayınca",
           "yarısı kadar konum kalır."]
    ozet = "6×6  ✳  3×3  ,  stride = 2   →   (6−3)/2 + 1 = 2   →   2×2"
    notlar = ["Filtre her seferinde 2 piksel kayar; aradaki konumlar atlanır.",
              "→ Stride büyüdükçe çıktı küçülür: hesap ucuzlar, ayrıntı kaybolur."]

    kareler.append(kare("ADIM 1a — Stride (filtrenin adım boyu)",
                        "Stride, filtrenin her hamlede kaç piksel kayacağıdır. "
                        "Girdi ve kernel aynı, değişen tek şey adım boyu.",
                        G6, [[None] * n2 for _ in range(n2)], ozet, notlar, yan=yan, not_satir=NOT_SATIR))
    sureler.append(3000)

    for r in range(n2):
        for c in range(n2):
            simdi = [[(t2[i][j] if (i < r or (i == r and j <= c)) else None)
                      for j in range(n2)] for i in range(n2)]
            kareler.append(kare(
                "ADIM 1a — Stride (filtrenin adım boyu)",
                f"Konum ({r},{c}) → girdide satır {r*2}, sütun {c*2}'den başlıyor. "
                f"Sonuç: {t2[r][c]}",
                G6, simdi, ozet, notlar,
                pencere=(r * 2, c * 2), aktif=(r, c), yan=yan, not_satir=NOT_SATIR))
            sureler.append(1300)

    kareler.append(kare("ADIM 1a — Stride (filtrenin adım boyu)",
                        "Bitti. Çıktı 2×2 — stride 1'de 4×4 olurdu.",
                        G6, t2, ozet, notlar, yan=yan, not_satir=NOT_SATIR))
    sureler.append(4200)
    return kareler, sureler


# ══════════════════════════════════════════════════════════════════════════
# 2) PADDING
# ══════════════════════════════════════════════════════════════════════════
def padding_animasyon():
    P = [[0] * 8 for _ in range(8)]
    for r in range(6):
        for c in range(6):
            P[r + 1][c + 1] = G6[r][c]
    pad = tuple([(0, c) for c in range(8)] + [(7, c) for c in range(8)]
                + [(r, 0) for r in range(1, 7)] + [(r, 7) for r in range(1, 7)])
    tam, n = konv(P, KERN, 1)

    yan = ["KARŞILAŞTIRMA", "padding yok  →  4×4",
           "padding 'same' →  6×6", "", "Girdiyle aynı boyut korunur."]
    ozet = "6×6 girdi → etrafına 0 → 8×8   ✳  3×3   →   (8−3)/1 + 1 = 6   →   6×6"
    notlar = ["Kenarlara bir sıra sıfır eklenir; böylece köşe pikselleri de "
              "filtrenin merkezine gelebilir.",
              "→ Çıktı girdiyle aynı boyutta kalır: Keras'ta padding='same'."]

    kareler, sureler = [], []
    kareler.append(kare("ADIM 1b — Padding (dolgulama)",
                        "Girdinin etrafına 0 eklenir. Amaç: çıktının boyutunu "
                        "korumak ve kenar bilgisini kurtarmak.",
                        P, [[None] * n for _ in range(n)], ozet, notlar,
                        pad_hucre=pad, yan=yan, not_satir=NOT_SATIR))
    sureler.append(3400)

    secim = [(0, 0), (0, 3), (0, 5), (2, 2), (4, 4), (5, 5)]
    for r, c in secim:
        simdi = [[(tam[i][j] if (i < r or (i == r and j <= c)) else None)
                  for j in range(n)] for i in range(n)]
        kareler.append(kare(
            "ADIM 1b — Padding (dolgulama)",
            f"Konum ({r},{c}) → sonuç {tam[r][c]}"
            + ("   (pencere sıfır dolguya değiyor)" if r == 0 or c == 0
               or r == n - 1 or c == n - 1 else ""),
            P, simdi, ozet, notlar, pencere=(r, c), aktif=(r, c),
            pad_hucre=pad, yan=yan))
        sureler.append(1400)

    kareler.append(kare("ADIM 1b — Padding (dolgulama)",
                        "Bitti. Çıktı 6×6 — girdiyle aynı boyut.",
                        P, tam, ozet, notlar, pad_hucre=pad, yan=yan, not_satir=NOT_SATIR))
    sureler.append(5000)
    return kareler, sureler


k, s = stride_animasyon()
kaydet("stride_gif.gif", k, s)
k, s = padding_animasyon()
kaydet("padding_gif.gif", k, s)
