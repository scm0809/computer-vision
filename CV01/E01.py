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