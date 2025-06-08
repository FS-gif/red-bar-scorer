import streamlit as st
import numpy as np
from PIL import Image
import cv2
import io

st.set_page_config(layout="wide")
st.title("赤バースコアリング v9")

uploaded_file = st.file_uploader("画像をアップロードしてください", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    img_array = np.array(image)
    st.image(image, caption="アップロード画像", use_container_width=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        r_val = st.slider("R値", 0, 255, 200)
    with col2:
        g_val = st.slider("G値", 0, 255, 50)
    with col3:
        b_val = st.slider("B値", 0, 255, 50)

    tolerance = st.slider("許容差 (±)", 0, 50, 30)

    # 色検出（RGB範囲）
    lower = np.array([r_val - tolerance, g_val - tolerance, b_val - tolerance])
    upper = np.array([r_val + tolerance, g_val + tolerance, b_val + tolerance])
    mask = cv2.inRange(img_array, lower, upper)

    # 輪郭検出
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    bar_data = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if w > 20 and h > 10:  # 最小サイズでフィルタ
            bar_data.append((x, y, w, h))

    # スコア計算
    bar_data = sorted(bar_data, key=lambda b: b[0])  # x位置で左→右にソート
    widths = [b[2] for b in bar_data]
    scores = []
    if widths:
        max_w = max(widths)
        bins = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
        thresholds = np.quantile(widths, [0, 0.1, 0.3, 0.5, 0.7, 0.9])
        for w in widths:
            for i, th in enumerate(thresholds[::-1]):
                if w >= th:
                    scores.append(bins[::-1][i])
                    break
    else:
        st.warning("赤バーが検出できませんでした。")

    # 結果表示
    annotated = img_array.copy()
    result_text = ""
    for (x, y, w, h), score in zip(bar_data, scores):
        cv2.rectangle(annotated, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(annotated, f"{score:.1f}", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        result_text += f"{score:.1f}\n"

    st.image(annotated, caption="検出＆スコア表示", use_container_width=True)
    st.download_button("スコアをコピー形式でダウンロード", result_text, file_name="scores.txt")