import streamlit as st
import numpy as np
from PIL import Image

st.set_page_config(page_title="Red Bar Scorer", layout="centered")
st.title("赤バースコア判定アプリ")
st.write("画像をアップロードすると、赤いバーの長さを検出して相対スコアを付けます。")

uploaded_file = st.file_uploader("画像をアップロード", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    img_array = np.array(image)
    red_mask = (img_array[:, :, 0] > 150) & (img_array[:, :, 1] < 100) & (img_array[:, :, 2] < 100)

    bar_lengths = []
    height, width = red_mask.shape
    bar_regions = np.array_split(red_mask, 8, axis=0)

    for region in bar_regions:
        bar_length = np.sum(np.any(region, axis=0))
        bar_lengths.append(bar_length)

    st.image(image, caption="アップロード画像", use_column_width=True)

    if any(bar_lengths):
        sorted_lengths = sorted(bar_lengths, reverse=True)
        scores = []
        for length in bar_lengths:
            rank = sorted_lengths.index(length)
            score = max(3 - 0.5 * rank, 0)
            scores.append(score)

        st.subheader("スコア一覧")
        for i, score in enumerate(scores, 1):
            st.write(f"枠{i}：{score}")
    else:
        st.warning("赤バーが検出されませんでした。画像を確認してください。")
