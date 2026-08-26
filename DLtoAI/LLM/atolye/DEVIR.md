# DEVİR — LLM Atölyesi (2. saat)

Yeni oturuma devir dokümanı. Önce bu dosyayı, sonra `akis.md`'yi oku.

---

## 1. Durum

| | Durum |
|---|---|
| Sunum (1. saat) | ✅ Bitti — `DL_MasterClass_Kuantum_LLM_v30.pptx`, 104 slayt |
| Atölye planı | ✅ Bitti — `atolye-brief.md`, `akis.md` |
| Atölye verisi | ✅ Kısmen — `veri/yonetmelik.md`, `veri/ogrenciler.json` hazır |
| Atölye kodu | ❌ **Hiç yazılmadı** — asıl iş bu |

**Sunucu:** Veysel Murat Görken · **Süre:** 60 dk, VSCode canlı · **Dil:** Türkçe
**Tema:** halüsinasyonla baş etme — prompt → few-shot → RAG → fine-tune

---

## 2. Dosyalar

`C:\dev\presentations\kuantum\LLM\atölye\`

| Dosya | Ne var içinde |
|---|---|
| **`akis.md`** | ⭐ **Ana referans.** Dakika dakika akış, her adımda ekranda ne görünecek, örnek terminal çıktıları, söylenecek cümleler, 4 kritik an, yedek planlar |
| **`atolye-brief.md`** | Kavramsal çerçeve: dört tekniğin hangi katmanı çözdüğü, ne zaman fine-tune yapılmalı, terminoloji, senaryo gerekçesi |
| `DEVIR.md` | Bu dosya |
| `veri/yonetmelik.md` | RAG korpusu — Çınar Üniversitesi (uydurma) yönetmeliği, 14 madde |
| `veri/ogrenciler.json` | Sahte DB — 15 öğrenci: no, ad, bölüm, GNO, borç, devamsızlık, ders programı |

`C:\dev\presentations\kuantum\LLM\` (üst klasör)

| Dosya | Ne |
|---|---|
| `DL_MasterClass_Kuantum_LLM_v30.pptx` | Güncel sunum. 30–50: attention; 101: pre-training/SFT/RLHF; 102: veri örnekleri; 103: soru-cevap sayfası |
| `sunucu-metni.md` / `sunucu-metni-kisa.md` | Sunucu notlarının uzun ve kısa sürümü |

**Kritik veri detayları:**
- Devamsızlık sınırı **%28 teorik / %18 uygulamalı** (Madde 12) — model %30/%20 uyduracak, kontrast buradan geliyor
- Demo öğrencisi **20210451 / Elif Yaman / GNO 3.42** — onur aralığında (Madde 25), araç cevabı yönetmelikle birleşiyor
- Borç demosu: **20210118 / Mert Doğan / 2.400 TL**

---

## 3. Referans repo

**https://github.com/erturkkadir/bpe** — Lisans: **GPL-3.0**. Türetip dağıtılırsa türev de GPL-3 olmak zorunda; atıf verilmeli.

| Dosya | Kullanım |
|---|---|
| `finetune/finetune_demo.py` | ⭐ **İskeleti al.** ÖNCE/SONRA kurgusu, renkli terminal (`baslik`, `duraklat`, ANSI kodları), `--hizli` bayrağı, `cevapla()`, `dene_ayristir()`. Araçları ve veriyi değiştir |
| `finetune/tool_demo.py` | Araç çağrısı ayrıştırma + dispatch döngüsü |
| `finetune/ornekler.jsonl` | Format örneği (içerik değişecek — döviz kuru/saat yerine öğrenci işleri) |
| `transformer.py` | Sıfırdan decoder-only GPT, Türkçe yorumlu. `Head` sınıfı 20 satırda Q/K/V + √d + causal mask. **Vaktin varsa 2. saatin başında 2 dakika aç:** "bir saattir anlattığım şey, işte 12 satır" |
| `bpe_demo.py` | Saf Python BPE. 1. saatte tokenizasyon zaten anlatıldı — repoda dursun, isteyen çalıştırır |

**Düzeltilecek hata:** `finetune_demo.py` içinde `VERI = pathlib.Path("veri/ornekler.jsonl")` yazıyor ama dosya `finetune/ornekler.jsonl`'de. İlk çalıştırmada `sys.exit(1)` yer.

---

## 4. Alınmış kararlar (tartışma bitti, uygula)

| Konu | Karar |
|---|---|
| Format | **Canlı demo `.py`** (kernel state yok, spoiler yok, Enter'la akıyor). **Katılımcıya `.ipynb`** — sadece fine-tune için, Colab GPU'su lazım |
| Model | `Qwen/Qwen2.5-0.5B-Instruct` — tek satırlık sabit. Provada `Qwen3-0.6B` / `Gemma-3-270m-it` de denenmeli. Kriter: **fine-tune öncesi görünür şekilde çuvallayan, sonrası düzelen** |
| Eğitim döngüsü | **Manuel döngü** (repodaki gibi). TRL `SFTTrainer` API'si sürümler arası değişiyor, atölye sabahı sürpriz istemiyoruz. SFTTrainer eşdeğerini kapanışta tek slaytta göster |
| RAG | **LangChain/LlamaIndex YOK.** `sentence-transformers` + numpy kosinüs, ~20 satır. Türkçe için çok dilli embedding şart (`intfloat/multilingual-e5-small`) |
| Canlı eğitim | **Yapılmayacak.** Provada `egitim_log.txt` üretilecek, atölyede o gösterilecek |
| Kod anlatımı | Satır satır **yok**. Anlatılan şey kod değil, çıktı |

---

## 5. Yapılacaklar

- [ ] **`ortak.py`** — model yükleme (tek `MODEL` sabiti), `sor(sistem, kullanici)`, renkli terminal yardımcıları, `duraklat()`, `--hizli` bayrağı, `--isit` (ders öncesi ısıtma)
- [ ] **`01_prompt.py`** — ① çıplak soru → uydurma ② aynı soruyu 3 kez sor, 3 farklı cevap bas ③ iyi prompt ("bilmiyorsan bilmiyorum de") → geri çekiliyor
- [ ] **`02_fewshot.py`** — 3 örnekle biçim düzeliyor, rakam yanlış kalıyor. Few-shot cevabını yönetmelikteki gerçek madde ile **yan yana** bas. Token maliyetini yazdır
- [ ] **`03_rag.py`** — 5 adım, her biri Enter ile: parçala → göm → kosinüs ara (benzerlik skorlarını bas) → prompt'a enjekte et (prompt'u kutuda göster) → cevapla + kaynak göster. **Son bölüm: "Ortalamam kaç? No: 20210451" ile RAG'in çuvallamasını göster**
- [ ] **Üç araç fonksiyonu** — `not_ortalamasi(no)`, `ders_programi(no)`, `borc_sorgula(no)`; `ogrenciler.json`'dan okuyacak
- [ ] **`veri/ornekler.jsonl`** — 50 satır. **~%70 araç gerektiren, ~%30 gerektirmeyen** ("Bu soru için araç gerekmiyor."). Numara formatları çeşitli olsun; bazen numara verilmiş, bazen sorulmalı
- [ ] **`04_finetune.py`** — `--once` / `--egit` / `--sonra` bayrakları. ÖNCE bozuk JSON → veri → LoRA config + eğitilebilir parametre oranı ve adapter boyutu → eğitim → SONRA + 5 adımlı araç akışı (sonucu modele geri ver)
- [ ] **`05_test.py`** — unutma testi ("Merhaba, nasılsın?") + 5 soruluk karışık test tablosu + karar tablosu
- [ ] **`04_finetune.ipynb`** — Colab sürümü, katılımcıya verilecek olan
- [ ] **`KURULUM.md`** + `requirements.txt` — provada çalışan sürümler sabitlensin
- [ ] **Prova** — gerçek süreleri ölç, `egitim_log.txt` üret, her demonun çıktısını yedek olarak kaydet

---

## 6. Uyarılar

- **Bu ortamdan Hugging Face'e erişilemiyor, torch kurulu değil.** Kod yazılabilir ve söz dizimi denetlenebilir; RAG matematiği sahte vektörlerle test edilebilir. **Ama model çıktıları test edilemez — Veysel çalıştıracak.** Prova pazarlık konusu değil.
- Dosyalar `C:\dev\presentations\kuantum\LLM\atölye\` altına yazılacak (device bridge ile).
- Üniversitenin uydurma olduğu ekranda bir kez söylenmeli — hem demo şartı hem de katılımcı yanlış bilgiyle çıkmasın diye.
- Fine-tune halüsinasyonu **çözmez**, kötüleştirebilir. Dört teknik bir merdiven değil: prompt/few-shot **biçim**, RAG **olgu**, fine-tune **davranış**. Bu çerçeve `atolye-brief.md` §2'de.
