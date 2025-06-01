import streamlit as st
import numpy as np
from PIL import Image

st.set_page_config(page_title="Red Bar Scorer", layout="centered")

st.title("赤バースコア判定アプリ（v4.2）")
st.write("画像をアップロードして、赤いバーの長さを検出しスコア化します。HSVスライダーで色調整可能です。")

uploaded_file = st.file_uploader("画像をアップロード（png/jpg/jpeg）", type=["png", "jpg", "jpeg"])

# HSV色域の指定
st.sidebar.title("色域調整（HSV）")
h_min = st.sidebar.slider("H min", 0, 179, 0)
h_max = st.sidebar.slider("H max", 0, 179, 10)
s_min = st.sidebar.slider("S min", 0, 255, 100)
s_max = st.sidebar.slider("S max", 0, 255, 255)
v_min = st.sidebar.slider("V min", 0, 255, 100)
v_max = st.sidebar.slider("V max", 0, 255, 255)

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    img_array = np.array(image)

    # RGB -> HSV
    hsv = np.zeros_like(img_array, dtype=np.uint8)
    for y in range(img_array.shape[0]):
        for x in range(img_array.shape[1]):
            r, g, b = img_array[y, x] / 255.0
            mx = max(r, g, b)
            mn = min(r, g, b)
            df = mx - mn
            h = s = v = 0
            if df == 0:
                h = 0
            elif mx == r:
                h = (60 * ((g - b) / df) + 360) % 360
            elif mx == g:
                h = (60 * ((b - r) / df) + 120) % 360
            elif mx == b:
                h = (60 * ((r - g) / df) + 240) % 360
            s = 0 if mx == 0 else (df / mx)
            v = mx
            hsv[y, x] = [int(h / 2), int(s * 255), int(v * 255)]

    # マスク作成
    h_mask = (hsv[:, :, 0] >= h_min) & (hsv[:, :, 0] <= h_max)
    s_mask = (hsv[:, :, 1] >= s_min) & (hsv[:, :, 1] <= s_max)
    v_mask = (hsv[:, :, 2] >= v_min) & (hsv[:, :, 2] <= v_max)
    mask = h_mask & s_mask & v_mask

    # 横方向に赤領域の幅をカウント
    bar_lengths = np.sum(mask, axis=1)
    average_length = np.mean(bar_lengths[bar_lengths > 0]) if np.any(bar_lengths > 0) else 0

    # スコア化（例：300px以上が満点3.0、50pxごとに0.5減点）
    if average_length >= 300:
        score = 3.0
    elif average_length >= 250:
        score = 2.5
    elif average_length >= 200:
        score = 2.0
    elif average_length >= 150:
        score = 1.5
    elif average_length >= 100:
        score = 1.0
    elif average_length >= 50:
        score = 0.5
    else:
        score = 0

    st.image(image, caption="アップロード画像", use_column_width=True)
    st.metric("赤バーの長さ平均", f"{average_length:.1f} px")
    st.metric("スコア", f"{score:.1f} 点")
