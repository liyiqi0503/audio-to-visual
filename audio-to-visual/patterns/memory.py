# patterns/memory.py —— 强制 float + 合法性校验 + path 兜底圆
import numpy as np
import svgwrite
from core.envelope import resample_envelope
from core.utils import svg_canvas, mm_to_px

DEFAULTS = {
    "particles": 150, "layers": 5,
    "center_offset_amp_px": 30, "max_diameter_mm": 1.2
}

def _safe_circle(dwg, x, y, r, fill="#000"):
    """优先用 <circle>；出错则用两段 A 圆弧 path 兜底"""
    x = float(x); y = float(y); r = float(r)
    if not np.isfinite(x) or not np.isfinite(y) or not np.isfinite(r) or r <= 0.0:
        return None
    try:
        return svgwrite.shapes.Circle(center=(x, y), r=r, fill=fill, stroke="none")
    except Exception:
        d = (
            f"M {x + r:.3f},{y:.3f} "
            f"A {r:.3f},{r:.3f} 0 1 0 {x - r:.3f},{y:.3f} "
            f"A {r:.3f},{r:.3f} 0 1 0 {x + r:.3f},{y:.3f} Z"
        )
        return dwg.path(d=d, fill=fill, stroke="none")

def draw(env, *, width, height, margin_x, margin_y, stroke_width,
         particles, layers, center_offset_amp_px, max_diameter_mm) -> svgwrite.Drawing:
    particles = int(max(2, particles))
    env = resample_envelope(env, particles)

    # 防 NaN/Inf，全部转为有限数
    if np.any(~np.isfinite(env)):
        env = np.nan_to_num(env, nan=0.0, posinf=1.0, neginf=0.0)

    W, H = int(width), int(height)
    avail_w = max(1.0, W - 2 * float(margin_x))
    cy = float(H) / 2.0
    xs = [float(margin_x) + (i / max(1, particles - 1)) * avail_w for i in range(particles)]
    max_diam_px = float(mm_to_px(float(max_diameter_mm)))
    base_step = max(4.0, max_diam_px * 0.6)

    dwg = svg_canvas(W, H)

    for i, e in enumerate(env):
        e = float(e)
        if not np.isfinite(e):
            e = 0.0
        x = float(xs[i])
        center_y = cy - e * float(center_offset_amp_px)

        # 层从中心向上/下扩散
        for L in range(-(layers - 1)//2, (layers // 2) + 1):
            y = center_y + float(L) * base_step
            # 按能量和层衰减直径
            scale_layer = max(0.2, 1.0 - abs(L) / max(1.0, float(layers)))
            d_px = max(0.5, min(
                max_diam_px,
                max_diam_px * (0.5 + 0.5 * max(0.0, e)) * scale_layer
            ))
            r = d_px / 2.0

            node = _safe_circle(dwg, x, y, r, fill="#000")
            if node is not None:
                dwg.add(node)

    return dwg
