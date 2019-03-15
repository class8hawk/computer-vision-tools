import os
import cv2
import numpy as np
import sys
import random

orgimgsize=96
cropimgsize=80
orgimgdir='fakehead'

distdir=orgimgdir+'_cropadd_'+str(cropimgsize)

if not os.path.exists(distdir):
    os.makedirs(distdir)
    
    
imgfilenames=os.listdir(orgimgdir)
total=len(imgfilenames)
for index,imgname in enumerate(imgfilenames):
    imgfullname=os.path.join(orgimgdir,imgname)
    imgorg=cv2.imread(imgfullname)
    imgresize=cv2.resize(imgorg,(orgimgsize,orgimgsize))
    if index%100==0:
        print('current:',index,'total:',total)
    for i in range(30):
        minx=random.randint(0,orgimgsize-cropimgsize)
        miny=random.randint(0,orgimgsize-cropimgsize)
        cropimg=imgresize[miny:miny+cropimgsize,minx:minx+cropimgsize]
        savename=os.path.splitext(imgname)[0]+'_'+str(i+1)+os.path.splitext(imgname)[1]
        cv2.imwrite(os.path.join(distdir,savename),cropimg)


