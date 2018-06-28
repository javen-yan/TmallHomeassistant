#coding:utf-8
# @Time    : 2018/6/27 下午3:42
# @Author  : yanzongzhen
# @Email   : yanzz@catial.cn
# @File    : autorun.py
# @Software: PyCharm
import time
from models.auth_token import AuthToken


def print_ts(message):
    print("[%s] %s"%(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), message))


def get_expired_token():
    tokens = AuthToken.select().dicts()
    for token in list(tokens):
        if (token['issued_at'] + token['expires_in']) < time.time():
            old = token['access_token']
            print('%s is expires' % old)
            p = AuthToken.delete().where(AuthToken.access_token == old)
            p.execute()
            print('%s has been deleted' % old)
        else:
            continue


def run(interval):
    print_ts("-"*100)
    print_ts("Starting every %s seconds."%interval)
    print_ts("-"*100)
    while True:
        try:
            # sleep for the remaining seconds of interval
            time_remaining = interval-time.time()%interval
            print_ts("Sleeping until %s (%s seconds)"%((time.ctime(time.time()+time_remaining)), time_remaining))
            time.sleep(time_remaining)
            print_ts("Starting Auto deleteToken.")
            # execute the command
            get_expired_token()
            print_ts("-"*100)
            print_ts("Command status = %s.")
        except Exception as e:
            print(e)


if __name__ == "__main__":
    interval = 43200
    run(interval)