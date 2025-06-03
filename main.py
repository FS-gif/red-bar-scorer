import streamlit as st
import numpy as np
from PIL import Image
import cv2

st.set_page_config(page_title="Red Bar Scorer", layout="centered")
st.title("赤バー長さスコアリングアプリ")
st.write("画像をアップロードし、RGBしきい値を調整して赤バーのスコアを算出します。")

uploaded_file = st.file_uploader("画像をアップロード", type=["png", "jpg", "jpeg"])

r_thresh = st.slider("赤 R (min)", 0, 255, 200)
g_thresh = st.slider("緑 G (max)", 0, 255, 100)
b_thresh = st.slider("青 B (max)", 0, 255, 100)

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    img_array = np.array(image)
    st.image(image, caption="アップロード画像", use_column_width=True)

    red_mask = (img_array[:, :, 0] >= r_thresh) & (img_array[:, :, 1] <= g_thresh) & (img_array[:, :, 2] <= b_thresh)

    height, width = red_mask.shape
    scores = []

    for y in range(height):
        bar_length = np.sum(red_mask[y, :]) / width * 3  # 長さをスコア化（最大3）
        if bar_length > 0:
            scores.append((y, round(bar_length, 1)))

    with st.expander("スコア一覧（縦位置・スコア）"):
        for y, score in scores:
            st.write(f"[ {y} ] → {score}")
