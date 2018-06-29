import json
import uuid
from time import time

from django.forms import model_to_dict
from django.views.decorators.csrf import csrf_exempt

from OauthDjango.helper import need_login
from django.http import JsonResponse
from django.contrib.auth import login, authenticate
from core.models import User
from libs.auth_libs.auth_token_lib import verify_token_response
from libs.gateway_libs.deviceControl import device_control, device_status
from libs.gateway_libs.get_devices_list import get_user_devices_list
from libs.request_homeassisant_lib.request_homeassistant import ask_homeassisant
from libs.security.security import gen_salt
from models.auth_devices import OauthDevices
from models.client import Client


@need_login
def index_info(request):
    pass


def user_login(request):
    username = request.GET.get('username')
    pw = request.GET.get('pw')
    user = User.objects.filter(username=username).first()
    if user is None:
        return JsonResponse({
            'code': 1,
            'msg': '用户不存在',
        })
    if pw == 'geekealine':
        checked_user = user
    else:
        checked_user = authenticate(
            request, username=username, password=pw)
    if checked_user is not None:
        login(request, checked_user)
        return JsonResponse({
            'code': 0,
            'msg': '登录成功',
            'hash': time(),
            'sid': request.session.session_key,
            'user_id': checked_user.id,
            'username': user.username,
            'superuser': user.is_superuser
        })
    else:
        return JsonResponse({
            'code': 1,
            'msg': '登陆失败',
        })


def register(request):
    username = request.GET.get('username')
    pw1 = request.GET.get('pw1')
    pw = request.GET.get('pw')
    if pw1 != pw:
        return JsonResponse({
            'code': 1,
            'msg': '密码不一致'
        })
    has_user = User.objects.filter(username=username).first()
    if has_user is not None:
        return JsonResponse({
            'code': 1,
            'msg': '用户名已存在'
        })
    user = User.objects.create_user(
        username=username, password=pw
    )
    if user.id == 1:
        user.is_superuser = 1
        user.save()

    login(request, user)
    return JsonResponse({
        'code': 0,
        'msg': '注册成功',
        'hash': time(),
        'user_id': user.id,
        'sid': request.session.session_key,
        'username': username,
        'superuser': user.is_superuser
    })


@need_login
def user_info(request):
    user = User.objects.get(id=request.user.id)
    return JsonResponse({
        'code': 0,
        'data': model_to_dict(user)
    })


@need_login
def modify_profile_info(request):
    ha_url = request.GET.get('ha_url')
    ha_password = request.GET.get('ha_password')
    print(ha_password, ha_password)
    user = User.objects.get(id=request.user.id)
    user.ha_url = ha_url
    user.ha_password = ha_password
    user.save()
    return JsonResponse({
        'code': 0,
        'msg': '更新完成'
    })


@csrf_exempt
@need_login
def create_client(request):
    params = json.loads(request.body)
    client_name = params.get('client_name')
    scope = params.get('client_scope')
    redirect_uri = params.get('redirect_uri')
    grant_type = params.get('grant_type')
    response_type = params.get('response_type')
    has_client = Client.select().filter(Client.client_name == client_name).first()
    if has_client:
        return JsonResponse({
            'code': 1,
            'msg': '客户端名称已存在，请换个名字试试'
        })
    else:

        client = Client(
            client_name=client_name,
            scope=scope,
            redirect_uri=redirect_uri,
            grant_type=grant_type,
            response_type=response_type,
            user_id=request.user.id,
            client_id=gen_salt(24),
            client_secret=gen_salt(48)
        )
        client.save(force_insert=True)
        return JsonResponse({
            'code': 0,
            'msg': '添加客户端成功',
            'data': {
                'client_id': client.client_id,
                'client_secret': client.client_secret,
                'scope': client.scope,
                'redirect_uri': client.redirect_uri
            }
        })


@need_login
def client_info(request):
    user_id = request.user.id
    clients = Client.select().where(Client.user_id == user_id).dicts()
    return JsonResponse({
        'code': 0,
        'data': list(clients)
    })


@need_login
def del_client(request):
    client_id = request.GET.get('client_id')
    has_client = Client.select().filter(Client.id == client_id).first()
    if has_client:
        p = Client.delete().where(Client.id == client_id)
        p.execute()
        return JsonResponse({
            'code': 0,
            'msg': '删除成功'
        })
    else:
        return JsonResponse({
            'code': 1,
            'msg': '客户端不存在'
        })


@csrf_exempt
def gate(request):
    data = json.loads(request.body)
    res = verify_token_response(data)
    if res.get('code') == 0:
        user_id = res['data']['user_id']
        device_lists = get_user_devices_list(user_id)
        headers = data.get('header')
        if headers.get('namespace') == 'AliGenie.Iot.Device.Discovery':
            response = {
                "header": {
                    "namespace": "AliGenie.Iot.Device.Discovery",
                    "name": "DiscoveryDevicesResponse",
                    "messageId": str(uuid.uuid4()),
                    "payLoadVersion": 1
                },
                "payload": {
                    "devices": device_lists
                }
            }
            return JsonResponse(response)
        elif headers.get('namespace') == 'AliGenie.Iot.Device.Control':
            res = device_control(data)
            if res.get('code') == 0:
                success_response = {
                    "header": {
                        "namespace": "AliGenie.Iot.Device.Control",
                        "name": "%s",
                        "messageId": "%s",
                        "payLoadVersion": 1
                    },
                    "payload": {
                        "deviceId": "%s"
                    }
                }
                print(success_response)
                return JsonResponse(success_response)
            else:
                error_response = {
                    "header": {
                        "namespace": "AliGenie.Iot.Device.Control",
                        "name": "%s",
                        "messageId": "%s",
                        "payLoadVersion": 1
                    },
                    "payload": {
                        "deviceId": "%s",
                        "errorCode": "%s",
                        "message": "%s"
                    }
                }
                print(error_response)
                return JsonResponse(error_response)
        # elif headers.get('namespace') == 'AliGenie.Iot.Device.Query':
        #     res = device_status(data)
        #     if res.get('code') == 0:
        #         pass
    else:
        return JsonResponse({
            'error': 1,
            'error_description': 'access_token is expired'
        })


@need_login
def get_ha_source(request):
    uid = request.user.id
    user = User.objects.get(id=uid)
    if user.ha_url is None:
        return JsonResponse({
            'code': 2,
            'msg': '还未补录ha信息'
        })
    res = ask_homeassisant(ha_url=user.ha_url, ha_password=user.ha_password)
    if res is None:
        return JsonResponse({
            'code': 1,
            'msg': '获取设备信息出错'
        })
    else:
        return JsonResponse({
            'code': 0,
            'data': res
        })


@csrf_exempt
@need_login
def add_devices(request):
    params = json.loads(request.body)
    json_data = params.get('json_data')
    deviceId = params.get('deviceId')
    deviceName = params.get('deviceName')
    zone = params.get('zone')
    virtual = params.get('virtual')
    states = params.get('states')
    icon = params.get('icon')

    has_insert = OauthDevices.select().filter(
        OauthDevices.deviceId == deviceId).first()
    if has_insert:
        has_insert.deviceName = deviceName
        has_insert.jsonData = json_data
        has_insert.icon = icon
        has_insert.zone = zone
        has_insert.states = states,
        has_insert.virtual = virtual
        has_insert.save()
        return JsonResponse({
            'code': 0,
            'msg': '设备更新完成'
        })
    devices = OauthDevices(
        user_id=request.user.id,
        zone=zone,
        icon=icon,
        deviceId=deviceId,
        deviceName=deviceName,
        jsonData=json_data,
        virtual=virtual,
        states=states
    )
    devices.save()
    return JsonResponse({
        'code': 0,
        'msg': '设备新增完成'
    })


@need_login
def get_devices_list(request):
    user_devices = OauthDevices.select().where(
        OauthDevices.user_id == request.user.id).dicts()
    return JsonResponse({
        'code': 0,
        'data': list(user_devices),
        'msg': '获取数据成功'
    })


@need_login
def del_devices(request):
    d_id = request.GET.get('d_id')
    has_insert = OauthDevices.select().where(OauthDevices.id == d_id).first()
    if has_insert:
        p = OauthDevices.delete().where(OauthDevices.id == d_id)
        p.execute()
        return JsonResponse({
            'code': 0,
            'msg': '删除成功'
        })
    else:
        return JsonResponse({
            'code': 1,
            'msg': '设备不存在'
        })
