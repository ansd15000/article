from django.http import HttpResponse
from django.http.response import JsonResponse
# Create your views here.
from django.template import loader
from django.shortcuts import render
from django.views import View
import json
import os
from .models import Article

from datetime import datetime
import time

# Create your views here.
# http://biz.khan.co.kr/khan_art_list.html?category=it
def index(request):
    return HttpResponse("Hello, Happy world")
    # template = loader.get_template('./t.html')
    # return render(request, 't.html')

class Test(View):
    def get(self, request):
        data = request.GET
        # if len(data) == 0 :
        #     return render(request, 't.html')
        # print(Article.)
        # a = '2021.06.13 21:36'
        # articleTime = datetime.strptime(a, '%Y.%m.%d %H:%M') # 초 정보가 없어서 타임테이블은 불가능
        # a = Article(news_agency= '0', tag = 'Tprtm', title = '아씨발쎅쓰하고싶다', subTitle = '오랄쎅쓰' ,date = articleTime)
        # a.save()

        # print(Article.objects.all())
        # print(Article.objects.filter(id = 1))
        # print(Article.objects.filter(title__contains='아씨발쎅쓰하고싶다').values()) # 쿼리셋은 데이터확인을 위해 values()를 사용한다.
        # 이때 values 인자값에 컬럼명을 넣어 필요한 데이터만 꺼내올수도 있음

        return HttpResponse("get 요청을 잘받았다")

    def post(self, request):
        return HttpResponse("Put 요청을 잘받았다")

    def put(self, request):
        return HttpResponse("Put 요청을 잘받았다")

    def delete(self, request):
        return HttpResponse("Delete 요청을 잘받았다")

# def test(request):
#     template = loader.get_template('t.html')
#     a = request.body.decode('utf-8')
#     print(a)
