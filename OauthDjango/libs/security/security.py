#coding:utf-8
# @Time    : 2018/6/5 下午8:53
# @Author  : yanzongzhen
# @Email   : yanzz@catial.cn
# @File    : security.py.py
# @Software: PyCharm
import string
from random import SystemRandom, random
from click._compat import range_type


SALT_CHARS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
_sys_rng = SystemRandom()
UNICODE_ASCII_CHARACTER_SET = string.ascii_letters + string.digits


def gen_salt(length):
    if length <= 0:
        raise ValueError('Salt length must be positive')
    return ''.join(_sys_rng.choice(SALT_CHARS) for _ in range_type(length))


def generate_token(length=30, chars=UNICODE_ASCII_CHARACTER_SET):
    rand = SystemRandom()
    return ''.join(rand.choice(chars) for x in range(length))