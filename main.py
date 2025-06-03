import streamlit as st
import numpy as np
import cv2
from PIL import Image

st.set_page_config(page_title="Red Bar Scorer", layout="wide")
st.title("赤バー判定アプリ（RGB調整）")

uploaded_file = st.file_uploader("画像をアップロードしてください", type=["png", "jpg", "jpeg"])
if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    img_array = np.array(image)

    st.image(image, caption="アップロード画像", use_column_width=True)

    st.sidebar.header("赤バー検出のRGB範囲")
    r_min = st.sidebar.slider("R min", 0, 255, 150)
    r_max = st.sidebar.slider("R max", 0, 255, 255)
    g_min = st.sidebar.slider("G min", 0, 255, 0)
    g_max = st.sidebar.slider("G max", 0, 255, 100)
    b_min = st.sidebar.slider("B min", 0, 255, 0)
    b_max = st.sidebar.slider("B max", 0, 255, 100)

    lower = np.array([r_min, g_min, b_min])
    upper = np.array([r_max, g_max, b_max])
    mask = cv2.inRange(img_array, lower, upper)

    red_pixels = cv2.bitwise_and(img_array, img_array, mask=mask)

    st.image(red_pixels, caption="検出された赤バー", use_column_width=True)

    scores = []
    for y in range(mask.shape[0]):
        row = mask[y]
        if np.sum(row) > 0:
            score = np.count_nonzero(row)
            scores.append((y, round(score / mask.shape[1] * 3, 1)))

    with st.expander("スコア一覧（縦位置・スコア）"):
        for y, score in scores:
            st.write(f"[ {y} ] → {score}")
