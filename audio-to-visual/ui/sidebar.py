# ui/sidebar.py
import streamlit as st
from core.audio import load_audio

def upload_audio():
    """
    渲染上传控件并读取音频。限制 ≤ 6 秒。
    返回: (y, sr, duration) 或 (None, None, None)
    """
    uploaded = st.file_uploader(
        "点击上传音频（支持 .wav/.mp3/.ogg/.flac/.m4a）",
        type=["wav", "mp3", "ogg", "flac", "m4a"]
    )
    if uploaded is None:
        return None, None, None
    try:
        y, sr, duration = load_audio(uploaded)
        if duration > 6.0:
            st.error("文件时长超出 6 秒限制，请更换文件。")
            return None, None, None
        st.success(f"上传成功：{uploaded.name}（{duration:.2f} 秒）")
        return y, sr, duration
    except Exception as e:
        st.error(f"上传失败：{e}")
        return None, None, None

def pick_style():
    label = st.selectbox(
        "请选择图案样式",
        options=[
            "Line（Signal Echo）",
            "Wave（Flowing Light）",
            "Circular（Fragment）",
            "Diamond（Resonant Core）",
            "Memory Dust（记忆尘）",
        ],
        index=0
    )
    if label.startswith("Line"):
        pattern = "line"
        spec = {
            "count": st.slider("线条数量（=RMS分段数）", 10, 300, 150, step=1),
            "height_ratio_pct": st.slider("高度比例(%)", 10, 100, 60, step=1),
            "min_height_px": st.slider("最小高度保底(px)", 0, 20, 5, step=1),
        }
    elif label.startswith("Wave"):
        pattern = "wave"
        spec = {
            "density": st.slider("波浪密度（=RMS分段数）", 10, 300, 150, step=1),
            "sharpness": st.slider("波浪锐度 (0=折线,1=圆润)", 0.0, 1.0, 0.6, step=0.1),
            "x_offset": st.slider("X 轴偏移量(px)", 0, 100, 30, step=1),
            "layers": st.slider("层数", 1, 10, 5, step=1),
            "layer_spacing": st.slider("层间距(px)", 0, 50, 20, step=1),
            "amp_px": st.slider("波浪高度倍率(px)", 10, 100, 50, step=1),
        }
    elif label.startswith("Circular"):
        pattern = "circular"
        spec = {
            "rays": st.slider("射线数量", 30, 360, 180, step=1),
            "head_tail_pct": st.slider("渐变头尾线占比(%)", 0, 20, 0, step=1),
            "min_height_ratio": st.slider("最小高度比例", 0.1, 1.0, 0.5, step=0.1),
            "center_offset_x": st.slider("圆心偏移(px)", -50, 50, 0, step=1),
        }
    elif label.startswith("Diamond"):
        pattern = "diamond"
        spec = {
            "diamonds": st.slider("菱形数量（=RMS分段数）", 10, 100, 30, step=1),
            "height_ratio_pct": st.slider("高度比例(%)", 10, 100, 50, step=1),
            "layers": st.slider("层数", 1, 6, 3, step=1),
            "layer_spacing": st.slider("层间距(px)", 0.0, 10.0, 1.0, step=0.5),
            "overlap_ratio": st.slider("横向重叠比(0..1)", 0.0, 1.0, 0.3, step=0.05),
        }
    else:
        pattern = "memory"
        spec = {
            "particles": st.slider("粒子数量（=RMS分段数）", 30, 300, 150, step=1),
            "layers": st.slider("层数（上下扩散）", 1, 10, 5, step=1),
            "center_offset_amp_px": st.slider("中心线偏移幅度(px)", 10, 80, 30, step=1),
            "max_diameter_mm": st.slider("最大粒子尺寸(直径, mm)", 0.5, 2.0, 1.2, step=0.1),
        }
    return pattern, spec

def common_params():
    c1, c2 = st.columns(2)
    with c1:
        canvas_w = st.number_input("画布宽度(px)", min_value=300, max_value=1200, value=800, step=10)
        margin_y = st.slider("垂直边距(px)", 0, 100, 40, step=1)
        stroke_w = st.slider("线条粗细(px)", 0.5, 10.0, 1.0, step=0.1)
        rms_seg_ms = st.slider("RMS 分段时长(ms)", 5, 50, 20, step=1)
    with c2:
        canvas_h = st.number_input("画布高度(px)", min_value=200, max_value=800, value=500, step=10)
        margin_x = st.slider("水平边距(px)", 0, 100, 40, step=1)
        silence_th = st.slider("静音阈值", 0.001, 0.1, 0.02, step=0.001)
    return {
        "canvas_w": int(canvas_w),
        "canvas_h": int(canvas_h),
        "margin_x": int(margin_x),
        "margin_y": int(margin_y),
        "stroke_w": float(stroke_w),
        "rms_seg_ms": int(rms_seg_ms),
        "silence_th": float(silence_th),
    }
