import cv2  # OpenCV 라이브러리 (영상 처리/이벤트 처리)
import numpy as np # 행렬 연산 라이브러리 (배경 도화지 생성용)

# 1. 초기 설정 및 요구사항 반영
brush_size = 5          # 초기 붓 크기를 5로 설정
color = (255, 0, 0)     # 기본 색상: 파란색 (BGR 순서: Blue=255)
is_drawing = False      # 마우스가 눌린 상태인지 확인하는 플래그

# 600x600 크기, 3채널(BGR)의 행렬을 생성하고 255를 곱해 흰색 배경 도화지 제작
img = np.ones((600, 600, 3), dtype=np.uint8) * 255

# 2. 마우스 콜백 함수 정의
# 이 함수는 마우스 동작이 감지될 때마다 OpenCV가 자동으로 호출.
def mouse_event(event, x, y, flags, param):
    global is_drawing, color, brush_size # 전역 변수를 함수 내에서 수정하기 위해 선언

    # 좌클릭 시 파란색으로 지정하고 원을 그림
    if event == cv2.EVENT_LBUTTONDOWN:   
        is_drawing = True                # 그리기 모드 시작
        color = (255, 0, 0)              # 색상을 파란색(BGR)으로 변경
        # cv2.circle(대상, 좌표, 반지름, 색상, -1은 채우기)
        cv2.circle(img, (x, y), brush_size, color, -1)

    # 우클릭 시 빨간색으로 지정하고 원을 그림
    elif event == cv2.EVENT_RBUTTONDOWN: 
        is_drawing = True                # 그리기 모드 시작
        color = (0, 0, 255)              # 색상을 빨간색(BGR)으로 변경
        cv2.circle(img, (x, y), brush_size, color, -1)

    # 드래그로 연속 그리기
    elif event == cv2.EVENT_MOUSEMOVE:    
        if is_drawing:                   # 버튼이 눌린 상태(is_drawing=True)일 때만 그림
            cv2.circle(img, (x, y), brush_size, color, -1)

    # 마우스 버튼을 떼면 그리기 중단
    elif event == cv2.EVENT_LBUTTONUP or event == cv2.EVENT_RBUTTONUP:
        is_drawing = False               # 그리기 모드 해제

# 3. 창 생성 및 이벤트 연결
cv2.namedWindow('Drawing Board')         # 이미지를 보여줄 창의 이름 설정
cv2.setMouseCallback('Drawing Board', mouse_event) # 해당 창에 마우스 함수 연결

print("준비 완료! '+'는 크게, '-'는 작게, 'q'는 종료입니다.")

# 4. 메인 루프 (화면 갱신 및 키보드 입력 처리)
while True:
    cv2.imshow('Drawing Board', img)     # 현재 도화지 상태를 화면에 표시
    
    # 1ms 동안 키보드 입력을 대기 (0xFF는 64비트 환경을 위한 마스킹)
    key = cv2.waitKey(1) & 0xFF

    # 'q' 키를 누르면 루프 종료 및 창 닫기
    if key == ord('q'): 
        break
        
    # '+' 또는 '=' 키를 누르면 붓 크기 증가 (최대 15로 제한)
    elif key == ord('+') or key == ord('='): 
        brush_size = min(15, brush_size + 1) # 15보다 커지지 않게 min 사용
        print(f"현재 붓 크기: {brush_size}")
        
    # '-' 또는 '_' 키를 누르면 붓 크기 감소 (최소 1로 제한)
    elif key == ord('-') or key == ord('_'): 
        brush_size = max(1, brush_size - 1)  # 1보다 작아지지 않게 max 사용
        print(f"현재 붓 크기: {brush_size}")

# 메모리 해제 및 모든 창 닫기
cv2.destroyAllWindows()