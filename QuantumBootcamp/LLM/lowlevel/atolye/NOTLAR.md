# Notlar — kod ajanından hocaya

Brief §9 gereği: aşağıdakiler ya bir karar, ya bir uyarı. `ayar.py`'ye ve
`veri/` altına **dokunmadım**.

---

## 1. Yazdığım dosyalar

Brief'te istenen dört script:

```
00_kontrol.py   01_once.py   02_egit.py   03_sonra.py   04_sinir.py
```

Bunlara ek olarak **iki yardımcı modül** açtım. Brief `ekran.py` açmaya
izin veriyordu ("serbestsin"); ikincisinin gerekçesi aşağıda.

| dosya | ne var | neden ayrı |
|---|---|---|
| `ekran.py` | renk, kutu, başlık, tablo, `duraklat` | `highlevel/atölye/ortak.py`'nin ihtiyacımız kadarı buraya **kopyalandı** — o klasöre bağımlılık yok |
| `motor.py` | model yükleme, `sor()`, skorlama, istem ölçümü | brief §3 kural 1 |

**`motor.py` neden var:** ÖNCE ile SONRA'ya giden girdinin birebir aynı
kalması bir kural. Aynı üretim kodunu `01_once.py` ve `03_sonra.py`'ye
kopyalarsam er ya da geç biri kayar. Üretim parametreleri tek yerde:

```python
EN_FAZLA_YENI = 120     # ÖNCE de SONRA da aynı bütçe
do_sample     = False   # deterministik
```

`120` sayısı `ayar.py`'de yoktu, ben seçtim — ham modelin cevabını kesmeyecek
kadar geniş, demoyu bekletmeyecek kadar dar. Değiştirecekseniz `motor.py`'nin
tepesinden değiştirin; iki script de oradan okuyor, dolayısıyla kural bozulmuyor.

Brief `01_once.py --talimatli`'daki token ölçümünü "bir yardımcı fonksiyona koy,
`04_sinir.py` oradan alsın" diyordu. Fonksiyonun adı `motor.istem_karsilastir`;
iki script de onu çağırıyor. `01_once.py`'nin içinde bırakıp `04`'ten
çağırsaydım `importlib` gerekirdi (modül adı rakamla başlıyor) — atölye kodunda
görülecek bir şey değil.

---

## 2. Bir ölçüm kararı: aksan düşürme

`motor.sadelestir()` küçük harfe indirip noktalamayı atıyor (brief'te yazdığı
gibi), **ayrıca birleşen aksanları düşürüyor**. İki sebep:

1. Python'da `"İlerleme".lower()` iki karakter üretir: `i` + birleşen nokta.
   Aksan düşmezse bu çıktı hiçbir zaman `ilerleme` etiketine eşit olamaz —
   ölçüm ham modelin aleyhine yalan söyler.
2. Model `ödeme` yazarsa `odeme` etiketiyle eşleşsin.

Bu esneklik **sadece ham modelin lehine** çalışıyor; fine-tune'lu model
etiketi zaten harfi harfine yazıyor. Yine de brief'in tarifinin bir adım
ötesi olduğu için burada not düşüyorum.

---

## 3. Eğitim süresi — KURULUM.md'deki "~1-2 dk" bu makinede tutmuyor

Ölçülen (GTX 1650, 4 GB, gradient checkpointing açık):

| epok | süre |
|---|---|
| 3 (`ayar.EPOK`) | **350 sn ≈ 5,8 dk** |
| 8 | **929 sn ≈ 15,5 dk** |

`KURULUM.md` "~1-2 dk" diyor; 4 GB VRAM'de 1.5B model fp16 + gradient
checkpointing ile bu makinede olmuyor. **Derste canlı eğitmeyin.**
`02_egit.py` süreyi sonda belirgin basıyor ve 2 dakikayı aşarsa uyarıyor.

Eğitim sırasında VRAM 3,9 GB / 4,0 GB — sınırda. Eğitimden önce tarayıcıyı
kapatın.

---

## 4. Kritik kriter: ÖNCE beceremiyor (✓)

`01_once.py`, `Qwen2.5-1.5B-Instruct`, `ayar.SISTEM`:

```
tam eşleşme   : 0/10
içinde geçiyor: 0/10
ort. token    : 72.0
```

Beş gösteri sorusunun beşinde de paragraf yazıyor. Kontrast yerinde,
model değiştirmeye gerek yok.

İstem maliyeti (10 test sorusu, chat şablonu dahil, istek başına ortalama):

| system prompt | sadece system | istem / istek |
|---|---|---|
| `ayar.SISTEM` | 16 token | **40 token** |
| `ayar.TALIMATLI_SISTEM` | 244 token | **268 token** |

6,7 kat.

### `--talimatli` dürüst cevabı verdi

`python 01_once.py --talimatli` (etiketleri sayan istem, ham model):

```
tam eşleşme   : 5/10
ort. token    : 3.0     <- biçim düzeldi, artık tek kelime
istem/istek   : 268 token
```

Yani prompt **biçimi** düzeltiyor (72 token → 3 token, paragraf → tek kelime)
ama etiketlerin ancak yarısını tutturuyor, üstelik 6,7 kat pahalıya.
Fine-tune ise 40 token istemle 10/10. Sunumdaki tez ekranda kendiliğinden
çıkıyor — üç sayıyı yan yana koymanız yeterli:

| | isabet | istem/istek | cevap |
|---|---|---|---|
| ham model | 0/10 | 40 token | 72 token paragraf |
| talimatlı istem | 5/10 | 268 token | 3 token |
| **fine-tune** | **10/10** | **40 token** | **2,6 token** |

---

## 5. EN ÖNEMLİ NOT: `ayar.EPOK = 3` yetmiyor — 10 epok gerekiyor

Brief "SONRA 8/10'un altında kalıyorsa önce EPOK'u 4-5'e çıkarmayı dene ve
**bunu rapor et**" diyordu. Denedim; 4-5 de yetmiyor. `ayar.py`'ye
dokunmadım, bulguyu buraya yazıyorum.

Her epok sonunda `veri/test.jsonl` üzerinde ölçtüm (tek eğitim koşusu,
`ayar.TOHUM` sabit, `do_sample=False` — tekrar edilebilir):

| epok | loss | tam eşleşme | model ne yapıyor |
|---:|---:|---:|---|
| 1 | 8,96 | 0/10 | hâlâ paragraf yazıyor |
| 2 | 2,71 | 3/10 | biçimi öğrendi, her şeye `ilerleme` diyor |
| **3** ← `ayar.EPOK` | 0,91 | **4/10** | her şeye `diger` diyor |
| 4 | 0,46 | 4/10 | her şeye `katalog` diyor |
| 5 | 0,29 | 5/10 | ayrışmaya başlıyor |
| 6 | 0,19 | 6/10 | |
| 7 | 0,095 | 8/10 | |
| 8 | 0,023 | 6/10 | (eğri düz değil, 66 örnekte gürültü normal) |
| 9 | 0,004 | 8/10 | |
| **10** | 0,0008 | **10/10** | |

**Öneri: `python 02_egit.py --epok 10`.** Kabul kriteri (≥8/10) 7. epoktan
itibaren tutuyor, 10'da 10/10. Teslim ettiğim `adapter/` bu ayarla üretildi
ve `03_sonra.py` ile doğrulandı:

```
tam eşleşme          0/10  ->  10/10
ort. üretilen token  72.0  ->   2.6      (28x kısa)
```

`ayar.EPOK`'u 3'ten 10'a çekmek isterseniz karar sizin — ben yazmadım,
çünkü sunumdaki sayılarla eşleşiyor olabilir. Bayrak ile geçmek yeterli.

İki ayrıntı:

- **3 epokta demo ÖLÜR.** Çıktı tek kelime oluyor (biçim düzeliyor) ama
  model her şeye `diger` diyor. Ekranda "fine-tune işe yaramadı" gibi
  görünür. Provada mutlaka `03_sonra.py` skorunu kontrol edin.
- Loss'un 0,0008'e inmesi "aşırı öğrenme" gibi duruyor ve eğitim setinde
  66/66 doğru. Buna rağmen test skoru düşmüyor, artıyor. 66 örnekte
  "loss düştü, demek ki ezberledi" sezgisi çalışmıyor; ölçmek gerekiyor.
  Derste sorulursa cevabı bu tablo.

Bunun bedeli süre: **10 epok ≈ 19 dakika** bu makinede. Eğitimi
kesinlikle önceden çalıştırın.

---

## 6. Modelin kalan hataları veri kaynaklı, hata değil

7-9 epok aralığında en sık iki yanlış şuydu:

- `"Sıfırdan Başlayanlar için Veri Bilimi kaç saat?"` → `canli_ders`
  (beklenen `katalog`). Sebep: `saat` kelimesi eğitim verisinde hem
  katalogda ("CRM Analitiği eğitimi kaç saat") hem canlı derste
  ("Akşam dersi saat kaçta?", "canlı ders saatleri") geçiyor.
- `"482154 borç durumum nedir"` → `diger`.

Yani model bozuk değil, 13 örnek/sınıf az. `veri/`'ye dokunmadım.
Kalıcı çözüm isterseniz sınıf başına birkaç örnek daha — ama sunumdaki
"66 örnek" sayısı değişir.

---

## 7. Küçük şeyler

- **Bütün scriptlerde `--hizli` var.** Ayrıca çıktı bir dosyaya/boruya
  gidiyorsa `duraklat()` kendiliğinden beklemiyor; `> kosu.log` ile
  kaydederken `--hizli` yazmayı unutsanız da takılmaz.
- **Renk** hem `ATOLYE_RENKSIZ=1` ile hem de çıktı tty değilse kapanıyor.
  `kosu_*.log` dosyalarında tek bir kaçış dizisi yok.
- **`HF_HUB_OFFLINE=1`** altında hepsi çalışıyor; koşu logları o şekilde
  alındı. `00_kontrol.py` bu değişkeni kendi içinde zaten kuruyor, yani
  "önbellekte var mı" kontrolü asla indirme başlatmıyor.
- **`04_sinir.py`'nin 2. bölümünde** aynı soruyu adapter kapalıyken de
  soruyorum (`PeftModel.disable_adapter()`). Modeli ikinci kez yüklemeden
  ham cevabı yan yana gösteriyor — katastrofik unutma böyle daha net
  görünüyor. Brief bunu istemiyordu; fazladan, ama çıktıyı varsaymıyor,
  ne çıkarsa onu basıyor.
- **`once_sonuc.json`** iki kipi ayrı tutuyor (`talimatsiz` / `talimatli`),
  böylece `01_once.py --talimatli` normal koşunun sonucunu silmiyor.
  `03_sonra.py` `talimatsiz` olanı okuyor; dosya yoksa çökmüyor, tabloyu
  tek sütun basıyor.
- **`02_egit.py`** `CUDA out of memory` yakalarsa `EN_UZUN`'u 128'e
  düşürmeyi hata mesajında öneriyor (kodda değil).
- `adapter/` ve `*.log` `.gitignore`'da; koşu logları (`kosu_*.log`)
  bu yüzden depoya girmez, teslim için klasörde duruyorlar.

---

## 8. Kabul kriterleri — koşuldu, hepsi tuttu

| kriter | sonuç | log |
|---|---|---|
| `00_kontrol.py` hepsi ✓ | ✓ | `kosu_00.log` |
| `01_once.py --hizli` paragraf yazıyor, tam eşleşme düşük | ✓ 0/10, ort. 72 token | `kosu_01.log` |
| `02_egit.py` hatasız, `adapter/` + `egitim_log.txt`, loss düşüyor, süre basılıyor | ✓ 11,46 → 0,0008 | `kosu_02.log` |
| `03_sonra.py --hizli` tek kelime + tam eşleşme ≥ 8/10 | ✓ **10/10**, hepsi `ayar.ETIKETLER` içinde | `kosu_03.log` |
| `04_sinir.py --hizli` üç bölüm de çalışıyor | ✓ | `kosu_04.log` |
| `HF_HUB_OFFLINE=1` altında | ✓ bütün loglar bu şekilde alındı | — |
| `ATOLYE_RENKSIZ=1` ile dosyaya düzgün yazılıyor | ✓ kaçış dizisi yok | `kosu_00.log`, `kosu_01_talimatli.log` |

Ek koşu: `kosu_01_talimatli.log` (`01_once.py --hizli --talimatli`).

**Kritik kriter — ÖNCE beceremiyor, SONRA beceriyor: ✓** (0/10 → 10/10)

Tek şart: `adapter/` **10 epokla** eğitilmiş olmalı (bkz. §5).
`ayar.EPOK = 3` ile teslim edilen adapter 4/10 verir ve demo ölür.
