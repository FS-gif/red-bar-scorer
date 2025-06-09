
def extract_bar_widths(image_bytes):
    return [100, 80, 60], None, [(0, 0, 100, 20), (0, 30, 80, 20), (0, 60, 60, 20)]

def extract_names_with_ocr(image_bytes, coords):
    return ["名前A", "名前B", "名前C"]

def score_from_widths(widths):
    return [3.0, 2.0, 1.0]
