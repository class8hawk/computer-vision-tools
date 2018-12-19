import os
import cv2
import numpy as np
import sys



def getimgfromdir(dirs,distdir,index):
    thisindex=index
    for eachdir in dirs:
        print(eachdir)
        imgs=os.listdir(eachdir)
        print('img num:',len(imgs))
        for jpgname in imgs:
            jpgnamedir=os.path.join(eachdir,jpgname)
            src = cv2.imdecode(np.fromfile(jpgnamedir,dtype = np.uint8),-1)
            
            if src is None:
                print(jpgnamedir)
                continue
            thisindex+=1
            Resizeimg = cv2.resize(src, (procsize,procsize))
            #print(Resizeimg.shape)
            distjpgname=os.path.join(distdir,str(thisindex)+'.jpg')
            cv2.imencode('.jpg',Resizeimg)[1].tofile(distjpgname)
            
def getimgfromdirflip(dirs,distdir,index,isflip):
    thisindex=index
    for eachdir in dirs:
        print(eachdir)
        imgs=os.listdir(eachdir)
        print('img num:',len(imgs))
        for jpgname in imgs:
            jpgnamedir=os.path.join(eachdir,jpgname)
            src = cv2.imdecode(np.fromfile(jpgnamedir,dtype = np.uint8),-1)
            
            if src is None:
                print(jpgnamedir)
                continue
            thisindex+=1
            Resizeimg = cv2.resize(src, (procsize,procsize))
            #print(Resizeimg.shape)
            distjpgname=os.path.join(distdir,str(thisindex)+'.jpg')
            cv2.imencode('.jpg',Resizeimg)[1].tofile(distjpgname)
            if isflip:
                flipdistjpgname=os.path.join(distdir,str(thisindex)+'_flip.jpg')
                flipimag=cv2.flip(Resizeimg,1)
                cv2.imencode('.jpg',flipimag)[1].tofile(flipdistjpgname)


procsize=128
posdist='posres'
negdist='negres'

possrcdir=[]

possrcdir.append(r'部分室外数据')
possrcdir.append(r'数据2')
possrcdir.append(r'门口数据')
possrcdir.append(r'以前数据')

negsrcdir=[]
negsrcdir.append(r'negceleba非活体\1208NEGCeleba')
negsrcdir.append(r'非活体\非活体2部分')
negsrcdir.append(r'非活体\非活体室外')

if not os.path.exists(posdist):
    os.makedirs(posdist)
if not os.path.exists(negdist):
    os.makedirs(negdist)


posnum=0
negnum=0
getimgfromdirflip(possrcdir,posdist,posnum,1)
getimgfromdirflip(negsrcdir,negdist,negnum,1)

        
        
'''
passnum=0
for index,jpgname in enumerate(os.listdir(srcdir)):
    jpgnamedir=os.path.join(srcdir,jpgname)
    #src = cv2.imdecode(np.fromfile(jpgnamedir,dtype = np.uint8),-1)
    src=cv2.imread(jpgnamedir)
    print(jpgnamedir)
    if src is None:
        print(jpgnamedir)
        continue
    print(src.shape)
    Resizeimg = cv2.resize(src, (128,128))
    #cv2.imshow('HSV',HSV)
    #cv2.waitKey(0)
    #dst=src[51:99,51:99]
    #dst=src[24:72,24:72]
    savedir=os.path.join(dstdir,jpgname)
    #cv2.imencode('.jpg',Resizeimg)[1].tofile(savedir)
    cv2.imwrite(savedir,Resizeimg)
    print(index)
'''