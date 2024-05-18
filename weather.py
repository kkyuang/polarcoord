#실행 전 모듈 설치 필요
#pip install (모듈명)
#모듈명: pandas / matplotlib / numpy

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap

#엑셀 파일 읽어오는 사용자 정의 함수(파일 경로, 시트 이름, x좌표 열, y좌표 열, 시작 행, 끝 행)
#열의 이름은 1행의 데이터값 기준임
def extract_data_from_excel(file_path, sheet_name, x_col, y_col, start_row, end_row):
    # 엑셀 파일 읽기
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    print(df)
    
    # 특정 범위의 데이터 선택
    x = df.loc[start_row:end_row, x_col].values
    y = df.loc[start_row:end_row, y_col].values
    
    return x, y

#데이터시트 이름(월별 기온 극좌표 등)
datasheetname = '100년간 평균기온, 부산'
#시작하는 행 번호
minR = 9
#데이터가 끝나는 행 번호
maxR = 1440

#x, y좌표 불러오기 => 카테시안으로 환산된 극좌표
x, y = extract_data_from_excel("월별 기온 극좌표.xls", datasheetname, 'x', 'y', minR, maxR)

#그리드의 x, y좌표 불러오기 => 평균 기온의 경우 0, 10, 20도 표현
x10, y10 = extract_data_from_excel("월별 기온 극좌표.xls", datasheetname, '10x', '10y', minR, maxR)
x20, y20 = extract_data_from_excel("월별 기온 극좌표.xls", datasheetname, '20x', '20y', minR, maxR)
x30, y30 = extract_data_from_excel("월별 기온 극좌표.xls", datasheetname, '30x', '30y', minR, maxR)

#색상 그라데이션 관련. 최근으로 올 수록 파란색 -> 빨간색
colors = np.linspace(0, 1, len(x))
cmap = plt.get_cmap('coolwarm')


#그리드 그리기(10도, 20도, 30도)
plt.plot(x10, y10, linestyle='-', color='black')
plt.plot(x20, y20, linestyle='-', color='black')
plt.plot(x30, y30, linestyle='-', color='black')


#산점도, 잇는 선 그리기. alpha는 그라데이션 효과
for i in range(len(x) - 1):
    plt.plot([x[i], x[i+1]], [y[i], y[i+1]], linestyle='-', color=cmap(i / (len(x) - 1)), alpha=0.2)
plt.scatter(x, y, c=colors, cmap='coolwarm', alpha=0.2)


#그래프 그리는 것에 관련한 함수
plt.legend()
#그래프의 x, y비율을 1:1로 설정
plt.gca().set_aspect('equal', adjustable='box')
#그래프 제목 설정
plt.title('Temperature by month(1908~2024)')
#축 이름 설정
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.show()
