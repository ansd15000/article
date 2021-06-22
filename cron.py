# 10분마다 크롤링 진행하기
import time, copy, os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from myapp.crawling import crawling
from myapp.models import Article, ArticleImg

import requests
from bs4 import BeautifulSoup

headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15'}

# 페이지 크롤링 및 저장
def __getpagelist(url, retry):
    data = requests.get(url, headers= headers, allow_redirects=False) # Exceeded 30 redirects. 때문에
    soup = BeautifulSoup(data.text, 'html.parser')

    for i in range(1, 16): # 경향비즈는 한 페이지에 기사가 15개
        news = str(soup.select(f"#container > div > div.content_Wrap > div.news_list > ul > li:nth-child({i}) > div > strong > a"))
        start = news.find('"') + 1
        end = news.find('"', start)
        
        titlestart = news.find('>') + 1
        titleend = news.find('<', titlestart)
        title = news[titlestart:titleend]

        # 디비에 저장된 기사가 있다. == 로직을 진행할 필요가 없다
        if len(Article.objects.filter(title = title)) > 0 :
            print(f'이미 있는 기사...{i}')
            if retry: continue
            else : break

        article, articleImg = crawling(news[start:end]) # url 추출
        print(f'page in article is...{i}')
        
        # 기사 저장
        if len(article['subTitle']) > 0 :
            q = Article(**article)
            q.save()
            if articleImg is not None:
                ArticleImg(article_id = q.id, articleImg = articleImg).save() # 이미지를 로컬로 다운로드 한 다음에 진행
        else :
            article['subTitle'] = None
            q = Article(**article)
            q.save()        
            if articleImg is not None:
                ArticleImg(article_id = q.id, articleImg = articleImg).save() # 이미지를 로컬로 다운로드 한 다음에 진행

def newswCrowling(url, start = 1, retry = True):
    try:
        for i in range(start, 51): # 일단 50개
            print(f'crawling page...{i}')
            __getpagelist(url + str(i), retry)
    except Exception as e:
        print(f'에러: page={i} \n {e}')

# 'http://biz.khan.co.kr/khan_art_list.html?category=it&page={i}'
# 'http://biz.khan.co.kr/khan_art_list.html?category=science&page={i}'
if __name__ == '__main__':
    newswCrowling('http://biz.khan.co.kr/khan_art_list.html?category=science&page=', 8)

