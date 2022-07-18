import requests

url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst'
params = {
    "serviceKey": "yy0vBlt7HwfUrdgLyhGHmJDELHnoI6h6Xs+j74Z49X50gO9Q8vtqAlEu4vQU/N+vz0iychRQMFH6kka6Xhpt1g==",
    "pageNo": "1",
    "numOfRows": "1000",
    "dataType": "json",
    "base_date": "20220718",
    "base_time": "0800",
    "nx": "55",
    "ny": "127"
}

response = requests.get(url, params=params)
print(response.text)
