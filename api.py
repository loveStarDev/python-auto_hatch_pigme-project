import time
import requests
import json
from datetime import datetime

API_HOST = "https://iotmakers.kt.com:443/api/v1/streams/K53604D1591100038854/log"
header = {
    'Authorization': 'Bearer eyJhbGciOiJSUzI1NiJ9.eyJzdmNfdGd0X3NlcSI6IjEwMDAwMDg4MTAiLCJ1c2VyX25hbWUiOiJLNTM2MDQxMyIsInB1Yl90aW1lIjoxNTkxNzEyMDIyNTk3LCJtYnJfaWQiOiJLNTM2MDQxMyIsIm1icl9zZXEiOiIxMDAwMDA4Njc1IiwibWJyX2NsYXMiOiIwMDAzIiwiYXV0aG9yaXRpZXMiOlsiUk9MRV9PUEVOQVBJIiwiUk9MRV9VU0VSIl0sInBsYXRmb3JtIjoiM01QIiwidGhlbWVfY2QiOiJQVEwiLCJjbGllbnRfaWQiOiJNalppWldNeE9HTmlOamcwTkdVMlpXSmxZell4WW1WaE5UWmxPV0l4WkRFeE5ETXlNakEyT1RnNE9UVTAiLCJhdWQiOlsiSU9ULUFQSSJdLCJ1bml0X3N2Y19jZCI6IjAwMSIsInNjb3BlIjpbInRydXN0Il0sImRzdHJfY2QiOiIwMDEiLCJjb21wYW55IjoiS3QiLCJtYnJfbm0iOiLstZzso7zsnYAiLCJleHAiOjE1OTIzMTIwMjIsImp0aSI6IjkxZjBkOTZlLWVkNmQtNDA4OS1hYWNjLWQwNTI4YTE1ZWVkZCJ9.MvkLfnJndy5e7UruSL2Ga-kOZZKV7G9umkfi1Y--ox_cD5MKDRb4FwaPiBJFoZwa-yetw36FZ7MPaeTW2ySrqCR1U-BSitH752Vm_bCiXbHeygd0NusR7OcQJwb-IFocOidLui1NJX1RGdm4NXA11w5UpkvJblVttb_rAO7e9oMbP870dpQhmCS7ckxAYbSEEbSA3UVGTwBvF40zDxz65183EG2y9I7GfRtx7SXLI63eV7JAMk36QLTiCSxsEH6oj-kDdskCRcSvdKG8tGL11-rIg10_gIFkj-4essJffq-xUb6luNC4PlT3RievUMEA6R8h5TyKR9CznNOrgoN2WQ'}


def req(path, method):
    url = API_HOST + path
    if method == 'GET':
        return requests.get(url, headers=header)


def return_value():
    end = int(time.mktime(datetime.now().timetuple())) * 1000
    start = end - 10000
    path = '?from=' + str(start) + '&to=' + str(end)
    resp = req(path, 'GET')
    resp_body = resp.json()

    try:
        return resp_body['data']

    except Exception as e:
        print(str(e))
        return None, None


if __name__ == '__main__':
    print(return_value())
