# encoding:utf-8
import urllib
import urllib.request, base64
import json
import os

'''
在线活体检测
'''
filedir='testimg/fake/xiaoheineg'
jpgdirs=os.listdir(filedir)
request_url = "https://aip.baidubce.com/rest/2.0/face/v3/faceverify"

# 二进制方式打开图文件
total=0;
posnum=0
negnum=0
for jpgname in jpgdirs:
    jpgfullname=os.path.join(filedir,jpgname)
    print(jpgfullname)
    f = open(jpgfullname, 'rb')
    img = base64.b64encode(f.read())
    f.close()
#params = {"image": img}
#img = urllib.parse.urlencode(img).encode(encoding='UTF8')

#params = "[{\"image\":"+str(img,'utf-8')+",\"image_type\":\"BASE64\",\"face_field\":\"age,beauty,expression\"}]"
#
    params = json.dumps(
        [{"image": str(img, 'utf-8'), "image_type": "BASE64", "face_field": "age"}])
    params=params.encode('utf-8')
    access_token = 'XXXXXXXX'
    request_url = request_url + "?access_token=" + access_token
    request = urllib.request.Request(url=request_url, data=params)
    request.add_header('Content-Type', 'application/json')
    #print(request)
    response = urllib.request.urlopen(request)
    content = response.read()
    if content:
        str1=str(content, encoding = "utf-8")
        resdata=eval(str1)
        if str1 is None:
            continue
        if resdata['error_msg']!='SUCCESS':
            continue
        total+=1
        res=resdata['result']['face_liveness']
        if res>0.05:
            posnum+=1
        else:
            negnum+=1
        print(res)
print('total:',total,'  posnum:',posnum,'  negnum:',negnum)
print('acc:',float(posnum)/float(total))
        #print(type(resdata))
