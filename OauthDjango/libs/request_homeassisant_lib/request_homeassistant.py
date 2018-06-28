#coding:utf-8
# @Time    : 2018/6/14 下午4:44
# @Author  : yanzongzhen
# @Email   : yanzz@catial.cn
# @File    : request_homeassistant.py
# @Software: PyCharm
import requests
import json


def ask_homeassisant(ha_url, ha_password):
    url = ha_url + '/api/states?api_password=' + ha_password
    res = requests.get(url=url,headers={'Content-Type': 'application/json'})
    if res.status_code == 200:
        devices = json.loads(res.text)
        parser_device = []
        for device in devices:
            d = device.get('entity_id').split('.')
            parser_device.append({d[0]: device.get('entity_id')})
        res = parser_list(parser_device)
        return res
    else:
        return None


def parser_list(params):
    res = []
    temp = {}
    for param in params:
        for k,v in param.items():
            temp.setdefault(k, []).append(v)
        res.append(temp)
    return temp


if __name__ == "__main__":
    # ha_url = 'http://ha.ealine.cn'
    # ha_password = '127521yzz'
    #
    # datas = ask_homeassisant(ha_url,ha_password)
    # print(datas)
    p = [{"group": "group.jinan_room"}, {"sensor": "sensor.phicomm_temperature"}, {"sun": "sun.sun"}, {"updater": "updater.updater"}, {"sensor": "sensor.phicomm_hcho"}, {"sensor": "sensor.phicomm_pm25"}, {"sensor": "sensor.phicomm_humidity"}]
    res = parser_list(p)
    print(res)