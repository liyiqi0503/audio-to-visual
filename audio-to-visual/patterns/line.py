# patterns/line.py  —— 修复 svgwrite 对 numpy 标量的校验问题
import numpy as np
import svgwrite
from core.envelope import resample_envelope
from core.utils import svg_canvas

DEFAULTS = {"count": 150, "height_ratio_pct": 60, "min_height_px": 5}

def draw(env, *, width, height, margin_x, margin_y, stroke_width,
         count, height_ratio_pct, min_height_px) -> svgwrite.Drawing:
    count = int(max(2, count))
    env = resample_envelope(env, count)
    # 防 NaN（某些极端音频或阈值会产生 NaN）
    if np.any(np.isnan(env)):
        env = np.nan_to_num(env, nan=0.0, posinf=1.0, neginf=0.0)

    W, H = int(width), int(height)
    avail_w = max(1.0, W - 2 * margin_x)
    avail_h = max(1.0, H - 2 * margin_y)
    max_line_h = avail_h * (float(height_ratio_pct) / 100.0)
    cy = H / 2.0

    dwg = svg_canvas(W, H)
    grp = dwg.g(stroke="#000", fill="none", stroke_width=float(stroke_width))

    for i, e in enumerate(env):
        # 统一转纯 Python float，避免 numpy 标量触发 svgwrite 的 list 校验
        x = float(margin_x + (i / max(1, count - 1)) * avail_w)
        line_h = float(max(min_height_px, float(e) * max_line_h))
        y1 = float(cy - line_h / 2.0)
        y2 = float(cy + line_h / 2.0)

        try:
            grp.add(dwg.line(start=(x, y1), end=(x, y2)))
        except Exception:
            # 兼容兜底：某些环境下 validator 仍可能挑剔，用 path 绘制等价直线
            d = f"M {x:.3f},{y1:.3f} L {x:.3f},{y2:.3f}"
            grp.add(dwg.path(d=d, stroke="#000", fill="none", stroke_width=float(stroke_width)))

    dwg.add(grp)
    return dwg
