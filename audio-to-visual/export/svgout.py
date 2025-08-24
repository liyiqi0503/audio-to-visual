# export/svgout.py
from datetime import datetime
import streamlit as st

def do_export(svg_bytes: bytes, pattern: str) -> None:
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    fname = f"voice-visual-{pattern}-{ts}.svg"
    st.download_button("点击下载 SVG", data=svg_bytes, file_name=fname, mime="image/svg+xml")
