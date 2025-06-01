import streamlit as st
import cv2
import numpy as np
from PIL import Image

st.set_page_config(layout="wide")
st.title("Red Bar Scorer - RGB Picker")

uploaded_file = st.file_uploader("画像をアップロードしてください", type=["png", "jpg", "jpeg"])
if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    image_np = np.array(image)
    st.image(image, caption="アップロード画像", use_container_width=True)

    st.subheader("RGB範囲の設定")
    r = st.slider("R", 0, 255, 200)
    g = st.slider("G", 0, 255, 0)
    b = st.slider("B", 0, 255, 0)
    tol = st.slider("許容誤差", 0, 100, 30)

    lower = np.clip([r - tol, g - tol, b - tol], 0, 255)
    upper = np.clip([r + tol, g + tol, b + tol], 0, 255)

    # マスク処理
    mask = cv2.inRange(image_np, np.array(lower), np.array(upper))
    result = cv2.bitwise_and(image_np, image_np, mask=mask)

    st.subheader("検出結果")
    st.image(result, caption="検出された赤バー", use_container_width=True)

    # 各行の赤バー幅（最大横幅）を計測
    gray = cv2.cvtColor(result, cv2.COLOR_RGB2GRAY)
    heights = []
    for y in range(gray.shape[0]):
        row = gray[y]
        indices = np.where(row > 0)[0]
        if len(indices) > 0:
            width = indices[-1] - indices[0]
            heights.append((y, width))
    if heights:
        # 上位スコア（最大3.0）
        max_width = max([w for y, w in heights])
        scored = [(y, round(3 * w / max_width, 1)) for y, w in heights]
        st.subheader("スコア一覧（縦位置・スコア）")
        st.write(scored)
    else:
        st.warning("赤バーが検出できませんでした")