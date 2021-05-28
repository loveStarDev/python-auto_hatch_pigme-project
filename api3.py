import requests

API_HOST = "https://iotmakers.kt.com:443/api/v1.1/devices/1/sensingTags"
header = {
    'Authorization': 'Bearer eyJhbGciOiJSUzI1NiJ9.eyJzdmNfdGd0X3NlcSI6IjEwMDAwMDg4MTAiLCJ1c2VyX25hbWUiOiJLNTM2MDQxMyIsInB1Yl90aW1lIjoxNTkxNzEyMDIyNTk3LCJtYnJfaWQiOiJLNTM2MDQxMyIsIm1icl9zZXEiOiIxMDAwMDA4Njc1IiwibWJyX2NsYXMiOiIwMDAzIiwiYXV0aG9yaXRpZXMiOlsiUk9MRV9PUEVOQVBJIiwiUk9MRV9VU0VSIl0sInBsYXRmb3JtIjoiM01QIiwidGhlbWVfY2QiOiJQVEwiLCJjbGllbnRfaWQiOiJNalppWldNeE9HTmlOamcwTkdVMlpXSmxZell4WW1WaE5UWmxPV0l4WkRFeE5ETXlNakEyT1RnNE9UVTAiLCJhdWQiOlsiSU9ULUFQSSJdLCJ1bml0X3N2Y19jZCI6IjAwMSIsInNjb3BlIjpbInRydXN0Il0sImRzdHJfY2QiOiIwMDEiLCJjb21wYW55IjoiS3QiLCJtYnJfbm0iOiLstZzso7zsnYAiLCJleHAiOjE1OTIzMTIwMjIsImp0aSI6IjkxZjBkOTZlLWVkNmQtNDA4OS1hYWNjLWQwNTI4YTE1ZWVkZCJ9.MvkLfnJndy5e7UruSL2Ga-kOZZKV7G9umkfi1Y--ox_cD5MKDRb4FwaPiBJFoZwa-yetw36FZ7MPaeTW2ySrqCR1U-BSitH752Vm_bCiXbHeygd0NusR7OcQJwb-IFocOidLui1NJX1RGdm4NXA11w5UpkvJblVttb_rAO7e9oMbP870dpQhmCS7ckxAYbSEEbSA3UVGTwBvF40zDxz65183EG2y9I7GfRtx7SXLI63eV7JAMk36QLTiCSxsEH6oj-kDdskCRcSvdKG8tGL11-rIg10_gIFkj-4essJffq-xUb6luNC4PlT3RievUMEA6R8h5TyKR9CznNOrgoN2WQ'}

JSON_Motor = '{ \
  "sensingTags": [ \
    { \
      "code": "Motor", \
      "value": "ON" \
    } ] \
}'

JSON_Fan = '{ \
  "sensingTags": [ \
    { \
      "code": "Fan", \
      "value": "ON" \
    } ] \
}'

JSON_Fan_off = '{ \
  "sensingTags": [ \
    { \
      "code": "Fan", \
      "value": "OFF" \
    } ] \
}'


def req(method, dev):
    url = API_HOST
    if method == 'PUT':
        if dev == 'Motor':
            return requests.put(url, headers=header, data=JSON_Motor)
        elif dev == 'Fan':
            return requests.put(url, headers=header, data=JSON_Fan)
        elif dev == "Fan_off":
            return requests.put(url, headers=header, data=JSON_Fan_off)


def return_value():
    resp = req('PUT')
    resp_body = resp.json()
    try:
        return resp_body
    except:
        return None


if __name__ == '__main__':
    print(return_value())
