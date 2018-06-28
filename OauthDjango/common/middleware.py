# coding:utf-8
# @Time    : 2018/6/15 上午9:21
# @Author  : yanzongzhen
# @Email   : yanzz@catial.cn
# @File    : middleware.py
# @Software: PyCharm

from django.contrib.sessions.middleware import SessionMiddleware
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from models.db import mysql_db


class OauthSessionMiddleware(SessionMiddleware):

    def process_request(self, request):
        sid = request.META.get('HTTP_SID') or request.GET.get(
            'sid') or request.POST.get('sid')
        print('sid: ', sid)
        if sid != 'null' and sid is not None:
            session_key = sid
            request.session = self.SessionStore(session_key)
        else:
            super().process_request(request)


class PeeweeConnectionMiddleware(MiddlewareMixin):

    def process_request(self, request):
        if request.method == 'OPTIONS':
            return HttpResponse('跳过 options 检查')
        print('----open---')
        mysql_db.connect()

    def process_response(self, request, response):
        print('----db----is close:', mysql_db.is_closed())
        if not mysql_db.is_closed():
            mysql_db.close()
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Headers"] = "*"
        return response
