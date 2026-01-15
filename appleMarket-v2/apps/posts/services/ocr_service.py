import numpy as np
import cv2
import threading

from paddleocr import PaddleOCR

# OCR 동시 실행 방지
_OCR_LOCK = threading.Lock()

_OCR = PaddleOCR(
    lang="korean",
    use_gpu=False,
    use_angle_cls=True,
    det_limit_side_len=1280,
    drop_score=0.2,
    show_log=False,
)


def preprocessimage(file_bytes: bytes) -> np.ndarray:
    """ 영양성분표(검은 배경, 흰 글자)에 특화된 전처리 """
    arr = np.frombuffer(file_bytes, np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("이미지 디코딩 실패")

    # webp / 메모리 primitive 안정화
    img = img.copy()
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    h, w = img.shape[:2]
    if h < 800 or w < 800:
        scale = max(800 / h, 800 / w)
        img = cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    denoised = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)

    clahe = cv2.createCLAHE(3.0, (8, 8))
    enhanced = clahe.apply(denoised)

    binary = cv2.adaptiveThreshold(
        enhanced, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        15, 10
    )

    if np.mean(binary) < 127:
        binary = cv2.bitwise_not(binary)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)

    return cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR)


def run_ocr(file_bytes: bytes) -> list[str]:
    """ OCR 결과를 줄 단위 리스트로 반환 """
    try:
        img = preprocessimage(file_bytes)

        with _OCR_LOCK:
            result = _OCR.ocr(img, cls=True)

        if not result or not result[0]:
            return []

        lines = []
        for _, (text, score) in result[0]:
            if score >= 0.3 and text.strip():
                lines.append(text.strip())

        return lines

    except Exception as e:
        print("OCR 실패:", e)
        return []
