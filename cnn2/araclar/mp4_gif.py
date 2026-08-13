"""Kullanıcının verdiği MP4 animasyonlarını GIF'e çevirir.

Neden bu kadar dolambaçlı:
  * MP4 not defterinin markdown hücresinde oynamaz, GIF oynar.
  * ffmpeg'in palettegen'i (stats_mode=diff) kanal renklerini (R/G/B) doğru
    korur; PIL'in ortak paleti maviyi griye çeviriyordu.
  * Ama ffmpeg GIF'e sabit kare süresi yazıyor. Videolar slayt temposunda
    (bazı kareler 0.48 sn, bazıları 1.10 sn) — bu tempo derste önemli.
    Bu yüzden GIF üretildikten sonra kare süreleri bayt düzeyinde yamanıyor.
"""
import json
import os
import struct
import subprocess

KAYNAK = "/sessions/peaceful-lucid-dijkstra/mnt/cnn2/resimler"
GENISLIK = 900
RENK = 255


def kare_sureleri(mp4):
    """Her karenin ekranda kaldığı süre (santisaniye)."""
    ham = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_frames",
         "-show_entries", "frame=pkt_duration_time", "-of", "json", mp4],
        capture_output=True, text=True, check=True).stdout
    cs = [max(2, int(round(float(k["pkt_duration_time"]) * 100)))
          for k in json.loads(ham)["frames"] if k.get("pkt_duration_time")]
    if cs:
        cs[-1] = max(cs[-1], 300)          # son kare 3 sn dursun
    return cs


def gce_konumlari(d):
    """GIF akışını gerçekten ayrıştırıp her Graphic Control Extension'ın
    gecikme baytlarının offsetini döndürür (imge verisinde yanlış eşleşme olmasın)."""
    i = 6                                   # "GIF89a"
    paket = d[i + 4]
    i += 7
    if paket & 0x80:                        # global renk tablosu
        i += 3 * (1 << ((paket & 7) + 1))

    konum = []
    while i < len(d):
        b = d[i]
        if b == 0x3B:                       # trailer
            break
        if b == 0x21:                       # extension
            etiket = d[i + 1]
            i += 2
            if etiket == 0xF9:
                konum.append(i + 2)         # uzunluk baytı + packed → gecikme
            while d[i]:                     # alt bloklar
                i += 1 + d[i]
            i += 1
        elif b == 0x2C:                     # image descriptor
            paket = d[i + 9]
            i += 10
            if paket & 0x80:                # yerel renk tablosu
                i += 3 * (1 << ((paket & 7) + 1))
            i += 1                          # LZW min code size
            while d[i]:
                i += 1 + d[i]
            i += 1
        else:
            raise ValueError(f"beklenmeyen blok 0x{b:02X} @ {i}")
    return konum


def sureleri_yaz(gif, cs):
    d = bytearray(open(gif, "rb").read())
    yer = gce_konumlari(d)
    if len(yer) != len(cs):
        raise ValueError(f"{gif}: {len(yer)} GCE ama {len(cs)} süre")
    for o, v in zip(yer, cs):
        d[o:o + 2] = struct.pack("<H", v)
    open(gif, "wb").write(d)


def cevir(ad):
    mp4 = os.path.join(KAYNAK, f"{ad}.mp4")
    gif = os.path.join(KAYNAK, f"{ad}.gif")
    pal = f"/tmp/{ad}_pal.png"
    olcek = f"scale={GENISLIK}:-2:flags=lanczos"

    subprocess.run(["ffmpeg", "-v", "error", "-i", mp4, "-vf",
                    f"{olcek},palettegen=max_colors={RENK}:stats_mode=diff",
                    "-y", pal], check=True)
    subprocess.run(["ffmpeg", "-v", "error", "-vsync", "0", "-i", mp4, "-i", pal,
                    "-lavfi", f"{olcek}[x];[x][1:v]paletteuse=dither=none:"
                              "diff_mode=rectangle",
                    "-gifflags", "+transdiff", "-y", gif], check=True)

    cs = kare_sureleri(mp4)
    sureleri_yaz(gif, cs)
    print(f"{ad:12s} {len(cs):3d} kare  {sum(cs)/100:5.1f} sn  "
          f"{os.path.getsize(gif)//1024:4d} KB")


for ad in ("conv_gif", "conv_gif2", "conv_gif3"):
    cevir(ad)
