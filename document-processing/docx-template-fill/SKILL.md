---
name: docx-template-fill
description: "Fill/modify Word .docx documents using python-docx — template-based document generation, table cell content replacement, image insertion, Chinese font handling. Use when user asks to create or modify .docx files programmatically, fill report templates, or generate academic documents."
triggers:
  - modify docx
  - fill word template
  - generate word document
  - 写入word
  - 操作docx
  - python-docx
  - 中期报告
  - 考核报告
  - academic report docx
---

# docx-template-fill

Fill/modify Word .docx documents programmatically using python-docx. Covers template-based generation, table cell manipulation, image insertion, Chinese academic document formatting.

## Dependencies

```
pip install python-docx pdfplumber PyPDF2
```

## Core Workflow

### Step 1: Read Template Structure

Always read the template first to understand its structure before modifying.

```python
from docx import Document

doc = Document('template.docx')
table = doc.tables[0]
print(f"表格: {len(table.rows)}行 x {len(table.columns)}列")
for ri, row in enumerate(table.rows):
    cell = row.cells[0]
    print(f"  行{ri}: {len(cell.paragraphs)}段")
    for pi, p in enumerate(cell.paragraphs):
        if p.text.strip():
            print(f"    [{pi}] ({p.style.name}) {p.text[:80]}")
```

### Step 2: Check Formatting Details

Before modifying, capture the existing formatting to preserve it:

```python
from docx.oxml.ns import qn

p = cell.paragraphs[0]
if p.runs:
    rpr = p.runs[0]._element.find(qn('w:rPr'))
    if rpr is not None:
        fonts = rpr.findall(qn('w:rFonts'))
        for f in fonts:
            print(f"ascii={f.get(qn('w:ascii'))}, eastAsia={f.get(qn('w:eastAsia'))}")
    print(f"size={p.runs[0].font.size}, bold={p.runs[0].font.bold}")
print(f"line_spacing={p.paragraph_format.line_spacing}")
```

### Step 3: Replace Text Preserving Formatting

```python
from copy import deepcopy

def replace_para_text(para, new_text):
    """Replace all text in paragraph while keeping first run's formatting."""
    if not para.runs:
        run = para.add_run(new_text)
        return
    first_run = para.runs[0]
    rpr = first_run._element.find(qn('w:rPr'))
    rpr_copy = deepcopy(rpr) if rpr is not None else None
    for r in list(para.runs):
        r._element.getparent().remove(r._element)
    new_run = para.add_run(new_text)
    if rpr_copy is not None:
        new_run._element.insert(0, rpr_copy)
```

### Step 4: Add New Paragraphs with Formatting

```python
from docx.oxml import OxmlElement

def add_para(cell, text, font_name='宋体', font_size=Pt(12), bold=False):
    p = cell.add_paragraph()
    p.style = doc.styles['Normal']
    p.paragraph_format.line_spacing = 1.5
    if text:
        run = p.add_run(text)
        run.font.size = font_size
        run.font.bold = bold
        rpr = run._element.find(qn('w:rPr'))
        if rpr is None:
            rpr = OxmlElement('w:rPr')
            run._element.insert(0, rpr)
        fonts = OxmlElement('w:rFonts')
        fonts.set(qn('w:ascii'), 'Times New Roman')
        fonts.set(qn('w:hAnsi'), 'Times New Roman')
        fonts.set(qn('w:eastAsia'), font_name)
        fonts.set(qn('w:hint'), 'eastAsia')
        rpr.insert(0, fonts)
    return p
```

### Step 5: Insert Images into Table Cells

```python
def add_image_after_para(cell, after_para_element, img_path, width=Inches(4.5)):
    """Add an image paragraph after the given paragraph element."""
    new_p = cell.add_paragraph()
    new_p.alignment = 1  # Center
    run = new_p.add_run()
    run.add_picture(img_path, width=width)
    # Move to correct position
    new_p_elem = new_p._element
    new_p_elem.getparent().remove(new_p_elem)
    after_para_element.addnext(new_p_elem)
    return new_p
```

### Step 6: Extract Images from PDF/PPT

```python
import pdfplumber
# For text extraction:
with pdfplumber.open('source.pdf') as pdf:
    for page in pdf.pages:
        text = page.extract_text()

# For PPT image extraction, use external tools or pre-extract
# The ppt_images/ directory pattern is common
```

## Critical Pitfalls

### P1: Chinese Font — eastAsia MUST Be 宋体
When modifying documents with Chinese text, the `w:rFonts` element must set `w:eastAsia` to `宋体`. A common bug is leaving it as `Times New Roman` or not setting it at all. Chinese characters will render incorrectly without this.

**Fix**: Always explicitly set eastAsia font:
```python
fonts.set(qn('w:eastAsia'), '宋体')
```

### P2: Line Spacing — Must Set on Every New Paragraph
New paragraphs added via `cell.add_paragraph()` default to `None` line spacing, not inheriting from the document style. For Chinese academic documents, 1.5x line spacing is standard.

**Fix**: Always set `p.paragraph_format.line_spacing = 1.5` on new paragraphs.

### P3: Image Insertion Order — Caption After Image
When inserting an image + caption pair, the insertion order matters because `addnext()` pushes content down. Insert the caption FIRST, then the image before it:
```python
# Wrong: image first, then caption → caption appears ABOVE image
# Right: caption first, then image before caption
caption_p = add_caption_after_para(cell, target._element, '图 X 标题')
add_image_after_para(cell, target._element, img_path)
```

### P4: Paragraph Index Shift After XML Manipulation
After inserting new paragraphs via XML manipulation (`addprevious`/`addnext`), the paragraph indices change. Always re-read the cell content after modifications:
```python
# Don't cache paragraph indices across insertions
cell3 = table.rows[3].cells[0]  # Re-read after each insertion batch
```

### P5: Clearing Cell Content
To completely rewrite a table cell's content:
```python
from docx.oxml.ns import qn
body = cell._element
for p in list(body.findall(qn('w:p'))):
    body.remove(p)
for t in list(body.findall(qn('w:tbl'))):
    body.remove(t)
```

### P6: Windows File Write Verification
On Windows (especially with WSL relay), always verify file writes with an independent check. Don't trust tool return values alone — re-read the file to confirm.

## Chinese Academic Document Standards

- **Title font**: 黑体 小三 (Heiti, ~15pt)
- **Body font**: 宋体 小四 (SimSun, 12pt)
- **Line spacing**: 1.5x
- **Reference font**: 宋体 五号 (10.5pt)
- **Figure captions**: Centered, 宋体 五号
- **English/numbers in Chinese text**: Times New Roman (set via ascii/hAnsi)

## PDF Content Extraction

```python
import pdfplumber

# Text extraction
with pdfplumber.open('source.pdf') as pdf:
    for i, page in enumerate(pdf.pages):
        text = page.extract_text()
        print(f"Page {i+1}: {text[:500]}")

# Check available attributes
with pdfplumber.open('source.pdf') as pdf:
    page = pdf.pages[0]
    print(f"Tables: {len(page.extract_tables())}")
    print(f"Images: {len(page.images)}")
```

## Verification Pattern

After modifying a document, always verify:
1. Structure matches template (same rows/columns)
2. Content covers all requirements
3. Images are actually embedded (check for `a:blip` elements)
4. Font formatting is correct (eastAsia = 宋体)
5. Line spacing is set on all paragraphs

```python
# Verify images
for pi, p in enumerate(cell.paragraphs):
    blips = p._element.findall('.//' + qn('a:blip'))
    if blips:
        print(f"  [{pi}] Has image: {blips[0].get(qn('r:embed'))}")

# Verify font
for f in p.runs[0]._element.find(qn('w:rPr')).findall(qn('w:rFonts')):
    assert f.get(qn('w:eastAsia')) == '宋体'
```
