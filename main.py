import streamlit as st
from utils import extract_bar_widths, extract_names_with_ocr, score_from_widths

st.set_page_config(layout="wide")
st.title("赤バースコア判定ツール v10")

uploaded_file = st.file_uploader("画像をアップロード", type=["png", "jpg", "jpeg"])
if uploaded_file:
    image_bytes = uploaded_file.read()
    widths, bar_image, coords = extract_bar_widths(image_bytes)
    names = extract_names_with_ocr(image_bytes, coords)
    scores = score_from_widths(widths)

    data = {"名前": names, "バー幅": widths, "スコア": scores}
    edited = st.data_editor(data, num_rows="dynamic")

    score_text = "\n".join([str(v) for v in edited['スコア']])
    st.code(score_text, language="text")

    st.image(bar_image, caption="検出されたバー", use_container_width=True)

    st.markdown("### RGB色指定")
    r = st.number_input("R", 0, 255, 200)
    g = st.number_input("G", 0, 255, 0)
    b = st.number_input("B", 0, 255, 0)

    st.markdown("### スコアコピー用")
    st.button("スコアをコピー")
