import streamlit as st
from PIL import Image
import numpy as np
import cv2

# ----------------------------
# ダミー関数（テスト用）
# ----------------------------
def extract_bar_widths(image_bytes):
    return [100, 80, 60], np.zeros((100, 300, 3), dtype=np.uint8), [(0, 0)]

def extract_names_with_ocr(image_bytes, coords):
    return ["騎手A", "騎手B", "騎手C"]

def score_from_widths(widths):
    return [3.0, 2.0, 1.5]

# ----------------------------
# Streamlit アプリ本体
# ----------------------------
st.set_page_config(layout="wide")
st.title("赤バースコア判定ツール vTEST")

uploaded_file = st.file_uploader("画像をアップロード", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image_bytes = uploaded_file.read()
    widths, bar_image, coords = extract_bar_widths(image_bytes)
    names = extract_names_with_ocr(image_bytes, coords)
    scores = score_from_widths(widths)

    data = {"名前": names, "バー幅": widths, "スコア": scores}
    edited = st.data_editor(data, num_rows="dynamic")

    score_text = "\n".join([str(v) for v in edited["スコア"]])
    st.code(score_text, language="text")

    # OpenCV→PIL変換
    if isinstance(bar_image, np.ndarray):
        bar_image = Image.fromarray(cv2.cvtColor(bar_image, cv2.COLOR_BGR2RGB))
    st.image(bar_image, caption="検出されたバー", use_container_width=True)

    # RGBスライダー
    st.markdown("### RGB色指定")
    r = st.number_input("R", 0, 255, 200)
    g = st.number_input("G", 0, 255, 0)
    b = st.number_input("B", 0, 255, 0)

    # スコアコピー用ボタン
    st.markdown("### スコアコピー用")
    st.download_button("スコアをコピー", score_text, file_name="scores.txt")
