
import streamlit as st
from PIL import Image
import numpy as np
from utils import extract_bar_widths, extract_names_with_ocr, score_from_widths

st.set_page_config(layout="wide")
st.title("赤バースコア判定ツール v11.2")

uploaded_file = st.file_uploader("画像をアップロード", type=["png", "jpg", "jpeg"])
if uploaded_file:
    image_bytes = uploaded_file.read()
    widths, bar_image, coords = extract_bar_widths(image_bytes)
    names = extract_names_with_ocr(image_bytes, coords)
    scores = score_from_widths(widths)

    # 表示と編集
    data = {"名前": names, "バー幅": widths, "スコア": scores}
    edited = st.data_editor(data, num_rows="dynamic")

    # コピーボタン用出力
    if edited is not None:
        score_text = "\n".join([str(v) for v in edited['スコア']])
        st.code(score_text, language="text")

    # bar_imageがndarrayならPILに変換
    if isinstance(bar_image, np.ndarray):
        bar_image = Image.fromarray(bar_image)

    # 検出画像表示
    st.image(bar_image, caption="検出されたバー", use_container_width=True)
