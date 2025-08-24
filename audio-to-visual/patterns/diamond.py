# patterns/diamond.py
import svgwrite
from core.envelope import resample_envelope
from core.utils import svg_canvas

DEFAULTS = {
    "diamonds": 30, "height_ratio_pct": 50, "layers": 3,
    "layer_spacing": 1.0, "overlap_ratio": 0.3
}

def draw(env, *, width, height, margin_x, margin_y, stroke_width,
         diamonds, height_ratio_pct, layers, layer_spacing, overlap_ratio) -> svgwrite.Drawing:
    env = resample_envelope(env, diamonds)
    W, H = width, height
    avail_w = max(1.0, W - 2 * margin_x)
    avail_h = max(1.0, H - 2 * margin_y)
    cy = H / 2.0
    Hmax = avail_h * (height_ratio_pct / 100.0)

    denom = 1.0 + (diamonds - 1) * (1.0 - overlap_ratio)
    w = avail_w / max(1e-6, denom)
    dx = w * (1.0 - overlap_ratio)
    start_x = margin_x + w / 2.0

    dwg = svg_canvas(W, H)
    grp = dwg.g(stroke="#000", fill="none", stroke_width=stroke_width)

    for i, e in enumerate(env):
        cx = start_x + i * dx
        h = e * Hmax
        for L in range(layers):
            shrink = L * layer_spacing
            hh = max(0.0, h - shrink)
            ww = max(0.0, w - 2 * shrink)
            if hh <= 0 or ww <= 0:
                continue
            p_top = (cx, cy - hh / 2.0)
            p_right = (cx + ww / 2.0, cy)
            p_bottom = (cx, cy + hh / 2.0)
            p_left = (cx - ww / 2.0, cy)
            d = f"M {p_top[0]:.3f},{p_top[1]:.3f} L {p_right[0]:.3f},{p_right[1]:.3f} L {p_bottom[0]:.3f},{p_bottom[1]:.3f} L {p_left[0]:.3f},{p_left[1]:.3f} Z"
            grp.add(dwg.path(d=d))
    dwg.add(grp)
    return dwg
