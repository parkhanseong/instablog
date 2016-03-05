from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name


class Post(models.Model): #모델 클래스의 모델 모듈을 상속 받음.
    #DB에 저장된 클래스 이름은 blog_post (앱 이름_모델이름)

    #user = models.ForeignKey(User) #가입한 유저만 글을 쓰게 하는것

    class Meta:
        ordering = ('-created_at', '-pk') #pk와 생성일 역순으로 정렬. 최신글 먼저 보게 하는거임.

    title = models.CharField(max_length=200) #문자열을 받는 최대 길이 설정.
    content = models.TextField() #본문 내용과 같은 글 많이 쓰는데는 TextField
    # tags = models.ManyToManyField('Tag') #문자열로 모델(Tag)을 넣어주면 나중에 모델 관계를 맺어줌.
    created_at = models.DateTimeField(auto_now_add=True) # true를 함으로써 생성즉시 생성일자 넣어줌.
    updated_at = models.DateTimeField(auto_now=True) #업데이트 마다 저장해줌.
    category = models.ForeignKey(Category, default=1)

    is_model_field = False
    #기본키를 만들어주지 않으면 id라는 기본 키를

    def __str__(self):
        return '{} - {}'.format(self.pk, self.title)

class Comment(models.Model):
    post = models.ForeignKey(Post)
    content = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'pK:{} {}번 post'.format(self.pk, self.post.pk)

class Tag(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name
