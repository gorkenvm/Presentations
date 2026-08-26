#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Deep Learning Master Class — Kuantum Bootcamp
Miuul şablonundan türetilmiş sunum. Bölüm 1: Açılış slaytları."""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR

SRC = "template.pptx"
OUT = "DL_MasterClass_Kuantum_v06.pptx"

# --- palet -------------------------------------------------------------
INK     = RGBColor(0x1A, 0x1A, 0x1A)
NAVY    = RGBColor(0x15, 0x26, 0x3F)
GOLD    = RGBColor(0xC0, 0x8A, 0x2E)
GRAY    = RGBColor(0x6E, 0x6E, 0x6E)
LIGHT   = RGBColor(0xF2, 0xF4, 0xF7)
RULE    = RGBColor(0xD5, 0xD5, 0xD5)
WHITE   = RGBColor(0xFF, 0xFF, 0xFF)
BLACK   = RGBColor(0x00, 0x00, 0x00)
SILVER  = RGBColor(0xC9, 0xC9, 0xC9)
DIM     = RGBColor(0x8A, 0x8A, 0x8A)

NV   = RGBColor(0x76, 0xB9, 0x00)   # NVIDIA yeşili
SOC  = RGBColor(0x18, 0x77, 0xF2)   # sosyal medya mavisi
WIKI = RGBColor(0x3A, 0x3A, 0x3A)
WEB  = RGBColor(0x2B, 0x57, 0x9A)

SW, SH = 26.67, 15.0          # slayt ölçüleri (inch)

prs = Presentation(SRC)
LAY_COVER   = prs.slide_masters[0].slide_layouts[0]   # "Açılış Ekranı"
LAY_CONTENT = prs.slide_masters[0].slide_layouts[4]   # "1_Ders Anlatımı"

# --- mevcut slaytları sil ---------------------------------------------
sldIdLst = prs.slides._sldIdLst
for sld in list(sldIdLst):
    prs.part.drop_rel(sld.rId)
    sldIdLst.remove(sld)


# --- yardımcılar -------------------------------------------------------
def txt(slide, x, y, w, h, runs, size=20, color=INK, bold=False,
        align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, line=None, space_after=0):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Emu(0)
    tf.margin_top = tf.margin_bottom = Emu(0)
    tf.vertical_anchor = anchor

    if isinstance(runs, str):
        runs = [runs]
    paras = [[(it, bold)] if isinstance(it, str) else it for it in runs]

    for i, para in enumerate(paras):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        if line:
            p.line_spacing = line
        if space_after:
            p.space_after = Pt(space_after)
        for t, b in para:
            r = p.add_run()
            r.text = t
            r.font.size = Pt(size)
            r.font.bold = b
            r.font.color.rgb = color
    return box


def rect(slide, x, y, w, h, fill=None, line=None, lw=1.0,
         shape=MSO_SHAPE.RECTANGLE, radius=None):
    s = slide.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    if fill is None:
        s.fill.background()
    else:
        s.fill.solid()
        s.fill.fore_color.rgb = fill
    if line is None:
        s.line.fill.background()
    else:
        s.line.color.rgb = line
        s.line.width = Pt(lw)
    if radius is not None and shape == MSO_SHAPE.ROUNDED_RECTANGLE:
        s.adjustments[0] = radius
    s.shadow.inherit = False
    s.text_frame.word_wrap = True
    return s


def line_(slide, x1, y1, x2, y2, color=RULE, lw=1.5):
    c = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT,
                                   Inches(x1), Inches(y1), Inches(x2), Inches(y2))
    c.line.color.rgb = color
    c.line.width = Pt(lw)
    return c


def content_slide(header, message_runs, msg_size=40):
    """Şablonun ders slaydı: sol üstte başlık, ortada tek büyük fikir cümlesi."""
    s = prs.slides.add_slide(LAY_CONTENT)
    tf = list(s.placeholders)[0].text_frame
    tf.paragraphs[0].text = ""
    r = tf.paragraphs[0].add_run()
    r.text = header
    r.font.size = Pt(32)
    r.font.color.rgb = INK
    txt(s, 2.26, 2.05, 22.14, 2.10, [message_runs], size=msg_size,
        align=PP_ALIGN.CENTER, line=1.15)
    return s


def chip_row(slide, cx, y, chips, size=15):
    """Ortalanmış küçük etiketler: [(metin, dolgu, yazı_rengi), ...]"""
    k = size / 15.0
    widths = [(0.12 * len(t) + 0.50) * k for t, _, _ in chips]
    gap = 0.14 * k
    total = sum(widths) + gap * (len(chips) - 1)
    x = cx - total / 2
    for (t, fill, fg), w in zip(chips, widths):
        c = rect(slide, x, y, w, 0.42 * k, fill=fill,
                 shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.42)
        tf = c.text_frame
        tf.margin_left = tf.margin_right = Emu(0)
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        r = p.add_run()
        r.text = t
        r.font.size = Pt(size)
        r.font.bold = True
        r.font.color.rgb = fg
        x += w + gap


def timeline_row(slide, items, axis_y, x0, x1, boxw,
                 year_size=26, title_size=21, desc_size=16, desc_h=1.40):
    """Tek satır zaman çizelgesi; etiketler eksenin altında.
    items: (yıl, başlık, açıklama, vurgu_mu, chips)"""
    line_(slide, 1.40, axis_y, 25.27, axis_y, color=RULE, lw=2.5)
    step = (x1 - x0) / (len(items) - 1)
    for i, item in enumerate(items):
        year, title, desc, hero = item[:4]
        chips = item[4] if len(item) > 4 else None
        cx = x0 + i * step
        accent = GOLD if hero else NAVY
        d = 0.46 if hero else 0.30
        rect(slide, cx - d / 2, axis_y - d / 2, d, d, fill=accent, shape=MSO_SHAPE.OVAL)
        line_(slide, cx, axis_y + d / 2, cx, axis_y + 0.42, color=RULE, lw=2.0)
        bx, y0 = cx - boxw / 2, axis_y + 0.48
        txt(slide, bx, y0, boxw, 0.58, year, size=year_size, color=accent,
            bold=True, align=PP_ALIGN.CENTER)
        txt(slide, bx, y0 + 0.66, boxw, 0.62, title, size=title_size, color=INK,
            bold=True, align=PP_ALIGN.CENTER)
        if chips:
            chip_row(slide, cx, y0 + 1.40, chips)
        txt(slide, bx, y0 + 1.95, boxw, desc_h, desc, size=desc_size,
            color=GRAY, align=PP_ALIGN.CENTER, line=1.25)


def logo(slide):
    rect(slide, 0.10, 13.92, 2.43, 0.90, fill=WHITE)
    slide.shapes.add_picture("logo_miuul.png", Inches(0.23), Inches(13.70),
                             Inches(2.17), Inches(1.33))


# --- hikâye slaytları için ortak parçalar -------------------------------
STRIP = ["1950", "1956", "1986", "1991", "2000'ler", "2007",
         "2009", "2012", "2015", "2017", "2022", "2024"]


def strip_bar(slide, active=None, y=2.35):
    """Sayfanın üstünde küçük zaman çizelgesi şeridi; aktif dönem altın."""
    line_(slide, 1.40, y, 25.27, y, color=RULE, lw=2.0)
    x0, x1 = 2.20, 24.47
    step = (x1 - x0) / (len(STRIP) - 1)
    for i, lab in enumerate(STRIP):
        cx = x0 + i * step
        on = (active is not None and i in (active if isinstance(active, (list, tuple)) else [active]))
        d = 0.34 if on else 0.20
        rect(slide, cx - d / 2, y - d / 2, d, d,
             fill=GOLD if on else RGBColor(0xB8, 0xBE, 0xC8), shape=MSO_SHAPE.OVAL)
        txt(slide, cx - 1.10, y + 0.30, 2.20, 0.45, lab, size=15,
            color=GOLD if on else RGBColor(0x9A, 0x9A, 0x9A), bold=on,
            align=PP_ALIGN.CENTER)


def story_slide(header, message_runs, active=None, msg_size=38):
    """Üstte şerit zaman çizelgesi, altında tek büyük fikir cümlesi."""
    s = prs.slides.add_slide(LAY_CONTENT)
    tf = list(s.placeholders)[0].text_frame
    tf.paragraphs[0].text = ""
    r = tf.paragraphs[0].add_run()
    r.text = header
    r.font.size = Pt(32)
    r.font.color.rgb = INK
    strip_bar(s, active)
    txt(s, 2.26, 3.35, 22.14, 1.90, [message_runs], size=msg_size,
        align=PP_ALIGN.CENTER, line=1.15)
    return s


def picture(slide, path, x, y, h, caption=None, cap_w=None):
    """Yüksekliğe göre ölçeklenen, ince çerçeveli görsel."""
    from PIL import Image
    iw, ih = Image.open(path).size
    w = h * iw / ih
    pic = slide.shapes.add_picture(path, Inches(x), Inches(y), Inches(w), Inches(h))
    pic.line.color.rgb = RGBColor(0xDD, 0xDD, 0xDD)
    pic.line.width = Pt(1.0)
    if caption:
        txt(slide, x, y + h + 0.18, cap_w or w, 0.55, caption, size=17,
            color=GRAY, align=PP_ALIGN.CENTER)
    return w


def band(slide, y, runs, h=1.30, size=24, fill=LIGHT):
    rect(slide, 1.40, y, 23.87, h, fill=fill)
    txt(slide, 2.20, y, 22.27, h, [runs], size=size, color=NAVY,
        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, line=1.2)


def card(slide, x, y, w, h, title, items, accent=NAVY, size=21):
    rect(slide, x, y, w, h, fill=LIGHT, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.05)
    txt(slide, x + 0.70, y + 0.60, w - 1.40, 0.80, title, size=27, color=accent, bold=True)
    paras = [[("•  ", False), (t, False)] for t in items]
    txt(slide, x + 0.70, y + 1.75, w - 1.40, h - 2.40, paras, size=size,
        color=INK, line=1.3, space_after=12)


# =======================================================================
# SLAYT 1 — İÇERİK
# =======================================================================
s1 = prs.slides.add_slide(LAY_COVER)
rect(s1, 0, 0, SW, SH, fill=BLACK)

txt(s1, 3.00, 1.55, 20.67, 1.9, "Deep Learning", size=92, color=WHITE,
    bold=True, align=PP_ALIGN.LEFT, line=0.95)

agenda = [
    ("01", "Derin Öğrenmenin Hikâyesi", "15 dk", False),
    ("02", "Neden Deep Learning?", "15 dk", False),
    ("03", "Nasıl Öğreniyor? Nöron, Loss, Gradient Descent", "25 dk", False),
    ("",   "Ara", "10 dk", True),
    ("04", "Hangi Mimariler Var? ANN, CNN, RNN / LSTM, Transformer", "25 dk", False),
    ("05", "Colab Uygulaması", "25 dk", False),
    ("06", "Özet & Ödev", "5 dk", False),
]

AY, AST = 4.55, 1.14
for i, (num, title, dur, muted) in enumerate(agenda):
    y = AY + i * AST
    col_num = DIM if muted else GOLD
    col_ttl = DIM if muted else WHITE
    if num:
        txt(s1, 3.00, y + 0.05, 1.30, 0.6, num, size=26, color=col_num, bold=True)
    txt(s1, 4.50, y, 15.60, 0.75, title, size=34, color=col_ttl, bold=not muted)
    txt(s1, 20.20, y + 0.06, 3.50, 0.6, dur, size=26, color=DIM, bold=True,
        align=PP_ALIGN.RIGHT)

line_(s1, 3.00, 13.10, 23.70, 13.10, color=RGBColor(0x3A, 0x3A, 0x3A), lw=1.5)
txt(s1, 3.00, 13.40, 20.67, 0.8, "Veysel Murat Görken", size=36, color=WHITE, bold=True)
txt(s1, 3.00, 14.15, 20.67, 0.6, "Data Scientist / AI Engineer",
    size=26, color=GOLD)

logo(s1)


# =======================================================================
# SLAYT 2 — DERİN ÖĞRENMENİN HİKÂYESİ
# =======================================================================
s2 = content_slide(
    "Derin Öğrenmenin Hikâyesi",
    [("Fikir 1986'da hazırdı. Patlama için ", False),
     ("veri, hesaplama gücü ve pes etmeyen birkaç kişinin", True),
     (" aynı anda olgunlaşması gerekti.", False)])

row1 = [
    ("1950", "Turing'in sorusu",
     "Turing zekâyı tanımlamak yerine ölçmeyi önerdi: taklit oyunu.",
     False, [("Turing Testi", NAVY, WHITE)]),
    ("1956–1959", "İki terim doğuyor",
     "Dartmouth'ta \"artificial intelligence\", 1959'da Arthur Samuel'in dama programıyla \"machine learning\".",
     False, [("Perceptron 1957", WIKI, WHITE)]),
    ("1986", "Backpropagation",
     "Rumelhart, Hinton & Williams. Ağı eğitmenin yolu bulundu, ama alan yine gözden düştü.",
     False, None),
    ("1991–1999", "Herkes web'e koşuyor",
     "WWW halka açıldı, dot-com çılgınlığı başladı. Zekâ da para da web'e aktı.",
     False, [("WWW", WEB, WHITE)]),
    ("2000'ler", "Ilya, Hinton'ın kapısında",
     "Toronto'da bir öğrenci, yaz tatilinde bedava çalışmak için \"ölü\" denen alanı seçti.",
     False, None),
    ("2007", "Hesaplama gücü geldi",
     "CUDA ile oyun ekran kartı bilim aletine dönüştü; eğitim haftalardan günlere indi.",
     False, [("NVIDIA CUDA", NV, WHITE)]),
]

row2 = [
    ("2009", "Veri geldi",
     "Web 2.0 kullanıcıyı üretici yaptı. ImageNet: milyonlarca etiketli görsel, tek yerde.",
     False, [("Sosyal medya", SOC, WHITE), ("Wikipedia", WIKI, WHITE)]),
    ("17 Ekim 2012", "AlexNet — kırılma anı",
     "Krizhevsky, Sutskever & Hinton. Top-5 hatası %26'dan %15'e düştü; herkes önce hile sandı.",
     True, [("2 × GPU", NV, WHITE)]),
    ("2013–2015", "Önce Google, sonra OpenAI",
     "Google Ilya'yı aldı. 2015'te Musk, Altman, Brockman ve Ilya OpenAI'ı kurdu.",
     False, None),
    ("2017", "Transformer",
     "\"Attention Is All You Need\". Ölçeklenebilir mimari, tüm alanların ortak dili oldu.",
     False, None),
    ("2022", "ChatGPT",
     "Ilya'nın tezi: ölçekle, gerisine karışma. Model büyüdükçe beklenmedik yetenekler belirdi.",
     False, None),
    ("2024", "Nobel Ödülleri",
     "Hinton'a Fizik (Hopfield ile), Hassabis & Jumper'a Kimya (AlphaFold).",
     False, None),
]

timeline_row(s2, row1, axis_y=4.45, x0=3.35, x1=23.35, boxw=3.90)
timeline_row(s2, row2, axis_y=9.05, x0=3.35, x1=23.35, boxw=3.90)

rect(s2, 1.40, 13.20, 23.87, 1.10, fill=LIGHT)
txt(s2, 2.10, 13.50, 22.47, 0.7,
    [[("Veri sosyal medyadan, hesaplama gücü oyun kartlarından geldi. ", False),
      ("Herkes web'e koşarken Ilya, kimsenin bakmadığı yere gitti.", True)]],
    size=22, color=NAVY, align=PP_ALIGN.CENTER)


# =======================================================================
# SLAYT 3 — HER HİKÂYENİN BİR İKİNCİ ADAMI VAR
# =======================================================================
s3 = story_slide(
    "Derin Öğrenmenin Hikâyesi",
    [("Jobs'ın yanında Wozniak, Frodo'nun yanında Sam vardı. ", False),
     ("Sam Altman'ın yanındaki isim: Ilya Sutskever.", True)])

trio = [("img/stevejobs.png", "Steve Jobs & Steve Wozniak"),
        ("img/frodo.png", "Frodo & Sam"),
        ("img/altmanvesustkever.png", "Sam Altman & Ilya Sutskever")]
COLW, GAPW, IMGH = 7.30, 0.55, 4.55
tot = 3 * COLW + 2 * GAPW
cx0 = (SW - tot) / 2
for i, (path, cap) in enumerate(trio):
    colx = cx0 + i * (COLW + GAPW)
    from PIL import Image as _I
    iw, ih = _I.open(path).size
    w = IMGH * iw / ih
    picture(s3, path, colx + (COLW - w) / 2, 5.55, IMGH)
    txt(s3, colx, 5.55 + IMGH + 0.22, COLW, 0.55, cap, size=18, color=GRAY,
        align=PP_ALIGN.CENTER)

band(s3, 11.55,
     [("OpenAI'ın arkasındaki asıl beyin. Kurduğu yapıya sonradan cephe alması yüzünden ona ", False),
      ("\"yapay zekâ çağının Oppenheimer'ı\"", True),
      (" deniyor — en büyük hataları en büyük zihinler yapar.", False)], h=1.55)


# =======================================================================
# SLAYT 4 — ILYA KİMDİR?
# =======================================================================
s4 = story_slide(
    "Ilya Sutskever kimdir?",
    [("1985'te Sovyetler'de doğdu, Kudüs'te büyüdü, lisede Kanada'ya taşındı — ", False),
     ("bir ay sonra Toronto Üniversitesi'ne alındı.", True)], active=4)

picture(s4, "img/ilyadogum.png", 1.60, 5.60, 6.15,
        caption="Kudüs, 1990 — Sovyetler dağıldıktan sonra ailesiyle İsrail'e taşınmıştı.")

card(s4, 15.05, 5.60, 10.00, 6.15,
     "Okul yıllarını bu soruların peşinde geçirdi",
     ["Zekâ nedir?",
      "Zekâ nasıl çalışır?",
      "Beyin örüntüleri nasıl okur?",
      "Hafıza dediğimiz şey nasıl çalışır?",
      "Nöronlar nasıl iletişim kurar?"], size=23)

band(s4, 12.60,
     [("Herkes 90'ların internet çılgınlığıyla meşgulken ", False),
      ("onun aklında düşünen makineler vardı.", True)], h=1.40)


# =======================================================================
# SLAYT 5 — HERKESİN "ÖLÜ" DEDİĞİ ALAN
# =======================================================================
s5 = story_slide(
    "Çöpten geleceğe: sinir ağları",
    [("Ilya, Hinton'ın kapısını çaldı: ", False),
     ("yaz tatilinde, ücretsiz çalışmak için.", True),
     (" Herkesin \"ölü\" dediği alanı seçmişti.", False)], active=4)

CW2, GP2 = 11.20, 0.90
x_a = (SW - (2 * CW2 + GP2)) / 2
card(s5, x_a, 5.60, CW2, 5.70, "Klasik yöntem: kuralı sen yaz",
     ["\"Bıyığı vardır, kulakları vardır, tüylüdür.\"",
      "Ya kedi arkasını dönmüşse?",
      "Ya fotoğrafta yarısı görünmüyorsa?",
      "Ya ışık iyi değilse?",
      "Tek bir kedi için on binlerce kural."], accent=RGBColor(0x8A, 0x3B, 0x2F), size=22)
card(s5, x_a + CW2 + GP2, 5.60, CW2, 5.70, "Hinton'ın fikri: örüntüyü o bulsun",
     ["Milyonlarca kedi fotoğrafı göster.",
      "Hiç kural koyma.",
      "Ağırlıkları veriden kendisi ayarlasın.",
      "Gereken tek şey: çok veri ve çok hesap.",
      "O dönem ikisi de yoktu."], accent=NAVY, size=22)

band(s5, 12.60,
     [("Amaç bilgisayara balık vermek değildi — ", False),
      ("balık tutmayı öğretmekti.", True)], h=1.40)


# =======================================================================
# SLAYT 6 — VERİ GELDİ
# =======================================================================
s6 = story_slide(
    "Eksik parça: veri",
    [("Web 2.0 kullanıcıyı üretici yaptı; ", False),
     ("ImageNet bu yığını etiketleyip tek çatı altında topladı.", True)], active=6)

IH2 = 5.60
w1 = 0
from PIL import Image as _I
sizes = [_I.open(p).size for p in ("img/imagenet.png", "img/imagenet_data.png")]
ws = [IH2 * a / b for a, b in sizes]
tot2 = sum(ws) + 0.80
sx = (SW - tot2) / 2
picture(s6, "img/imagenet.png", sx, 5.55, IH2,
        caption="ImageNet (2009) — Fei-Fei Li ve ekibi, Princeton")
picture(s6, "img/imagenet_data.png", sx + ws[0] + 0.80, 5.55, IH2,
        caption="Milyonlarca etiketli görsel, hiyerarşik sınıflarla")

band(s6, 12.55,
     [("Sosyal medya, forumlar, Wikipedia... ", False),
      ("Rüya gibiydi ve formül hazırdı: veri + hesaplama gücü + sinir ağı.", True)], h=1.40)


# =======================================================================
# SLAYT 7 — ALEXNET DEVRİMİ
# =======================================================================
s7 = story_slide(
    "AlexNet devrimi",
    [("2012 ImageNet yarışmasında AlexNet, top-5 hatasını ", False),
     ("%26'dan %15'e", True),
     (" düşürdü. Herkes önce hile olduğunu sandı.", False)], active=7)

picture(s7, "img/ilyahintonalex.png", 1.70, 5.55, 5.60,
        caption="Alex Krizhevsky, Geoffrey Hinton ve Ilya Sutskever — Toronto")

# ILSVRC top-5 hata oranı (%) — elle çizilen sütun grafiği
CH_X, CH_W = 12.20, 12.90
BASE, MAXH, SCALE = 11.30, 5.10, 0.175
bars = [("2010", 28.2, False), ("2011", 25.8, False), ("2012", 15.3, True),
        ("2013", 11.7, False), ("2014", 6.7, False), ("2015", 3.6, False)]
BW, BG = 1.45, 0.60
tot3 = len(bars) * BW + (len(bars) - 1) * BG
bx0 = CH_X + (CH_W - tot3) / 2
txt(s7, CH_X, 5.20, CH_W, 0.6, "ImageNet (ILSVRC) top-5 hata oranı, %",
    size=22, color=INK, bold=True, align=PP_ALIGN.CENTER)
line_(s7, bx0 - 0.40, BASE, bx0 + tot3 + 0.40, BASE, color=RULE, lw=2.0)
for i, (yr, val, hot) in enumerate(bars):
    bx = bx0 + i * (BW + BG)
    bh = val * SCALE
    rect(s7, bx, BASE - bh, BW, bh,
         fill=GOLD if hot else RGBColor(0xC7, 0xCD, 0xD6))
    txt(s7, bx - 0.35, BASE - bh - 0.62, BW + 0.70, 0.55, f"%{val}".replace(".", ","),
        size=20, color=GOLD if hot else GRAY, bold=hot, align=PP_ALIGN.CENTER)
    txt(s7, bx - 0.35, BASE + 0.18, BW + 0.70, 0.5, yr, size=20,
        color=GOLD if hot else GRAY, bold=hot, align=PP_ALIGN.CENTER)
txt(s7, bx0 + 2 * (BW + BG) - 1.10, BASE + 0.80, BW + 2.20, 0.5, "AlexNet",
    size=21, color=GOLD, bold=True, align=PP_ALIGN.CENTER)

band(s7, 12.60,
     [("O güne kadar hata payı yılda birkaç puan düşüyordu. ", False),
      ("O gün, bir anlamda ChatGPT'nin de doğum günüydü.", True)], h=1.40)


# =======================================================================
# SLAYT 8 — GÜÇ SAVAŞLARI VE OPENAI
# =======================================================================
s8 = story_slide(
    "Güç savaşları, OpenAI ve Transformer",
    [("Soru artık \"işe yarıyor mu\" değildi: ", False),
     ("bu teknoloji gerçekse, onu kim kontrol edecek?", True)], active=[8, 9, 10])

C3W, C3G = 7.55, 0.55
c3x = (SW - (3 * C3W + 2 * C3G)) / 2
C3Y, C3H = 5.55, 5.85

card(s8, c3x, C3Y, C3W, C3H, "Önce Google",
     ["Devler trene atladı; en kolay yol satın almaktı.",
      "Google, Hinton ve ekibinin şirketini aldı.",
      "Ilya'nın her şeyi vardı: veri, işlem gücü, kaynak.",
      "Ama özgürlük yoktu."], size=20)

card(s8, c3x + C3W + C3G, C3Y, C3W, C3H, "Sonra o akşam yemeği",
     ["Masada Altman, Brockman, Musk ve Ilya (2015).",
      "Musk finansman, Altman yönetim, Brockman mühendislik.",
      "Ilya bilimsel vizyonu üstlendi.",
      "Konuşulan asıl konu ChatGPT değil, AGI'ydı."],
     accent=GOLD, size=20)

# üçüncü sütun: Transformer makalesi
c3 = c3x + 2 * (C3W + C3G)
rect(s8, c3, C3Y, C3W, C3H, fill=LIGHT, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.05)
txt(s8, c3 + 0.70, C3Y + 0.60, C3W - 1.40, 0.80, "Ve sonra Transformer",
    size=27, color=NAVY, bold=True)
rect(s8, c3 + 0.70, C3Y + 1.70, C3W - 1.40, 2.15, fill=WHITE,
     line=RGBColor(0xC8, 0xC8, 0xC8), lw=1.2)
_t = txt(s8, c3 + 0.95, C3Y + 2.05, C3W - 1.90, 1.10, "Attention Is All You Need",
         size=30, color=INK, bold=True, align=PP_ALIGN.CENTER, line=1.05)
for _p in _t.text_frame.paragraphs:
    for _r in _p.runs:
        _r.font.name = "Cambria"
txt(s8, c3 + 0.95, C3Y + 3.15, C3W - 1.90, 0.5,
    "Vaswani ve ekibi, Google · NeurIPS 2017", size=17, color=GRAY,
    align=PP_ALIGN.CENTER)
txt(s8, c3 + 0.70, C3Y + 4.20, C3W - 1.40, 1.40,
    [[("•  ", False), ("Tekrarlı yapı yok, paralel eğitim.", False)],
     [("•  ", False), ("Ölçekleme fikri karşılığını burada buldu.", False)]],
    size=20, color=INK, line=1.3, space_after=12)

band(s8, 12.55,
     [("Ilya'nın tezi: ", False),
      ("\"Ölçeklendir ve gerisine karışma.\"", True),
      ("  Model yeterince büyürse, beklemediğimiz yetenekler kendiliğinden çıkar.", False)],
     h=1.40)


# --- konuşmacı notları -------------------------------------------------
s3.notes_slide.notes_text_frame.text = (
    "Açılış: \"Güç yozlaştırır, mutlak güç mutlaka yozlaştırır.\" Jobs'ın yolu Wozniak'tan, "
    "Frodo'nunki Sam'den ayrı düşünülemez. Altman'ın hikâyesindeki o karakter Ilya Sutskever.\n\n"
    "Ilya, birlikte kurdukları şirkette Altman'ı etik vizyondan yoksun olmakla suçlayıp koltuğundan "
    "etti; Altman daha güçlü döndü, Ilya tasını tarağını topladı. Buna rağmen Musk dahil kimse Ilya "
    "hakkında kötü konuşmaz. Oppenheimer benzetmesini burada kur."
)
s4.notes_slide.notes_text_frame.text = (
    "Rus, Kanadalı, Amerikalı ve İsrailli — adeta BM'nin vücut bulmuş hali. 1985'te Sovyetler'de "
    "Yahudi bir ailede doğdu; Sovyetler dağılınca aile İsrail'e taşındı, çocukluğu Kudüs'te geçti.\n\n"
    "Kanada'ya taşındıklarında liseye başladı ama öğretmenleri bir ay içinde potansiyeli gördü ve "
    "Toronto Üniversitesi'ne bilgisayar bilimleri okumaya alındı. Orada Geoffrey Hinton ile tanıştı — "
    "'yapay zekânın babası', sonradan Turing ve Nobel Fizik ödüllerini alacak isim."
)
s5.notes_slide.notes_text_frame.text = (
    "O yıllarda sinir ağları çöpe atılmak üzereydi; birçok kişi bu alanın bir sonu olmadığını "
    "düşünüyordu. Ilya tam tersini gördü ve yaz tatilinde Hinton'ın laboratuvarında ücretsiz "
    "çalışmak istedi.\n\n"
    "Kedi örneğini burada interaktif yap: katılımcılara sor, \"bilgisayara kediyi nasıl tarif "
    "edersiniz?\" Gelen her kurala bir istisna söyle. Sonra Hinton'ın cevabını ver: kural yazma, "
    "milyonlarca örnek göster."
)
s6.notes_slide.notes_text_frame.text = (
    "Veri nereden geldi? Web 2.0 — kullanıcı odaklı paylaşım. Sosyal medya, forumlar, Wikipedia. "
    "ImageNet ise bunu yarışmaya çevirdi: dünyanın dört bir yanından ekipler aynı veri kümesinde "
    "yarışıyordu. Fei-Fei Li ve ekibinin işi."
)
s7.notes_slide.notes_text_frame.text = (
    "Ilya, Hinton'a 2012 yarışmasına hazırlanmaları gerektiğini söyledi. Alex Krizhevsky algoritmayı "
    "yazdı. İtalya'daki oturumda sonuçlar açıklandığında herkes şok oldu: yıllardır %26 civarında "
    "duran hata bir anda %15'e indi.\n\n"
    "Grafikte 2012'den sonrasını da göster: bir kez kırıldıktan sonra düşüş durmadı (2015'te %3,6 — "
    "insan performansının altı). Herkes önce hile sandı; analizler devrimi doğruladı. Kısıtlı "
    "imkanlarla iki ekran kartı, milyon dolarlık geleneksel sistemleri geçti.\n\n"
    "Fotoğraftaki takvimde 17'nin işaretli olduğuna dikkat çekebilirsin."
)
s8.notes_slide.notes_text_frame.text = (
    "Google her şeyi verdi ama özgürlüğü veremedi. Bir gün Altman'dan bir e-posta geldi: "
    "\"Yapay zeka konusunda önemli bir fırsat var, akşam buluşalım.\"\n\n"
    "Hayal: Google ve DeepMind'a rakip olabilecek, kâr amacı gütmeyen açık bir laboratuvar. "
    "Ejderhalara kılıçla gitmek gibiydi. Transformer + trilyonlarca kelime + 'bir sonraki kelimeyi "
    "tahmin et' → dil, mantık, kod yazma kendiliğinden geldi. Sonrası ChatGPT.\n\n"
    "Kapanış: asıl hedef ChatGPT değil AGI'ydı; Ilya bunun kontrolsüz gelişmesinin tehdidinin de "
    "farkındaydı.\n\n"
    "Transformer'a sadece değin: 2017'de Google'dan çıkan bu makale, ölçekleme fikrinin karşılığını "
    "bulduğu mimari. Ayrıntısı 04'te. Buradan 02'ye (Neden Deep Learning?) geç."
)

s1.notes_slide.notes_text_frame.text = (
    "KENDİMİ TANITIRKEN (30-45 sn):\n"
    "2011-2016 arası biyomedikal mühendisliği okudum; Java ile programlamaya, MATLAB ile "
    "medikal görüntü işlemeye başlamıştım. 2017'de yüksek lisans yaparken makine öğrenmesi, "
    "özellikle ağaç modelleri üzerine çalıştım. 3 yıl yönetim danışmanlığı yaptım; şirketlerin "
    "Ar-Ge merkezi kurulum süreçlerini yönetiyordum. 2020'de Python ile oyun yapma eğitimi "
    "verdim. 2021'de Miuul ile tanıştım; ML, DL ve Transformer modellere odaklandım. 3 yıl veri "
    "bilimci olarak çalıştım. 7 aydır Almanya'dayım; Berlin'de iklim üzerine çalışan bir firmada "
    "AI Engineer olarak çalışıyorum. Aynı zamanda Miuul'da Deep Learning Bootcamp'ında "
    "mentörlük yapıyorum.\n\n"
    "Beklentiyi netleştir: matematik türetmeyeceğiz, sezgi kuracağız. Arayı burada duyur."
)
s2.notes_slide.notes_text_frame.text = (
    "AÇILIŞ SORULARI: \"Fikir 1986'da hazırmış. Peki 25 yıl ne bekledi?\" — veri ve hesaplama gücü. "
    "\"Sizce veri nereden geldi?\" (sosyal medya, Web 2.0) \"Hesaplama gücü nereden geldi?\" (NVIDIA, "
    "oyun kartları) \"90'larda herkes neyle uğraşıyordu?\" (web, dot-com). Cevaplar geldikçe "
    "etiketleri göster.\n\n"
    "HİKÂYE: Ilya Sutskever 1985'te Sovyetler'de doğdu, Kudüs'te büyüdü, lisede Kanada'ya taşındı. "
    "Bir ay sonra Toronto Üniversitesi'ne alındı. Hinton'ın kapısını çaldı, yaz tatilinde bedavaya "
    "çalışmak istedi. O yıllarda sinir ağları 'ölü' sayılıyordu.\n\n"
    "KEDİ ÖRNEĞİ: Klasik yöntem kural yazıyor — bıyığı vardır, kulağı vardır, tüylüdür. Peki kedi "
    "arkası dönükse? Işık kötüyse? Kural sayısı on binlere çıkıyor. Hinton'ın fikri: balık verme, "
    "balık tutmayı öğret.\n\n"
    "17 EKİM 2012, İTALYA: O zamana kadar hata payı %26 civarındaydı ve yılda çok az düşüyordu. "
    "AlexNet bir anda %15'e indirdi. Herkes hile sandı; analizler devrimi doğruladı. Bu düğümde "
    "dur — algı kırılması, paradigma değişimlerinin en önemli anıdır.\n\n"
    "KENDİ HİKÂYENİ ARAYA SERPİŞTİR: 1986-2000 anlatırken 'ben o sırada henüz doğmamıştım / "
    "biyomedikalde MATLAB ile hâlâ kural yazıyordum', 2021'de Miuul, 2026'da Berlin."
)

prs.save(OUT)
print("kaydedildi:", OUT)
