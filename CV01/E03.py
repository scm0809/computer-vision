import cv2      # OpenCV 라이브러리 가져오기
import numpy as np # 행렬 연산을 위한 Numpy 가져오기

# 전역 변수 설정 (프로그램 전체에서 공유되는 변수)
is_dragging = False      # 마우스가 드래그 중인지 상태를 저장 (True/False)
start_x, start_y = -1, -1 # 드래그를 시작한 지점의 좌표 저장
roi = None               # 선택된 영역(Region of Interest) 이미지를 담을 변수

# 1. 이미지 불러오기
# '~~.jpg' 파일을 불러옵니다. (경로에 파일이 있어야 함)
original_img = cv2.imread('soccer.jpg')

# 파일 읽기 실패 시 에러 메시지 출력 후 종료
if original_img is None:
    print("이미지를 불러올 수 없습니다. 파일명을 확인하세요!")
    exit()

# 화면에 보여줄 이미지 복사본 생성 (원본을 보호하면서 사각형을 그리기 위함)
img_display = original_img.copy()

# 2. 마우스 콜백 함수 정의 (마우스 움직임이 있을 때마다 호출됨)
def mouse_handler(event, x, y, flags, param):
    global is_dragging, start_x, start_y, img_display, roi

    # 마우스 왼쪽 버튼을 눌렀을 때 (드래그 시작)
    if event == cv2.EVENT_LBUTTONDOWN:
        is_dragging = True      # 드래그 상태 시작
        start_x, start_y = x, y # 현재 클릭한 위치를 시작 좌표로 저장

    # 마우스가 움직일 때
    elif event == cv2.EVENT_MOUSEMOVE:
        if is_dragging:         # 드래그 중인 상태라면
            # 매순간 원본을 새로 복사하여 이전 사각형 잔상을 지움
            img_display = original_img.copy()
            # 실시간으로 드래그 중인 사각형 그리기 (초록색, 두께 2)
            cv2.rectangle(img_display, (start_x, start_y), (x, y), (0, 255, 0), 2)

    # 마우스 왼쪽 버튼을 뗐을 때 (드래그 종료)
    elif event == cv2.EVENT_LBUTTONUP:
        is_dragging = False     # 드래그 상태 종료
        
        # 사각형의 가로, 세로 크기 계산 (절대값 이용)
        w = abs(x - start_x)
        h = abs(y - start_y)

        # 크기가 0보다 큰 영역을 선택했을 경우에만 처리
        if w > 0 and h > 0:
            # Numpy 슬라이싱을 위해 좌표 정렬 (시작점보다 끝점이 작을 경우 대비)
            left, right = min(start_x, x), max(start_x, x)
            top, bottom = min(start_y, y), max(start_y, y)
            
            # Numpy 슬라이싱으로 ROI 영역 잘라내기 [y행 범위, x열 범위]
            roi = original_img[top:bottom, left:right]
            
            # 잘라낸 영역을 'ROI'라는 별도 창에 출력
            cv2.imshow('ROI', roi)

# 3. 메인 설정
cv2.namedWindow('Select ROI')           # 메인 윈도우 창 생성
cv2.setMouseCallback('Select ROI', mouse_handler) # 마우스 이벤트 연결

print("사용법: 드래그(영역 선택), 'r'(리셋), 's'(저장), 'q'(종료)")

# 4. 무한 루프 (화면 갱신 및 키 입력 대기)
while True:
    # 사각형이 그려지고 있는 이미지를 화면에 표시
    cv2.imshow('Select ROI', img_display)
    
    # 1ms 동안 키 입력을 기다림
    key = cv2.waitKey(1) & 0xFF

    # 'q' 키를 누르면 루프 종료
    if key == ord('q'):
        break
    
    # 'r' 키를 누르면 영역 선택 리셋
    elif key == ord('r'):
        img_display = original_img.copy() # 화면 이미지를 원본으로 초기화
        roi = None                        # 저장된 ROI 데이터 삭제
        # 만약 ROI 창이 열려있다면 닫기
        if cv2.getWindowProperty('ROI', cv2.WND_PROP_VISIBLE) >= 1:
            cv2.destroyWindow('ROI')
        print("리셋되었습니다. 다시 선택하세요.")
        
    # 's' 키를 누르면 선택한 영역을 파일로 저장
    elif key == ord('s'):
        if roi is not None:
            # cv2.imwrite()를 사용하여 이미지 파일로 저장
            cv2.imwrite('selected_roi.jpg', roi)
            print("저장 완료: selected_roi.jpg")
        else:
            print("선택된 영역이 없습니다!")

# 모든 창 닫기 및 프로그램 종료
cv2.destroyAllWindows()