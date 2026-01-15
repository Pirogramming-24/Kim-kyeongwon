import mediapipe as mp
import math, time
import cv2 as cv
from mediapipe.tasks.python import vision
from mediapipe.tasks import python
from visualization import draw_manual, print_RSP_result

## 필요한 함수 작성
def calculate_distance(point1, point2):
    """두 랜드마크 사이의 거리 계산"""
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

def is_finger_extended(hand_landmarks, tip_index, pip_index):
    """손가락이 펴져있는지 판단"""
    tip_to_wrist = calculate_distance(hand_landmarks[tip_index], hand_landmarks[0])
    pip_to_wrist = calculate_distance(hand_landmarks[pip_index], hand_landmarks[0])
    return tip_to_wrist > pip_to_wrist

def classify_rps(detection_result):
    """가위바위보 판별: 0=Rock, 1=Paper, 2=Scissors"""
    if not detection_result or not detection_result.hand_landmarks:
        return None
    
    hand_landmarks = detection_result.hand_landmarks[0]
    
    # 검지(8,6), 중지(12,10), 약지(16,14), 소지(20,18)
    fingers = [(8, 6), (12, 10), (16, 14), (20, 18)]
    extended_count = sum(1 for tip, pip in fingers if is_finger_extended(hand_landmarks, tip, pip))
    
    if extended_count <= 1:
        return 0  # Rock
    elif extended_count == 2:
        return 2  # Scissors
    elif extended_count >= 4:
        return 1  # Paper
    return None

def process_frame(result, output_image, timestamp_ms):
    """콜백 함수"""
    global latest_result
    latest_result = result

latest_result = None

if __name__ == "__main__":
    # HandLandmarker 설정
    base_options = python.BaseOptions(model_asset_path='hand_landmarker.task')
    options = vision.HandLandmarkerOptions(
        base_options=base_options,
        running_mode=vision.RunningMode.LIVE_STREAM,
        num_hands=1,
        result_callback=process_frame
    )
    
    landmarker = vision.HandLandmarker.create_from_options(options)
    
    # 웹캠 초기화
    cap = cv.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    
    timestamp = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        frame = cv.flip(frame, 1)
        rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        
        timestamp += 1
        landmarker.detect_async(mp_image, timestamp)
        
        if latest_result:
            frame = draw_manual(frame, latest_result)
            rps_result = classify_rps(latest_result)
            frame = print_RSP_result(frame, rps_result)
        
        cv.imshow('Rock Paper Scissors', frame)
        
        if cv.waitKey(1) == ord('q'):
            break
    
    cap.release()
    cv.destroyAllWindows()
    landmarker.close()