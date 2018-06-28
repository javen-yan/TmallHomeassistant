#coding:utf-8
# @Time    : 2018/6/15 上午9:24
# @Author  : yanzongzhen
# @Email   : yanzz@catial.cn
# @File    : helper.py
# @Software: PyCharm

from django.http import HttpResponse


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
