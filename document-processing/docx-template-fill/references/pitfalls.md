---
description: "Common pitfalls and fixes from real docx manipulation sessions"
---

# Pitfall Reference

## Font Rendering Issues

### Symptom
Chinese characters render as tofu/boxes or wrong font in Word.

### Root Cause
`w:rFonts` element missing `w:eastAsia` attribute, or set to wrong value.

### Fix
```python
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

# For every run with Chinese text:
fonts = OxmlElement('w:rFonts')
fonts.set(qn('w:ascii'), 'Times New Roman')   # English chars
fonts.set(qn('w:hAnsi'), 'Times New Roman')   # High-ANSI
fonts.set(qn('w:eastAsia'), '宋体')            # Chinese chars ← CRITICAL
fonts.set(qn('w:hint'), 'eastAsia')            # Tell Word to use eastAsia
```

### Verification
```python
rpr = run._element.find(qn('w:rPr'))
for f in rpr.findall(qn('w:rFonts')):
    assert f.get(qn('w:eastAsia')) == '宋体', f"Got {f.get(qn('w:eastAsia'))}"
```

---

## Image Not Appearing After Insertion

### Symptom
`add_picture()` succeeds but image doesn't show in Word.

### Root Cause
Image paragraph inserted at wrong position (inside text flow, or wrong XML parent).

### Fix
Use the `addprevious`/`addnext` pattern on the XML element level:
```python
new_p = cell.add_paragraph()
run = new_p.add_run()
run.add_picture(img_path, width=width)
# Reposition
new_p_elem = new_p._element
new_p_elem.getparent().remove(new_p_elem)
target_element.addnext(new_p_elem)
```

---

## Line Spacing Defaults to Single

### Symptom
New paragraphs have single spacing instead of 1.5x.

### Root Cause
`cell.add_paragraph()` doesn't inherit document-level line spacing.

### Fix
```python
p = cell.add_paragraph()
p.paragraph_format.line_spacing = 1.5
```

---

## Paragraph Index Shift

### Symptom
After inserting images/captions, code references wrong paragraphs.

### Root Cause
Cached paragraph indices become stale after XML manipulation.

### Fix
Always re-read the cell after batch insertions:
```python
cell = table.rows[3].cells[0]  # Re-read fresh reference
```

---

## WSL File Write Failures

### Symptom
`write_file` tool reports success but file is empty or unchanged on disk.

### Root Cause
WSL relay issue on Windows hosts.

### Fix
Use `execute_code` with `open()` for direct writes, or verify with independent read-back.
