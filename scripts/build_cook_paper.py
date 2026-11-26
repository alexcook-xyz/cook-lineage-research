"""Compile Cook_Lineage_Unified_Manuscript.md and cropped archival plates into C:\\Users\\alx93781\\Cook_Lineage_Pittsylvania_Paper.pdf."""
import os
import re
import html
from PIL import Image as PILImage
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    KeepTogether, HRFlowable, Image as RLImage, PageBreak, CondPageBreak
)

BASE_DIR = r"C:\Users\alx93781\.gemini\antigravity-cli\brain\3f8803b5-4b41-45d6-8a55-7d9df2f386d5\scratch"
MD_PATH = os.path.join(BASE_DIR, "Cook_Lineage_Unified_Manuscript.md")
PLATES_DIR = os.path.join(BASE_DIR, "plates")
OUT_PDF = r"C:\Users\alx93781\Cook_Lineage_Pittsylvania_Paper.pdf"
PREVIEW_DIR = os.path.join(BASE_DIR, "pdf_preview")

NAVY = colors.HexColor("#1B365D")
SLATE = colors.HexColor("#2C425F")
CHARCOAL = colors.HexColor("#1E293B")
MUTED = colors.HexColor("#475569")
BRONZE = colors.HexColor("#8C6D46")
BORDER = colors.HexColor("#CBD5E1")
TINT_BG = colors.HexColor("#F4F7FA")
PARCHMENT_BG = colors.HexColor("#FAF8F3")
ROW_ALT = colors.HexColor("#F8FAFC")

# Detailed Chicago / Evidence Explained captions for each embedded plate
PLATE_CITATIONS = {
    "plate_00_obituaries.png": (
        "Left: Obituary clipping for Arlin Cook (age 56, died Sunday, 15 December 1991, Columbia, Adair County, KY), "
        "unidentified Columbia newspaper, Cook Family Tree digital archive (Arlin Cook Obituary.jpg). "
        "Right: Obituary clipping for Elsie Cook (age 51, died Friday, 28 February 1986, Campbellsville, Taylor County, KY), "
        "unidentified Campbellsville newspaper, Cook Family Tree digital archive (Elsie Cook Obituary.jpg)."
    ),
    "plate_01_russell_draft.png": (
        "U.S. Selective Service System, Registration Card (D.S.S. Form 1) for Russell Cook, Serial No. 1836, Order No. 1578, "
        "Adair County, Kentucky (born 28 November 1916, age 23; employer Goff's Furniture Store; next of kin Mrs. Anna Cook, Mother), "
        "Cook Family Tree digital archive (Russell Cook WWII Draft Card .png)."
    ),
    "plate_02_1911_marriage.png": (
        "Adair County, Kentucky, Marriage Bond and License Book, Vol. 22:491, George W. Cook (age 58, 1st marriage) to "
        "Enna/Emma Janes (age 17, 1st marriage, daughter of Wesley Janes), solemnized 27 September 1911 by J. G. Smith in the presence "
        "of John H. Sneed and Maggie Richards; County Clerk's Office, Columbia (Adair_1911_Marriage_Cook_Janes.png)."
    ),
    "plate_03_1935_death_cert.png": (
        "Commonwealth of Kentucky, Bureau of Vital Statistics, Certificate of Death No. 18658 (Registered No. 2000), "
        "George William Cook (born 26 February 1852, died 16 July 1935, age 83 years, 20 days; intestinal tuberculosis; father George Cook "
        "[hearsay 'Ky']; mother Cole; informant Mrs. G. W. Cook), Frankfort (Adair_1935_DeathCert_18658.png)."
    ),
    "plate_04_dbz_p195_deed.png": (
        "Adair County, Kentucky, Deed Book Z:195, George W. Cook to Thos. H. Cook, 19 February 1877, $356 for two undivided shares "
        "('2/6 or 1/3') of 142 acres on Russell's Creek 'owned by my father George Cook at the time of his death'; "
        "County Clerk's Office, Columbia (Adair_DBZ_p194-195_EXACT.png)."
    ),
    "plate_05_wbm_eliza_will.png": (
        "Adair County, Kentucky, Will Book M:133–134, Last Will and Testament of Eliza E. Cook, dated 8 October 1900 (top, p. 133) "
        "and proved 1 January 1906 (bottom, p. 134), devising to sons Thomas H. Cook, John D. Cook, and George W. Cook; "
        "County Clerk's Office, Columbia (Adair_WBM_p132-133start.png; Adair_WBM_p133.png)."
    ),
    "plate_06_wbm_james_will.png": (
        "Adair County, Kentucky, Will Book M:7, Last Will and Testament of James Cook, dated 18 October 1890, proved 1 May 1893, "
        "devising to wife Susanah for life and remainder to nephew and executor George W. Curry; "
        "County Clerk's Office, Columbia (Adair_WBM_p7.png)."
    ),
    "plate_07_db33_p101.png": (
        "Pittsylvania County, Virginia, Deed Book 33:101, Catharine Cook (widow of George Cook Dec'd) and adult heirs David, James, "
        "Elizabeth, Washington, and John Cook to James Nance, 15 October 1831 (recorded 21 November 1831), $140.74 for 'two hundred "
        "and Seventy Seven Acres'; Henry and George Cook omitted from signatures (Pittsylvania_DB33_p101.png)."
    ),
    "plate_08_db39_p242_poa.png": (
        "Pittsylvania County, Virginia, Deed Book 39:242, Power of Attorney from George Cook and Henry Cook of Cumberland County, "
        "Kentucky, to 'our Brother James Cook of Adair County,' 2 November 1836 (recorded 19 December 1836), reciting scribal drift "
        "'two hundred and twenty seven acres' descended from 'George Cook Deceased' (Pittsylvania_DB39_p242.png)."
    ),
    "plate_09_db39_p256_deed.png": (
        "Pittsylvania County, Virginia, Deed Book 39:256, James Cook of Adair County, Kentucky (attorney-in-fact for George and Henry Cook) "
        "to James Nance, 10 November 1836 (recorded 19 December 1836), $45, reciting 'at which time the said deed was made the aforesaid "
        "George & Henry Cook were infants' (Pittsylvania_DB39_p256-257.png)."
    ),
    "plate_10_db39_p319_320_sheriff.png": (
        "Pittsylvania County, Virginia, Deed Book 39:319–320, Thomas H. Wooding, late Sheriff and administrator c.t.a. of George Cook Senr. "
        "Dec'd, to John Williams, 27 January 1837 (proved 29 January 1837), $107.67 for 97 acres on Sandy Creek adjoining Thomas Flippin "
        "'according to the Will of the said Cook' (Pittsylvania_DB39_p319-320_EXACT.png)."
    ),
    "plate_12_dw11_p240_pruett.png": (
        "Pittsylvania County, Virginia, Deeds & Wills Book 11:240, Will of Samuell Pruett, dated 13 November 1801, proved 21 December 1801, "
        "twice naming 'my Daughter Ruth Cook' (Pittsylvania_DW11_p240.png)."
    ),
    "plate_13_db18_p68_1812.png": (
        "Pittsylvania County, Virginia, Deed Book 18:68, George Cook and Ruth Cook to John Clark, executed in the thirty-fifth year of the "
        "Commonwealth (4 July 1810–3 July 1811), proved 17 August 1812, witnessed by Thomas Clark, Leonard Clark, and a second George Cook "
        "(george-cook-jr-deed-clark-1812-db18-p68.jpg)."
    ),
    "plate_11a_ac_index.png": (
        "Pittsylvania County, Virginia, General Index No. 1 to Accounts Current, Inventories, Etc., entry for George Cook: "
        "'Inv & app | Book 7 | Page 210 | May 19, 1823' (Pittsylvania_AC_Index_Cook.png)."
    ),
    "plate_11b_ac7_inv.png": (
        "Pittsylvania County, Virginia, Accounts Current Book 7:210–211, Inventory and Appraisement of the Estate of George Cook Deceased "
        "($240.50), appraised 27 March 1823 and returned 19 May 1823 by Richard B. Cook, administrator "
        "(Pittsylvania_AC7_GeorgeCook_Inventory_pp276-277.png)."
    ),
    "plate_14a_amelia_1750_patent.png": (
        "Virginia Land Office, Patents No. 29 (1749–1751), pp. 316–317, Royal Patent to George Cook for 400 acres on the head branches "
        "of Harris's Creek, Amelia County, 3 November 1750, signed by Council President Thomas Lee; Library of Virginia, Richmond "
        "(LVA_Patents29_p316.png; LVA_Patents29_p317.png)."
    ),
    "plate_14b_pe_1768_deed.png": (
        "Prince Edward County, Virginia, Deed Book 3:366–368, George Cook of Prince Edward County to Alexander Guill, 18 April 1768 "
        "(acknowledged April Court 1768, Test Fr. Watkins D.C.), £13 for 150 acres on the branches of Harris's Creek matching the southern "
        "survey bearings of the 1750 Amelia patent (PrinceEdward_1768_Cook_to_Guill_Deed.png; p367-368.png)."
    ),
    "plate_15_grantsA_1780_josiah.png": (
        "Virginia Land Office, Grants A (1779–1780), pp. 403–404, Commonwealth Grant to Josiah Cook for 261 acres on the branches of "
        "Sandy Creek, Pittsylvania County, surveyed 25 March 1779, granted 12 June 1780, signed by Governor Thomas Jefferson; "
        "Library of Virginia, Richmond (LVA_GrantsA_p403.png; LVA_GrantsA_p404.png)."
    ),
}


def register_fonts():
    fonts_dir = r"C:\Windows\Fonts"
    pdfmetrics.registerFont(TTFont("Georgia", os.path.join(fonts_dir, "georgia.ttf")))
    pdfmetrics.registerFont(TTFont("Georgia-Bold", os.path.join(fonts_dir, "georgiab.ttf")))
    pdfmetrics.registerFont(TTFont("Georgia-Italic", os.path.join(fonts_dir, "georgiai.ttf")))
    pdfmetrics.registerFont(TTFont("Georgia-BoldItalic", os.path.join(fonts_dir, "georgiaz.ttf")))
    pdfmetrics.registerFontFamily(
        "Georgia",
        normal="Georgia", bold="Georgia-Bold",
        italic="Georgia-Italic", boldItalic="Georgia-BoldItalic"
    )
    pdfmetrics.registerFont(TTFont("Segoe", os.path.join(fonts_dir, "segoeui.ttf")))
    pdfmetrics.registerFont(TTFont("Segoe-Bold", os.path.join(fonts_dir, "segoeuib.ttf")))
    pdfmetrics.registerFont(TTFont("Segoe-Italic", os.path.join(fonts_dir, "segoeuii.ttf")))
    pdfmetrics.registerFont(TTFont("Segoe-BoldItalic", os.path.join(fonts_dir, "segoeuiz.ttf")))
    pdfmetrics.registerFontFamily(
        "Segoe",
        normal="Segoe", bold="Segoe-Bold",
        italic="Segoe-Italic", boldItalic="Segoe-BoldItalic"
    )


class CleanPageNumberCanvas(canvas.Canvas):
    """Canvas with minimal centered page numbers only (pages 2+) and zero fake headers/banners."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        for state in self._saved_page_states:
            self.__dict__.update(state)
            if self._pageNumber > 1:
                self.saveState()
                self.setFont("Georgia", 9)
                self.setFillColor(MUTED)
                self.drawCentredString(letter[0] / 2.0, 28, str(self._pageNumber))
                self.restoreState()
            super().showPage()
        super().save()


def inline_md_to_rml(text):
    """Convert inline markdown (**bold**, *italic*, `code`, [^n]) to clean ReportLab XML."""
    # Extract backticked code spans first so asterisks inside them (e.g. `Cook*`) are protected
    code_spans = []
    def _save_code(m):
        code_spans.append(html.escape(m.group(1), quote=False))
        return f"\x00CODE{len(code_spans)-1}\x00"

    s = re.sub(r'`([^`]+?)`', _save_code, text)
    s = html.escape(s, quote=False)
    # Bold + italic ***text***
    s = re.sub(r'\*\*\*(.+?)\*\*\*', r'<b><i>\1</i></b>', s)
    # Bold **text**
    s = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', s)
    # Italic *text*
    s = re.sub(r'(?<!\*)\*([^*]+?)\*(?!\*)', r'<i>\1</i>', s)
    # Consecutive footnote markers [^2][^3] -> comma-separated superscript 2,3
    def _join_footnotes(m):
        nums = re.findall(r'\[\^(\d+)\]', m.group(0))
        return f'<super><font face="Segoe-Bold" size="6.8" color="#1B365D">{",".join(nums)}</font></super>'

    s = re.sub(r'(?:\[\^\d+\])+', _join_footnotes, s)
    # Restore code spans
    for idx, ctext in enumerate(code_spans):
        s = s.replace(f"\x00CODE{idx}\x00", f'<font face="Segoe" size="8.8" color="#0F172A">{ctext}</font>')
    # Ensure glyphs absent from Georgia (arrows, superscript 4, small square bullet) render via Segoe
    for sym in ("→", "←", "↔", "⁴", "▪"):
        if sym in s:
            s = s.replace(sym, f'<font face="Segoe">{sym}</font>')
    return s


def make_styles():
    base = ParagraphStyle("Base", fontName="Georgia", fontSize=9.7, leading=14.0, textColor=CHARCOAL)
    return {
        "title": ParagraphStyle(
            "Title", parent=base, fontName="Georgia-Bold", fontSize=16.5, leading=21.0,
            alignment=TA_CENTER, textColor=NAVY, spaceAfter=6
        ),
        "author": ParagraphStyle(
            "Author", parent=base, fontName="Georgia", fontSize=11.0, leading=15.0,
            alignment=TA_CENTER, textColor=SLATE, spaceAfter=10
        ),
        "abstract_hdr": ParagraphStyle(
            "AbsHdr", parent=base, fontName="Segoe-Bold", fontSize=9.2, leading=12.0,
            textColor=NAVY, spaceAfter=3
        ),
        "abstract": ParagraphStyle(
            "AbsBody", parent=base, fontName="Georgia", fontSize=9.3, leading=13.4,
            alignment=TA_JUSTIFY, textColor=CHARCOAL
        ),
        "h2": ParagraphStyle(
            "H2", parent=base, fontName="Georgia-Bold", fontSize=12.5, leading=16.0,
            textColor=NAVY, spaceBefore=14, spaceAfter=4, keepWithNext=True
        ),
        "h3": ParagraphStyle(
            "H3", parent=base, fontName="Georgia-Bold", fontSize=10.7, leading=14.2,
            textColor=SLATE, spaceBefore=10, spaceAfter=3, keepWithNext=True
        ),
        "h4": ParagraphStyle(
            "H4", parent=base, fontName="Segoe-Bold", fontSize=9.8, leading=13.2,
            textColor=NAVY, spaceBefore=7, spaceAfter=2, keepWithNext=True
        ),
        "body": ParagraphStyle(
            "Body", parent=base, fontName="Georgia", fontSize=9.7, leading=14.0,
            alignment=TA_JUSTIFY, spaceAfter=6
        ),
        "bullet": ParagraphStyle(
            "Bullet", parent=base, fontName="Georgia", fontSize=9.5, leading=13.5,
            alignment=TA_JUSTIFY, leftIndent=16, firstLineIndent=-10, spaceAfter=4
        ),
        "subbullet": ParagraphStyle(
            "SubBullet", parent=base, fontName="Georgia", fontSize=9.3, leading=13.0,
            alignment=TA_JUSTIFY, leftIndent=30, firstLineIndent=-10, spaceAfter=3
        ),
        "quote": ParagraphStyle(
            "Quote", parent=base, fontName="Georgia-Italic", fontSize=9.3, leading=13.2,
            alignment=TA_JUSTIFY, textColor=CHARCOAL, spaceAfter=2
        ),
        "callout": ParagraphStyle(
            "Callout", parent=base, fontName="Georgia", fontSize=9.2, leading=13.0,
            alignment=TA_JUSTIFY, textColor=CHARCOAL, spaceAfter=2
        ),
        "tbl_hdr": ParagraphStyle(
            "TblHdr", fontName="Segoe-Bold", fontSize=8.0, leading=10.2,
            textColor=colors.white, alignment=TA_LEFT
        ),
        "tbl_cell": ParagraphStyle(
            "TblCell", fontName="Segoe", fontSize=7.8, leading=10.2,
            textColor=CHARCOAL, alignment=TA_LEFT
        ),
        "plate_cap": ParagraphStyle(
            "PlateCap", fontName="Segoe", fontSize=8.1, leading=11.0,
            textColor=CHARCOAL, alignment=TA_LEFT
        ),
        "note": ParagraphStyle(
            "Note", parent=base, fontName="Georgia", fontSize=8.4, leading=11.4,
            alignment=TA_LEFT, leftIndent=18, firstLineIndent=-18, spaceAfter=3.5
        ),
    }


def build_callout(lines, styles, is_transcript=False):
    text = " ".join(l.strip() for l in lines)
    style = styles["quote"] if is_transcript else styles["callout"]
    p = Paragraph(inline_md_to_rml(text), style)
    bg = PARCHMENT_BG if is_transcript else TINT_BG
    bar = BRONZE if is_transcript else NAVY
    t = Table([[p]], colWidths=[7.0 * inch])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("LINEBEFORE", (0, 0), (0, -1), 2.5, bar),
        ("BOX", (0, 0), (-1, -1), 0.4, BORDER),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    return KeepTogether([Spacer(1, 3), t, Spacer(1, 7)])


def compute_col_widths(headers, total_width=7.0 * inch):
    h0 = headers[0].lower()
    n = len(headers)
    if n == 6 and "gen" in h0:
        fracs = [0.05, 0.17, 0.14, 0.15, 0.34, 0.15]
    elif n == 6 and "profile" in h0:
        fracs = [0.15, 0.13, 0.13, 0.27, 0.15, 0.17]
    elif n == 4 and "trap" in h0:
        fracs = [0.20, 0.21, 0.25, 0.34]
    elif n == 3 and "excluded" in h0:
        fracs = [0.24, 0.25, 0.51]
    elif n == 4 and "survey" in h0:
        fracs = [0.16, 0.27, 0.27, 0.30]
    else:
        fracs = [1.0 / n] * n
    return [f * total_width for f in fracs]


def build_table(rows, styles):
    headers = rows[0]
    body_rows = rows[2:]  # skip separator row
    col_widths = compute_col_widths(headers)
    data = [[Paragraph(inline_md_to_rml(c), styles["tbl_hdr"]) for c in headers]]
    for r in body_rows:
        padded = r + [""] * (len(headers) - len(r))
        data.append([Paragraph(inline_md_to_rml(c), styles["tbl_cell"]) for c in padded[:len(headers)]])

    tbl = Table(data, colWidths=col_widths, repeatRows=1, splitByRow=1)
    ts = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.4, BORDER),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4.5),
    ]
    for idx in range(1, len(data)):
        if idx % 2 == 0:
            ts.append(("BACKGROUND", (0, idx), (-1, idx), ROW_ALT))
        else:
            ts.append(("BACKGROUND", (0, idx), (-1, idx), colors.white))
    tbl.setStyle(TableStyle(ts))
    return [Spacer(1, 4), tbl, Spacer(1, 8)]


def build_plate(plate_num, filename, short_title, styles):
    img_path = os.path.join(PLATES_DIR, filename)
    jpg_dir = os.path.join(BASE_DIR, "plates_jpg")
    os.makedirs(jpg_dir, exist_ok=True)
    jpg_path = os.path.join(jpg_dir, os.path.splitext(filename)[0] + ".jpg")
    with PILImage.open(img_path) as pim:
        px_w, px_h = pim.size
        pim.convert("RGB").save(jpg_path, format="JPEG", quality=90, optimize=True)

    # Fit inside 6.72 in wide x max_h tall while maintaining legible scale
    max_w = 6.72 * inch
    if filename == "plate_00_obituaries.png":
        max_h = 2.0 * inch
    elif filename in ("plate_01_russell_draft.png", "plate_11a_ac_index.png"):
        max_h = 3.5 * inch
    elif filename in ("plate_10_db39_p319_320_sheriff.png", "plate_14b_pe_1768_deed.png"):
        max_h = 4.2 * inch
    else:
        max_h = 6.2 * inch

    aspect = px_h / px_w
    disp_w = max_w
    disp_h = disp_w * aspect
    if disp_h > max_h:
        disp_h = max_h
        disp_w = disp_h / aspect

    rl_img = RLImage(jpg_path, width=disp_w, height=disp_h)
    citation = PLATE_CITATIONS.get(filename, short_title)
    cap_html = f"<b>Plate {plate_num}. {html.escape(short_title)}.</b> {html.escape(citation)}"
    cap_p = Paragraph(cap_html, styles["plate_cap"])

    frame = Table([[rl_img], [cap_p]], colWidths=[7.0 * inch])
    frame.setStyle(TableStyle([
        ("ALIGN", (0, 0), (0, 0), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#FAFBFC")),
        ("BOX", (0, 0), (-1, -1), 0.6, BORDER),
        ("LINEBELOW", (0, 0), (0, 0), 0.4, BORDER),
        ("TOPPADDING", (0, 0), (0, 0), 7),
        ("BOTTOMPADDING", (0, 0), (0, 0), 7),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 1), (0, 1), 6),
        ("BOTTOMPADDING", (0, 1), (0, 1), 6),
    ]))
    return KeepTogether([Spacer(1, 5), frame, Spacer(1, 8)])


def parse_markdown_to_story(md_text, styles):
    lines = md_text.splitlines()
    story = []
    i = 0
    plate_counter = 0

    # Extract Title & Author at top
    title_text = ""
    author_text = ""
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith("# "):
            title_text = line[2:].strip()
            i += 1
            continue
        if line.startswith("**Author:**"):
            author_text = line.replace("**Author:**", "").strip()
            i += 1
            continue
        if line in ("", "---"):
            i += 1
            if title_text and author_text and line == "---":
                break
            continue
        break

    story.append(Paragraph(inline_md_to_rml(title_text), styles["title"]))
    story.append(HRFlowable(width="35%", thickness=1.2, color=BRONZE, hAlign="CENTER", spaceBefore=2, spaceAfter=6))
    story.append(Paragraph(f"<b>{html.escape(author_text)}</b>", styles["author"]))
    story.append(Spacer(1, 4))

    in_abstract = False
    abstract_buf = []
    in_notes = False

    while i < len(lines):
        raw = lines[i]
        line = raw.strip()

        if not line or line == "---":
            if in_abstract and abstract_buf:
                abs_p = Paragraph(inline_md_to_rml(" ".join(abstract_buf)), styles["abstract"])
                abs_hdr = Paragraph("ABSTRACT", styles["abstract_hdr"])
                abs_box = Table([[abs_hdr], [abs_p]], colWidths=[7.0 * inch])
                abs_box.setStyle(TableStyle([
                    ("BACKGROUND", (0, 0), (-1, -1), TINT_BG),
                    ("LINEBEFORE", (0, 0), (0, -1), 2.5, NAVY),
                    ("BOX", (0, 0), (-1, -1), 0.4, BORDER),
                    ("LEFTPADDING", (0, 0), (-1, -1), 11),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 11),
                    ("TOPPADDING", (0, 0), (0, 0), 7),
                    ("BOTTOMPADDING", (0, 0), (0, 0), 2),
                    ("TOPPADDING", (0, 1), (0, 1), 2),
                    ("BOTTOMPADDING", (0, 1), (0, 1), 8),
                ]))
                story.append(KeepTogether([abs_box, Spacer(1, 8)]))
                abstract_buf = []
                in_abstract = False
            i += 1
            continue

        if line == "## Abstract":
            in_abstract = True
            i += 1
            continue

        if in_abstract:
            abstract_buf.append(line)
            i += 1
            continue

        # Embedded plate marker: **[EMBED PLATE N: `filename` — short_title]**
        m_plate = re.match(r'^\*\*\[EMBED PLATE \d+:\s*`([^`]+)`\s*[—-]\s*(.+?)\]\*\*$', line)
        if m_plate:
            plate_counter += 1
            fname, short_title = m_plate.group(1), m_plate.group(2)
            story.append(build_plate(plate_counter, fname, short_title, styles))
            i += 1
            continue

        # Headings (prevent orphaned headings by requiring ample vertical space below H2/H3/H4)
        # Look ahead to see if a table immediately follows this heading
        j = i + 1
        while j < len(lines) and not lines[j].strip():
            j += 1
        next_is_table = (j < len(lines) and lines[j].strip().startswith("|"))

        if line.startswith("## "):
            hdr_text = line[3:].strip()
            if hdr_text.startswith("Notes"):
                in_notes = True
                story.append(PageBreak())
            elif hdr_text.startswith("Selected Bibliography"):
                in_notes = False
                story.append(CondPageBreak(2.0 * inch))
            else:
                story.append(CondPageBreak(2.4 * inch if next_is_table else 1.8 * inch))
            story.append(Paragraph(inline_md_to_rml(hdr_text), styles["h2"]))
            story.append(HRFlowable(width="100%", thickness=0.6, color=BORDER, spaceBefore=0, spaceAfter=6))
            i += 1
            continue
        if line.startswith("### "):
            hdr_text = line[4:].strip()
            if hdr_text.startswith("Master Lineage Summary"):
                story.append(CondPageBreak(3.2 * inch))
            else:
                story.append(CondPageBreak(2.4 * inch if next_is_table else 1.5 * inch))
            story.append(Paragraph(inline_md_to_rml(hdr_text), styles["h3"]))
            i += 1
            continue
        if line.startswith("#### "):
            story.append(CondPageBreak(2.0 * inch if next_is_table else 1.1 * inch))
            story.append(Paragraph(inline_md_to_rml(line[5:].strip()), styles["h4"]))
            i += 1
            continue

        # Tables
        if line.startswith("|"):
            tbl_rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                row_str = lines[i].strip().strip("|")
                cells = [c.strip() for c in row_str.split("|")]
                tbl_rows.append(cells)
                i += 1
            story.extend(build_table(tbl_rows, styles))
            continue

        # Blockquotes / Callouts
        if line.startswith(">"):
            q_lines = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                q_lines.append(lines[i].strip()[1:].strip())
                i += 1
            is_transcript = any(q.startswith('*"') for q in q_lines)
            story.append(build_callout(q_lines, styles, is_transcript=is_transcript))
            continue

        # Endnotes
        if in_notes and re.match(r'^\[\^(\d+)\]:\s*', line):
            m_note = re.match(r'^\[\^(\d+)\]:\s*(.+)$', line)
            n_num, n_body = m_note.group(1), m_note.group(2)
            story.append(Paragraph(f"<b>{n_num}.</b> {inline_md_to_rml(n_body)}", styles["note"]))
            i += 1
            continue

        # Sub-bullets (indented `- ` or `   - `)
        if re.match(r'^\s{2,}-\s+', raw):
            content = re.sub(r'^\s+-\s+', '', raw).strip()
            story.append(Paragraph(f"▪&nbsp;&nbsp;{inline_md_to_rml(content)}", styles["subbullet"]))
            i += 1
            continue

        # Top-level bullets (`- `)
        if line.startswith("- "):
            story.append(Paragraph(f"•&nbsp;&nbsp;{inline_md_to_rml(line[2:].strip())}", styles["bullet"]))
            i += 1
            continue

        # Numbered list items (`1. `, `2. `)
        m_num = re.match(r'^(\d+)\.\s+(.+)$', line)
        if m_num:
            num, body = m_num.group(1), m_num.group(2)
            story.append(Paragraph(f"<b>{num}.</b>&nbsp;&nbsp;{inline_md_to_rml(body)}", styles["bullet"]))
            i += 1
            continue

        # Standard paragraph (merge consecutive plain prose lines)
        para_lines = [line]
        i += 1
        while i < len(lines):
            nxt = lines[i].strip()
            if (not nxt or nxt == "---" or nxt.startswith("#") or nxt.startswith("|")
                    or nxt.startswith(">") or nxt.startswith("- ") or nxt.startswith("**[EMBED")
                    or re.match(r'^(\d+)\.\s+', nxt) or re.match(r'^\s{2,}-\s+', lines[i])
                    or re.match(r'^\[\^\d+\]:', nxt)):
                break
            para_lines.append(nxt)
            i += 1
        story.append(Paragraph(inline_md_to_rml(" ".join(para_lines)), styles["body"]))

    return story, plate_counter


def audit_and_preview():
    import pymupdf
    os.makedirs(PREVIEW_DIR, exist_ok=True)
    doc = pymupdf.open(OUT_PDF)
    full_text = "\n".join(page.get_text("text") for page in doc)

    # Zero-tolerance checks
    banned_dna = re.findall(r'\b(dna|y-dna|mtdna|autosomal|genetic genealogy|chromosom\w*)\b', full_text, re.I)
    banned_fake = re.findall(r'(quarterly|ngsq|antigravity|prepared by|case study|vol\.\s*\d+,\s*no\.)', full_text, re.I)
    raw_md = re.findall(r'(\*\*|\[\^\d+\]|`)', full_text)

    print(f"PDF Pages: {len(doc)}")
    print(f"DNA hits: {banned_dna}")
    print(f"Fake-banner/AI hits: {banned_fake}")
    print(f"Raw markdown residue hits: {raw_md[:10]}")

    # Check bottom lines of every page for potential orphaned headings
    for idx, page in enumerate(doc):
        lines_p = [ln.strip() for ln in page.get_text("text").splitlines() if ln.strip()]
        # Strip trailing page number
        if lines_p and lines_p[-1].isdigit() and int(lines_p[-1]) == idx + 1:
            lines_p = lines_p[:-1]
        tail = lines_p[-1] if lines_p else ""
        print(f"  p.{idx+1:02d} tail: {tail[:90]}")

    for old_png in os.listdir(PREVIEW_DIR):
        if old_png.endswith(".png"):
            os.remove(os.path.join(PREVIEW_DIR, old_png))
    for idx, page in enumerate(doc):
        pix = page.get_pixmap(dpi=130)
        pix.save(os.path.join(PREVIEW_DIR, f"page_{idx+1:02d}.png"))
    print(f"Rendered {len(doc)} preview PNGs to {PREVIEW_DIR}")


def main():
    register_fonts()
    with open(MD_PATH, "r", encoding="utf-8") as f:
        md_text = f.read()

    styles = make_styles()
    story, plate_count = parse_markdown_to_story(md_text, styles)
    print(f"Parsed {len(story)} flowables, {plate_count} documentary plates.")

    doc = SimpleDocTemplate(
        OUT_PDF,
        pagesize=letter,
        leftMargin=0.75 * inch,
        rightMargin=0.75 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.70 * inch,
        title="From South-Central Kentucky to the Dan River and Harris's Creek: Patrilineal Lineage of Alex Haley Cook",
        author="Alex Cook",
    )
    doc.build(story, canvasmaker=CleanPageNumberCanvas)
    print(f"Successfully built {OUT_PDF} ({os.path.getsize(OUT_PDF):,} bytes)")
    audit_and_preview()


if __name__ == "__main__":
    main()
