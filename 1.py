from audioop import add
from selenium import webdriver
from selenium.webdriver.common.by import By
import string
import time
import os
import django
from urllib.request import urlopen
url_list = []
data_id = []
datas = []
from bs4 import BeautifulSoup
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pjt.settings")
django.setup()

from test_food.models import Store
from Restaurant.models import Restaurant
import time 
# 영화 사이트 이동 : 영화 제목과 줄거리 저장
def get_data(url):
    # url 요청
    url+="/home/"
    # print(url)
    request = urlopen(url)
    byte_data = request.read()
    # 디코딩
    text_data = byte_data.decode("utf-8")
    # html 파싱
    soup  = BeautifulSoup(text_data, "html.parser")
    img = soup.select_one(".K0PDV").get('style').replace('width:100%;height:100%;background-image:url("', '').replace('");background-position:50% 0', '')
    
    #data2 = soup.select_one(".K0PDV").get('style')
    # tag & 내용 수집
    #img = soup.find("img")["src"]
    #print(img)
    # dictionary로 저장
    # context = {
    #     "img": img[:-15],
    # }

    return img

# base="https://m.map.naver.com/search2/search.naver?query=강남역+피자"
# get_data(base)
def naverMapCrawling(search):
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome("./chromedriver.exe",chrome_options=options) #selenium 사용에 필요한 chromedriver.exe 파일 경로 지정
    
    driver.get(f"https://m.map.naver.com/search2/search.naver?query={search}") 
    driver.implicitly_wait(3) # 로딩이 끝날 때 까지 10초까지는 기다림
    #time.sleep(10)

    items = driver.find_elements(By.CSS_SELECTOR, '._item ') 
    cnt=0
    baseurl="https://m.place.naver.com/restaurant/"
    for item in items:
        # time.sleep(1)
        cnt+=1
        title = item.get_attribute('data-title')
        cat = item.find_element(By.CSS_SELECTOR,'.item_tit >em').text
        address = item.find_element(By.CSS_SELECTOR,'.item_address ').text.replace('주소보기\n', '')
        longtitude = float(item.get_attribute('data-longitude'))
        latitude = float(item.get_attribute('data-latitude'))
        tel = item.get_attribute('data-tel')
        id = int(item.get_attribute('data-id'))
        #aitem = item.find_elements(By.CSS_SELECTOR, '.item_info > .item_common > .sp_map btn_spi2 naver-splugin').text
        #print(aitem,type(aitem)) 20472120
        sid=item.get_attribute('data-sid')
        url=item.find_element(By.CSS_SELECTOR, '.item_common > a').get_attribute('data-url')
        #url_list.append(url)
        sid=baseurl+sid
        url_list.append(sid)
        img=get_data(sid)
        #print(sid)
        for character in string.punctuation:
            title = title.replace(character, '') # 특수기호 제거(파이어베이스에 경로로 저장하기 위해서)
        #document.querySelector("#ct > div.search_listview._content._ctList > ul > li:nth-child(1) > div.item_info > a.a_item.a_item_distance._linkSiteview > div > em")
        #ct > div.search_listview._content._ctList > ul > li:nth-child(1) > div.item_info > a.a_item.a_item_distance._linkSiteview > div > em
        # for url in url_list:
        #     get_data(url)
        datas.append({
            "id" : id,
            "cat":cat,
            "title" : title,
            "addr" : address,
            "longtitude" : longtitude,
            "latitude" : latitude,
            "tel" : tel,
            "img":img
            })
        
  
        data_id.append(id)
        #딱 30개만
        if cnt>29:
            break    
    #print(datas)
    #print(url_list)
    return datas
def add_data():
    result = []

    # 자료 수집 함수 실행
    for data in datas:
        tmp = data
        # 만들어진 dic를 리스트에 저장
        result.append(tmp)
    #print(result)
    # DB에 저장
    for item in result:
    #     # Store(
    #     # #id=(item["id"]),
    #     # category=item["cat"],
    #     # title=item["title"],
    #     # addr=item["addr"],
    #     # longtitude=item["longtitude"],
    #     # latitude=item["latitude"],
    #     # tel=item["tel"]).save(),
        Restaurant(
        #id=(item["id"]),
        category=item["cat"],
        title=item["title"],
        addr=item["addr"],
        longtitude=item["longtitude"],
        latitude=item["latitude"],
        tel=item["tel"],
        imgurl=item["img"]
          ).save()


    return result


# DB 저장 함수 강제 실행(임시로 실행)

search = input("검색어를 입력해주세요 >> ")
naverMapCrawling(search)
add_data()