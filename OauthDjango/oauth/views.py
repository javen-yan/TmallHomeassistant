from django.http import JsonResponse
from django.shortcuts import redirect
from urllib.parse import quote_plus

from django.views.decorators.csrf import csrf_exempt
from OauthDjango.settings import HOST
from libs.auth_libs.auth_code_lib import gen_auth_code, verify_auth_code
from libs.auth_libs.auth_token_lib import gen_token_return, gen_refresh_token_return
from models.client import Client


def authorize(request):
    client_id = request.GET.get('client_id')
    redirect_url = request.GET.get('redirect_uri')
    raw_redirect_url = redirect_url.split('?')[0]
    _state = request.GET.get('state')
    _redirect_url = redirect_url + '&state=%s' % _state
    print('view_redirect_url', _redirect_url)
    response_type = request.GET.get('response_type')
    grant = Client.select().filter(Client.client_id == client_id).first()
    if grant:
        if grant.response_type != response_type:
            return JsonResponse(
                {'code': 1, 'msg': 'Not support response_type'})
        else:
            if raw_redirect_url == grant.redirect_uri:
                _redirect_url = quote_plus(_redirect_url)
                uri = HOST + '/#/auth/%s/%s/%s' % (_redirect_url, grant.client_name, grant.scope)
                # uri = 'http://127.0.0.1:8080' + '/#/auth/%s/%s/%s' % (_redirect_url, grant.client_name, grant.scope)
                return redirect(uri)
            else:
                return JsonResponse(
                    {'code': 1, 'msg': 'incorrect redirect_uri'})
    else:
        return JsonResponse({'code': 1, 'msg': 'grant Not such client'})


def authorize_confirm(request):
    redirect_uri = request.GET.get('redirect_uri')
    client_name = request.GET.get('name')
    grant = Client.select().filter(Client.client_name == client_name).first()
    if grant:
        uri = gen_auth_code(grant,redirect_uri,request.user)
        print(uri)
        return JsonResponse({
            'code': 0,
            'url': uri
        })
    else:
        return JsonResponse({
            'code': 1,
            'msg': '没有此用户'
        })


@csrf_exempt
def gent_token(request):
    if request.method == 'POST':
        params = request.POST
        grant_type = params.get('grant_type')
        if grant_type == 'authorization_code':
            res = verify_auth_code(params)
            if res.get('code') == 1:
                return JsonResponse({
                    'error': 1,
                    'error_description': res.get('msg')
                })
            else:
                response = gen_token_return(params)
                if response.get('code') == 1:
                    return JsonResponse({
                        'error': 1,
                        'error_description': res.get('msg')
                    })
                else:
                    res_data = response.get('data')
                    return JsonResponse({
                        'access_token': res_data.access_token,
                        'refresh_token': res_data.refresh_token,
                        'expires_in': res_data.expires_in,
                    })
        else:
            response = gen_refresh_token_return(params)
            if response.get('code') == 1:
                return JsonResponse({
                    'error': 1,
                    'error_description': response.get('msg')
                })
            else:
                res_data = response.get('data')
                return JsonResponse({
                    'access_token': res_data.access_token,
                    'refresh_token': res_data.refresh_token,
                    'expires_in': res_data.expires_in,
                })
    else:
        return JsonResponse({
            'error': 1,
            'error_description': 'not support get method'
        })