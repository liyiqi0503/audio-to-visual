# patterns/circular.py
import math
import svgwrite
from core.envelope import resample_envelope
from core.utils import clamp, svg_canvas

DEFAULTS = {
    "rays": 180, "head_tail_pct": 0, "min_height_ratio": 0.5, "center_offset_x": 0
}

def draw(env, *, width, height, margin_x, margin_y, stroke_width,
         rays, head_tail_pct, min_height_ratio, center_offset_x) -> svgwrite.Drawing:
    env = resample_envelope(env, rays)
    W, H = width, height
    cx = W / 2.0 + center_offset_x
    cy = H / 2.0
    R = max(1.0, min(W - 2 * margin_x, H - 2 * margin_y) * 0.48)
    Lmax = R * 0.9
    fade_n = int(rays * head_tail_pct / 100.0)

    dwg = svg_canvas(W, H)
    grp = dwg.g(stroke="#000", fill="none", stroke_width=stroke_width)

    def pol2cart(r, th):
        return cx + r * math.cos(th), cy + r * math.sin(th)

    for i, e in enumerate(env):
        th = (i / rays) * 2 * math.pi
        fade_factor = 1.0
        if fade_n > 0:
            if i < fade_n:
                fade_factor = i / fade_n
            elif i >= rays - fade_n:
                fade_factor = (rays - 1 - i) / fade_n
            fade_factor = clamp(fade_factor, 0.0, 1.0)

        seg_len = max(min_height_ratio * Lmax, e * Lmax) * fade_factor
        gap_ratio = clamp((1.0 - e) * 0.3, 0.0, 0.3)
        gap_start = 0.5 - gap_ratio / 2.0
        gap_end   = 0.5 + gap_ratio / 2.0
        r0 = R - seg_len / 2.0
        r1 = R + seg_len / 2.0

        inner = pol2cart(r0, th)
        pre_gap = pol2cart(r0 + (r1 - r0) * gap_start, th)
        post_gap = pol2cart(r0 + (r1 - r0) * gap_end, th)
        outer = pol2cart(r1, th)

        if seg_len > 0:
            grp.add(svgwrite.shapes.Line(inner, pre_gap))
            grp.add(svgwrite.shapes.Line(post_gap, outer))
    dwg.add(grp)
    return dwg
