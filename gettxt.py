import os
import cv2
import numpy as np
import sys

def gettxtfromimg(filetxt,label,imgfilename):
    imgfilenames=os.listdir(imgfilename)
    print(imgfilename+' len:'+str(len(imgfilenames)))
    for imgname in imgfilenames:
        filetxt.write(imgfilename+'/'+imgname+' '+str(label)+'\n')
istest=0
if istest:
    #negfileimgs='test'
    #posfileimgs='test'
    pass
else:
    negfileimgs='train/0917neg_crop8080'
    posfileimgs='train/0917pos_crop8080'
if istest:
    filetxt=open('test_size3090_d0904.txt','w')
else:
    filetxt=open('train_size4580_d1011.txt','w')

gettxtfromimg(filetxt,0,'close_aug')

  
gettxtfromimg(filetxt,1,'open_aug')

filetxt.close()



