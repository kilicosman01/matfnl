import fitz, json, re

pdf = fitz.open(r'c:\Users\Osman Ali\OneDrive\Desktop\mat2final\Matematik II Dersi Alıştırma Soruları.pdf')

# Get full text with page info
full_text = ''
for i, page in enumerate(pdf):
    text = page.get_text()
    full_text += f'===PAGE {i+1}===\n' + text + '\n'

# Save full text
with open(r'c:\Users\Osman Ali\OneDrive\Desktop\mat2final\full_text.txt', 'w', encoding='utf-8') as f:
    f.write(full_text)

print("Full text saved.")
print("Total pages:", len(pdf))

# Print some sections around LİMİT
lines = full_text.split('\n')
for i, line in enumerate(lines):
    if any(x in line.upper() for x in ['LIM', 'SUREK', 'TÜREV', 'TUREV', 'INTEGRAL', 'NTEGRAL']):
        print(f'Line {i}: {repr(line)}')
