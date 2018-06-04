import json

import pysolr
from django.contrib import admin
from .models import News, NewsKeyword, Keyword, NewsPatent
import jieba.analyse
import requests
import os


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
        patents = set()
        for key in keywords:
            if len(patents) >= 5:
                break
            url = os.environ['host'] + '/patent/simple/search?ttl=' + key
            try:
                res = json.loads(requests.get(url).content.decode('utf-8'))
                num = min(5-len(patents), 2)
                for patent in res['patent'][:num]:
                    patents.add(patent)
            except Exception:
                continue

        for patent in patents:
            news_patent = NewsPatent()
            news_patent.news = obj
            news_patent.patent_id = patent
            news_patent.save()

        keys = Keyword.objects.filter(keyword__in=keywords)

        NewsKeyword.objects.filter(news=obj.id).delete()
        key_li = []
        for k in keys:
            nk = NewsKeyword()
            nk.news = obj
            nk.keyword = k
            nk.save()
            key_li.append(k.keyword)

        solr = pysolr.Solr(os.environ['solr_url'], timeout=10)
        result = solr.search("KEYWORD:(" + ' OR '.join(key_li) + ')')
        if len(result) > 10:
            result = result[:10]
        for r in result:
            url = os.environ['host'] + '/wxserver/send_message'
            open_id = r['OPEN_ID']
            data = {
                "open_id": open_id,
                "url": os.environ['fe_host'] + "/detail/" + str(obj.id),
                "title": obj.title,
                "content": obj.content[:100]
            }
            headers = {
                'Content-Type': 'application/json',
            }
            print('SENDING NOTIFICATION: ' + data['open_id'])

            requests.post(url, data=json.dumps(data), headers=headers)


class KeywordAdmin(admin.ModelAdmin):

    fields = ['keyword']

    def save_model(self, request, obj, form, change):
        obj.save()


admin.site.register(News, NewsAdmin)
admin.site.register(Keyword, KeywordAdmin)