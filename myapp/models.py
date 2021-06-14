from django.db import models

# Create your models here.

# 기사 테이블 
# 언론사 명(혹은 숫자), 기사 분류, 제목, 부제목, 기사 내용, 날짜, 이미지(저장해서 사용할 예정)
class Article(models.Model):
    id = models.AutoField(primary_key = True) # 안쓰면 자동으로 생성된다고 함
    news_agency = models.PositiveSmallIntegerField() # 0 ~ 32767 언론사는 숫자로 분류하자
    tag = models.CharField(max_length=10) # 기사분류
    title = models.CharField(max_length=70) # 기사제목
    subTitle = models.CharField(max_length=140) # 기사 부제목
    main = models.TextField() # 기사 내용
    date = models.DateField() # 날짜
    
    class Meta:
        ordering = ['date']

    def __str__(self):
        return str(self.id)

class ArticleImg(models.Model):
    article = models.ForeignKey(Article, on_delete= models.CASCADE)
    articleImg = models.FileField(upload_to = 'articleImgs/', null= True) # match 로 정규식 조건줄수있음
    
    def __str__(self):
        return self.article

# 사용자 테이블 
# 사용자 아이디, 비번, 성별,
class user(models.Model):
    user_id = models.CharField(max_length = 30, primary_key = True)
    user_pw = models.TextField(max_length = 64) # sha256 쓸꺼임
    gender = models.CharField(max_length = 1) # 남,여
    nickname = models.CharField(max_length = 20)

    def __str__(self):
        return self.user_id

# 사용자의 기사정보 
# 언론글, 블라인드(T/F), 좋아요, 
class userHistory(models.Model): # 유저가 본 기사가 저장되며 좋/싫 누르거나 메인에서 블라인드 처리할 수 있음.
    user = models.ForeignKey(user, on_delete = models.CASCADE)     # user 정보 삭제되면 같이 삭제하기
    article = models.ForeignKey(Article, on_delete=models.CASCADE) # 마찬가지
    blind = models.BooleanField(default = False)
    isgood = models.BooleanField(default = False)

    def __str__(self):
        return self.user

# json쓰는거 안쓰는거 두개로 해보기
# 사용자 기사정보
# 알아두자! SQL은 한놈한테 데이터가 여러개면 걍 레코드 한줄 더 쓴다!
