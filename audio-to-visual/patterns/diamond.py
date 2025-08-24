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
        h = float(max(0.0, e * Hmax))
        if h <= 0.0:
            continue

        # 外层半宽/半高（作为“等距内缩”的参照）
        a0 = float(w) / 2.0  # half width
        b0 = h / 2.0  # half height

        # 法向缩放系数的“像素→比例”换算（单位：1/px）
        # 注意：若外层极扁（a0 或 b0 很小）会放大系数；零值直接跳过。
        if a0 <= 1e-6 or b0 <= 1e-6:
            continue
        normal_scale = ((1.0 / a0) ** 2 + (1.0 / b0) ** 2) ** 0.5

        for L in range(int(layers)):
            # 以外层为参照，累计内缩 Δ = L * layer_spacing（保证层间距恒为 layer_spacing）
            s = 1.0 - float(L) * float(layer_spacing) * normal_scale
            if s <= 0.0:
                continue

            aL = a0 * s  # half width of layer L
            bL = b0 * s  # half height of layer L

            # 计算四个顶点（使用纯 float，避免 svgwrite 类型校验问题）
            p_top = (float(cx), float(cy) - bL)
            p_right = (float(cx) + aL, float(cy))
            p_bottom = (float(cx), float(cy) + bL)
            p_left = (float(cx) - aL, float(cy))

            d = (f"M {p_top[0]:.3f},{p_top[1]:.3f} "
                 f"L {p_right[0]:.3f},{p_right[1]:.3f} "
                 f"L {p_bottom[0]:.3f},{p_bottom[1]:.3f} "
                 f"L {p_left[0]:.3f},{p_left[1]:.3f} Z")
            grp.add(dwg.path(d=d, stroke="#000", fill="none", stroke_width=float(stroke_width)))

    dwg.add(grp)
    return dwg
