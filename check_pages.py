import fitz
import base64
import os
import re

pdf = fitz.open(r'c:\Users\Osman Ali\OneDrive\Desktop\mat2final\Matematik II Dersi Alıştırma Soruları.pdf')

# Extract question numbers per page
def get_questions_on_page(page_idx):
    text = pdf[page_idx].get_text()
    nums = re.findall(r'^(\d+)\.$', text, re.MULTILINE)
    return [int(n) for n in nums]

# Pages for each section (0-indexed)
limit_pages = list(range(43, 49))   # pages 44-49
turev_pages = list(range(49, 61))   # pages 50-61
integral_pages = list(range(61, 67)) # pages 62-67

print("=== LİMİT VE SÜREKLİLİK ===")
for i in limit_pages:
    qs = get_questions_on_page(i)
    print(f"  Page {i+1}: Q{qs}")

print("\n=== TÜREV ===")
for i in turev_pages:
    qs = get_questions_on_page(i)
    print(f"  Page {i+1}: Q{qs}")

print("\n=== İNTEGRAL ALMA ===")
for i in integral_pages:
    qs = get_questions_on_page(i)
    print(f"  Page {i+1}: Q{qs}")
