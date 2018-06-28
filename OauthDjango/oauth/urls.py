#coding:utf-8
# @Time    : 2018/6/15 上午8:54
# @Author  : yanzongzhen
# @Email   : yanzz@catial.cn
# @File    : urls.py
# @Software: PyCharm
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^authorize$', views.authorize),
    url(r'^authorize_confirm$', views.authorize_confirm),
    url(r'^token$', views.gent_token)
]