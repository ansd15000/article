from re import sub
import requests
from bs4 import BeautifulSoup


# 쓸데없는 html 태그 삭제
def deltag(txt):
    data = str(txt)
    start = data.find('>') + 1
    end = data.find('<',start)
    return data[start:end]

# 이미지 태그에서 캡션과 링크 추출
def get_caption_imgLink(txt):
    data = str(txt)
    alt_start = data.find('"') + 1
    alt_end  = data.find('"',alt_start)
    caption = data[alt_start:alt_end]

    start = data.find('"', alt_end + 1) + 1
    end = data.find('"',start)
    imglink = data[start:end]
    return caption, imglink

# 날짜 추출
def articleDate(txt):
    
    pass

# 부제목 추출
def forSubTitle(txt):
    subTitles = list()
    data = str(txt)
    start = data.find('ㆍ') + 1
    while start != -1: # find로 못찾으면 break
        end = data.find('<',start)
        subTitles.append(data[start:end])
        start = data.find('ㆍ', end) 
    return subTitles

# 기사 메인 내용
def getmain(txt):
    maindata = ''
    for i in txt:
        maindata += deltag(i)
    return maindata

# 배열로 데이터를 처리하면 좀 더 속도가 빨라지려나?
def crawling(url):
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15'}
    data = requests.get(url, headers= headers)
    soup = BeautifulSoup(data.text, 'html.parser')

    title = deltag(soup.select('#articleTtitle'))
    subTitle = soup.select('#container > div.main_container > div.art_cont > div.art_body > div.art_subtit > p')
    date = soup.select_one('#bylineArea')
    img = soup.select_one('#container > div.main_container > div.art_cont > div.art_body > div.art_photo.photo_center > div > img')
    main = soup.select('p.content_text')

    print(date)


if __name__ == "__main__" :
    # url = 'http://biz.khan.co.kr/khan_art_view.html?artid=202106082157015&code=930100&med_id=khan'
    url = 'http://biz.khan.co.kr/khan_art_view.html?artid=202106132132005&code=930100&med_id=khan'
    crawling(url)