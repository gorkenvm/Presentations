# Ders demosu — Havlama Tespiti

Transfer learning / fine-tuning dersinde **bonus canlı demo** olarak
gösterilmek üzere hazırlanmış kısa bir notebook (15 hücre).

```
havlama_tespiti_demo.ipynb   ← tek dosya, kendi kendine yeter (684 KB)
data/ornek_ses.wav           ← aynı sesin WAV hali (notebook için GEREKLİ DEĞİL)
```

## 🚀 Google Colab'da çalıştırma

Notebook **kendi kendine yeter**: 1 dakikalık ses kaydı FLAC olarak base64
biçiminde notebook'un içine gömülüdür. Yani:

1. `havlama_tespiti_demo.ipynb` dosyasını Colab'a yükleyin
   (*File → Upload notebook*),
2. *Runtime → Run all*.

Başka hiçbir dosya yüklemeniz gerekmez. Eksik paket varsa (Colab'da genelde
`tensorflow_hub`) ilk hücre otomatik kurar. Bu senaryo, veri klasörü olmayan
boş bir dizinde çalıştırılarak test edildi.

## 💻 Yerelde çalıştırma

```powershell
code teaching/havlama_tespiti_demo.ipynb    # VS Code: kernel olarak .venv seçin
```

İlk çalıştırmada YAMNet ağırlıkları (~15 MB) TF-Hub'dan indirilir.
CPU'da toplam ~1 dakika.

> Notebook **çıktısız** kaydedildi — hücreleri derste sınıfın önünde
> çalıştırmak için. Böylece dosya küçük kalıyor ve "şimdi dinleyelim /
> şimdi bakalım" akışı bozulmuyor.

## Akış (3 adım)

1. **Dinle** — 1 dakikalık gerçek kamera kaydı çalınır, sınıf kaç havlama
   duyduğunu sayar.
2. **Tespit et** — hazır YAMNet modeli yüklenir, çalıştırılır, havlamalar
   otomatik bulunur. Hiçbir eğitim yapılmaz. Modelin en emin olduğu andaki
   ilk 5 tahmini de gösterilir (`Dog 0.99`, `Bark 0.85` ...).
3. **Grafikte incele + tekrar dinle** — ses dalgası ve model skoru yan yana
   çizilir, ardından **bulunan her havlama tek tek dinlenir**; numaralar
   grafikteki turuncu bantlarla eşleşir.

Bu kayıtta model 5 havlamanın 5'ini de buluyor (skorlar 0.72–0.99).

## Veri hakkında

10.08.2026 kaydının 11:03:54–11:04:36 aralığından alınmış **kesintisiz** bir
kesit — yapay olarak birleştirilmiş değil. Köpek evde yalnız; arka planda
Berlin'de yoğun bir caddenin trafiği var, yani "kolay" bir stüdyo kaydı değil.

## Derste değinebileceğiniz iki gözlem

- **Tespitler ~1 saniye geç başlıyor.** YAMNet 0.96 sn'lik pencerelere bakar;
  havlamanın pencereye tam yerleşmesi gerekir. Pencere tabanlı modellerin
  kaçınılmaz gecikmesi.
- **Skor bazı havlamaların ortasında düşüyor** (köpek nefes alıyor). Bu yüzden
  ham kare skoru değil, birleştirilmiş **olaylar** raporlanır — notebook'ta
  arası 1 saniyeden az olan parçalar tek havlama sayılıyor.

Bu demonun tam üretim hali ana projede: çoklu oturum, mutlak zaman ekseni,
elle etiketleme ile doğrulama, raporlama → `../README.md`
