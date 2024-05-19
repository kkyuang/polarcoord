import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point
import pandas as pd
import numpy as np
from matplotlib.colors import ListedColormap

#엑셀 파일 읽어오는 사용자 정의 함수(파일 경로, 시트 이름, x좌표 열, y좌표 열, 시작 행, 끝 행)
#열의 이름은 1행의 데이터값 기준임
def extract_data_from_excel(file_path, sheet_name, x_col, start_row, end_row):
    # 엑셀 파일 읽기
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    print(df)
    
    # 특정 범위의 데이터 선택
    x = df.loc[start_row:end_row, x_col].values
    
    return x

#데이터시트 이름(월별 기온 극좌표 등)
datasheetname = 'Sheet1'

# 대한민국 지도 데이터 (여기서는 세계 지도를 사용하여 대한민국만 잘라냅니다)
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
south_korea = world[world.name == "South Korea"]

x = extract_data_from_excel("지역 해파리 출몰률 데이터.xlsx", datasheetname, '경도', 0, 13)
y = extract_data_from_excel("지역 해파리 출몰률 데이터.xlsx", datasheetname, '위도', 0, 13)
nom = extract_data_from_excel("지역 해파리 출몰률 데이터.xlsx", datasheetname, '전체합', 0, 13)

# 예제 데이터: 위치 (경도, 위도)와 수치 배열
data = []
for i in range(len(x)):
    data.append({'coords': (x[i], y[i]), 'value': nom[i]})

# 점의 색상과 크기를 수치에 따라 설정
values = [item['value'] for item in data]
colors = plt.cm.viridis([v / max(values) for v in values])
sizes = [v/3 for v in values]

# 대한민국 지도 플롯
fig, ax = plt.subplots(1, 1, figsize=(10, 10))
south_korea.boundary.plot(ax=ax)

# 각 위치에 점을 찍기
for item, color, size in zip(data, colors, sizes):
    x, y = item['coords']
    ax.scatter(x, y, color=color, s=size, label=f"Value: {item['value']}")

plt.xlim([125, 130.5])
plt.ylim([32, 39])
plt.title("South Korea Map with Colored Points")
plt.xlabel("Longitude")
plt.ylabel("Latitude")

plt.show()
