#coding:utf-8
# @Time    : 2018/6/5 下午7:10
# @Author  : yanzongzhen
# @Email   : yanzz@catial.cn
# @File    : auth_token.py
# @Software: PyCharm
import time
from peewee import *
from models.db import mysql_db


class AuthToken(Model):
    user_id = IntegerField()
    client_id = CharField(max_length=48)
    token_type = CharField(max_length=40)
    access_token = CharField(max_length=255, unique=True)
    refresh_token = CharField(max_length=255, index=True)
    scope = TextField(default='')
    revoked = BooleanField(default=False)
    issued_at = IntegerField(default=lambda: int(time.time()))
    expires_in = IntegerField(default=0)

    def get_scope(self):
        return self.scope

    def get_expires_in(self):
        return self.expires_in

    def get_expires_at(self):
        return self.issued_at + self.expires_in

    def is_refresh_token_expired(self):
        expires_at = self.issued_at + self.expires_in * 2
        return expires_at < time.time()

    def is_access_token_expired(self):
        expires_at = self.issued_at + self.expires_in
        return expires_at < time.time()

    class Meta:
        database = mysql_db
        db_table = 'auth_token'

