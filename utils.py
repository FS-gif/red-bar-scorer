import cv2
import numpy as np
import pytesseract
from PIL import Image
from io import BytesIO

def extract_bar_widths(image_bytes):
    image = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower = np.array([0, 100, 100])
    upper = np.array([10, 255, 255])
    mask = cv2.inRange(hsv, lower, upper)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    widths = []
    coords = []
    output = image.copy()
    for cnt in sorted(contours, key=lambda x: cv2.boundingRect(x)[1]):
        x, y, w, h = cv2.boundingRect(cnt)
        if w > 20 and h > 10:
            cv2.rectangle(output, (x, y), (x+w, y+h), (0, 255, 0), 2)
            widths.append(w)
            coords.append((x, y, w, h))

    _, buf = cv2.imencode(".png", output)
    return widths, buf.tobytes(), coords

def extract_names_with_ocr(image_bytes, coords):
    image = Image.open(BytesIO(image_bytes)).convert("RGB")
    names = []
    for x, y, w, h in coords:
        left = max(x - 180, 0)
        top = y
        region = image.crop((left, top, x - 5, top + h))
        text = pytesseract.image_to_string(region, lang="jpn").strip()
        names.append(text if text else "-")
    return names

def score_from_widths(widths):
    sorted_w = sorted(widths, reverse=True)
    if not sorted_w:
        return []
    max_w = sorted_w[0]
    thresholds = [max_w, max_w * 0.7, max_w * 0.6, max_w * 0.5, max_w * 0.4, max_w * 0.3]
    scores = []
    for w in widths:
        if w >= thresholds[0]:
            scores.append(3.0)
        elif w >= thresholds[1]:
            scores.append(2.5)
        elif w >= thresholds[2]:
            scores.append(2.0)
        elif w >= thresholds[3]:
            scores.append(1.5)
        elif w >= thresholds[4]:
            scores.append(1.0)
        else:
            scores.append(0.5)
    return scores