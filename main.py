import streamlit as st
import numpy as np
import pandas as pd
import cv2
from PIL import Image
from io import BytesIO

st.set_page_config(page_title="Red Bar Scorer", layout="centered")
st.title("赤バーのスコア判定アプリ")
st.write("赤バーの長さを検出し、スコアを算出します。")

# HSVしきい値指定スライダー
st.sidebar.title("赤色検出の色域設定 (HSV)")
h_min = st.sidebar.slider("H: min", 0, 179, 0)
h_max = st.sidebar.slider("H: max", 0, 179, 10)
s_min = st.sidebar.slider("S: min", 0, 255, 100)
s_max = st.sidebar.slider("S: max", 0, 255, 255)
v_min = st.sidebar.slider("V: min", 0, 255, 100)
v_max = st.sidebar.slider("V: max", 0, 255, 255)

uploaded_file = st.file_uploader("画像をアップロードしてください（PNG/JPG）", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    img_array = np.array(image)
    hsv = cv2.cvtColor(img_array, cv2.COLOR_RGB2HSV)

    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])
    mask = cv2.inRange(hsv, lower, upper)

    # 検出領域ごとのバー長（横幅）を抽出
    height, width = mask.shape
    bar_lengths = []

    # 各行について赤ピクセルが存在する範囲を計測
    for row in mask:
        x_indices = np.where(row > 0)[0]
        if x_indices.size > 0:
            length = x_indices[-1] - x_indices[0]
            bar_lengths.append(length)

    if bar_lengths:
        # スコアリング処理（最大7段階）
        sorted_lengths = sorted(bar_lengths, reverse=True)
        thresholds = []

        if len(sorted_lengths) > 1:
            diffs = np.diff(sorted_lengths)
            for i, d in enumerate(diffs):
                if d > 1:
                    thresholds.append(i + 1)
        else:
            thresholds = [1]

        # 点数割り当て：上から3→2.5→2…0まで
        scores = []
        max_score = 3.0
        step = 0.5

        for i, val in enumerate(sorted_lengths):
            score = max(max_score - step * i, 0)
            scores.append(round(score, 2))

        # スコア表示
        df = pd.DataFrame({
            "バー番号": [f"{i+1}" for i in range(len(bar_lengths))],
            "バー長さ（px）": sorted_lengths,
            "スコア": scores
        })
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("赤バーが検出されませんでした。色域設定を見直してください。")

    # 画像とマスク表示
    st.image(image, caption="アップロード画像", use_column_width=True)
    st.image(mask, caption="検出マスク（赤領域）", use_column_width=True)
else:
    st.info("画像ファイルをアップロードしてください。")

