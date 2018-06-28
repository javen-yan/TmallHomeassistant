#coding:utf-8
# @Time    : 2018/6/5 下午6:57
# @Author  : yanzongzhen
# @Email   : yanzz@catial.cn
# @File    : db.py
# @Software: PyCharm
from OauthDjango.settings import DATABASES
from peewee import MySQLDatabase

mysql_db = MySQLDatabase(
    database=DATABASES['default']['NAME'],
    user=DATABASES['default']['USER'],
    password=DATABASES['default']['PASSWORD'],
    host=DATABASES['default']['HOST'],
    port=int(DATABASES['default']['PORT'])
)
