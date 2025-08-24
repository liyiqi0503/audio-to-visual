# patterns/wave.py
import svgwrite
from core.envelope import resample_envelope
from core.utils import svg_canvas

DEFAULTS = {
    "density": 150, "sharpness": 0.6, "x_offset": 30,
    "layers": 5, "layer_spacing": 20, "amp_px": 50
}

def _bezier_path_from_points(points, smooth: float) -> str:
    if len(points) < 2:
        return ""
    if smooth <= 0:
        cmds = [f"M {points[0][0]:.3f},{points[0][1]:.3f}"]
        for x, y in points[1:]:
            cmds.append(f"L {x:.3f},{y:.3f}")
        return " ".join(cmds)
    s = smooth
    P = points
    path_cmds = [f"M {P[0][0]:.3f},{P[0][1]:.3f}"]
    for i in range(len(P) - 1):
        p0 = P[i - 1] if i - 1 >= 0 else P[i]
        p1 = P[i]
        p2 = P[i + 1]
        p3 = P[i + 2] if i + 2 < len(P) else P[i + 1]
        c1x = p1[0] + (p2[0] - p0[0]) * s / 6.0
        c1y = p1[1] + (p2[1] - p0[1]) * s / 6.0
        c2x = p2[0] - (p3[0] - p1[0]) * s / 6.0
        c2y = p2[1] - (p3[1] - p1[1]) * s / 6.0
        path_cmds.append(f"C {c1x:.3f},{c1y:.3f} {c2x:.3f},{c2y:.3f} {p2[0]:.3f},{p2[1]:.3f}")
    return " ".join(path_cmds)

def draw(env, *, width, height, margin_x, margin_y, stroke_width,
         density, sharpness, x_offset, layers, layer_spacing, amp_px) -> svgwrite.Drawing:
    env = resample_envelope(env, density)
    W, H = width, height
    avail_w = max(1.0, W - 2 * margin_x)
    cy = H / 2.0
    xs = [margin_x + (i / max(1, density - 1)) * avail_w for i in range(density)]

    dwg = svg_canvas(W, H)
    for L in range(layers):
        offset = ((-1)**L) * x_offset
        pts = []
        base_y_shift = (L - (layers - 1) / 2.0) * layer_spacing
        for i, e in enumerate(env):
            x = xs[i] + offset
            y = cy + base_y_shift - (e * amp_px)
            pts.append((x, y))
        d = _bezier_path_from_points(pts, smooth=sharpness)
        if d:
            # 显式设置描边/填充
            dwg.add(dwg.path(d=d, stroke="#000", fill="none", stroke_width=stroke_width))
    return dwg
