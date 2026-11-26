"""Prepare cropped, contrast-enhanced archival document plates for the Cook Lineage paper."""
import os
from PIL import Image, ImageOps, ImageEnhance, ImageFilter

OUT_DIR = r"C:\Users\alx93781\.gemini\antigravity-cli\brain\3f8803b5-4b41-45d6-8a55-7d9df2f386d5\scratch\plates"
os.makedirs(OUT_DIR, exist_ok=True)

DL = r"C:\Users\alx93781\Downloads"
TREE = r"C:\Users\alx93781\Desktop\Flash Drive Backup\Old Hard Drive Backup\Ancestry\Cook Family Tree"


def crop_frac(img, box):
    w, h = img.size
    x0, y0, x1, y1 = box
    return img.crop((int(w * x0), int(h * y0), int(w * x1), int(h * y1)))


def enhance_doc(img, grayscale=True, autocontrast_cutoff=1, sharpen=1.35, contrast=1.15, max_width=2400):
    if img.mode == "RGBA":
        bg = Image.new("RGB", img.size, (255, 255, 255))
        bg.paste(img, mask=img.split()[3])
        img = bg
    elif img.mode == "1":
        img = img.convert("L")
    if grayscale and img.mode != "L":
        img = img.convert("L")
    elif not grayscale and img.mode != "RGB":
        img = img.convert("RGB")

    if autocontrast_cutoff is not None:
        img = ImageOps.autocontrast(img, cutoff=autocontrast_cutoff)
    if contrast != 1.0:
        img = ImageEnhance.Contrast(img).enhance(contrast)
    if sharpen != 1.0:
        img = ImageEnhance.Sharpness(img).enhance(sharpen)

    if img.width > max_width:
        ratio = max_width / img.width
        img = img.resize((max_width, int(img.height * ratio)), Image.Resampling.LANCZOS)

    # Convert to RGB for clean ReportLab embedding
    if img.mode != "RGB":
        img = img.convert("RGB")
    return img


def stack_vertical(imgs, gap=14, bg_color=(245, 245, 242)):
    target_w = max(im.width for im in imgs)
    resized = []
    for im in imgs:
        if im.width != target_w:
            ratio = target_w / im.width
            im = im.resize((target_w, int(im.height * ratio)), Image.Resampling.LANCZOS)
        resized.append(im)
    total_h = sum(im.height for im in resized) + gap * (len(resized) - 1)
    canvas = Image.new("RGB", (target_w, total_h), bg_color)
    y = 0
    for im in resized:
        canvas.paste(im, (0, y))
        y += im.height + gap
    return canvas


def stack_horizontal(imgs, gap=16, bg_color=(245, 245, 242)):
    target_h = max(im.height for im in imgs)
    resized = []
    for im in imgs:
        if im.height != target_h:
            ratio = target_h / im.height
            im = im.resize((int(im.width * ratio), target_h), Image.Resampling.LANCZOS)
        resized.append(im)
    total_w = sum(im.width for im in resized) + gap * (len(resized) - 1)
    canvas = Image.new("RGB", (total_w, target_h), bg_color)
    x = 0
    for im in resized:
        canvas.paste(im, (x, 0))
        x += im.width + gap
    return canvas


def save_plate(img, name):
    out = os.path.join(OUT_DIR, name)
    img.save(out, format="PNG", optimize=True)
    print(f"Saved {name}: {img.size[0]}x{img.size[1]}")


def main():
    # 0. Obituaries (Arlin Cook 1991 & Elsie Cook 1986)
    with Image.open(os.path.join(TREE, "Arlin Cook Obituary.jpg")) as ob1, \
         Image.open(os.path.join(TREE, "Elsie Cook Obituary.jpg")) as ob2:
        # Trim top stray "day." line on Arlin obit and upscale cleanly
        ob1_clean = crop_frac(ob1, (0.000, 0.145, 1.000, 1.000))
        o1 = ImageOps.expand(
            enhance_doc(ob1_clean, grayscale=True, autocontrast_cutoff=1, contrast=1.18, sharpen=1.25, max_width=1800)
            .resize((1350, int(ob1_clean.height * (1350 / ob1_clean.width))), Image.Resampling.LANCZOS),
            border=14, fill=(255, 255, 255)
        )
        o2 = ImageOps.expand(
            enhance_doc(ob2, grayscale=True, autocontrast_cutoff=1, contrast=1.18, sharpen=1.25, max_width=1800)
            .resize((1350, int(ob2.height * (1350 / ob2.width))), Image.Resampling.LANCZOS),
            border=14, fill=(255, 255, 255)
        )
        # Pad shorter image vertically to align neatly
        max_h = max(o1.height, o2.height)
        if o2.height < max_h:
            pad = Image.new("RGB", (o2.width, max_h), (255, 255, 255))
            pad.paste(o2, (0, (max_h - o2.height) // 2))
            o2 = pad
        save_plate(stack_horizontal([o1, o2], gap=28, bg_color=(240, 242, 245)), "plate_00_obituaries.png")

    # 1. Russell Cook WWII Draft Card
    with Image.open(os.path.join(TREE, "Russell Cook WWII Draft Card .png")) as im:
        c = crop_frac(im, (0.262, 0.165, 0.738, 0.838))
        save_plate(enhance_doc(c, grayscale=False, autocontrast_cutoff=0.5, contrast=1.12, sharpen=1.25, max_width=2000),
                   "plate_01_russell_draft.png")

    # 2. 1911 Marriage Register & Certificate (p. 491)
    with Image.open(os.path.join(DL, "Adair_1911_Marriage_Cook_Janes.png")) as im:
        c = crop_frac(im, (0.505, 0.055, 0.955, 0.935))
        save_plate(enhance_doc(c, grayscale=True, autocontrast_cutoff=2, contrast=1.35, sharpen=1.4, max_width=2000),
                   "plate_02_1911_marriage.png")

    # 3. 1935 Death Certificate #18658 (George William Cook)
    with Image.open(os.path.join(DL, "Adair_1935_DeathCert_18658.png")) as im:
        c = crop_frac(im, (0.125, 0.215, 0.895, 0.815))
        save_plate(enhance_doc(c, grayscale=True, autocontrast_cutoff=2, contrast=1.25, sharpen=1.35, max_width=1800),
                   "plate_03_1935_death_cert.png")

    # 4. Adair DB Z:195 (19 Feb 1877 George W. Cook to Thos. H. Cook)
    with Image.open(os.path.join(DL, "Adair_DBZ_p194-195_EXACT.png")) as im:
        hdr = enhance_doc(crop_frac(im, (0.505, 0.042, 0.985, 0.105)), grayscale=True, autocontrast_cutoff=2, contrast=1.28, sharpen=1.4, max_width=2200)
        body = enhance_doc(crop_frac(im, (0.505, 0.315, 0.985, 0.935)), grayscale=True, autocontrast_cutoff=2, contrast=1.28, sharpen=1.4, max_width=2200)
        save_plate(stack_vertical([hdr, body], gap=12), "plate_04_dbz_p195_deed.png")

    # 5. Eliza E. Cook Will (8 Oct 1900) & Probate (1 Jan 1906) - WBM pp. 133-134
    with Image.open(os.path.join(DL, "Adair_WBM_p132-133start.png")) as im1, \
         Image.open(os.path.join(DL, "Adair_WBM_p133.png")) as im2:
        top = enhance_doc(crop_frac(im1, (0.510, 0.500, 0.975, 0.925)), contrast=1.32, sharpen=1.4, max_width=2000)
        bot = enhance_doc(crop_frac(im2, (0.065, 0.055, 0.505, 0.425)), contrast=1.32, sharpen=1.4, max_width=2000)
        save_plate(stack_vertical([top, bot], gap=18), "plate_05_wbm_eliza_will.png")

    # 6. James Cook Will (18 Oct 1890 / 1 May 1893) - WBM p. 7
    with Image.open(os.path.join(DL, "Adair_WBM_p7.png")) as im:
        c = crop_frac(im, (0.515, 0.050, 0.985, 0.920))
        save_plate(enhance_doc(c, grayscale=True, autocontrast_cutoff=2, contrast=1.30, sharpen=1.4, max_width=2000),
                   "plate_06_wbm_james_will.png")

    # 7. Pittsylvania DB 33:101 (15 Oct / 21 Nov 1831)
    with Image.open(os.path.join(DL, "Pittsylvania_DB33_p101.png")) as im:
        c = crop_frac(im, (0.488, 0.215, 0.992, 0.988))
        save_plate(enhance_doc(c, grayscale=True, autocontrast_cutoff=2, contrast=1.32, sharpen=1.45, max_width=2200),
                   "plate_07_db33_p101.png")

    # 8. Pittsylvania DB 39:242 (2 Nov 1836 Power of Attorney)
    with Image.open(os.path.join(DL, "Pittsylvania_DB39_p242.png")) as im:
        c = crop_frac(im, (0.480, 0.565, 0.995, 0.955))
        save_plate(enhance_doc(c, grayscale=True, autocontrast_cutoff=2, contrast=1.30, sharpen=1.4, max_width=2200),
                   "plate_08_db39_p242_poa.png")

    # 9. Pittsylvania DB 39:256 (10 Nov / 19 Dec 1836 Infant Deed)
    with Image.open(os.path.join(DL, "Pittsylvania_DB39_p256-257.png")) as im:
        c = crop_frac(im, (0.495, 0.220, 0.995, 0.955))
        save_plate(enhance_doc(c, grayscale=True, autocontrast_cutoff=2, contrast=1.30, sharpen=1.4, max_width=2200),
                   "plate_09_db39_p256_deed.png")

    # 10. Pittsylvania DB 39:319-320 (27 Jan / 29 Jan 1837 Sheriff c.t.a. Deed)
    with Image.open(os.path.join(DL, "Pittsylvania_DB39_p319-320_EXACT.png")) as im:
        left = enhance_doc(crop_frac(im, (0.035, 0.545, 0.490, 0.980)), contrast=1.30, sharpen=1.4, max_width=1400)
        right = enhance_doc(crop_frac(im, (0.505, 0.025, 0.990, 0.835)), contrast=1.30, sharpen=1.4, max_width=1400)
        save_plate(stack_horizontal([left, right], gap=20), "plate_10_db39_p319_320_sheriff.png")

    # 11a. Pittsylvania Accounts Current Index (George Cook, Book 7, p. 210, May 19, 1823)
    with Image.open(os.path.join(DL, "Pittsylvania_AC_Index_Cook.png")) as im:
        c = crop_frac(im, (0.505, 0.014, 0.985, 0.365))
        save_plate(enhance_doc(c, grayscale=True, autocontrast_cutoff=2, contrast=1.28, sharpen=1.35, max_width=2200),
                   "plate_11a_ac_index.png")

    # 11b. Pittsylvania AC 7:210-211 (Inventory & Appraisement of George Cook Decd, 27 Mar / 19 May 1823)
    with Image.open(os.path.join(DL, "Pittsylvania_AC7_GeorgeCook_Inventory_pp276-277.png")) as im:
        top = enhance_doc(crop_frac(im, (0.005, 0.020, 0.495, 0.230)), contrast=1.32, sharpen=1.4, max_width=2000)
        bot = enhance_doc(crop_frac(im, (0.505, 0.025, 0.992, 0.560)), contrast=1.32, sharpen=1.4, max_width=2000)
        save_plate(stack_vertical([top, bot], gap=16), "plate_11b_ac7_inv.png")

    # 12. Pittsylvania DW 11:240 (Samuell Pruett Will, 13 Nov / 21 Dec 1801)
    with Image.open(os.path.join(DL, "Pittsylvania_DW11_p240.png")) as im:
        c = crop_frac(im, (0.015, 0.045, 0.495, 0.855))
        save_plate(enhance_doc(c, grayscale=True, autocontrast_cutoff=2, contrast=1.28, sharpen=1.4, max_width=2000),
                   "plate_12_dw11_p240_pruett.png")

    # 13. Pittsylvania DB 18:68 (George Cook & Ruth Cook to John Clark, 17 Aug 1812)
    with Image.open(os.path.join(DL, "george-cook-jr-deed-clark-1812-db18-p68.jpg")) as im:
        c = crop_frac(im, (0.115, 0.020, 0.995, 0.460))
        save_plate(enhance_doc(c, grayscale=True, autocontrast_cutoff=2, contrast=1.25, sharpen=1.4, max_width=1900),
                   "plate_13_db18_p68_1812.png")

    # 14a. Virginia Patents 29:316-317 (3 Nov 1750 George Cook 400a Amelia Co., Harris's Creek)
    with Image.open(os.path.join(DL, "LVA_Patents29_p316.png")) as p316, \
         Image.open(os.path.join(DL, "LVA_Patents29_p317.png")) as p317:
        top = enhance_doc(crop_frac(p316, (0.065, 0.720, 0.945, 0.975)), autocontrast_cutoff=0, contrast=1.15, sharpen=1.2, max_width=2000)
        bot = enhance_doc(crop_frac(p317, (0.080, 0.005, 0.915, 0.625)), autocontrast_cutoff=0, contrast=1.15, sharpen=1.2, max_width=2000)
        save_plate(stack_vertical([top, bot], gap=14), "plate_14a_amelia_1750_patent.png")

    # 14b. Prince Edward DB 3:366-368 (18 Apr 1768 George Cook to Alexander Guill 150a)
    with Image.open(os.path.join(DL, "PrinceEdward_1768_Cook_to_Guill_Deed.png")) as d1, \
         Image.open(os.path.join(DL, "PrinceEdward_1768_Cook_to_Guill_Deed_p367-368.png")) as d2:
        left = enhance_doc(crop_frac(d1, (0.515, 0.030, 0.975, 0.925)), contrast=1.28, sharpen=1.4, max_width=1400)
        sig = enhance_doc(crop_frac(d2, (0.080, 0.560, 0.500, 0.860)), contrast=1.28, sharpen=1.4, max_width=1400)
        prob = enhance_doc(crop_frac(d2, (0.515, 0.035, 0.965, 0.490)), contrast=1.28, sharpen=1.4, max_width=1400)
        right = stack_vertical([sig, prob], gap=14)
        save_plate(stack_horizontal([left, right], gap=20), "plate_14b_pe_1768_deed.png")

    # 15. Virginia Land Grants A:403-404 (12 Jun 1780 Josiah Cook 261a Sandy Creek, Thos. Jefferson)
    with Image.open(os.path.join(DL, "LVA_GrantsA_p403.png")) as g1, \
         Image.open(os.path.join(DL, "LVA_GrantsA_p404.png")) as g2:
        top = enhance_doc(crop_frac(g1, (0.075, 0.000, 0.855, 0.995)), autocontrast_cutoff=0, contrast=1.15, sharpen=1.2, max_width=1900)
        bot = enhance_doc(crop_frac(g2, (0.165, 0.000, 0.885, 0.175)), autocontrast_cutoff=0, contrast=1.15, sharpen=1.2, max_width=1900)
        save_plate(stack_vertical([top, bot], gap=12), "plate_15_grantsA_1780_josiah.png")


if __name__ == "__main__":
    main()
