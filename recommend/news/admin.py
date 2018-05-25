import pysolr
from django.contrib import admin
from .models import News, NewsKeyword, Keyword
import jieba.analyse


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
        keywords = jieba.analyse.extract_tags(title + content, topK=10)

        keys_saved = set()

        for k in Keyword.objects.filter(keyword__in=keywords):
            keys_saved.add(k.keyword)

        for k in keywords:
            if k not in keys_saved:
                new_key = Keyword()
                new_key.keyword = k
                new_key.save()

        keys = Keyword.objects.filter(keyword__in=keywords)

        NewsKeyword.objects.filter(news=obj.id).delete()
        key_li = []
        for k in keys:
            nk = NewsKeyword()
            nk.news = obj
            nk.keyword = k
            nk.save()
            key_li.append(k.keyword)

        solr = pysolr.Solr('http://localhost:8983/patsnap/keyword', timeout=10)
        result = solr.search("KEYWORD:(" + ' OR '.join(key_li) + ')')
        for r in result:
            # TODO send notification
            print(r)


class KeywordAdmin(admin.ModelAdmin):

    fields = ['keyword']

    def save_model(self, request, obj, form, change):
        obj.save()


admin.site.register(News, NewsAdmin)
admin.site.register(Keyword, KeywordAdmin)