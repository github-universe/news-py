from django.contrib import admin
from .models import News, NewsKeyword, Keyword
import jieba


# Register your models here.
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'created')
    search_fields = ['title']
    fields = ['title', 'content']

    def save_model(self, request, obj, form, change):
        super(NewsAdmin, self).save_model(request, obj, form, change)
        data_dict = request.POST
        title = data_dict['title']
        content = data_dict['content']
        ttl_gen = jieba.cut(title)
        content_gen = jieba.cut(content)
        keywords = set()
        for key in ttl_gen:
            keywords.add(key)
        for key in content_gen:
            keywords.add(key)
        keys = Keyword.objects.filter(keyword__in=keywords)

        NewsKeyword.objects.filter(news=obj.id).delete()
        if len(keys) > 5:
            keys = keys[:5]
        for k in keys:
            nk = NewsKeyword()
            nk.news = obj
            nk.keyword = k
            nk.save()



class KeywordAdmin(admin.ModelAdmin):

    fields = ['keyword']

    def save_model(self, request, obj, form, change):
        obj.save()


admin.site.register(News, NewsAdmin)
admin.site.register(Keyword, KeywordAdmin)