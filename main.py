import streamlit as st
import numpy as np
from PIL import Image
import cv2

st.set_page_config(page_title="Red Bar Scorer", layout="wide")
st.title("赤バー解析＆スコア表示アプリ")

uploaded_file = st.file_uploader("画像をアップロード", type=["png", "jpg", "jpeg"])
if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    img_array = np.array(image)

    # RGBスライダー（minのみ）
    st.sidebar.subheader("赤バー検出のRGB範囲")
    r_min = st.sidebar.slider("R min", 0, 255, 200)
    g_min = st.sidebar.slider("G min", 0, 255, 0)
    b_min = st.sidebar.slider("B min", 0, 255, 0)

    # RGB上限固定（単純化）
    r_max, g_max, b_max = 255, 100, 100

    red_mask = (
        (img_array[:, :, 0] >= r_min) & (img_array[:, :, 0] <= r_max) &
        (img_array[:, :, 1] >= g_min) & (img_array[:, :, 1] <= g_max) &
        (img_array[:, :, 2] >= b_min) & (img_array[:, :, 2] <= b_max)
    )

    result_image = img_array.copy()
    result_image[red_mask] = [0, 0, 0]  # 赤バーを黒で可視化

    st.image(result_image, caption="検出された赤バー", use_column_width=True)

    # スコア計算（縦方向にスキャン）
    bar_positions = np.where(red_mask.any(axis=1))[0]
    unique_rows = np.unique(bar_positions)

    # 簡易スコア（赤ピクセルの横幅を基準に）
    scores = []
    for y in unique_rows:
        row = red_mask[y, :]
        width = np.sum(row)
        if width > 0:
            score = min(round(width / 50, 1), 3.0)  # 例：最大スコア3.0
            scores.append((y, score))

    with st.expander("スコア一覧（縦位置・スコア）"):
        for y, score in scores:
            st.write(f"[{y}] → {score}")
else:
    st.info("左に画像をアップロードしてください。")