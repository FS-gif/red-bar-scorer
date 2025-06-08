# 仮のutils.py（本番ではv9ベースのutils.pyを上書き）
def extract_bar_widths(image_bytes):
    return [100, 80, 60], None, [(0, 0), (0, 0), (0, 0)]

def extract_names_with_ocr(image_bytes, coords):
    return ["川田将雅", "ルメール", "レーン"]

def score_from_widths(widths):
    return [3.0 if w >= 100 else 2.0 if w >= 80 else 1.0 for w in widths]
