import json

import requests


def test_gate():
    data = {
        'header': {
            'messageId': 'ec7af886-544f-447e-906a-d957d227d9fd',
            'name': 'DiscoveryDevices',
            'namespace': 'AliGenie.Iot.Device.Discovery',
            'payLoadVersion': 1},
        'payload': {
            'accessToken': 'YUe3b15yk2XEYjXbWAGRDRMoraN9lwHl5tlHy8rIxnQy2STx'
        }
    }
    res = requests.post(
        url='https://oauth.ealine.cn/v1/api/gate',
        data=json.dumps(data),
        headers={
            'Content-Type': 'application/json'})
    if res.status_code == 200:
        print(json.loads(res.text))


if __name__ == "__main__":
    test_gate()