# E01.py 이미지 로드 및 흑백 변환 합치기
컬러 이미지를 읽어온 후, 이를 흑백(Grayscale)으로 변환하여 원본과 변환본을 하나의 창에 가로로 합쳐 출력.

###주요기능:
이미지 로드 및 색상 공간 변환 (Image Loading & Color Space Conversion)
이미지 읽기: `cv2.imread()`를 사용하여 로컬 환경의 이미지 파일을 행렬 데이터로 로드합니다.
색상 변환: `cv2.cvtColor()`를 활용하여 컬러(BGR) 이미지를 흑백(Grayscale) 이미지로 변환합니다.
이미지 병합: `np.hstack()` 기능을 이용해 데이터 채널을 맞춘 원본 이미지와 흑백 이미지를 가로로 연결하여 비교 출력합니다.

###전체코드

```
import cv2      # OpenCV 라이브러리 (이미지 처리 핵심)
import numpy as np # 행렬 연산 라이브러리 (이미지 가로 합치기용)

# 1. 이미지 로드
# 'soccer.jpg' 파일을 읽어옵니다. (같은 폴더에 파일이 있어야 함)
img = cv2.imread('soccer.jpg')

# 이미지가 제대로 읽혔는지 확인 (경로가 틀리면 None이 반환됨)
if img is None:
    print("파일을 찾을 수 없습니다. 파일명이나 경로를 확인하세요.")
else:
    # 2. 흑백 변환
    # 컬러 이미지(BGR)를 흑백(GRAY)으로 변환합니다.
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # 3. 흑백 이미지를 3채널로 변경
    # hstack으로 합치려면 '원본(채널3개)'과 '흑백(채널1개)'의 채널 수가 같아야 함.
    # 흑백 이미지를 겉모양만 BGR 형식으로 바꿔서 채널 3개로 만들어줌.
    gray_3channel = cv2.cvtColor(gray_img, cv2.COLOR_GRAY2BGR)
    
    # 4. 가로로 붙이기 (왼쪽: 원본, 오른쪽: 흑백)
    # np.hstack은 두 행렬(이미지)을 수평(Horizontal)으로 이어 붙임.
    combined = np.hstack((img, gray_3channel))
    
    # 5. [추가] 화면 크기 조절
    # 이미지가 너무 크면 모니터를 벗어나므로 크기를 절반으로 줄임.
    # (0, 0)은 결과 크기를 직접 지정하지 않겠다는 뜻이고, fx/fy=0.5는 비율을 50%로 설정한 것.
    small_combined = cv2.resize(combined, (0, 0), fx=0.5, fy=0.5)
    
    # 6. 결과 출력
    # 'Left: Color / Right: Gray'라는 제목의 창에 이미지를 띄움.
    cv2.imshow('Left: Color / Right: Gray', small_combined)
    
    # 사용자가 키보드 아무 키나 누를 때까지 창을 닫지 않고 대기.
    cv2.waitKey(0)
    
    # 키를 누르면 모든 이미지 출력 창을 닫고 프로그램을 종료.
    cv2.destroyAllWindows()
```

###결과 사진

<img width="2811" height="1002" alt="스크린샷 2026-03-05 151723" src="https://github.com/user-attachments/assets/04826610-8130-4f66-ba5d-844df8ae6b16" />

# E02.py 마우스 이벤트를 이용한 드로잉 툴
마우스 왼쪽 버튼(파란색)과 오른쪽 버튼(빨간색)을 이용하여 이미지 위에 자유롭게 그림을 그리는 실습. 
  - `+` 키를 누르면 붓 크기 증가 (최대 15)
  - `-` 키를 누르면 붓 크기 감소 (최소 1)

####주요기능:
인터랙티브 드로잉 툴 (Interactive Drawing Tool)
마우스 이벤트 처리: `cv2.setMouseCallback()`을 사용하여 마우스 클릭 및 이동 상태에 따라 이미지 위에 원(`cv2.circle`)을 그립니다.
키보드 실시간 제어: `cv2.waitKey()`를 통해 사용자 입력을 감지하며, `+`와 `-` 키를 사용하여 붓(Brush)의 크기를 실시간으로 조절합니다.
분기 처리: 마우스 왼쪽 버튼은 파란색, 오른쪽 버튼은 빨간색으로 색상을 다르게 지정하여 이벤트를 처리합니다.

###결과 사진

<img width="1188" height="1245" alt="image" src="https://github.com/user-attachments/assets/f007a745-07ed-4d14-90b2-c3d10c504644" />

###전체코드
```
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
```

# E03.py 마우스 드래그를 이용한 ROI 추출 및 저장
마우스 드래그로 이미지의 특정 영역을 선택하고, 선택된 영역(ROI)만 별도의 창으로 띄운 뒤 파일(`selected_roi.jpg`)로 저장합니다.

###주요기능: 
ROI 설정 및 이미지 저장 (ROI Extraction & Image Saving)
관심 영역(ROI) 추출: 마우스 드래그의 시작점과 끝점 좌표를 획득하여 NumPy 슬라이싱 기법으로 이미지의 특정 영역만 잘라냅니다.
개별 창 출력: 전체 이미지와 별개로 선택된 ROI 영역만을 독립된 윈도우 창에 표시합니다.
파일 저장: `cv2.imwrite()`를 실행하여 사용자가 선택한 특정 영역을 `selected_roi.jpg`라는 파일명으로 로컬에 저장합니다.

###전체코드
```
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
```
###결과 사진


![selected_roi](https://github.com/user-attachments/assets/a92ccd46-88d0-434d-9aa8-b1d1c2078f85)




