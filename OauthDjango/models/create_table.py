# coding:utf-8
# Created by wyc at 2018/3/21

import importlib
import os
import sys
base = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../')
base = os.path.abspath(base)
sys.path.append(base)
print(sys.path)

c = [
    'client.Client',
    'auth_devices.OauthDevices',
    'auth_code.AuthCode',
    'auth_token.AuthToken'
]


def drop_table():
    for i in c:
        _m, _c = i.split('.')
        print('- drop %s' % _c)
        getattr(importlib.import_module(_m, 'models'), _c).drop_table()


def create_table():
    for i in c:
        _m, _c = i.split('.')
        print('+ create %s' % _c)
        getattr(importlib.import_module(_m, 'models'), _c).create_table()


if __name__ == '__main__':
    sys.path.append('.')
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'create'
    print(cmd)
    if cmd == 'rebuild':
        drop_table()
        create_table()
    elif cmd == 'create':
        create_table()
    elif cmd == 'drop':
        drop_table()




