
import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io

st.title("Red Bar Scorer (RGB Based, Simplified)")

uploaded_file = st.file_uploader("画像をアップロードしてください", type=["png", "jpg", "jpeg"])
r_thresh = st.slider("Rしきい値", 0, 255, 150)
g_thresh = st.slider("Gしきい値", 0, 255, 100)
b_thresh = st.slider("Bしきい値", 0, 255, 100)

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    image_np = np.array(image)
    st.image(image, caption="アップロード画像", use_container_width=True)

    # 赤バー検出（閾値以下のRGBでマスク作成）
    lower_bound = np.array([r_thresh, g_thresh, b_thresh])
    upper_bound = np.array([255, 255, 255])
    mask = cv2.inRange(image_np, lower_bound, upper_bound)

    # 検出マスクと元画像合成（赤→緑表示）
    result_img = image_np.copy()
    result_img[mask > 0] = [0, 255, 0]
    st.image(result_img, caption="検出結果", use_container_width=True)

    # スコア計算（行ごとに赤バーの幅を評価）
    scores = []
    height, width, _ = image_np.shape
    for y in range(0, height, 40):  # 約40pxおきに縦走査
        line = mask[y:y+30, :]
        red_pixels = cv2.countNonZero(line)
        score = round(min(3.0, 3.0 * red_pixels / width / 30), 2)
        if red_pixels > 10:
            scores.append((y, score))

    if scores:
        st.subheader("スコア一覧")
        for y, score in scores:
            st.write(f"位置 {y}px → スコア: {score}")
    else:
        st.warning("有効な赤バーが見つかりませんでした。")
