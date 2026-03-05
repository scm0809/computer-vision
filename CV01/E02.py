import cv2  # OpenCV 라이브러리 (영상 처리/이벤트 처리)
import numpy as np # 행렬 연산 라이브러리

# 1. 초기 설정 및 사진 불러오기
brush_size = 5          # 초기 붓 크기
color = (255, 0, 0)     # 기본 색상: 파란색
is_drawing = False      # 마우스 플래그

# [수정된 부분] 흰 도화지 대신 'soccer.jpg' 파일을 불러옵니다.
img = cv2.imread('soccer.jpg')

# 파일이 없는 경우를 대비한 예외 처리
if img is None:
    print("이미지를 불러올 수 없습니다. 파일명을 확인하세요!")
    exit()

# 2. 마우스 콜백 함수 정의
def mouse_event(event, x, y, flags, param):
    global is_drawing, color, brush_size

    # 좌클릭 시 파란색
    if event == cv2.EVENT_LBUTTONDOWN:   
        is_drawing = True
        color = (255, 0, 0) 
        cv2.circle(img, (x, y), brush_size, color, -1)

    # 우클릭 시 빨간색
    elif event == cv2.EVENT_RBUTTONDOWN: 
        is_drawing = True
        color = (0, 0, 255)
        cv2.circle(img, (x, y), brush_size, color, -1)

    # 드래그 시 연속 그리기
    elif event == cv2.EVENT_MOUSEMOVE:    
        if is_drawing:
            cv2.circle(img, (x, y), brush_size, color, -1)

    # 마우스 버튼을 떼면 중단
    elif event == cv2.EVENT_LBUTTONUP or event == cv2.EVENT_RBUTTONUP:
        is_drawing = False

# 3. 창 생성 및 이벤트 연결
cv2.namedWindow('Drawing on Image') 
cv2.setMouseCallback('Drawing on Image', mouse_event)

print("준비 완료! 사진 위에 그림을 그리세요.")
print("'+'는 크게, '-'는 작게, 'q'는 종료입니다.")

# 4. 메인 루프
while True:
    cv2.imshow('Drawing on Image', img) 
    
    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'): 
        break
    elif key == ord('+') or key == ord('='): 
        brush_size = min(15, brush_size + 1)
        print(f"현재 붓 크기: {brush_size}")
    elif key == ord('-') or key == ord('_'): 
        brush_size = max(1, brush_size - 1)
        print(f"현재 붓 크기: {brush_size}")

cv2.destroyAllWindows()