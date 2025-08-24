# app.py
import streamlit as st
from ui.sidebar import upload_audio, pick_style, common_params
from ui.preview import render_svg, show
from export.svgout import do_export

st.set_page_config(page_title="声纹图生成工具 v2.3", layout="wide")

# 如需完全规避 Markdown，可改用 st.components.v1.html 渲染标题
st.title("🎼 声纹图生成工具（Audio-to-Visual Engraving Tool）")
st.caption("将音频转化为可雕刻/印刷的 SVG 图案 · v2.3")

col_preview, col_ctrl = st.columns([7, 5], gap="large")

with col_ctrl:
    st.subheader("1) 音频上传（≤ 6 秒）")
    y, sr, duration = upload_audio()   # ✅ 新版：返回 3 个值

    st.subheader("2) 图案样式选择")
    pattern, spec = pick_style()

    st.subheader("3) 通用参数")
    common = common_params()

    st.subheader("5) 导出")
    export_clicked = st.button("导出 SVG")

with col_preview:
    st.subheader("图案实时预览")
    if y is None:
        st.info("请先上传不超过 6 秒的音频文件。")
        svg_bytes = None
    else:
        svg_str, svg_bytes = render_svg(y, sr, common, pattern, spec)
        show(svg_str, common["canvas_h"])

if export_clicked:
    if svg_bytes:
        do_export(svg_bytes, pattern)
    else:
        st.warning("暂无可导出的图案，请先上传音频并生成预览。")
