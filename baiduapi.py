import urllib, urllib.request, sys
import ssl

# client_id 为官网获取的AK， client_secret 为官网获取的SK
host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=v2aMfYDr7PvcI6DGUoh9byEh&client_secret=hxFIGWcr9IDs43j49giIk3HkLiTkqEPt'
request = urllib.request.Request(host)
request.add_header('Content-Type', 'application/json; charset=UTF-8')
response = urllib.request.urlopen(request)
content = response.read()
if (content):
    print(content)
taken=open("baiduapi.txt",'wb+')
taken.write(content)
taken.close()