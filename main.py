
import streamlit as st
import numpy as np
import cv2
from PIL import Image
from utils import extract_bar_widths, extract_names_with_ocr, score_from_widths

st.set_page_config(layout="wide")
st.title("赤バースコア判定ツール v9-RGB")

uploaded_file = st.file_uploader("画像をアップロード", type=["png", "jpg", "jpeg"])
if uploaded_file:
    image_bytes = uploaded_file.read()

    st.subheader("RGB色域指定")
    r_min = st.number_input("R最小", min_value=0, max_value=255, value=150)
    r_max = st.number_input("R最大", min_value=0, max_value=255, value=255)
    g_min = st.number_input("G最小", min_value=0, max_value=255, value=0)
    g_max = st.number_input("G最大", min_value=0, max_value=255, value=80)
    b_min = st.number_input("B最小", min_value=0, max_value=255, value=0)
    b_max = st.number_input("B最大", min_value=0, max_value=255, value=80)

    rgb_range = ((r_min, g_min, b_min), (r_max, g_max, b_max))

    widths, bar_image, coords = extract_bar_widths(image_bytes, rgb_range)
    names = extract_names_with_ocr(image_bytes, coords)
    scores = score_from_widths(widths)

    data = {"名前": names, "バー幅": widths, "スコア": scores}
    edited = st.data_editor(data, num_rows="dynamic")

    if edited is not None:
        score_text = "\n".join([str(v) for v in edited["スコア"]])
        st.code(score_text, language="text")

    st.image(bar_image, caption="検出されたバー", use_container_width=True)
