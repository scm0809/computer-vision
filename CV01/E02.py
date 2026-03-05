import cv2  # OpenCV 라이브러리: 이미지 로드, 출력, 이벤트 처리를 담당
import numpy as np # 행렬 연산 라이브러리: 이미지 데이터(행렬) 처리를 도움

# --- 1. 전역 변수 설정 (프로그램 전체에서 공유되는 설정값) ---
brush_size = 5          # 그림을 그릴 붓(원)의 초기 반지름 크기
color = (255, 0, 0)     # 기본 그리기 색상 (BGR 순서: Blue=255, Green=0, Red=0 -> 파란색)
is_drawing = False      # 마우스 버튼이 눌려 있는 상태인지 확인하는 스위치 (True: 그림 그리는 중)

# [이미지 로드] 'soccer.jpg' 파일을 읽어서 img 변수에 행렬 형태로 저장
# 이미지 파일은 반드시 해당 .py 파일과 같은 폴더에 있어야 합니다.
img = cv2.imread('soccer.jpg')

# [예외 처리] 이미지 파일이 없거나 경로가 틀려 로드에 실패했을 경우 프로그램 종료
if img is None:
    print("이미지를 불러올 수 없습니다. 파일명이나 폴더 위치를 확인하세요!")
    exit()

# --- 2. 마우스 콜백 함수 정의 (마우스 동작 시 자동 실행되는 함수) ---
def mouse_event(event, x, y, flags, param):
    """
    event: 마우스 이벤트 종류 (클릭, 이동 등)
    x, y: 이벤트가 발생한 지점의 좌표
    """
    global is_drawing, color, brush_size # 함수 밖의 변수를 수정하기 위해 전역 변수 선언

    # 마우스 왼쪽 버튼을 눌렀을 때 (좌클릭)
    if event == cv2.EVENT_LBUTTONDOWN:   
        is_drawing = True                # 그리기 모드 활성화
        color = (255, 0, 0)              # 색상을 파란색으로 변경
        # cv2.circle: (대상 이미지, 중심좌표, 반지름, 색상, -1=내부채우기)
        cv2.circle(img, (x, y), brush_size, color, -1)

    # 마우스 오른쪽 버튼을 눌렀을 때 (우클릭)
    elif event == cv2.EVENT_RBUTTONDOWN: 
        is_drawing = True                # 그리기 모드 활성화
        color = (0, 0, 255)              # 색상을 빨간색(BGR: 0, 0, 255)으로 변경
        cv2.circle(img, (x, y), brush_size, color, -1)

    # 마우스가 화면 위에서 움직일 때
    elif event == cv2.EVENT_MOUSEMOVE:    
        if is_drawing:                   # 마우스 버튼이 눌린 상태(드래그 중)일 때만 그림
            cv2.circle(img, (x, y), brush_size, color, -1)

    # 마우스 버튼(왼쪽 또는 오른쪽)을 뗐을 때
    elif event == cv2.EVENT_LBUTTONUP or event == cv2.EVENT_RBUTTONUP:
        is_drawing = False               # 드래그 종료, 그리기 모드 비활성화

# --- 3. 창 생성 및 마우스 이벤트 연결 ---
cv2.namedWindow('Drawing on Image')      # 이미지를 표시할 윈도우 창의 이름 설정
# 'Drawing on Image' 창에서 발생하는 모든 마우스 동작을 mouse_event 함수와 연결
cv2.setMouseCallback('Drawing on Image', mouse_event)

print("==== 이미지 드로잉 가이드 ====")
print("1. 마우스 좌클릭 드래그: 파란색 그리기")
print("2. 마우스 우클릭 드래그: 빨간색 그리기")
print("3. '+' 또는 '=' 키: 붓 크기 증가 (최대 15)")
print("4. '-' 또는 '_' 키: 붓 크기 감소 (최소 1)")
print("5. 'q' 키: 프로그램 종료 및 저장")

# --- 4. 메인 루프 (실시간 화면 갱신 및 키보드 입력 처리) ---
while True:
    # 현재까지 그려진 내용이 포함된 이미지 데이터를 화면에 출력
    cv2.imshow('Drawing on Image', img) 
    
    # 1ms 동안 키 입력을 대기 (0xFF는 64비트 OS와의 호환성을 위한 처리)
    key = cv2.waitKey(1) & 0xFF

    # 'q'를 누르면 반복문 탈출
    if key == ord('q'): 
        break
    
    # '+' 키를 누르면 붓의 크기를 1 증가 (최대치 15로 제한)
    elif key == ord('+') or key == ord('='): 
        brush_size = min(15, brush_size + 1)
        print(f"현재 붓 크기: {brush_size}")
        
    # '-' 키를 누르면 붓의 크기를 1 감소 (최소치 1로 제한)
    elif key == ord('-') or key == ord('_'): 
        brush_size = max(1, brush_size - 1)
        print(f"현재 붓 크기: {brush_size}")

# 메모리 해제 및 모든 윈도우 창 닫기
cv2.destroyAllWindows()