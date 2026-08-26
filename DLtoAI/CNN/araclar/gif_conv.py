"""Evrişim animasyonları: convolution (stride=1), stride=2 ve padding.

Üç GIF üretir. Hepsinde aynı düzen:  Girdi  ⊛  Kernel  =  Öznitelik haritası
Altta o adımın çarpım-toplam işlemi yazılır.
"""
import os

from PIL import Image, ImageDraw, ImageFont

DIZIN = "/sessions/peaceful-lucid-dijkstra/mnt/cnn2/resimler"
F_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
F_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

# --- renkler ---------------------------------------------------------------
BEYAZ = (255, 255, 255)
CIZGI = (176, 176, 176)
YAZI = (38, 38, 38)
VURGU = (196, 62, 42)          # aktif pencere
PENCERE = (253, 232, 214)      # aktif pencere dolgusu
KERNEL = (219, 234, 250)
KERNEL_K = (52, 108, 176)
CIKTI = (222, 244, 226)
CIKTI_K = (46, 132, 72)
DOLGU = (243, 243, 243)        # padding hücreleri
DOLGU_Y = (150, 150, 150)
SOLUK = (128, 128, 128)

f_bas = ImageFont.truetype(F_BOLD, 25)
f_etiket = ImageFont.truetype(F_BOLD, 19)
f_hucre = ImageFont.truetype(F_BOLD, 20)
f_alt = ImageFont.truetype(F_REG, 19)
f_sembol = ImageFont.truetype(F_BOLD, 34)

HUCRE = 52


def orta_yaz(d, kutu, metin, font, renk):
    x0, y0, x1, y1 = kutu
    l, t, r, b = d.textbbox((0, 0), metin, font=font)
    d.text((x0 + (x1 - x0 - (r - l)) / 2 - l,
            y0 + (y1 - y0 - (b - t)) / 2 - t), metin, font=font, fill=renk)


def matris(d, x0, y0, veri, dolgu=None, kenar=None, yazi=None,
           pencere=None, bos=None, dolgulu=()):
    """veri: 2B liste. pencere=(r,c,h,w) vurgulanacak bölge. bos: çizilmeyecek değerler."""
    n_sat, n_sut = len(veri), len(veri[0])
    for r in range(n_sat):
        for c in range(n_sut):
            x, y = x0 + c * HUCRE, y0 + r * HUCRE
            kutu = (x, y, x + HUCRE, y + HUCRE)
            icinde = pencere and (pencere[0] <= r < pencere[0] + pencere[2]
                                  and pencere[1] <= c < pencere[1] + pencere[3])
            pad = (r, c) in dolgulu
            f = PENCERE if icinde else (DOLGU if pad else (dolgu or BEYAZ))
            k = VURGU if icinde else (DOLGU_Y if pad else (kenar or CIZGI))
            d.rectangle(kutu, fill=f, outline=k, width=2 if (icinde or pad) else 1)
            v = veri[r][c]
            if bos is not None and v is bos:
                continue
            orta_yaz(d, kutu, str(v), f_hucre,
                     DOLGU_Y if pad else (VURGU if icinde else (yazi or YAZI)))
    if pencere:
        r, c, h, w = pencere
        d.rectangle((x0 + c * HUCRE, y0 + r * HUCRE,
                     x0 + (c + w) * HUCRE, y0 + (r + h) * HUCRE),
                    outline=VURGU, width=4)


def kare_ciz(girdi, kernel, cikti, baslik, altyazi, pencere=None,
             aktif_cikti=None, dolgulu=(), W=980):
    g_sat, g_sut = len(girdi), len(girdi[0])
    c_sat, c_sut = len(cikti), len(cikti[0])
    ust = 96
    H = ust + max(g_sat, 3, c_sat) * HUCRE + 100   # altyazı bandı taşmasın

    im = Image.new("RGB", (W, H), BEYAZ)
    d = ImageDraw.Draw(im)
    d.text((26, 18), baslik, font=f_bas, fill=VURGU)
    gx = 30
    kx = gx + g_sut * HUCRE + 74
    cx = kx + 3 * HUCRE + 78

    # dikey ortalama
    en_uzun = max(g_sat, 3, c_sat)
    gy = ust + (en_uzun - g_sat) * HUCRE // 2
    ky = ust + (en_uzun - 3) * HUCRE // 2
    cy = ust + (en_uzun - c_sat) * HUCRE // 2

    d.text((gx, gy - 30), f"Girdi  {g_sat}×{g_sut}", font=f_etiket, fill=YAZI)
    d.text((kx, ky - 30), "Kernel 3×3", font=f_etiket, fill=KERNEL_K)
    d.text((cx, cy - 30), f"Öznitelik haritası  {c_sat}×{c_sut}",
           font=f_etiket, fill=CIKTI_K)

    matris(d, gx, gy, girdi, pencere=pencere, dolgulu=dolgulu)
    matris(d, kx, ky, kernel, dolgu=KERNEL, kenar=KERNEL_K, yazi=KERNEL_K)

    goster = [[("" if v is None else v) for v in sat] for sat in cikti]
    matris(d, cx, cy, goster, dolgu=CIKTI, kenar=CIKTI_K, yazi=CIKTI_K, bos="")
    if aktif_cikti:
        r, c = aktif_cikti
        d.rectangle((cx + c * HUCRE, cy + r * HUCRE,
                     cx + (c + 1) * HUCRE, cy + (r + 1) * HUCRE),
                    outline=VURGU, width=4)

    orta_yaz(d, (kx - 62, ky, kx - 12, ky + 3 * HUCRE), "⊛", f_sembol, YAZI)
    orta_yaz(d, (cx - 62, cy, cx - 12, cy + c_sat * HUCRE), "=", f_sembol, YAZI)

    y = H - 78
    d.line([(26, y), (W - 26, y)], fill=(226, 226, 226), width=2)
    for i, satir in enumerate(altyazi):
        d.text((26, y + 16 + i * 27), satir, font=f_alt,
               fill=VURGU if i == 0 else YAZI)
    return im


def kaydet(ad, kareler, sureler):
    p = [k.convert("P", palette=Image.ADAPTIVE, colors=64) for k in kareler]
    yol = os.path.join(DIZIN, ad)
    p[0].save(yol, save_all=True, append_images=p[1:],
              duration=sureler, loop=0, optimize=True)
    print(f"{ad:24s} {os.path.getsize(yol)//1024:4d} KB  {len(p)} kare")


def carpim_metni(pencere_deg, kernel):
    parcalar = []
    for r in range(3):
        for c in range(3):
            k = kernel[r][c]
            parcalar.append(f"{pencere_deg[r][c]}·{k}" if k >= 0
                            else f"{pencere_deg[r][c]}·({k})")
    return " + ".join(parcalar)


# ══════════════════════════════════════════════════════════════════════════
# Ortak veri: dikey kenarlı 5×5 görüntü + dikey kenar bulucu kernel
# ══════════════════════════════════════════════════════════════════════════
GIRDI = [[10, 10, 0, 0, 0] for _ in range(5)]
KERN = [[1, 0, -1], [1, 0, -1], [1, 0, -1]]


def hesapla(girdi, kernel, stride):
    n = len(girdi)
    c_n = (n - 3) // stride + 1
    out = [[0] * c_n for _ in range(c_n)]
    for r in range(c_n):
        for c in range(c_n):
            s = 0
            for i in range(3):
                for j in range(3):
                    s += girdi[r * stride + i][c * stride + j] * kernel[i][j]
            out[r][c] = s
    return out, c_n


def animasyon(girdi, kernel, stride, baslik, son_not, dolgulu=(), atla=1):
    """Filtrenin gezinme animasyonunu üretir."""
    tam, c_n = hesapla(girdi, kernel, stride)
    n = len(girdi)
    kareler, sureler = [], []

    bos = [[None] * c_n for _ in range(c_n)]
    kareler.append(kare_ciz(
        girdi, kernel, bos, baslik,
        [f"Çıktı boyutu = (girdi − kernel) / stride + 1 = "
         f"({n} − 3) / {stride} + 1 = {c_n}",
         "Filtre sol üst köşeden başlar, her konumda çarpıp toplar."],
        dolgulu=dolgulu))
    sureler.append(2600)

    sayac = 0
    for r in range(c_n):
        for c in range(c_n):
            sayac += 1
            son = (r == c_n - 1 and c == c_n - 1)
            if sayac % atla and not son:
                continue
            simdi = [[(tam[i][j] if (i < r or (i == r and j <= c)) else None)
                      for j in range(c_n)] for i in range(c_n)]
            pd = [[girdi[r * stride + i][c * stride + j] for j in range(3)]
                  for i in range(3)]
            kareler.append(kare_ciz(
                girdi, kernel, simdi, baslik,
                [f"Konum ({r},{c}):  {carpim_metni(pd, kernel)}  =  {tam[r][c]}",
                 "Pencere ile kernel eleman eleman çarpılır, sonuçlar toplanır."],
                pencere=(r * stride, c * stride, 3, 3),
                aktif_cikti=(r, c), dolgulu=dolgulu))
            sureler.append(1100)

    kareler.append(kare_ciz(
        girdi, kernel, tam, baslik,
        ["Bitti — öznitelik haritası hazır.", son_not],
        dolgulu=dolgulu))
    sureler.append(3800)
    return kareler, sureler


# ── 1) Convolution, stride = 1 ────────────────────────────────────────────
k, s = animasyon(GIRDI, KERN, 1, "Convolution  ·  stride = 1",
                 "Dikey kenar bulucu kernel: kenarın olduğu sütunlar 30, düz bölgeler 0.")
kaydet("conv_stride1.gif", k, s)

# ── 2) Stride = 2 ─────────────────────────────────────────────────────────
k, s = animasyon(GIRDI, KERN, 2, "Convolution  ·  stride = 2  (filtre 2'şer atlar)",
                 "stride=1'de 3×3 idi, stride=2'de 2×2 oldu: hesap ucuzlar, ayrıntı kaybolur.")
kaydet("conv_stride2.gif", k, s)

# ── 3) Padding = same ─────────────────────────────────────────────────────
P = [[0] * 7 for _ in range(7)]
for r in range(5):
    for c in range(5):
        P[r + 1][c + 1] = GIRDI[r][c]
DOLGU_HUC = tuple([(0, c) for c in range(7)] + [(6, c) for c in range(7)]
                  + [(r, 0) for r in range(1, 6)] + [(r, 6) for r in range(1, 6)])

k, s = animasyon(P, KERN, 1, "Padding = 'same'  ·  kenarlara 0 eklenir",
                 "Çıktı 5×5 — girdiyle aynı. Kenardaki −20/−30 ise sıfır dolgunun "
                 "yarattığı yapay kenardır.",
                 dolgulu=DOLGU_HUC, atla=3)
k[0] = kare_ciz(P, KERN, [[None] * 5 for _ in range(5)],
                "Padding = 'same'  ·  kenarlara 0 eklenir",
                ["5×5 girdinin etrafına bir sıra 0 eklendi → 7×7",
                 "Çıktı = (7 − 3)/1 + 1 = 5  →  girdi ile aynı boyut, kenar bilgisi korunur."],
                dolgulu=DOLGU_HUC)
kaydet("conv_padding.gif", k, s)
