# -*- coding: utf-8 -*-
"""
03_rag.py — Olguyu modelin hafızasından değil, belgeden getir.

Beş adım, her biri Enter ile:
  1  PARÇALA    katalog → eğitim kayıtları
  2  GÖM        her parça → vektör
  3  ARA        soru vektörü ile kosinüs benzerliği
  4  ENJEKTE ET bulunan parçalar prompt'a girer   ← 1. saate köprü
  5  CEVAPLA    model sadece o metinden konuşur + kaynak gösterilir

Sonra ⭐ KÖPRÜ: RAG'in çuvalladığı soru.
"Benim ilerlemem ne durumda?" — bu bilgi hiçbir belgede yok, veritabanında.

LangChain yok. sentence-transformers + numpy kosinüs, o kadar.

Çalıştır:  python 03_rag.py
"""
import sys

from ortak import (CY, GOMME_MODELI, KL, KR, MR, MV, R, SN, SR, YS, altbaslik,
                   alan, baslik, bilgi, cubuk, duraklat, kutu, parcala, sor)

SORU = "Data Scientist Path kaç saat sürüyor ve ücreti ne kadar?"
KOPRU_SORU = "Benim ilerlemem ne durumda? Kayıt numaram 482137"

KAC_PARCA = 3

# Provada altı varyant denendi. Kazanan kurgu bu:
# talimat ÖNDE değil ARKADA, ve "bulamazsan şunu de" cümlesi EN SONDA.
# Kaçış cümlesi başa konduğunda küçük modeller onu refleks olarak basıp
# önlerindeki metni hiç okumuyor — RAG demolarının klasik sessiz hatası.
TALIMAT = """Cevabını yukarıdaki kayıtlardan al. Süre ve ücret gibi sayıları
kayıtta yazdığı gibi aktar ve sonuna hangi eğitimden aldığını yaz.
Kayıtlarda cevap gerçekten yoksa "Bu bilgi katalogda yer almıyor." yaz."""

_gomucu = None


def gom(metinler, onek):
    """Metinleri vektöre çevirir.

    e5 ailesi 'query:' ve 'passage:' öneklerini bekliyor. Bu önek
    unutulursa benzerlik skorları gözle görülür şekilde bozulur —
    RAG demolarının bir başka klasik sessiz hatası.
    """
    global _gomucu
    if _gomucu is None:
        from sentence_transformers import SentenceTransformer
        print(SN + "   gömme modeli yükleniyor: " + GOMME_MODELI + R, flush=True)
        _gomucu = SentenceTransformer(GOMME_MODELI)
    return _gomucu.encode([f"{onek}: {m}" for m in metinler],
                          normalize_embeddings=True, batch_size=32)


def ara(soru, parcalar, vektorler, kac=KAC_PARCA):
    """Kosinüs benzerliği. Vektörler normalize olduğu için nokta çarpımı yeter."""
    import numpy as np
    s = gom([soru], "query")[0]
    skorlar = vektorler @ s
    sira = np.argsort(-skorlar)[:kac]
    return [(parcalar[i], float(skorlar[i])) for i in sira]


def istem_kur(soru, bulunan):
    baglam = "\n\n".join(p["tam"] for p, _ in bulunan)
    return (f"Aşağıdaki katalog kayıtlarını oku ve soruyu cevapla.\n\n"
            f"{baglam}\n\nSORU: {soru}\n\n{TALIMAT}")


def skor_cizgisi(p, s, renk=MV):
    # 0.80–0.95 aralığını görünür kıl: skorlar hep yüksek çıkar,
    # önemli olan aralarındaki FARK.
    return f"   {cubuk((s - 0.78) / 0.17, renk=renk)}  {s:.3f}  {p['baslik'][:44]}"


def main():
    baslik("03 — RAG:  olguyu dışarıdan getir")
    bilgi("Model hâlâ aynı model. Değişen tek şey: kataloğu prompt'a koyuyoruz.")
    duraklat("başlamak için Enter")

    # ── ADIM 1 — PARÇALA ─────────────────────────────────────────────
    altbaslik("ADIM 1 — PARÇALA:  katalog → kayıtlar")
    parcalar = parcala()
    print()
    alan("kaynak", "veri/miuul_katalog.md")
    alan("parça", f"{len(parcalar)} kayıt")
    print()
    for p in parcalar[8:13]:
        ozet = " ".join(p["metin"].split())[:46]
        print(f"{SN}   {R}{p['baslik'][:36]:<36}{SN} {ozet}…{R}")
    print(f"{SN}   ...  (toplam {len(parcalar)} parça){R}")
    print()
    bilgi("Burada işimiz kolay: katalog zaten eğitim eğitim ayrılmış.")
    bilgi("Gerçek hayatta parçalama stratejisi RAG kalitesinin yarısıdır.")
    duraklat()

    # ── ADIM 2 — GÖM ─────────────────────────────────────────────────
    altbaslik("ADIM 2 — GÖM:  her parça → vektör")
    print()
    vektorler = gom([p["tam"] for p in parcalar], "passage")
    alan("gömme modeli", GOMME_MODELI, MV, 15)
    alan("matris", f"{vektorler.shape[0]} parça × {vektorler.shape[1]} boyut",
         "", 15)
    print()
    bilgi("Türkçe için çok dilli bir model şart. İngilizce-only modeller")
    bilgi("bu katalogda gözle görülür şekilde yanlış parça getiriyor.")
    duraklat()

    # ── ADIM 3 — ARA ─────────────────────────────────────────────────
    altbaslik("ADIM 3 — ARA:  soru vektörü ile kosinüs benzerliği")
    alan("soru", SORU, KL)
    print()
    ilk_bes = ara(SORU, parcalar, vektorler, kac=5)
    for i, (p, s) in enumerate(ilk_bes):
        isaret = f"  {YS}◀ en yakın{R}" if i == 0 else ""
        print(skor_cizgisi(p, s) + isaret)
    print()
    bilgi(f"En yakın {KAC_PARCA} parçayı alıyoruz.")
    bilgi("Skorlara dikkat: aradaki FARK önemli. Hepsi birbirine yakınsa")
    bilgi("arama katmanı zorlanıyor demektir — izlenmesi gereken metrik bu.")
    duraklat()

    # ── ADIM 4 — ENJEKTE ET ──────────────────────────────────────────
    altbaslik("ADIM 4 — ENJEKTE ET:  bulunan parçalar prompt'a giriyor", MR)
    print()
    bulunan = ilk_bes[:KAC_PARCA]
    istem = istem_kur(SORU, bulunan)
    kutu(istem, "modele giden prompt", MR)
    print()
    kutu("Buradaki tek numara metni BAĞLAM PENCERESİNE sokmak.\n"
         "Attention o metne de bakıyor — bir saat önce çizdiğimiz\n"
         "aynı mekanizma çalışıyor. Dışarıdan gelen bir sihir yok.",
         "1. saate köprü", CY)
    duraklat()

    # ── ADIM 5 — CEVAPLA ─────────────────────────────────────────────
    altbaslik("ADIM 5 — CEVAPLA", YS)
    print()
    cevap = sor("", istem, sicaklik=0.0, en_fazla=170)
    kutu(" ".join(cevap.split()), "model", YS)
    print()

    kaynak, skor = bulunan[0]
    dogru_satir = next((s for s in kaynak["metin"].split("\n")
                        if s.startswith("Süre:")), "")
    alan("kaynak", f"{kaynak['baslik']}   (benzerlik {skor:.3f})", CY, 12)
    alan("katalogda", dogru_satir[:60], SN, 12)
    print()
    bilgi("Kaynağı MODEL söylemiyor — sistem zaten biliyor, hangi parçayı")
    bilgi("verdiğini kendisi kaydetti. RAG'in en büyük üstünlüğü bu:")
    bilgi("DENETLENEBİLİRLİK. Cevabın nereden geldiğini gösterebiliyorsunuz.")
    print()
    bilgi("Halüsinasyon bitti mi? Bu soru için bitti.")
    bilgi("Çünkü cevabı modelin hafızasından değil, katalogdan aldık.")
    duraklat()

    # ── KÖPRÜ ⭐ ─────────────────────────────────────────────────────
    baslik("⭐ KÖPRÜ — RAG'in çuvalladığı an", KR)
    bilgi("Aynı sistemi hiç değiştirmeden yeni bir soru soruyoruz.")
    print()
    alan("soru", KOPRU_SORU, KL)
    print()
    duraklat("aramayı çalıştır")

    kopru = ara(KOPRU_SORU, parcalar, vektorler, KAC_PARCA)
    print(f"{SN}   en yakın parçalar:{R}")
    for p, s in kopru:
        print(skor_cizgisi(p, s, KR))
    print()

    yayilim = kopru[0][1] - kopru[-1][1]
    bilgi(f"Skorlar arasındaki fark: {yayilim:.3f}  "
          f"(yukarıdaki soruda {ilk_bes[0][1] - ilk_bes[2][1]:.3f} idi)")
    bilgi("Neredeyse düz. Arama katmanı size 'hiçbiri uymuyor' diyor.")
    print()

    k_cevap = sor("", istem_kur(KOPRU_SORU, kopru), sicaklik=0.0, en_fazla=140)
    kutu(" ".join(k_cevap.split()), "model", MV)
    print()

    kutu("RAG burada çaresiz.\n"
         "Çünkü bu bilgi hiçbir belgede YOK — veritabanında.\n"
         "\n"
         "Belgede arayamazsınız; SORGULAMANIZ gerekir.\n"
         "Elimizde ilerleme_durumu() diye bir Python fonksiyonu var.\n"
         "\n"
         "Peki model bir fonksiyonu kendi kendine nasıl çağıracak?\n"
         "→ 04_finetune.py",
         "her şeyi RAG çözmez", KR)
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
