# coding:utf-8
# @Time    : 2018/6/15 上午8:55
# @Author  : yanzongzhen
# @Email   : yanzz@catial.cn
# @File    : urls.py
# @Software: PyCharm
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'index_info', views.index_info),
    url(r'reg', views.register),
    url(r'login', views.user_login),
    url(r'create_client', views.create_client),
    url(r'client_info', views.client_info),
    url(r'del_client', views.del_client),
    url(r'user_info', views.user_info),
    url(r'modify_profile_info', views.modify_profile_info),
    url(r'gate', views.gate),
    url(r'get_ha_source', views.get_ha_source),
    url(r'add_devices', views.add_devices),
    url(r'get_devices_list', views.get_devices_list),
    url(r'del_devices', views.del_devices),
]
