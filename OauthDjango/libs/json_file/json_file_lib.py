# coding:utf-8
# @Time    : 2018/6/1 下午3:37
# @Author  : yanzongzhen
# @Email   : yanzz@catial.cn
# @File    : json_file_lib.py
# @Software: PyCharm
import os
import json

json_file_path = os.path.join(
os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)))),
    'count.json')


def json_file_redaer():
    with open(json_file_path, encoding='utf-8') as f:
        line = f.readline()
        d = json.loads(line)
        return d


def json_write(params):
    with open(json_file_path, 'w', encoding='utf-8') as f:
        print(params)
        t = json.dumps(params)
        f.write(t)


if __name__ == "__main__":
    count = json_file_redaer()
    print(count)
