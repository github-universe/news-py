import jieba.analyse
from django.http import HttpResponse, JsonResponse
from .models import News, NewsKeyword, Keyword, User, NewsPatent
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
import pysolr
import json
import requests
import os


class NewsListView:

    def __init__(self):
        self.news = []
        self.pageNum = 0
        self.pageSize = 10
        self.total = 0

    def obj_dict(self):
        dic = dict()
        dic['news'] = [n.obj_dict() for n in self.news]
        dic['pageNum'] = self.pageNum
        dic['pageSize'] = self.pageSize
        dic['total'] = self.total
        return dic


class NewsView:
    def __init__(self, news):
        self.id = news.id
        self.title = news.title
        self.content = news.content
        self.created = news.created
        self.keywords = []
        self.patents = []

    def obj_dict(self):
        dic = dict()
        dic['id'] = self.id
        dic['title'] = self.title
        dic['content'] = self.content
        dic['created'] = self.created.strftime("%Y-%m-%d %H:%M")
        dic['keywords'] = self.keywords
        dic['patents'] = self.patents
        return dic


# Create your views here.
def index(request):
    newses = News.objects.all().order_by('-created')
    pageSize = 10 if request.GET.get('pageSize') is None else request.GET.get('pageSize')
    page = 1 if request.GET.get('pageNum') is None else request.GET.get('pageNum')
    paginator = Paginator(newses, pageSize)

    news_res = paginator.page(page)

    news_views = []
    for n in news_res:
        view = newsToView(n)
        news_views.append(view)
    nl = NewsListView()
    nl.news = news_views
    nl.pageSize = pageSize
    nl.pageNum = news_res.number
    nl.total = paginator.count

    return HttpResponse(JsonResponse(nl.obj_dict(), safe=False), content_type='application/json')


def newsToView(n):
    view = NewsView(n)
    for newsKeyword in NewsKeyword.objects.filter(news=n):
        view.keywords.append(newsKeyword.keyword.keyword)
    if len(view.keywords) > 3:
        view.keywords = view.keywords[:3]
    patents = NewsPatent.objects.filter(news=n)
    for patent in patents:
        view.patents.append(patent.patent_id)
    return view


def detail(request, newsId):
    news = get_object_or_404(News, pk=newsId)
    view = newsToView(news)
    return HttpResponse(JsonResponse(view.obj_dict(), safe=False), content_type="application/json")


def get_similar_words(query_keywords):
    similar_words = []
    if len(query_keywords) > 0:
        url = os.environ['qa_host'] + 'compute/kwd_helper_cn/'
        data = {
            "data": {
                "words": ','.join(query_keywords),
                "topn": 3
            },
            "session": "string"
        }
        headers = {
            'content-type': 'application/json',
            'X-PatSnap-Version': 'v1'
        }
        res = requests.post(url, data=json.dumps(data), headers=headers)
        res_data = json.loads(res.content.decode('utf-8'))['data']
        for d in res_data:
            similar_words.append(d['keyword'])
    return similar_words


def save_to_solr(uid, openId, query):
    solr = pysolr.Solr(os.environ['solr_url'], timeout=10)
    doc = dict()
    result = solr.search('USER_ID:' + uid)

    query_keywords = set(jieba.analyse.extract_tags(query, topK=3))

    similar_words = get_similar_words(query_keywords)
    if len(result.docs) > 0:
        for doc in result.docs:
            if 'KEYWORD' in doc.keys():
                keywords = doc.get('KEYWORD')
            else:
                keywords = []
            total_keywords = set()
            for key in keywords:
                total_keywords.add(key)
            for key in query_keywords:
                total_keywords.add(key)
            for key in similar_words:
                total_keywords.add(key)
            doc['KEYWORD'] = list(total_keywords)
        solr.add(result)
    else:
        doc['USER_ID'] = uid
        doc['OPEN_ID'] = openId
        doc['KEYWORD'] = list(query_keywords) + similar_words
        solr.add([doc])


def cut(request, query):
    words = jieba.cut(query)
    return HttpResponse(JsonResponse([word for word in words], safe=False), content_type='application/json')


def save_query(request, openId, query):
    users = User.objects.filter(openid=openId)
    if len(users) > 0:
        for u in users:
            save_to_solr(u.id, openId, query)
    return HttpResponse('success')

