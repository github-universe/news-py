import jieba
from django.http import HttpResponse, JsonResponse
from .models import News, NewsKeyword, Keyword, User
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
import pysolr


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

    def obj_dict(self):
        dic = dict()
        dic['id'] = self.id
        dic['title'] = self.title
        dic['content'] = self.content
        dic['created'] = self.created.strftime("%Y-%m-%d %H:%M")
        dic['keywords'] = self.keywords
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
    return view


def detail(request, newsId):
    news = get_object_or_404(News, pk=newsId)
    view = newsToView(news)
    return HttpResponse(JsonResponse(view.obj_dict(), safe=False), content_type="application/json")


def save_to_solr(uid, openId, query):
    solr = pysolr.Solr('http://localhost:8983/patsnap/keyword', timeout=10)
    doc = dict()
    result = solr.search('USER_ID:' + uid)

    query_gen = jieba.cut(query)
    query_keywords = set()
    for key in query_gen:
        query_keywords.add(key)
    keys = Keyword.objects.filter(keyword__in=query_keywords)
    total_keywords = set()
    if len(result) > 0:
        for doc in result:
            keywords = doc['KEYWORD']
            for key in keywords:
                total_keywords.add(key)
            for key in keys:
                total_keywords.add(key)
            doc['KEYWORD'] = total_keywords
        solr.add(result)
    else:
        doc['USER_ID'] = uid
        doc['OPEN_ID'] = openId
        doc['KEYWORD'] = [k for k in keys]
        solr.add([doc])


def save_query(request, openId, query):
    user = User.objects.filter(openid=openId)
    if len(user) == 1:
        save_to_solr(user[0].id, openId, query)
    return HttpResponse('success')
