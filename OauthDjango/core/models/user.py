#coding:utf-8
# @Time    : 2018/6/15 上午9:09
# @Author  : yanzongzhen
# @Email   : yanzz@catial.cn
# @File    : user.py
# @Software: PyCharm

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ha_url = models.TextField(null=True)
    ha_password = models.CharField(max_length=200)

    def get_user_id(self):
        return self.id

    class Meta:
        db_table = 'user'