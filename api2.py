import requests

API_HOST = "https://iotmakers.kt.com:443/api/v1.1/devices?id=K53604D1591100038854"
header = {'Authorization': 'Bearer eyJhbGciOiJSUzI1NiJ9.eyJzdmNfdGd0X3NlcSI6IjEwMDAwMDg4MTAiLCJ1c2VyX25hbWUiOiJLNTM2MDQxMyIsInB1Yl90aW1lIjoxNTkxNzEyMDIyNTk3LCJtYnJfaWQiOiJLNTM2MDQxMyIsIm1icl9zZXEiOiIxMDAwMDA4Njc1IiwibWJyX2NsYXMiOiIwMDAzIiwiYXV0aG9yaXRpZXMiOlsiUk9MRV9PUEVOQVBJIiwiUk9MRV9VU0VSIl0sInBsYXRmb3JtIjoiM01QIiwidGhlbWVfY2QiOiJQVEwiLCJjbGllbnRfaWQiOiJNalppWldNeE9HTmlOamcwTkdVMlpXSmxZell4WW1WaE5UWmxPV0l4WkRFeE5ETXlNakEyT1RnNE9UVTAiLCJhdWQiOlsiSU9ULUFQSSJdLCJ1bml0X3N2Y19jZCI6IjAwMSIsInNjb3BlIjpbInRydXN0Il0sImRzdHJfY2QiOiIwMDEiLCJjb21wYW55IjoiS3QiLCJtYnJfbm0iOiLstZzso7zsnYAiLCJleHAiOjE1OTIzMTIwMjIsImp0aSI6IjkxZjBkOTZlLWVkNmQtNDA4OS1hYWNjLWQwNTI4YTE1ZWVkZCJ9.MvkLfnJndy5e7UruSL2Ga-kOZZKV7G9umkfi1Y--ox_cD5MKDRb4FwaPiBJFoZwa-yetw36FZ7MPaeTW2ySrqCR1U-BSitH752Vm_bCiXbHeygd0NusR7OcQJwb-IFocOidLui1NJX1RGdm4NXA11w5UpkvJblVttb_rAO7e9oMbP870dpQhmCS7ckxAYbSEEbSA3UVGTwBvF40zDxz65183EG2y9I7GfRtx7SXLI63eV7JAMk36QLTiCSxsEH6oj-kDdskCRcSvdKG8tGL11-rIg10_gIFkj-4essJffq-xUb6luNC4PlT3RievUMEA6R8h5TyKR9CznNOrgoN2WQ'}


def req(method):
    url = API_HOST
    if method == 'GET':
        return requests.get(url, headers=header)
    elif method == 'PUT':
        return requests.put(url, headers=header)


def return_value():
    resp = req('GET')
    resp_body = resp.json()
    try:
        return resp_body['data'][0]['sensingTags'][4]['value'], resp_body['data'][0]['sensingTags'][2]['value']
    except:
        return None


if __name__ == '__main__':
    print(return_value())
