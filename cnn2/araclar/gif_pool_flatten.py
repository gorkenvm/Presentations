"""Pooling (max vs average) ve Flatten animasyonları.

Sayılar uydurma DEĞİL: conv_gif3'ün ekranda gösterdiği 4 kanallı 4×4 haritalar
birebir alındı. Böylece conv → pooling → flatten zinciri kopmuyor.
"""
from cizim import (KANAL, KANAL_A, GRI, KOYU, ACIK, BEYAZ, VURGU, ZEMIN,
                   f_et, f_not, izgara, kaydet, ok, orta, zemin, dipnot)

# conv_gif3'ten okunan 4 kanallı 4×4 giriş
HARITA = [
    [[1, 1, 7, 4], [5, 6, 7, 0], [4, 1, 4, 9], [5, 0, 5, 1]],
    [[7, 9, 9, 6], [8, 3, 1, 5], [4, 6, 9, 2], [8, 1, 3, 7]],
    [[2, 6, 4, 5], [9, 8, 8, 5], [9, 9, 1, 2], [3, 5, 8, 4]],
    [[9, 3, 9, 5], [7, 2, 5, 8], [8, 8, 9, 1], [7, 4, 6, 2]],
]
PENCERE = [(0, 0), (0, 1), (1, 0), (1, 1)]      # 2×2 çıktıdaki konumlar


def havuz(m, r, c, kip):
    p = [m[2 * r][2 * c], m[2 * r][2 * c + 1],
         m[2 * r + 1][2 * c], m[2 * r + 1][2 * c + 1]]
    return max(p) if kip == "max" else round(sum(p) / 4, 2)


def sonuc(m, kip):
    return [[havuz(m, r, c, kip) for c in range(2)] for r in range(2)]


# ══════════════════════════════════════════════════════════════════════
# 1) Max vs Average pooling — tek kanal üstünde yan yana
# ══════════════════════════════════════════════════════════════════════
def max_avg():
    M = HARITA[0]
    mx, av = sonuc(M, "max"), sonuc(M, "ort")
    W, Y = 1120, 470
    baslik = "Pooling: Max mı, Average mı?"
    kareler, sureler = [], []

    ozet = "4×4  →  2×2 pencere, stride 2  →  2×2   (kanal sayısı değişmez)"
    notlar = ["Max en güçlü sinyali seçer; average pencereyi yumuşatır.",
              "→ Kenar/doku gibi 'var mı yok mu' bilgisinde max, "
              "genel parlaklıkta average işe yarar."]

    for adim in range(5):
        im, d = zemin(W, Y, baslik,
                      "Aynı 4×4 harita, aynı pencere — sadece pencere içinden "
                      "ne aldığımız değişiyor.")
        acik = PENCERE[:adim]
        simdi = PENCERE[adim] if adim < 4 else None
        hucre = set()
        if simdi:
            r, c = simdi
            hucre = {(2 * r, 2 * c), (2 * r, 2 * c + 1),
                     (2 * r + 1, 2 * c), (2 * r + 1, 2 * c + 1)}

        d.text((42, 112), "GİRDİ  4×4  (kanal 1)", font=f_et, fill=KOYU)
        izgara(d, 42, 136, M, vurgu=hucre)

        gm = [[(mx[r][c] if (r, c) in acik or (r, c) == simdi else None)
               for c in range(2)] for r in range(2)]
        ga = [[(av[r][c] if (r, c) in acik or (r, c) == simdi else None)
               for c in range(2)] for r in range(2)]

        d.text((330, 112), "MAX POOLING  2×2", font=f_et, fill=KANAL[1])
        izgara(d, 330, 136, gm, h=56, dolgu=KANAL_A[1], kenar=(206, 196, 224),
               yazi=KANAL[1], kalin={simdi} if simdi else set())

        d.text((580, 112), "AVERAGE POOLING  2×2", font=f_et, fill=KANAL[2])
        izgara(d, 580, 136, ga, h=56, dolgu=KANAL_A[2], kenar=(198, 224, 224),
               yazi=KANAL[2], kalin={simdi} if simdi else set())

        ok(d, 250, 196, 316)
        if simdi:
            r, c = simdi
            p = [M[2 * r][2 * c], M[2 * r][2 * c + 1],
                 M[2 * r + 1][2 * c], M[2 * r + 1][2 * c + 1]]   # okuma sırası
            d.text((42, 320), f"Pencere: {p}", font=f_not, fill=VURGU)
            d.text((42, 344), f"max = {mx[r][c]}     ortalama = "
                              f"{sum(p)}/4 = {av[r][c]}", font=f_not, fill=VURGU)

        dipnot(d, 388, ozet, notlar)
        kareler.append(im)
        sureler.append(1700 if simdi else 4000)
    return kareler, sureler


# ══════════════════════════════════════════════════════════════════════
# 2) Flatten — 2×2×4 blok tek sıraya serilir
# ══════════════════════════════════════════════════════════════════════
def flatten():
    havuzlu = [sonuc(m, "max") for m in HARITA]        # 4 adet 2×2
    # TensorFlow/Keras channels_last sırası: (satır, sütun, kanal)
    sira = [(r, c, k) for r in range(2) for c in range(2) for k in range(4)]
    vektor = [havuzlu[k][r][c] for r, c, k in sira]

    W, Y = 1180, 566
    baslik = "ADIM 3 — Flatten (düzleştirme)"
    alt = ("Pooling'den çıkan 2×2×4 blok tek sıra sayıya serilir. "
           "Bilgi aynı, sadece şekli değişti.")
    ozet = "2 × 2 × 4  =  16 değer   →   Dense (Fully Connected) katmanının girişi"
    notlar = ["Sıra: önce (0,0) konumunun 4 kanalı, sonra (0,1)... "
              "yani satır → sütun → kanal.",
              "→ Flatten hiçbir şey öğrenmez, ağırlığı yoktur; sadece şekil değiştirir."]

    kareler, sureler = [], []
    for adim in range(5):
        im, d = zemin(W, Y, baslik, alt)
        konum = [(r, c) for r in range(2) for c in range(2)]
        aktif = konum[adim] if adim < 4 else None

        d.text((42, 112), "POOLING ÇIKTISI  2×2×4", font=f_et, fill=KOYU)
        for k in range(4):
            y = 134 + k * 74
            d.text((42, y - 18), f"kanal {k+1}", font=f_et, fill=KANAL[k])
            izgara(d, 42, y, havuzlu[k], h=34, dolgu=KANAL_A[k],
                   kenar=ACIK, yazi=KANAL[k],
                   vurgu={aktif} if aktif else set(), vurgu_renk=VURGU)

        vx, vy = 300, 258
        d.text((vx, vy - 30), "FLATTEN  →  16 elemanlı vektör", font=f_et, fill=KOYU)
        dolu = (adim if adim < 4 else 4) * 4
        gost = [[(vektor[i] if i < dolu else None) for i in range(16)]]
        izgara(d, vx, vy, gost, h=34, dolgu=BEYAZ, kenar=ACIK,
               kalin={(0, i) for i in range(dolu - 4, dolu)} if aktif else set())
        for i in range(16):
            orta(d, (vx + i * 34, vy + 34, vx + (i + 1) * 34, vy + 52),
                 f"k{sira[i][2]+1}", f_et, ACIK if i >= dolu else KANAL[sira[i][2]])

        if aktif:
            r, c = aktif
            d.text((300, 158), f"Konum ({r},{c}) → 4 kanalın bu hücresi "
                               f"sırayla vektöre yazılıyor", font=f_not, fill=VURGU)
            d.text((300, 184), "  ".join(str(havuzlu[k][r][c]) for k in range(4)),
                   font=f_not, fill=VURGU)

        dipnot(d, 452, ozet, notlar)
        kareler.append(im)
        sureler.append(2000 if aktif else 4500)
    return kareler, sureler


k, s = max_avg()
kaydet("pool_max_avg.gif", k, s)
k, s = flatten()
kaydet("flatten_gif.gif", k, s)
