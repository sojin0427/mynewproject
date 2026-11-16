import cv2
import mediapipe as mp

# MediaPipe Hands 모듈 초기화 (mediapipe==0.10.14 버전 필요)
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# 웹캠 설정 (0번 카메라)
cap = cv2.VideoCapture(0)

# Hands 객체 생성
with mp_hands.Hands(
    max_num_hands=2,            # 동시에 인식할 최대 손 개수
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
) as hands:

    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("웹캠을 찾을 수 없습니다.")
            break

        # 거울 모드처럼 보기 편하도록 화면을 좌우 반전합니다.
        image = cv2.flip(image, 1)

        # MediaPipe는 RGB 이미지를 사용하므로 BGR에서 RGB로 변환합니다.
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # 손 인식 수행
        results = hands.process(image_rgb)

        # 인식된 손 정보가 있을 경우 처리
        if results.multi_hand_landmarks:
            for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                # MediaPipe가 판별한 손의 종류 (Left / Right)
                # 이미지를 좌우 반전(flip)했기 때문에 화면 기준 실제 사용자의 손 방향에 맞춰 텍스트를 매칭합니다.
                detected_label = handedness.classification.label
                
                if detected_label == "Right":
                    hand_text = "Left"
                else:
                    hand_text = "Right"

                # 1. 화면에 손 관절(Landmarks) 그리기
                mp_drawing.draw_landmarks(
                    image, hand_landmarks, mp_hands.HAND_CONNECTIONS
                )

                # 2. 우측 상단 코너에 텍스트 표시
                h, w, _ = image.shape
                text_position = (w - 150, 50)  # 우측 끝에서 150 픽셀 왼쪽, 상단에서 50 픽셀 아래
                
                cv2.putText(
                    image, 
                    hand_text, 
                    text_position, 
                    cv2.FONT_HERSHEY_SIMPLEX, 
                    1.5,          # 글자 크기
                    (0, 255, 0),  # 글자 색상 (초록색)
                    3,            # 글자 두께
                    cv2.LINE_AA
                )

        # 결과 화면 표시
        cv2.imshow('Hand Recognition', image)

        # 키 입력 대기 (Q, q, Esc 입력 시 종료)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or key == ord('Q') or key == 27:  # 27은 Esc 키의 아스키 코드
            break

# 자원 해제
cap.release()
cv2.destroyAllWindows()
