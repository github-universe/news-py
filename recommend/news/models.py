from django.db import models


# Create your models here.
class News(models.Model):

    title = models.CharField(max_length=255)
    content = models.CharField(max_length=4000)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title + self.content


class Keyword(models.Model):

    keyword = models.CharField(max_length=255)

    def __str__(self):
        return self.keyword


class NewsKeyword(models.Model):

    news = models.ForeignKey(News, on_delete=models.CASCADE)
    keyword = models.ForeignKey(Keyword, on_delete=models.CASCADE)


class NewsPatent(models.Model):

    news = models.ForeignKey(News, on_delete=models.CASCADE)
    patent_id = models.CharField(max_length=255)


class User(models.Model):

    id = models.CharField(max_length=255, primary_key=True)
    created_by = models.CharField(max_length=255)
    created_time = models.DateTimeField
    deleted = models.IntegerField
    updated_by = models.CharField(max_length=255)
    updated_time = models.DateTimeField
    openid = models.CharField(max_length=255)
    user_id = models.IntegerField

    class Meta:
        db_table = 'user'
        managed = False

    def __str__(self):
        return self.name


class Tag(models.Model):

    tag = models.CharField(max_length=255)

    def __str__(self):
        return self.tag


