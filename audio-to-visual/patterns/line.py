# patterns/line.py
import svgwrite
from core.envelope import resample_envelope
from core.utils import svg_canvas

DEFAULTS = {"count": 150, "height_ratio_pct": 60, "min_height_px": 5}

def draw(env, *, width, height, margin_x, margin_y, stroke_width,
         count, height_ratio_pct, min_height_px) -> svgwrite.Drawing:
    env = resample_envelope(env, count)
    W, H = width, height
    avail_w = max(1.0, W - 2 * margin_x)
    avail_h = max(1.0, H - 2 * margin_y)
    max_line_h = avail_h * (height_ratio_pct / 100.0)
    cy = H / 2.0

    dwg = svg_canvas(W, H)
    # 显式设置描边/填充
    grp = dwg.g(stroke="#000", fill="none", stroke_width=stroke_width)
    for i, e in enumerate(env):
        x = margin_x + (i / max(1, count - 1)) * avail_w
        line_h = max(min_height_px, e * max_line_h)
        y1 = cy - line_h / 2.0
        y2 = cy + line_h / 2.0
        grp.add(dwg.line(start=(x, y1), end=(x, y2)))
    dwg.add(grp)
    return dwg
