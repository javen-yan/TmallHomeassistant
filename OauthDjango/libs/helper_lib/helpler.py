#coding:utf-8
# @Time    : 2018/6/7 下午2:15
# @Author  : yanzongzhen
# @Email   : yanzz@catial.cn
# @File    : helpler.py
# @Software: PyCharm
import json

from django.http import HttpResponse

from models.auth_token import AuthToken


def need_login(fn):
    """
    Decorator for views that checks that the user is logged in
    """

    def wrapper(request, *args, **kwargs):
        if request.user.is_anonymous:
            return HttpResponse('Unauthorized', status=401)
        else:
            return fn(request, *args, **kwargs)
    return wrapper


def need_auth(fn):
    def wrapper(request, *args, **kwargs):
        auth = json.loads(request.data.decode()).get('payload')
        if auth:
            token_tmp = AuthToken.select().filter(AuthToken.access_token == auth.get('accessToken')).first()
            if token_tmp:
                if token_tmp.is_access_token_expired():
                    return HttpResponse('access_token_expired', status=401)
                else:
                    return fn(request, *args, **kwargs)
            else:
                return HttpResponse('access_token_invalid', status=401)
        else:
            return HttpResponse('Unauthorized', status=401)
    return wrapper
