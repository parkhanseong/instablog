from django.db import models
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=40)

class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=200, db_index=True)
    content = models.TextField()
    tags = models.ManyToManyField('Tag', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_model_field = False

#    class Meta:
#        ordering = ('-updated_at', '-pk', )

    def __str__(self):
        return '{} - {}'.format(self.pk, self.title)


class Comment(models.Model):
    post = models.ForeignKey(Post)
    content = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} of {}'.format(self.pk, self.post.pk)


class Tag(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name
