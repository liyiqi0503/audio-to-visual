# ui/preview.py
import streamlit as st
import numpy as np
from patterns import get_drawer
from core.envelope import rms_envelope
from core.audio import clean_silence

def render_svg(y, sr, common, pattern, spec):
    # 清洗静音 → RMS 包络
    y_clean = clean_silence(y, common["silence_th"])
    env = rms_envelope(y_clean, sr, common["rms_seg_ms"])
    if len(env) == 0:
        env = np.array([0.0], dtype=np.float32)

    # 调用对应样式绘制器
    drawer, _defaults = get_drawer(pattern)
    dwg = drawer(
        env,
        width=common["canvas_w"],
        height=common["canvas_h"],
        margin_x=common["margin_x"],
        margin_y=common["margin_y"],
        stroke_width=common["stroke_w"],
        **spec,
    )
    svg_str = dwg.tostring()
    svg_bytes = svg_str.encode("utf-8")
    return svg_str, svg_bytes

def show(svg_str: str, canvas_h: int):
    # 用 HTML 内嵌 SVG，避免 Markdown/GFM 正则兼容问题
    st.components.v1.html(
        f"""
        <div style="width:100%;overflow:auto;border:1px dashed #ccc;border-radius:8px;padding:8px;background:#fafafa">
          {svg_str}
        </div>
        """,
        height=canvas_h + 40,
        scrolling=True,
    )
