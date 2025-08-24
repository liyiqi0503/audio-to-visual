# patterns/circular.py —— 强制 float + 失败时用 path 兜底
import math
import numpy as np
import svgwrite
from core.envelope import resample_envelope
from core.utils import clamp, svg_canvas

DEFAULTS = {
    "rays": 180,
    "head_tail_pct": 0,
    "min_height_ratio": 0.5,
    "center_offset_x": 0,
}

def _pt(p):
    """确保点坐标是纯 Python float"""
    return (float(p[0]), float(p[1]))

def _safe_line(grp, dwg, p1, p2, stroke_width):
    """优先用 <line>，若校验仍挑剔，则用 path 画等价直线"""
    x1, y1 = _pt(p1); x2, y2 = _pt(p2)
    try:
        grp.add(dwg.line(start=(x1, y1), end=(x2, y2)))
    except Exception:
        d = f"M {x1:.3f},{y1:.3f} L {x2:.3f},{y2:.3f}"
        grp.add(dwg.path(d=d, stroke="#000", fill="none", stroke_width=float(stroke_width)))

def draw(env, *, width, height, margin_x, margin_y, stroke_width,
         rays, head_tail_pct, min_height_ratio, center_offset_x) -> svgwrite.Drawing:
    rays = int(max(2, rays))
    env = resample_envelope(env, rays)
    # 防 NaN/Inf
    if np.any(np.isnan(env)) or np.any(~np.isfinite(env)):
        env = np.nan_to_num(env, nan=0.0, posinf=1.0, neginf=0.0)

    W, H = int(width), int(height)
    cx = float(W) / 2.0 + float(center_offset_x)
    cy = float(H) / 2.0
    # 以短边为准的半径
    R = max(1.0, min(W - 2 * margin_x, H - 2 * margin_y) * 0.48)
    Lmax = R * 0.9
    fade_n = int(rays * max(0.0, head_tail_pct) / 100.0)

    dwg = svg_canvas(W, H)
    grp = dwg.g(stroke="#000", fill="none", stroke_width=float(stroke_width))

    def pol2cart(r, th):
        return (cx + r * math.cos(th), cy + r * math.sin(th))

    for i, e in enumerate(env):
        th = (i / rays) * 2.0 * math.pi

        # 头尾渐隐
        fade_factor = 1.0
        if fade_n > 0:
            if i < fade_n:
                fade_factor = i / fade_n
            elif i >= rays - fade_n:
                fade_factor = (rays - 1 - i) / fade_n
            fade_factor = clamp(float(fade_factor), 0.0, 1.0)

        seg_len = max(float(min_height_ratio) * Lmax, float(e) * Lmax) * fade_factor

        # 中断间隙（映射 RMS 反比，能量低时中断更明显）
        gap_ratio = clamp((1.0 - float(e)) * 0.3, 0.0, 0.3)
        gap_start = 0.5 - gap_ratio / 2.0
        gap_end   = 0.5 + gap_ratio / 2.0

        r0 = R - seg_len / 2.0
        r1 = R + seg_len / 2.0

        inner = pol2cart(r0, th)
        pre_gap = pol2cart(r0 + (r1 - r0) * gap_start, th)
        post_gap = pol2cart(r0 + (r1 - r0) * gap_end, th)
        outer = pol2cart(r1, th)

        if seg_len > 0:
            _safe_line(grp, dwg, inner, pre_gap, stroke_width)
            _safe_line(grp, dwg, post_gap, outer, stroke_width)

    dwg.add(grp)
    return dwg
