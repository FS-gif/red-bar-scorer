import streamlit as st
import numpy as np
import cv2
from PIL import Image

st.set_page_config(page_title="Red Bar Scorer", layout="centered")
st.title("赤バー スコア判定アプリ（スポイト選択対応）")
st.write("画像をアップロードして、赤バーの色をスポイトで指定してください。")

uploaded_file = st.file_uploader("画像をアップロード", type=["png", "jpg", "jpeg"])
if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    img_array = np.array(image)
    st.image(image, caption="アップロード画像", use_column_width=True)

    st.markdown("### スポイトで赤色を指定（画像をクリック）")
    click_info = st.experimental_data_editor({"click_x": 0, "click_y": 0}, num_rows="dynamic")

    if "click_x" in click_info and "click_y" in click_info:
        x, y = click_info["click_x"], click_info["click_y"]
        if 0 <= y < img_array.shape[0] and 0 <= x < img_array.shape[1]:
            selected_rgb = img_array[y, x]
            hsv_color = cv2.cvtColor(np.uint8([[selected_rgb]]), cv2.COLOR_RGB2HSV)[0][0]

            # 色域範囲を定義
            lower = np.array([max(hsv_color[0] - 10, 0), 70, 50])
            upper = np.array([min(hsv_color[0] + 10, 179), 255, 255])

            hsv = cv2.cvtColor(img_array, cv2.COLOR_RGB2HSV)
            mask = cv2.inRange(hsv, lower, upper)

            result = cv2.bitwise_and(img_array, img_array, mask=mask)
            st.image(result, caption="赤バー検出マスク", use_column_width=True)