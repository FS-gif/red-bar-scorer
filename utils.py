
import cv2
import numpy as np
from PIL import Image
import pytesseract
from io import BytesIO

def extract_bar_widths(image_bytes):
    image = Image.open(BytesIO(image_bytes)).convert("RGB")
    cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    hsv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)
    lower_red1 = np.array([0, 100, 100])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([160, 100, 100])
    upper_red2 = np.array([180, 255, 255])
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask = cv2.bitwise_or(mask1, mask2)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    bar_info = []
    coords = []

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if h > 10 and w > 10:
            bar_info.append((x, w))
            coords.append((x, y, w, h))

    bar_info.sort(key=lambda x: x[0])
    coords.sort(key=lambda c: c[0])

    for x, y, w, h in coords:
        cv2.rectangle(cv_image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    bar_image = Image.fromarray(cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB))
    widths = [w for _, w in bar_info]
    return widths, bar_image, coords

def extract_names_with_ocr(image_bytes, coords):
    image = Image.open(BytesIO(image_bytes)).convert("RGB")
    names = []
    for x, y, w, h in coords:
        left = max(x - 200, 0)
        crop = image.crop((left, y, x, y + h))
        name = pytesseract.image_to_string(crop, config="--psm 7", lang="jpn").strip()
        names.append(name if name else "不明")
    return names

def score_from_widths(widths):
    if not widths:
        return []

    sorted_widths = sorted(widths, reverse=True)
    unique_sorted = sorted(set(sorted_widths), reverse=True)

    def assign_score(w):
        rank = unique_sorted.index(w)
        score = 3.0 - 0.5 * round(rank)
        return max(score, 0.5)

    return [assign_score(w) for w in widths]
