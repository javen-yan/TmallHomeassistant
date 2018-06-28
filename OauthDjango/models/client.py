#coding:utf-8
# @Time    : 2018/6/5 下午7:02
# @Author  : yanzongzhen
# @Email   : yanzz@catial.cn
# @File    : client.py
# @Software: PyCharm
from peewee import *
from models.db import mysql_db


class Client(Model):
    id = AutoField(primary_key=True)
    user_id = IntegerField()
    client_name = CharField(max_length=40)
    client_id = CharField(max_length=48)
    client_secret = CharField(max_length=120)
    expires_at = IntegerField(default=0)
    redirect_uri = TextField(default='')
    grant_type = TextField(default='')
    response_type = TextField(default='')
    scope = TextField(default='')

    class Meta:
        database = mysql_db
        db_table = 'client'

