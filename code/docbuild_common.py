"""Shared python-docx helpers for the Fock Variance Ladder documents."""
import json, os
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
R = json.load(open(os.path.join(ROOT, "results", "results.json")))
FIG = os.path.join(ROOT, "figures")
AUTHOR = "M. L. McKnight"
ORG = "ML Innovations Research Lab (ML Innovations LLC)"
PLACE = "Pheba, Mississippi"
EMAIL = "ml.innovation.research.lab@gmail.com"
AI_ACK = ("AI tools assisted with code and drafting. The author reviewed all text, code and results "
          "and takes full responsibility for the content.")

def f(x, d=4):
    return f"{x:.{d}f}"

def e(x, d=1):
    return f"{x:.{d}e}".replace("e-0", "e-").replace("e+0", "e+")

def new_doc(title, subject, keywords, header_text, footer_text):
    d = Document()
    st = d.styles["Normal"]; st.font.name = "Calibri"; st.font.size = Pt(11)
    st.element.rPr.rFonts.set(qn("w:eastAsia"), "Calibri")
    for s in d.sections:
        s.left_margin = s.right_margin = Inches(1); s.top_margin = s.bottom_margin = Inches(0.9)
        hp = s.header.paragraphs[0]; hp.text = header_text; hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        for r in hp.runs: r.font.size = Pt(8); r.font.color.rgb = RGBColor(0x55, 0x55, 0x55)
        fp = s.footer.paragraphs[0]; fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = fp.add_run(footer_text + " — Page "); run.font.size = Pt(8)
        add_field(fp, "PAGE")
    cp = d.core_properties
    cp.author = AUTHOR; cp.last_modified_by = AUTHOR; cp.title = title; cp.subject = subject
    cp.keywords = keywords; cp.comments = AI_ACK; cp.category = "physics.ed-ph"
    return d

def add_field(par, code):
    r = par.add_run(); r.font.size = Pt(8)
    f1 = OxmlElement("w:fldChar"); f1.set(qn("w:fldCharType"), "begin")
    it = OxmlElement("w:instrText"); it.set(qn("xml:space"), "preserve"); it.text = code
    f2 = OxmlElement("w:fldChar"); f2.set(qn("w:fldCharType"), "end")
    r._r.append(f1); r._r.append(it); r._r.append(f2)

def H(d, text, level=1):
    p = d.add_paragraph(); r = p.add_run(text); r.bold = True
    r.font.size = Pt({0: 20, 1: 15, 2: 12.5, 3: 11}[level]); r.font.color.rgb = RGBColor(0x1A, 0x36, 0x5D)
    p.paragraph_format.space_before = Pt(12 if level <= 1 else 8); p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    return p

def P(d, text="", bold_lead=None, size=11, italic=False, align=None):
    p = d.add_paragraph()
    if bold_lead:
        r = p.add_run(bold_lead); r.bold = True; r.font.size = Pt(size)
    r = p.add_run(text); r.font.size = Pt(size); r.italic = italic
    p.paragraph_format.space_after = Pt(5)
    if align == "center": p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    elif align == "justify": p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    return p

def EQ(d, text, num=None):
    p = d.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(text); r.font.name = "Cambria Math"; r.font.size = Pt(11.5)
    r._element.rPr.rFonts.set(qn("w:hAnsi"), "Cambria Math")
    if num is not None:
        r2 = p.add_run(f"     ({num})"); r2.font.size = Pt(10)
    p.paragraph_format.space_after = Pt(5)
    return p

def BUL(d, text, lead=None):
    p = d.add_paragraph(style="List Bullet")
    if lead:
        r = p.add_run(lead); r.bold = True
    p.add_run(text); return p

def TABLE(d, rows, header=True, widths=None, size=9):
    t = d.add_table(rows=len(rows), cols=len(rows[0])); t.style = "Table Grid"
    for i, row in enumerate(rows):
        for j, val in enumerate(row):
            c = t.cell(i, j); c.text = ""
            r = c.paragraphs[0].add_run(str(val)); r.font.size = Pt(size)
            if header and i == 0:
                r.bold = True
                sh = OxmlElement("w:shd"); sh.set(qn("w:val"), "clear"); sh.set(qn("w:fill"), "DCE6F1")
                c._tc.get_or_add_tcPr().append(sh)
    if widths:
        for row in t.rows:
            for j, w in enumerate(widths): row.cells[j].width = Inches(w)
    d.add_paragraph().paragraph_format.space_after = Pt(2)
    return t

def FIGURE(d, fname, caption, width=6.5):
    p = d.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.add_run().add_picture(os.path.join(FIG, fname), width=Inches(width))
    p.paragraph_format.keep_with_next = True
    c = d.add_paragraph(); c.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r = c.add_run(caption); r.font.size = Pt(9); r.italic = True
    return c

def title_block(d, kicker, title_lines, subtitle, version_line):
    P(d, kicker, size=10, align="center").runs[0].bold = True
    for t in title_lines:
        p = P(d, "", align="center"); r = p.add_run(t); r.bold = True; r.font.size = Pt(20); r.font.color.rgb = RGBColor(0x1A, 0x36, 0x5D)
    if subtitle: P(d, subtitle, size=12, align="center", italic=True)
    P(d, "")
    p = P(d, "", align="center"); r = p.add_run(AUTHOR); r.bold = True; r.font.size = Pt(12)
    P(d, ORG, size=11, align="center"); P(d, PLACE, size=11, align="center")
    P(d, EMAIL, size=10, align="center")
    P(d, version_line, size=10, align="center")
