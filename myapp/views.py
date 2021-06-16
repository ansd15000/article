from django.http import HttpResponse
# from django.http.response import JsonResponse
# Create your views here.
# from django.template import loader
from django.shortcuts import render # template 로 html 파일 렌더링하기
from django.views import View
from .models import Article, ArticleImg
from .crawling import crawling
import copy

# Create your views here.
# http://biz.khan.co.kr/khan_art_list.html?category=it
def index(request):
    return HttpResponse("Hello, Happy world")
    # template = loader.get_template('./t.html')
    # return render(request, 't.html')

class Test(View):
    def get(self, request):
        data = request.GET
        if len(data) == 0 :
            return render(request, 't.html')
        return HttpResponse("Hello, Happy world")
        # print(Article.)
        # a = '2021.06.13 21:36'
        # articleTime = datetime.strptime(a, '%Y.%m.%d %H:%M') # 초 정보가 없어서 타임테이블은 불가능
        # a = Article(news_agency= '0', tag = 'Tprtm', title = '아씨발쎅쓰하고싶다', subTitle = '오랄쎅쓰' ,date = articleTime)
        # a.save()

        # print(Article.objects.all())
        # print(Article.objects.filter(id = 1))
        # print(Article.objects.filter(title__contains='아씨발쎅쓰하고싶다').values()) # 쿼리셋은 데이터확인을 위해 values()를 사용한다.
        # 이때 values 인자값에 컬럼명을 넣어 필요한 데이터만 꺼내올수도 있음

    def post(self, request):
        print('???')
        article, articleImg = crawling('http://biz.khan.co.kr/khan_art_view.html?artid=202106082157015&code=930100&med_id=khan')
        # a = Article.objects.all()
        # a.delete()
        # print(Article.objects.all())
        for subtitle in article['subTitle']:
            news = copy.deepcopy(article)
            news['subTitle'] = subtitle
            Article(**news).save()


        
        # print(article['subTitle'])
        # Article(**article).save() # subtitle이 배열이니까 2개로 나눠서 넣으셈
        # ArticleImg(articleImg).save() # 이미지를 로컬로 다운로드 한 다음에 진행하자



        return HttpResponse("Put 요청을 잘받았다")

    def put(self, request):
        return HttpResponse("Put 요청을 잘받았다")

    def delete(self, request):
        return HttpResponse("Delete 요청을 잘받았다")

# def test(request):
#     template = loader.get_template('t.html')
#     a = request.body.decode('utf-8')
#     print(a)
