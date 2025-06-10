from PIL import Image
import numpy as np
import io

def extract_bar_widths(image_bytes):
    image = Image.open(io.BytesIO(image_bytes))
    dummy_image = np.array(image)  # NumPy配列として返す
    return [100, 80, 60], dummy_image, [(0,0)]

def extract_names_with_ocr(image_bytes, coords):
    return ["騎手A", "騎手B", "騎手C"]

def score_from_widths(widths):
    return [3.0, 2.0, 1.5]
def extract_bar_widths(image_bytes):
    return [100, 80, 60], "dummy_image", [(0,0)]

def extract_names_with_ocr(image_bytes, coords):
    return ["騎手A", "騎手B", "騎手C"]

def score_from_widths(widths):
    return [3.0, 2.0, 1.5]
