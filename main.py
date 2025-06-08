
import streamlit as st
import cv2
import numpy as np
from PIL import Image
import pytesseract
import io
import pandas as pd

st.title("赤バー横幅スコアリング v11（名前OCR + スコア編集）")

uploaded_file = st.file_uploader("画像をアップロードしてください", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    img_array = np.array(image)

    st.image(image, caption="アップロードされた画像", use_container_width=True)

    lower_red = np.array([150, 0, 0])
    upper_red = np.array([255, 100, 100])

    mask = cv2.inRange(img_array, lower_red, upper_red)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    bar_info = []

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if w > 30 and h > 10:
            roi = img_array[y:y+h, x-150:x]  # バーの左側の名前部分
            roi_gray = cv2.cvtColor(roi, cv2.COLOR_RGB2GRAY)
            roi_pil = Image.fromarray(roi_gray)
            name = pytesseract.image_to_string(roi_pil, config='--psm 6').strip()

            bar_info.append({"名前": name, "横幅(px)": w})

    if bar_info:
        df = pd.DataFrame(bar_info)
        df["スコア"] = pd.cut(df["横幅(px)"],
                         bins=[0, 40, 60, 80, 100, 120, 160, np.inf],
                         labels=[0.5, 1.0, 1.5, 2.0, 2.5, 2.8, 3.0],
                         include_lowest=True).astype(float)

        df = st.data_editor(df, num_rows="dynamic", key="editable_scores")
        st.download_button("📋 スコアのみコピー（CSV）", df[["スコア"]].to_csv(index=False), "scores.csv", "text/csv")
    else:
        st.warning("赤バーが検出されませんでした。画像を確認してください。")
