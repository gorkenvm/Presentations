# Deep Learning MasterClass

Derin öğrenmenin hikâyesinden nöron, loss ve gradient descent'e; ANN, CNN, RNN/LSTM ve Transformer mimarilerinden canlı bir Colab uygulamasına.

| Yol | İçerik |
|---|---|
| [`ders-notlari.md`](ders-notlari.md) | **Katılımcı ders notları** — dersin tamamının okunabilir metni |
| `DL_MasterClass_Kuantum_v16 - share.pptx` | Sunum, 46 slayt |
| [`YuzAnalizi/`](YuzAnalizi) | Colab defteri: yüz tespiti, duygu / yaş / cinsiyet, yüz vektörü, YOLO nesne tespiti, kamerayla canlı takip |
| `resimler/` | Sunumda kullanılan görseller |

## Colab defteri

[`YuzAnalizi/DL_MasterClass_Colab_YuzAnalizi.ipynb`](YuzAnalizi/DL_MasterClass_Colab_YuzAnalizi.ipynb) dosyasını Colab'da *Dosya → Not defteri yükle* ile açın ve hücreleri sırayla çalıştırın.

- Colab'ın hazır paketlerine dokunmaz; yalnızca `deepface`, `retina-face`, `ultralytics`, `ultralytics-thop` ve `lap` sabit sürümleriyle, bağımlılıksız kurulur (~10 sn).
- CPU çalışma zamanında çalışır, GPU gerekmez. Model ağırlıkları (~1,3 GB) ilk çalıştırmada bir kez indirilir (~1 dk).
- Hiçbir model eğitilmez; Google Drive kullanılmaz.
- 27 Ekim 2026'da Colab'da (Python 3.13, CPU) baştan sona test edilmiştir.
