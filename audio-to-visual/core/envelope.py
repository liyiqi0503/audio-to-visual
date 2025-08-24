# core/envelope.py
import math
import numpy as np

def rms_envelope(y: np.ndarray, sr: int, segment_ms: float) -> np.ndarray:
    """按 segment_ms 分段计算 RMS，归一化到 0..1"""
    samples_per_seg = max(1, int(sr * segment_ms / 1000.0))
    n_segs = int(math.ceil(len(y) / samples_per_seg))
    if n_segs <= 0:
        return np.zeros(0, dtype=np.float32)

    out = []
    for i in range(n_segs):
        seg = y[i * samples_per_seg: (i + 1) * samples_per_seg]
        if len(seg) == 0:
            rms = 0.0
        else:
            rms = float(np.sqrt(np.mean(seg * seg)))
        out.append(rms)
    arr = np.array(out, dtype=np.float32)
    mx = float(np.max(arr)) if len(arr) else 0.0
    if mx > 0:
        arr = arr / mx
    return arr

def resample_envelope(env: np.ndarray, target_len: int) -> np.ndarray:
    """线性插值到指定长度"""
    if target_len <= 1:
        return np.array([float(np.mean(env)) if len(env) else 0.0], dtype=np.float32)
    if len(env) == 0:
        return np.zeros(target_len, dtype=np.float32)
    x_old = np.linspace(0, 1, num=len(env))
    x_new = np.linspace(0, 1, num=target_len)
    return np.interp(x_new, x_old, env).astype(np.float32)
