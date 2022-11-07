from urllib.request import urlopen as url_open
from urllib import parse
from urllib.request import Request
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import json


def get_geo(addr):
    # 11월 10일 api 정보 삭제 예정
    # naver map api key
    client_id = "ureszraal9"
    # 본인이 할당받은 ID 입력
    client_pw = "mM198tK1l9K1yvDiLT315g8IWY5bogukDngUNxDF"
    # 본인이 할당받은 Secret 입력

    api_url = "https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode?query="
    geo_coordi = {}
    add_urlenc = parse.quote(addr)
    url = api_url + add_urlenc

    request = Request(url)
    request.add_header("X-NCP-APIGW-API-KEY-ID", client_id)
    request.add_header("X-NCP-APIGW-API-KEY", client_pw)
    context = 0
    try:
        response = url_open(request)
    except HTTPError as e:
        print("HTTP Error!")
        latitude = None
        longitude = None
    else:
        rescode = response.getcode()
        if rescode == 200:
            response_body = response.read().decode("utf-8")
            response_body = json.loads(response_body)  # json
            if response_body["addresses"] == []:
                print("'result' not exist!")
                latitude = None
                longitude = None
            else:
                latitude = response_body["addresses"][0]["y"]
                longitude = response_body["addresses"][0]["x"]
                print("Success!")
        else:
            print("Response error code : %d" % rescode)
            latitude = None
            longitude = None

    geo_coordi = {"longtitude": longitude, "latitude": latitude}
    print(geo_coordi)
    return geo_coordi
