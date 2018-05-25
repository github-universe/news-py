from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:newsId>/", views.detail, name="detail"),
    path("open_id/<str:openId>/query/<str:query>/", views.save_query, name="save_query"),
    path("cut/<str:query>/", views.cut, name="cut")

]