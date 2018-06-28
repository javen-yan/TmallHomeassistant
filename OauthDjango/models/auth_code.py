#coding:utf-8
# @Time    : 2018/6/5 下午7:19
# @Author  : yanzongzhen
# @Email   : yanzz@catial.cn
# @File    : auth_code.py
# @Software: PyCharm
import time
from peewee import *
from models.db import mysql_db


class AuthCode(Model):
    user_id = IntegerField()
    code = CharField(max_length=120,unique=True)
    client_id = CharField(max_length=48)
    redirect_uri = TextField(default='')
    response_type = TextField(default='')
    scope = TextField(default='')
    nonce = TextField(null=True)
    auth_time = IntegerField(default=lambda: int(time.time()))

    def is_expired(self):
        return self.auth_time + 300 < time.time()

    def get_redirect_uri(self):
        return self.redirect_uri

    def get_scope(self):
        return self.scope

    def get_nonce(self):
        return self.nonce

    def get_auth_time(self):
        return self.auth_time

    class Meta:
        database = mysql_db
        db_table = 'auth_code'

