import streamlit as st
import numpy as np
import cv2
from PIL import Image

st.set_page_config(page_title="Red Bar Scorer", layout="centered")

st.title("赤バースコア判定アプリ（スポイト対応版）")
st.write("画像をアップロードして、赤バーの長さを検出して相対スコアを算出します。")

uploaded_file = st.file_uploader("画像をアップロード", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    image_np = np.array(image)
    hsv = cv2.cvtColor(image_np, cv2.COLOR_RGB2HSV)

    st.image(image, caption="アップロード画像", use_column_width=True)

    click = st.image(image_np, caption="画像をタップして色を選択", use_column_width=True)
    st.write("※ 現在はスポイトは実装段階にあり、Streamlit上で画像タップは対応中です。")

    # 手動入力の代替スポイト（仮のHSV）
    h = st.slider("H (色相)", 0, 179, 0)
    s = st.slider("S (彩度)", 0, 255, 200)
    v = st.slider("V (明度)", 0, 255, 200)
    h_range = st.slider("H範囲", 0, 50, 10)
    s_range = st.slider("S範囲", 0, 127, 60)
    v_range = st.slider("V範囲", 0, 127, 60)

    lower_hsv = np.array([h - h_range, max(0, s - s_range), max(0, v - v_range)])
    upper_hsv = np.array([h + h_range, min(255, s + s_range), min(255, v + v_range)])

    mask = cv2.inRange(hsv, lower_hsv, upper_hsv)

    st.image(mask, caption="赤バー検出マスク", use_column_width=True)

    # 各行に対してバーの横幅をスキャン（1列ずつ）
    row_sums = []
    for i in range(mask.shape[0]):
        row = mask[i]
        count = 0
        max_count = 0
        for val in row:
            if val > 0:
                count += 1
                max_count = max(max_count, count)
            else:
                count = 0
        if max_count > 10:
            row_sums.append(max_count)

    if row_sums:
        max_len = max(row_sums)
        scores = [round((val / max_len) * 3, 1) for val in row_sums]
        for idx, score in enumerate(scores):
            st.write(f"{idx+1}位： スコア = {score}")
    else:
        st.warning("赤バーが検出されませんでした。HSVを調整してください。")
