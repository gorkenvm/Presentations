# Görev: Colab'da DeepFace çalışmıyor — `cv2` bozuk

## Ortam
- Google Colab (ücretsiz katman), Python **3.12**, CPU runtime
- Google Drive **bağlı değil** ve Drive alanı yok — defter her seferinde
  *Dosya → Not defteri yükle* ile yükleniyor
- Defter: `DL_MasterClass_Colab_YuzAnalizi.ipynb` — DeepFace ile yüz tespiti,
  duygu / yaş / cinsiyet analizi ve yüz embedding'i gösteriyor
- Kullanım amacı: canlı ders sunumu, 2 saatlik bir eğitimin uygulama bölümü

## Hata
```
AttributeError: module 'cv2' has no attribute 'CascadeClassifier'
```
`deepface/models/face_detection/OpenCv.py` içinde `__build_cascade` çağrısında
patlıyor. Yani `DeepFace.extract_faces(..., detector_backend="opencv")` çalışmıyor.

## Teşhis çıktısı (Colab'da alındı)
```
Package                  Version
opencv-python-headless   5.0.0.93
cv2 sürüm : 5.0.0
cv2 dosya : /usr/local/lib/python3.12/dist-packages/cv2/__init__.py
CascadeClassifier var mı : False
```

## Kök sebep (tespit edilen)
1. `pip install deepface` bağımlılık olarak `opencv-python` çekiyor ve pip
   varsayılan olarak **en yeni** sürümü alıyor: **OpenCV 5.0**.
2. OpenCV 5.0'da `cv2.CascadeClassifier` (Haar cascade API) çekirdek
   `objdetect` modülünden **kaldırıldı**. DeepFace hâlâ 4.x API'sini kullanıyor.
3. Ayrıca Colab'da zaten kurulu olan `opencv-python-headless` ile `deepface`'in
   kurduğu `opencv-python` **aynı `cv2/` dizinine** yazıyor; pip biri kaldırılınca
   diğerinin dosyalarını temizlemediği için dizinde karışık/artık dosyalar kalıyor.

## Şu ana kadar denenenler (hepsi başarısız)
1. `pip uninstall -y opencv-python opencv-contrib-python opencv-python-headless
   opencv-contrib-python-headless` → `pip install opencv-python-headless`
2. Aynısı + kurulumdan sonra runtime'ı
   `IPython.Application.instance().kernel.do_shutdown(True)` ile otomatik yeniden
   başlatma (bozuk `cv2` bir kez import edildiyse pip'in düzeltemediği için)
3. Sürüm sabitleme: `pip install "opencv-python-headless>=4.10,<5"`
4. Runtime'ı tamamen silip (Çalışma zamanı → Çalışma zamanını sil) baştan çalıştırma

Hepsinden sonra `cv2.__version__` hâlâ `5.0.0` ve `hasattr(cv2,
"CascadeClassifier")` hâlâ `False` dönüyor.

## İstenen
`deepface`'in `DeepFace.extract_faces`, `DeepFace.analyze`,
`DeepFace.represent` ve `DeepFace.verify` fonksiyonları Colab'da çalışsın.

### Muhtemel çözüm yolları (denenmesi istenen sırayla)
1. **`cv2` dizinini elle temizlemek.** pip'in bıraktığı artık dosyalar
   şüpheli. Kurulumdan önce:
   ```
   !pip uninstall -y opencv-python opencv-contrib-python opencv-python-headless opencv-contrib-python-headless
   !rm -rf /usr/local/lib/python3.12/dist-packages/cv2*
   !pip install "opencv-python-headless==4.12.0.88"
   ```
   ardından runtime'ı yeniden başlatıp `import cv2; print(cv2.__version__,
   hasattr(cv2, "CascadeClassifier"))` ile doğrulamak.
   > Not: `pip install` sonrası `pip list` ile 4.x göründüğü hâlde `import cv2`
   > 5.0 diyorsa, `cv2.__file__` ve `sys.path` sırasına bakılmalı — Colab'ın
   > `/usr/lib/python3/dist-packages` veya benzeri bir dizinde ikinci bir kopya
   > olabilir.
2. **OpenCV cascade'ine hiç ihtiyaç duymayan bir detektör kullanmak.**
   `detector_backend="retinaface"` / `"mtcnn"` / `"mediapipe"` — bunlar Haar
   cascade kullanmıyor. Ancak DeepFace görüntü okuma için yine de `cv2`'ye
   ihtiyaç duyuyor; `cv2` tamamen bozuksa bu da yetmeyebilir, kontrol edilmeli.
3. **DeepFace'i sabit bir sürüme çekmek** (ör. `deepface==0.0.93`) ve
   bağımlılıklarını `--no-deps` ile elle kurmak, böylece OpenCV 5 hiç gelmesin.
4. **DeepFace'ten tamamen vazgeçmek.** Alternatifler: `insightface`,
   `facenet-pytorch` (MTCNN + InceptionResnetV1), ya da `transformers` üzerinden
   hazır yüz duygu/yaş sınıflandırma modelleri. Bu durumda defterin 2–6.
   bölümlerindeki hücrelerin yeni kütüphaneye göre yeniden yazılması gerekir.

## Kabul kriteri
Temiz bir Colab runtime'ında defter baştan sona hatasız çalışmalı ve şu ikisi
sağlanmalı:
```python
import cv2
assert hasattr(cv2, "CascadeClassifier")

from deepface import DeepFace
DeepFace.extract_faces(img_path="foto.jpg", enforce_detection=False)
DeepFace.analyze(img_path="foto.jpg", actions=["emotion", "age", "gender"],
                 enforce_detection=False)
```

## Kısıtlar
- Kurulum + doğrulama toplam **2 dakikayı geçmemeli** (canlı derste çalıştırılacak)
- Google Drive kullanılmayacak
- GPU gerektirmemeli
- Türkçe açıklamalı, hücreler sırayla çalıştırıldığında akan bir defter olmalı
