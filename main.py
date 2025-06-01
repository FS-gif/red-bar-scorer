import streamlit as st
import numpy as np
from PIL import Image

st.set_page_config(page_title="Red Bar Scorer", layout="centered")
st.title("赤バーのスコア判定アプリ")
st.write("画像をアップロードすると、赤バーの長さを検出して相対スコアを付けます。")

uploaded_file = st.file_uploader("画像をアップロード", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    img_array = np.array(image)

    # HSV変換
    hsv_image = np.array(image.convert("HSV"))

    # 赤色の範囲を手動指定（上下で調整可能）
    st.sidebar.subheader("赤色の検出範囲（HSV）")
    h_low = st.sidebar.slider("Hue Low", 0, 179, 0)
    h_high = st.sidebar.slider("Hue High", 0, 179, 10)
    s_low = st.sidebar.slider("Saturation Low", 0, 255, 100)
    s_high = st.sidebar.slider("Saturation High", 0, 255, 255)
    v_low = st.sidebar.slider("Value Low", 0, 255, 100)
    v_high = st.sidebar.slider("Value High", 0, 255, 255)

    # HSVマスク作成
    lower_bound = np.array([h_low, s_low, v_low])
    upper_bound = np.array([h_high, s_high, v_high])
    mask = np.all((hsv_image >= lower_bound) & (hsv_image <= upper_bound), axis=2)

    # 赤バーの長さを垂直方向に集計（各列ごとの合計）
    vertical_sums = np.sum(mask, axis=0)
    non_zero_columns = vertical_sums[vertical_sums > 0]
    scores = list(non_zero_columns)

    # スコアを四分位範囲に基づいて7段階評価（例：3→2.5→2→…）
    final_scores = []
    if scores:
        q1 = np.percentile(scores, 25)
        q2 = np.percentile(scores, 50)
        q3 = np.percentile(scores, 75)
        max_score = np.max(scores)
        for s in scores:
            if s >= max_score:
                final_scores.append(3.0)
            elif s >= q3:
                final_scores.append(2.5)
            elif s >= q2:
                final_scores.append(2.0)
            elif s >= q1:
                final_scores.append(1.5)
            else:
                final_scores.append(1.0)
        st.success("スコア付け完了！")
        st.write(f"スコア一覧（{len(final_scores)}本）：", final_scores)
    else:
        st.warning("赤バーが検出されませんでした。")

    st.image(image, caption="アップロード画像", use_column_width=True)
