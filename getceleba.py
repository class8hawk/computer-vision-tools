import sys
import os
import cv2
import argparse
import numpy as np
import base64
from easydict import EasyDict as edict
import numpy.random as npr

img_celeba_dir='img_celeba'
bboxlist=open('list_bbox_celeba.txt','r')
labellines=bboxlist.readlines()
#print(len(labellines))
for i,line in enumerate(labellines):
  line=line.strip()
  if i<2:
    print(line)
    continue
  if i%1000==0:
    print 'total :',len(labellines),'now:',i
  splits_line=line.split()
  if len(splits_line)<5:
    print(line)
    continue
  x=int(splits_line[1])
  y=int(splits_line[2])
  w=int(splits_line[3])
  h=int(splits_line[4])
  imgname=os.path.join(img_celeba_dir,splits_line[0])
  img=cv2.imread(imgname,0)
  try:
    img.shape
  except:
    print 'lord img:',imgname,' failed'
    continue
  height = img.shape[0]#height(rows) of image
  width = img.shape[1]#width(colums) of image
  adddiff=(h-w)/2
  addx=x-adddiff if x-adddiff>0 else 0
  #addy=y-h/10 if y-h/10>0 else 0
  addw=w+adddiff*2 if w+adddiff*2<width else width-x-1
  
  addrandom=npr.randint(h,int(h*1.3))
  
  addrandomdiff=(addrandom-h)/2
  addx=addx-addrandomdiff if addx-addrandomdiff>0 else 0
  addw=addw+addrandomdiff*2 if addw+addrandomdiff*2<width else width-x-1
  addy=y-addrandomdiff if y-addrandomdiff>0 else 0
  addh=h+addrandomdiff*2 if h+addrandomdiff*2<height else height-x-1
  #addh=h*6/5 if h*6/5<height else height-y-1
  #print(addx,addy,addw,addh)
  imgcrop= img[y:(y+h),addx:(addx+addw)]
  savename=os.path.join('imgface',splits_line[0])
  cv2.imwrite(savename,imgcrop)
