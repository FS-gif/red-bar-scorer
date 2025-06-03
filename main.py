import streamlit as st
import cv2
import numpy as np
from PIL import Image

st.title("Red Bar Scorer v9")

uploaded_file = st.file_uploader("画像をアップロード", type=["png", "jpg", "jpeg"])
if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    img_array = np.array(image)

    st.image(image, caption="元画像", use_container_width=True)

    r_thresh = st.slider("R 最小値", 0, 255, 150)
    g_thresh = st.slider("G 最大値", 0, 255, 80)
    b_thresh = st.slider("B 最大値", 0, 255, 80)

    mask = (img_array[:, :, 0] >= r_thresh) & \
           (img_array[:, :, 1] <= g_thresh) & \
           (img_array[:, :, 2] <= b_thresh)

    output = np.zeros_like(img_array)
    output[mask] = img_array[mask]

    gray = cv2.cvtColor(output, cv2.COLOR_RGB2GRAY)
    contours, _ = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    bar_info = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if w > 10 and h > 5:
            bar_info.append((y, w))

    bar_info = sorted(bar_info, key=lambda x: x[0])
    widths = [w for (_, w) in bar_info]

    scores = []
    if widths:
        q3 = np.percentile(widths, 75)
        for w in widths:
            if w >= q3:
                scores.append(3.0)
            elif w >= q3 * 0.85:
                scores.append(2.5)
            elif w >= q3 * 0.7:
                scores.append(2.0)
            elif w >= q3 * 0.55:
                scores.append(1.5)
            elif w >= q3 * 0.4:
                scores.append(1.0)
            elif w >= q3 * 0.25:
                scores.append(0.5)
            else:
                scores.append(0.0)

    st.subheader("スコア一覧")
    for i, (y, w) in enumerate(bar_info):
        st.write(f"{i+1}列目: 横幅 = {w}px → スコア = {scores[i]:.1f}")

    bar_img = np.zeros_like(img_array)
    bar_img[mask] = img_array[mask]
    st.image(bar_img, caption="検出された赤バー部分", use_container_width=True)
