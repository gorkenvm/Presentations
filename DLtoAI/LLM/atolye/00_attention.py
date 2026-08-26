# -*- coding: utf-8 -*-
"""
00_attention.py — Bir saattir anlattığımız şey, çalışan modelin içinde.

Üç bölüm, toplam ~3 dakika:
  ①  TOKENLAR    cümle → parçalar (1. saatteki BPE, aynı model)
  ②  ATTENTION   bir token diğerlerine ne kadar bakıyor?  (gerçek matris)
  ③  KUTULAR     q_proj / k_proj / v_proj / o_proj — modelin içindeki Linear'lar

③ kasıtlı. 30 dakika sonra 04_finetune.py'de aynı isimler
LoraConfig(target_modules=[...]) satırında yeniden karşımıza çıkacak.

Bu betik aynı zamanda MODELİ ISITIR — ilk çağrının gecikmesi salonda geçmesin.

Çalıştır:  python 00_attention.py
"""
import sys

from ortak import (CY, KL, MR, MV, R, SN, SR, YS, altbaslik, alan, baslik,
                   bilgi, cubuk, duraklat, kutu, yukle)

# Koreferans örneği: "o" kime işaret ediyor?
CUMLE = "Öğrenci sınava giremedi çünkü o çok hastaydı."

# Bakacağımız token. Provada seçildi.
HEDEF = "o"

# Provada taranıp sabitlenen (katman, kafa) çifti.
# None ise betik en iyi çifti kendisi arar ve ekrana yazar.
KATMAN_KAFA = None


def temiz(t: str) -> str:
    """Tokenizer'ın 'Ġ' (boşluk) işaretini okunur hale getirir."""
    return t.replace("Ġ", "·").replace("Ċ", "\\n")


def en_iyi_kafa(dikkat, hedef_idx, kaynak_idx):
    """hedef token'ın kaynak token'a en çok baktığı (katman, kafa) çiftini bulur.

    Gerçek bir yorumlanabilirlik iddiası değil — sınıfta göstermeye
    en uygun kafayı seçiyoruz. Attention ağırlıkları bir açıklama değil,
    bir ölçüm; bu ayrımı söylemekte fayda var.
    """
    en_iyi, skor = (0, 0), -1.0
    for k, kat in enumerate(dikkat):
        for h in range(kat.shape[1]):
            d = float(kat[0, h, hedef_idx, kaynak_idx])
            if d > skor:
                skor, en_iyi = d, (k, h)
    return en_iyi, skor


def main():
    baslik("00 — ATTENTION:  1. saatte çizdiğimiz şey, modelin içinde")
    bilgi("Bu, atölyede kullanacağımız modelin ta kendisi. Oyuncak örnek değil.")
    duraklat("modeli yükle")

    import torch
    tok, model = yukle(attention_ile=True)

    # ── ① TOKENLAR ───────────────────────────────────────────────────
    altbaslik("① TOKENLAR — cümle nasıl parçalanıyor?")
    alan("cümle", CUMLE, KL)
    print()
    kimlikler = tok(CUMLE, return_tensors="pt")
    idler = kimlikler["input_ids"][0].tolist()
    parcalar = tok.convert_ids_to_tokens(idler)
    print("   " + " ".join(f"{SR}{temiz(p)}{R}{SN}|{R}" for p in parcalar))
    print()
    alan("token", f"{len(parcalar)} adet")
    alan("kelime", f"{len(CUMLE.split())} adet")
    print()
    bilgi("Türkçe ekler yüzünden token sayısı kelime sayısından fazla.")
    bilgi("Aynı cümle İngilizce olsaydı daha az token ederdi — ve daha ucuz olurdu.")
    duraklat()

    # ── ② ATTENTION ──────────────────────────────────────────────────
    altbaslik("② ATTENTION — 'o' token'ı neye bakıyor?", MV)

    girdi = {k: v.to(model.device) for k, v in kimlikler.items()}
    with torch.no_grad():
        cikti = model(**girdi, output_attentions=True)
    dikkat = [a.float().cpu() for a in cikti.attentions]

    # hedef token'ın yerini bul
    hedef_idx = None
    for i, p in enumerate(parcalar):
        if temiz(p).strip("·") == HEDEF:
            hedef_idx = i
    if hedef_idx is None:
        hedef_idx = len(parcalar) - 2

    kaynak_idx = 0  # "Öğrenci" — cümlenin ilk içerikli token'ı

    if KATMAN_KAFA is None:
        (kat, kafa), skor = en_iyi_kafa(dikkat, hedef_idx, kaynak_idx)
    else:
        kat, kafa = KATMAN_KAFA
        skor = float(dikkat[kat][0, kafa, hedef_idx, kaynak_idx])

    print()
    alan("toplam", f"{len(dikkat)} katman × {dikkat[0].shape[1]} kafa"
                   f" = {len(dikkat) * dikkat[0].shape[1]} attention haritası")
    alan("bakılan", f"katman {kat}, kafa {kafa}", MV)
    alan("token", f"'{temiz(parcalar[hedef_idx])}'  (sıra {hedef_idx})", KL)
    print()

    satir = dikkat[kat][0, kafa, hedef_idx, :hedef_idx + 1]
    en_buyuk = float(satir.max())
    sirali = sorted(range(len(satir)), key=lambda i: -float(satir[i]))

    for i in range(hedef_idx + 1):
        d = float(satir[i])
        vurgu = KL + YS if i == sirali[0] else ""
        etiket = temiz(parcalar[i])
        print(f"   {cubuk(d / max(en_buyuk, 1e-9))}  {d:.3f}  "
              f"{vurgu}{etiket}{R}")
    print()

    en_cok = temiz(parcalar[sirali[0]]).strip("·")
    print(f"{YS}{KL}   → '{HEDEF}' en çok '{en_cok}' token'ına bakıyor.{R}")
    print()
    bilgi("Causal maskeyi de görüyorsunuz: token yalnızca KENDİSİNDEN ÖNCEKİLERE")
    bilgi("bakabiliyor. Sonrasına bakamaz — bu yüzden 'sonraki token'ı tahmin et'.")
    print()
    bilgi("Uyarı: attention bir AÇIKLAMA değil, bir ÖLÇÜM. 'Model şunu düşündü'")
    bilgi("diyemeyiz; 'bu kafa şu token'a ağırlık verdi' diyebiliriz.")
    duraklat()

    # ── ③ KUTULAR ────────────────────────────────────────────────────
    altbaslik("③ O MATRİSİ ÜRETEN KUTULAR", MR)
    print()
    kat0 = model.model.layers[0].self_attn
    satirlar = []
    for ad in ("q_proj", "k_proj", "v_proj", "o_proj"):
        m = getattr(kat0, ad, None)
        if m is None:
            continue
        satirlar.append(f"{ad:<8} Linear({m.in_features} → {m.out_features})")
    kutu("\n".join(satirlar), f"{type(kat0).__name__}  — katman 0", MR)
    print()

    toplam = sum(p.numel() for p in model.parameters())
    dikkat_p = sum(p.numel() for n, p in model.named_parameters()
                   if any(x in n for x in ("q_proj", "k_proj", "v_proj", "o_proj")))
    alan("model", f"{toplam / 1e6:.0f} M parametre", "", 14)
    alan("bu 4 kutu", f"{dikkat_p / 1e6:.0f} M parametre "
                      f"(%{100 * dikkat_p / toplam:.0f})", MR, 14)
    print()

    kutu("Q · K · V — bir saat önce tahtada çizdiğimiz üç kutu.\n"
         "Burada isimleri var: q_proj, k_proj, v_proj, o_proj.\n"
         "\n"
         "Bu isimleri aklınızda tutun.\n"
         "30 dakika sonra fine-tune ederken tam olarak bunları eğiteceğiz.",
         "aklınızda kalsın", CY)
    print()
    bilgi("Model artık yüklü ve ısındı. Sıradaki demolar hızlı açılacak.")
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
