import os
import urllib.request
import cv2
import numpy as np
import streamlit as st
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

st.title("손 인식 앱 (Hand Recognition)")

# 1. 최신 MediaPipe용 손 인식 모델 파일 자동 다운로드
MODEL_PATH = "hand_landmarker.task"
if not os.path.exists(MODEL_PATH):
    url = "https://googleapis.com"
    urllib.request.urlretrieve(url, MODEL_PATH)

# 2. HandLandmarker 객체 초기화
base_options = python.BaseOptions(model_asset_path=MODEL_PATH)
options = vision.HandLandmarkerOptions(
    base_options=base_options,
    num_hands=2,
    min_hand_detection_confidence=0.5,
    min_tracking_confidence=0.5
)
detector = vision.HandLandmarker.create_from_options(options)

# 손가락 관절 연결선 정의
HAND_CONNECTIONS = [
    (0, 1), (1, 2), (2, 3), (3, 4),        # 엄지
    (0, 5), (5, 6), (6, 7), (7, 8),        # 검지
    (5, 9), (9, 10), (10, 11), (11, 12),   # 중지
    (9, 13), (13, 14), (14, 15), (15, 16), # 약지
    (13, 17), (17, 18), (18, 19), (19, 20),# 소지
    (0, 17)                                # 손바닥 외곽
]

# 3. Streamlit 웹캠 입력 위젯
img_file = st.camera_input("카메라로 손을 비추고 촬영 버튼을 누르세요")

if img_file is not None:
    # 업로드된 이미지를 OpenCV 형식으로 변환
    file_bytes = np.asarray(bytearray(img_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    # 거울 모드처럼 좌우 반전
    image = cv2.flip(image, 1)
    h, w, _ = image.shape

    # RGB 변환 및 MediaPipe 이미지 객체 생성
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image_rgb)

    # 손 인식 수행
    detection_result = detector.detect(mp_image)

    if detection_result.hand_landmarks:
        for idx, hand_landmarks in enumerate(detection_result.hand_landmarks):
            # 좌우 반전으로 인해 라벨 반전 매칭
            detected_label = detection_result.handedness[idx][0].category_name
            hand_text = "Left" if detected_label == "Right" else "Right"

            # 관절 좌표 픽셀 변환
            points = [(int(lm.x * w), int(lm.y * h)) for lm in hand_landmarks]

            # 관절 연결선 그리기
            for start_idx, end_idx in HAND_CONNECTIONS:
                cv2.line(image, points[start_idx], points[end_idx], (255, 255, 255), 2)

            # 관절 점 그리기
            for pt in points:
                cv2.circle(image, pt, 5, (0, 0, 255), -1)

            # 우측 상단 코너에 텍스트 표시 (여러 손일 경우 아래로 줄바꿈)
            text_position = (w - 150, 50 + (idx * 50))
            cv2.putText(
                image,
                hand_text,
                text_position,
                cv2.FONT_HERSHEY_SIMPLEX,
                1.5,
                (0, 255, 0),
                3,
                cv2.LINE_AA
            )
    else:
        st.warning("손이 인식되지 않았습니다. 손을 화면 중앙에 잘 보이게 다시 촬영해 주세요.")

    # 결과 이미지를 웹 화면에 출력 (BGR -> RGB 변환)
    st.image(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), caption="인식 결과", use_container_width=True)
