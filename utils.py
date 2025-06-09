
# これは仮のutils.pyです
def extract_bar_widths(image_bytes, rgb_range):
    return [100, 80, 60], None, [(0, 0), (0, 1), (0, 2)]

def extract_names_with_ocr(image_bytes, coords):
    return ["ルメール", "川田", "武"]

def score_from_widths(widths):
    return [3.0, 2.0, 1.5]
