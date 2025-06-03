import streamlit as st
import numpy as np
import cv2
from PIL import Image

st.set_page_config(page_title="Red Bar Scorer", layout="centered")

st.title("赤バースコア判定アプリ")
st.write("画像をアップロードして、赤バーの長さを測定しスコアを算出します。")

uploaded_file = st.file_uploader("画像をアップロード", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    img_array = np.array(image)

    st.image(image, caption="アップロード画像", use_column_width=True)

    st.write("バーの基準となる色を画像上からクリックして選択してください：")
    clicked = st.image(img_array, caption="画像クリックで色取得", use_column_width=True)

    st.write("スコア一覧（縦位置・スコア）")

    # ※クリック検出は現状Streamlitの制約で開発中です。仮の赤色範囲を指定
    # RGB範囲を指定（仮の赤色マスク） - 通常はユーザー選択色に基づいて調整
    lower_rgb = np.array([200, 50, 50])
    upper_rgb = np.array([255, 120, 120])

    red_mask = cv2.inRange(img_array, lower_rgb, upper_rgb)

    bar_scores = {}
    for y in range(red_mask.shape[0]):
        row = red_mask[y]
        bar_length = np.sum(row > 0)
        if bar_length > 0:
            bar_scores[y] = round(3.0 * bar_length / red_mask.shape[1], 1)

    for y in sorted(bar_scores.keys()):
        st.markdown(f"- `{y: >3}` px → スコア: **{bar_scores[y]}**")
