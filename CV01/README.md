# E01.py 이미지 로드 및 흑백 변환 합치기
컬러 이미지를 읽어온 후, 이를 흑백(Grayscale)으로 변환하여 원본과 변환본을 하나의 창에 가로로 합쳐 출력.

###주요기능:
이미지 로드 및 색상 공간 변환 (Image Loading & Color Space Conversion)
이미지 읽기: `cv2.imread()`를 사용하여 로컬 환경의 이미지 파일을 행렬 데이터로 로드합니다.
색상 변환: `cv2.cvtColor()`를 활용하여 컬러(BGR) 이미지를 흑백(Grayscale) 이미지로 변환합니다.
이미지 병합: `np.hstack()` 기능을 이용해 데이터 채널을 맞춘 원본 이미지와 흑백 이미지를 가로로 연결하여 비교 출력합니다.

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


# E03.py 마우스 드래그를 이용한 ROI 추출 및 저장
마우스 드래그로 이미지의 특정 영역을 선택하고, 선택된 영역(ROI)만 별도의 창으로 띄운 뒤 파일(`selected_roi.jpg`)로 저장합니다.

###주요기능: 
ROI 설정 및 이미지 저장 (ROI Extraction & Image Saving)
관심 영역(ROI) 추출: 마우스 드래그의 시작점과 끝점 좌표를 획득하여 NumPy 슬라이싱 기법으로 이미지의 특정 영역만 잘라냅니다.
개별 창 출력: 전체 이미지와 별개로 선택된 ROI 영역만을 독립된 윈도우 창에 표시합니다.
파일 저장: `cv2.imwrite()`를 실행하여 사용자가 선택한 특정 영역을 `selected_roi.jpg`라는 파일명으로 로컬에 저장합니다.

전체코드



###결과 사진


![selected_roi](https://github.com/user-attachments/assets/a92ccd46-88d0-434d-9aa8-b1d1c2078f85)




