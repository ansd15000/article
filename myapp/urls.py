from django.urls import path

from . import views
# 2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
urlpatterns = [
    path('', views.index), # myapp의 디폴트 주소
    path('test/', views.Test.as_view(), name = 'test')
]