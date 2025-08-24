# core/utils.py
import svgwrite

def clamp(v, lo, hi):
    return max(lo, min(hi, v))

def mm_to_px(mm: float) -> float:
    # SVG 1mm ≈ 3.543307 px
    return mm * 3.543307

def svg_canvas(width: int, height: int) -> svgwrite.Drawing:
    # 不再使用 profile="tiny"，避免 <style> 受限
    dwg = svgwrite.Drawing(size=(f"{width}px", f"{height}px"))
    # 这些属性在 full profile 下可用
    dwg.attribs["shape-rendering"] = "geometricPrecision"
    dwg.attribs["stroke-linecap"] = "round"
    dwg.attribs["stroke-linejoin"] = "round"
    # ❌ 不再往 defs 里添加 <style>，统一改为显式 stroke/fill
    return dwg
