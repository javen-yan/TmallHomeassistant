# coding:utf-8
# @Time    : 2018/6/6 下午8:06
# @Author  : yanzongzhen
# @Email   : yanzz@catial.cn
# @File    : auth_code_lib.py
# @Software: PyCharm
from libs.security.security import gen_salt
from models.auth_code import AuthCode
from models.client import Client


def gen_auth_code(grant, redirect_uri,grant_user):
    code = gen_salt(24)
    authcode_tmp = AuthCode(
        user_id=grant_user.id,
        client_id=grant.client_id,
        redirect_uri=redirect_uri,
        scope=grant.scope,
        response_type=grant.response_type,
        code=code
    )
    authcode_tmp.save()
    _redirect_uri = redirect_uri + '&code=%s' % code
    print('redirect', _redirect_uri)
    return _redirect_uri


def verify_auth_code(data):
    client = Client.select().filter(Client.client_id == data.get('client_id')).first()
    if client:
        if data.get('client_secret') != client.client_secret:
            return {'code': 1, 'msg': 'client_secret is error'}
        else:
            authcode = AuthCode.select().filter(AuthCode.code == data.get('code')).first()
            if authcode:
                if authcode.is_expired():
                    return {'code': 1, 'msg': 'code is_expired'}
                else:
                    return {'code': 0, 'msg': 'code is ok'}
            else:
                return {'code': 1, 'msg': 'code is error'}
    else:
        return {'code': 1, 'msg': 'code verify error no such client'}

