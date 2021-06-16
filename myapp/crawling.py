# 경향비즈 
import requests
from bs4 import BeautifulSoup
from datetime import datetime

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
    
# 이미지 태그에서 캡션과 링크 추출
def __get_caption_imgLink(txt):
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
    start = data.find('ㆍ') + 1
    while start >= 1  : # find로 못찾으면 break
        end = data.find('<',start)
        subTitles.append(data[start:end])
        start = data.find('ㆍ', end) 
    return subTitles

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

# 배열로 데이터를 처리하면 좀 더 속도가 빨라지려나?
def crawling(url):
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15'}
    data = requests.get(url, headers= headers)
    soup = BeautifulSoup(data.text, 'html.parser')
    title = __deltag(soup.select('#articleTtitle'))
    subtitle = soup.select('#container > div.main_container > div.art_cont > div.art_body > div.art_subtit > p')
    tag = __forTag(soup.select_one('#topMenuArea > div > ul > li.on > a'))
    date = soup.select_one('#bylineArea')
    main = soup.select('p.content_text')
    img = soup.select_one('#container > div.main_container > div.art_cont > div.art_body > div.art_photo.photo_center > div > img')
    caption, imgLink = __get_caption_imgLink(img)
    
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
        "subTitle" : __forSubTitle(subtitle), # Array
        "main" : __getmain(main),
        "date" : __articleDate(date),
    }
    articleImg = { "articleImg" : imgLink }
        

    return article, articleImg


if __name__ == "__main__" :
    # url = 'http://biz.khan.co.kr/khan_art_view.html?artid=202106082157015&code=930100&med_id=khan'
    # url = 'http://biz.khan.co.kr/khan_art_view.html?artid=202106132132005&code=930100&med_id=khan'
    url = 'http://biz.khan.co.kr/khan_art_view.html?artid=202106141610011&code=930100&med_id=khan'
    # url = 'http://biz.khan.co.kr/khan_art_view.html?artid=202106142245001&code=920301&med_id=khan'
    a = crawling(url)


# news_agency = 0
# tag
# title
# subTitle
# main
# date

# article
# articleImg

# a = {"q": 1, "w" : 2}
# def test(**args):
#     for i, j in args.items():
#         print(i, j)

# test(**a) # unpack operator
