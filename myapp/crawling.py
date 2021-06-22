# 경향비즈 
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import urllib.request
import os 

headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15'}
def __imgdir(path):
    if os.path.exists(path): pass
    else: os.mkdir(path)

# 쓸데없는 html 태그 삭제
def __deltag(txt):
    data = str(txt)
    start = data.find('>') + 1
    end = data.find('<',start)
    return data[start:end]

def __forTag(txt):
    data = str(txt)
    start = data.find('y=') + 2 # category=IT 
    end = data.find('"', start)
    return data[start:end]
    
# 이미지 태그에서 캡션과 링크 추출. 이미지가 다수일 경우 코드 수정 필요
def __get_caption_imgLink(txt):
    caption, imglink = None, None
    if txt is None:
        return caption, imglink

    data = str(txt)
    alt_start = data.find('"') + 1
    alt_end  = data.find('"',alt_start)
    caption = data[alt_start:alt_end]

    start = data.find('"', alt_end + 1) + 1
    end = data.find('"',start)
    imglink = data[start:end]
    return caption, imglink

# 부제목 추출
def __forSubTitle(txt):
    subTitles = list() # 부제목이 여러개인 경우가 있음
    data = str(txt)
    start = data.find('ㆍ')
    while start >= 1  : # find로 못찾으면 break
        end = data.find('<',start)
        subTitles.append(data[start:end])
        start = data.find('ㆍ', end) 
    return dict.fromkeys(subTitles)

# 날짜 추출 및 날짜 타입으로 변환
def __articleDate(txt):
    data = str(txt)
    start = data.find('수정')
    if start != -1:
        start = data.find('2', start)
    else :
        start = data.find(': ') + 2
    end = data.find('<', start)
    articleTime = datetime.strptime(data[start:end], '%Y.%m.%d %H:%M') # 초 정보가 없어서 타임테이블은 불가능
    return articleTime

# 기사 메인 내용
def __getmain(txt):
    maindata = ''
    for i in txt:
        maindata += __deltag(i)
    return maindata

# 이미지 저장 및 디렉토리 분별
def __saveImg(links) :
    if links is None :
        return None
    newsStart = links.find(':') + 3 # https : <- 이거! 
    newsEnd = links.find('/',newsStart)
    imgstart = links.rfind('/') + 1
    path = f'/root/article/{links[newsStart:newsEnd]}'
    imgpath = path + '/' + links[imgstart:]
    __imgdir(path)
    urllib.request.urlretrieve(links, imgpath)
    return imgpath

# 배열로 데이터를 처리하면 좀 더 속도가 빨라지려나?
def crawling(url):
    data = requests.get(url, headers= headers, allow_redirects=False)
    soup = BeautifulSoup(data.text, 'html.parser')
    title = __deltag(soup.select('#articleTtitle'))
    subtitle = soup.select('#container > div.main_container > div.art_cont > div.art_body > div.art_subtit > p')
    tag = __forTag(soup.select_one('#topMenuArea > div > ul > li.on > a'))
    date = soup.select_one('#bylineArea')
    main = soup.select('p.content_text')
    
    img = soup.select_one('#container > div.main_container > div.art_cont > div.art_body > div.art_photo.photo_center > div > img')
    if img is None:
        img = soup.select_one('#container > div.main_container > div.art_cont > div.art_body > div.art_photo.photo_center > div > a > img')   
        if img is None:
            img = soup.select_one('#container > div.main_container > div.art_cont > div.art_body > div.art_photo.photo_right > div > img')

    _, imgLink = __get_caption_imgLink(img)
    # result = {
    #     'title': title,
    #     'subtitle': __forSubTitle(subtitle),
    #     'date': __articleDate(date),
    #     'tag' : tag,
    #     'imglink' : imgLink,
    #     'caption' : caption, # 쓰진 않지만 혹시 모르니 ㅇㅇ
    #     'main' : __getmain(main)
    # }
    
    article = {
        "news_agency" : 0,
        "tag" : tag,
        "title" : title,
        "subTitle" : __forSubTitle(subtitle), # dict. Array로 할랬더니 mysql에 어떻게 될지 모르겟음
        "main" : __getmain(main),
        "date" : __articleDate(date),
    }
    articleImg = __saveImg(imgLink)
    return article, articleImg

# def getpagelist(url):
#     data = requests.get(url, headers= headers)
#     soup = BeautifulSoup(data.text, 'html.parser')
#     # page = soup.select('#container > div > div.content_Wrap > div.news_list > ul > li')
#     for i in range(15): # 경향비즈는 한 페이지에 기사가 15개
#         news = str(soup.select(f"#container > div > div.content_Wrap > div.news_list > ul > li:nth-child({i+1}) > div > strong > a"))
#         start = news.find('"') + 1
#         end = news.find('"', start)
#         crawling(news[start:end])

if __name__ == "__main__" :
    url = "http://biz.khan.co.kr/khan_art_view.html?artid=202102090000001&code=610100&med_id=khan"
    a, _ = crawling(url)
    print(a)
    # print(len(a['subTitle']))
    pass
