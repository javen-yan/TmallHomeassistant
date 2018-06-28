#coding:utf-8
# @Time    : 2018/6/26 下午4:18
# @Author  : yanzongzhen
# @Email   : yanzz@catial.cn
# @File    : get_devices_list.py
# @Software: PyCharm
from models.auth_devices import OauthDevices


def get_user_devices_list(user_id):
    devices = list(OauthDevices.select(OauthDevices.jsonData).where(OauthDevices.user_id == user_id).dicts())
    devices_list = []
    for device in devices:
        devices_list.append(eval(device.get('jsonData')))
    return devices_list


if __name__ == "__main__":
    print(get_user_devices_list(1))