# patterns/memory.py
import svgwrite
from core.envelope import resample_envelope
from core.utils import svg_canvas, mm_to_px

DEFAULTS = {
    "particles": 150, "layers": 5,
    "center_offset_amp_px": 30, "max_diameter_mm": 1.2
}

def draw(env, *, width, height, margin_x, margin_y, stroke_width,
         particles, layers, center_offset_amp_px, max_diameter_mm) -> svgwrite.Drawing:
    env = resample_envelope(env, particles)
    W, H = width, height
    avail_w = max(1.0, W - 2 * margin_x)
    cy = H / 2.0
    xs = [margin_x + (i / max(1, particles - 1)) * avail_w for i in range(particles)]
    max_diam_px = mm_to_px(max_diameter_mm)

    dwg = svg_canvas(W, H)
    # 记忆尘是点阵，显式填充黑色、无描边
    for i, e in enumerate(env):
        x = xs[i]
        center_y = cy - e * center_offset_amp_px
        for L in range(-(layers - 1)//2, (layers // 2) + 1):
            y = center_y + L * (max(4.0, max_diam_px * 0.6))
            scale_layer = max(0.2, 1.0 - abs(L) / max(1.0, layers))
            d_px = max(0.5, min(max_diam_px, max_diam_px * (0.5 + 0.5 * e) * scale_layer))
            r = d_px / 2.0
            dwg.add(svgwrite.shapes.Circle(center=(x, y), r=r, fill="#000", stroke="none"))
    return dwg
