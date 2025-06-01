import streamlit as st
import numpy as np
import cv2
from PIL import Image

st.set_page_config(page_title="Red Bar Scorer v2", layout="centered")
st.title("赤バースコア判定アプリ v2")
st.write("画像をアップロードすると、赤バーの長さを検出してスコアを表示します。")

st.sidebar.header("赤バー検出 HSV設定")
h_min = st.sidebar.slider("H min", 0, 179, 0)
h_max = st.sidebar.slider("H max", 0, 179, 10)
s_min = st.sidebar.slider("S min", 0, 255, 100)
s_max = st.sidebar.slider("S max", 0, 255, 255)
v_min = st.sidebar.slider("V min", 0, 255, 100)
v_max = st.sidebar.slider("V max", 0, 255, 255)

uploaded_file = st.file_uploader("画像をアップロード", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    img_array = np.array(image)
    hsv = cv2.cvtColor(img_array, cv2.COLOR_RGB2HSV)

    lower_bound = np.array([h_min, s_min, v_min])
    upper_bound = np.array([h_max, s_max, v_max])
    mask = cv2.inRange(hsv, lower_bound, upper_bound)

    bar_lengths = []
    height, width = mask.shape
    bar_regions = np.array_split(mask, 8, axis=0)

    for region in bar_regions:
        bar_length = np.sum(np.any(region > 0, axis=0))
        bar_lengths.append(bar_length)

    # スコア算出
    if any(bar_lengths):
        sorted_lengths = sorted(bar_lengths, reverse=True)
        scores = []
        for length in bar_lengths:
            rank = sorted_lengths.index(length)
            score = max(3 - 0.5 * rank, 0)
            scores.append(score)

        st.subheader("スコア一覧")
        for i, score in enumerate(scores, 1):
            st.write(f"枠{i}：{score:.1f}")

        # マスク表示
        mask_rgb = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)
        combined = np.hstack((img_array, mask_rgb))
        st.image(combined, caption="アップロード画像（左）と検出結果（右）", use_column_width=True)
    else:
        st.warning("赤バーが検出されませんでした。HSV設定を調整してください。")
