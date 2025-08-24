# core/audio.py
import io
import os
import tempfile
import numpy as np
import librosa
import soundfile as sf  # 确保 requirements 里有 soundfile

def _ext_from_name(name: str) -> str:
    if not name:
        return ""
    i = name.rfind(".")
    return name[i:] if i != -1 else ""

def load_audio(file_like):
    """
    稳定读取音频为单声道 float32，保持原采样率。
    支持：Streamlit UploadedFile / BytesIO / bytes / 路径字符串。
    返回: (y: np.ndarray[float32], sr: int, duration_s: float)
    """
    # 直接是路径字符串的情况
    if isinstance(file_like, (str, os.PathLike)):
        y, sr = librosa.load(str(file_like), sr=None, mono=True)
        y = y.astype(np.float32)
        return y, sr, len(y) / sr

    # 统一拿到字节与原始文件名（若有）
    name = getattr(file_like, "name", None)
    if hasattr(file_like, "read"):
        data = file_like.read()
    elif isinstance(file_like, (bytes, bytearray)):
        data = bytes(file_like)
    else:
        # 其它类文件对象
        data = file_like.read()

    # 1) 尝试：用 soundfile 直接从内存解码（适合 WAV/FLAC/OGG）
    try:
        with sf.SoundFile(io.BytesIO(data)) as s:
            # 总是读为 float32
            audio = s.read(always_2d=False, dtype="float32")
            sr = s.samplerate
        y = np.asarray(audio, dtype=np.float32)
        if y.ndim > 1:
            y = np.mean(y, axis=1)  # 转单声道
        return y, sr, len(y) / sr
    except Exception:
        pass  # 继续走临时文件方案（适合 MP3/M4A 等）

    # 2) 兜底：写入临时文件，再用 librosa/audioread 解码（mp3/m4a 更稳）
    suffix = _ext_from_name(name) or ".bin"
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
        tmp.write(data)
        tmp_path = tmp.name
    try:
        y, sr = librosa.load(tmp_path, sr=None, mono=True)
        y = y.astype(np.float32)
        return y, sr, len(y) / sr
    finally:
        try:
            os.remove(tmp_path)
        except Exception:
            pass

def clean_silence(y: np.ndarray, threshold: float) -> np.ndarray:
    """
    移除 |sample| < threshold 的样本（头尾/中段都清理）。
    若全部被清除则返回原始 y（避免空数组）。
    """
    mask = np.abs(y) >= threshold
    return y if not np.any(mask) else y[mask]
