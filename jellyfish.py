import requests
import json

def get_api_data(base_url, endpoint, headers=None, params=None):
    # 완전한 URL 구성
    url = f"{base_url}"
    
    # GET 요청 보내기
    response = requests.get(url, headers=headers, params=params)
    
    # 응답 상태 코드 확인
    if response.status_code == 200:
        # JSON 데이터 파싱
        data = response.json()
        return data
    else:
        raise Exception(f"요청 실패, 상태 코드: {response.status_code}")

# 변수 설정
base_url = "https://www.nifs.go.kr/OpenAPI_json?id=jellyList"
endpoint = ""
headers = {
    "Authorization": "Bearer YOUR_ACCESS_TOKEN",
    "Content-Type": "application/json"
}
params = {
    "key": "qPwOeIrU-2405-CDDWHR-0800",
    "sdate": "20180516",
    "edate": "20240516"
}
# GET 요청 예제

jellydates = []
try:
    get_data = get_api_data(base_url, endpoint, headers=headers, params=params)

    for d in get_data['body']['item']:
        if d['gbn'] == '0':
            print(d['board_idx'])
            jellydates.append(d['board_idx'])
except Exception as e:
    print(e)


def convert_string_to_number(s): 
    try:
        # 숫자로 변환을 시도
        return float(s) if '.' in s else int(s)
    except ValueError:
        # 변환이 실패하면 0을 반환
        return 0


nomSumList = [0 for i in range(0, 12)]

for i in range(len(jellydates)):
    # 변수 설정
    base_url = "https://www.nifs.go.kr/OpenAPI_json?id=jellyDetail2"
    endpoint = ""
    headers = {
        "Authorization": "Bearer YOUR_ACCESS_TOKEN",
        "Content-Type": "application/json"
    }
    params = {
        "key": "qPwOeIrU-2405-CDDWHR-0800",
        "srcode": jellydates[i],
    }
    get_data = get_api_data(base_url, endpoint, headers=headers, params=params)
    
    #출현률 획득
    for i in range(0, 12):
        nomSumList[i] += convert_string_to_number(get_data['body']['item'][0]['etc_ratio_' + "{:02}".format(i+1)])


print(nomSumList)