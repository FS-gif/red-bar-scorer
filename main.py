
import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io

st.title("Red Bar Scorer")

uploaded_file = st.file_uploader("画像をアップロードしてください", type=["png", "jpg", "jpeg"])
if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    img_array = np.array(image)
    st.image(image, caption="アップロード画像", use_container_width=True)

    r_min = st.slider("R 最小", 0, 255, 150)
    r_max = st.slider("R 最大", 0, 255, 255)
    g_min = st.slider("G 最小", 0, 255, 0)
    g_max = st.slider("G 最大", 0, 255, 80)
    b_min = st.slider("B 最小", 0, 255, 0)
    b_max = st.slider("B 最大", 0, 255, 80)

    mask = cv2.inRange(img_array, (r_min, g_min, b_min), (r_max, g_max, b_max))
    result = cv2.bitwise_and(img_array, img_array, mask=mask)

    gray = cv2.cvtColor(result, cv2.COLOR_RGB2GRAY)
    contours, _ = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    widths = [cv2.boundingRect(cnt)[2] for cnt in contours if cv2.boundingRect(cnt)[2] > 30]
    widths.sort(reverse=True)

    scores = []
    for w in widths:
        if w >= 130:
            scores.append(3.0)
        elif w >= 100:
            scores.append(2.5)
        elif w >= 70:
            scores.append(2.0)
        elif w >= 60:
            scores.append(1.5)
        elif w >= 50:
            scores.append(1.0)
        else:
            scores.append(0.5)

    st.image(result, caption="検出された赤バー", use_container_width=True)

    if scores:
        st.subheader("スコア")
        for i, s in enumerate(scores):
            st.write(f"{i+1}列目: スコア = {s}")
        score_text = "\n".join([str(s) for s in scores])
        st.download_button("スコアをコピー用に保存", score_text, file_name="scores.txt")
