#coding:utf-8
# @Time    : 2018/6/15 下午1:46
# @Author  : yanzongzhen
# @Email   : yanzz@catial.cn
# @File    : auth_devices.py
# @Software: PyCharm
from peewee import *
import time
from models.db import mysql_db


class OauthDevices(Model):
    id = AutoField(primary_key=True)
    user_id = IntegerField()
    icon = TextField()
    virtual = IntegerField(default=0)
    zone = CharField(max_length=64)
    deviceId = CharField(max_length=255)
    deviceName = CharField(max_length=255)
    jsonData = TextField()
    time = TimestampField(default=int(time.time()))
    Del = BooleanField(default=False)
    states = TextField(null=True)

    class Meta:
        database = mysql_db
        db_table = 'auth_devices'


if __name__ == "__main__":
    devices = list(OauthDevices.select(OauthDevices.jsonData).where(OauthDevices.user_id == 1).dicts())
    devices_list = []
    for device in devices:
        devices_list.append(device.get('jsonData'))
    for i in devices_list:
        print(eval(i))