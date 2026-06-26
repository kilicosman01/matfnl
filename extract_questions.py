import fitz
import base64
import os
import re
import json

pdf = fitz.open(r'c:\Users\Osman Ali\OneDrive\Desktop\mat2final\Matematik II Dersi Alıştırma Soruları.pdf')

def crop_question(page, rect, zoom=2.5):
    clip = fitz.Rect(rect)
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat, clip=clip)
    img_bytes = pix.tobytes("png")
    return base64.b64encode(img_bytes).decode('utf-8')

def extract_questions_from_page(page_idx, question_nums, padding=6, zoom=2.5):
    page = pdf[page_idx]
    W = page.rect.width
    H = page.rect.height

    # Get all words with positions
    words = page.get_text("words")

    # Find question number positions, skip header area (y < 110)
    q_positions = {}
    for w in words:
        x0, y0, x1, y1, text, *_ = w
        if re.match(r'^\d+\.$', text.strip()):
            num = int(text.strip()[:-1])
            if num in question_nums and y0 > 70:  # skip header area (headers at y~50)
                if num not in q_positions:
                    q_positions[num] = {'x': x0, 'y': y0, 'x1': x1, 'y1': y1}

    if not q_positions:
        print(f"  WARNING: No question positions on page {page_idx+1}")
        return {}

    # Use fixed page midpoint for column crop boundaries
    # (answer choices span full column width, so we must use page W/2)
    mid_x = W / 2

    # Classify left vs right by question number x position
    # Left questions typically at x~42, right at x~312 for 595px pages
    left_qs  = {n: p for n, p in q_positions.items() if p['x'] < mid_x}
    right_qs = {n: p for n, p in q_positions.items() if p['x'] >= mid_x}

    results = {}

    for col_qs, col_x_start, col_x_end in [
        (left_qs,  2,        mid_x + 2),   # left column: 0 to half-page
        (right_qs, mid_x - 2, W - 2)       # right column: half-page to edge
    ]:
        sorted_qs = sorted(col_qs.items(), key=lambda x: x[1]['y'])

        for i, (qnum, pos) in enumerate(sorted_qs):
            y_start = pos['y'] - padding

            if i + 1 < len(sorted_qs):
                y_end = sorted_qs[i + 1][1]['y'] - padding
            else:
                # Last question: go to near bottom of page
                y_end = H - 25

            # Clamp
            x_start = max(0, col_x_start)
            x_end = min(W, col_x_end)
            y_start = max(0, y_start)
            y_end = min(H, y_end)

            rect = (x_start, y_start, x_end, y_end)
            b64 = crop_question(page, rect, zoom=zoom)
            results[qnum] = b64

    return results

print("Extracting individual question images...")

sections = {
    'limit': [
        (43, [1,2,3,4,5,6,7,8,9,10,11]),
        (44, [12,13,14,15,16,17,18,19,20]),
        (45, [21,22,23,24,25,26,27,28,29,30]),
        (46, [31,32,33,34,35,36,37,38,39,40]),
        (47, [41,42,43,44,45,46,47]),
        (48, [48,49,50]),
    ],
    'turev': [
        (49, [1,2,3,4,5,6,7,8,9,10,11,12]),
        (50, [13,14,15,16,17,18,19,20,21,22,23]),
        (51, [24,25,26,27,28,29,30,31,32,33]),
        (52, [34,35,36,37,38,39,40,41,42,43,44,45]),
        (53, [46,47,48,49,50,51,52,53,54,55]),
        (54, [56,57,58,59,60,61,62,63,64,65,66,67,68]),
        (55, [69,70,71,72,73,74,75,76,77]),
        (56, [78,79,80,81,82,83,84]),
        (57, [85,86,87,88,89]),
        (58, [90,91,92,93,94,95]),
        (59, [96,97,98,99]),
        (60, [100]),
    ],
    'integral': [
        (61, [1,2,3,4,5,6,7,8,9,10]),
        (62, [11,12,13,14,15,16,17,18,19,20]),
        (63, [21,22,23,24,25,26,27,28,29,30]),
        (64, [31,32,33,34,35,36,37,38]),
        (65, [39,40,41,42,43,44,45,46,47,48]),
        (66, [49,50]),
    ],
}

all_questions = {}
for section, pages in sections.items():
    all_questions[section] = {}
    for page_idx, question_nums in pages:
        print(f"  Page {page_idx+1} ({section}): Q{question_nums}...")
        q_images = extract_questions_from_page(page_idx, question_nums)
        for qnum, img in q_images.items():
            all_questions[section][str(qnum)] = img
        missing = [q for q in question_nums if q not in q_images]
        if missing:
            print(f"    MISSING: {missing}")

out_path = r'c:\Users\Osman Ali\OneDrive\Desktop\mat2final\questions_data.json'
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(all_questions, f)

for section in ['limit', 'turev', 'integral']:
    expected = {'limit': 50, 'turev': 100, 'integral': 50}[section]
    got = len(all_questions[section])
    print(f"{section}: {got}/{expected}")

print("Done!")
