# coding:utf-8
import urllib, urllib.request, base64


access_token = '24.de400468096bb90914f3cab87a37d243.2592000.1550149779.282335-15426577'
url = 'https://aip.baidubce.com/rest/2.0/ocr/v1/general?access_token=' + access_token
# 二进制方式打开图文件
f = open(r'jiangzhuang.jpg', 'rb')
# 参数image：图像base64编码
img = base64.b64encode(f.read())
params = {"image": img}
params = urllib.parse.urlencode(params).encode(encoding='UTF8')
request = urllib.request.Request(url, params)
request.add_header('Content-Type', 'application/x-www-form-urlencoded')
response = urllib.request.urlopen(request)
content = response.read()
if (content):
    print(content)
res=open("res.txt",'wb')
res.write(content)
res.close()