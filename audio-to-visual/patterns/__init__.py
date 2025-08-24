# patterns/__init__.py
from .line import draw as draw_line, DEFAULTS as LINE_DEFAULTS
from .wave import draw as draw_wave, DEFAULTS as WAVE_DEFAULTS
from .circular import draw as draw_circular, DEFAULTS as CIRC_DEFAULTS
from .diamond import draw as draw_diamond, DEFAULTS as DIAMOND_DEFAULTS
from .memory import draw as draw_memory, DEFAULTS as MEMORY_DEFAULTS

REGISTRY = {
    "line": (draw_line, LINE_DEFAULTS),
    "wave": (draw_wave, WAVE_DEFAULTS),
    "circular": (draw_circular, CIRC_DEFAULTS),
    "diamond": (draw_diamond, DIAMOND_DEFAULTS),
    "memory": (draw_memory, MEMORY_DEFAULTS),
}

def list_patterns():
    return list(REGISTRY.keys())

def get_drawer(name: str):
    """返回 (callable, defaults_dict)"""
    return REGISTRY[name]
