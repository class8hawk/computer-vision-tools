import os
import cv2
import numpy as np
import sys
import argparse

def parse_args():
  parser = argparse.ArgumentParser(description='convert the pic')
  # general
  parser.add_argument('--srcdir', default='', help='origin directory')
  parser.add_argument('--dstdir', default='', help='Destination directory to save imgs')
  parser.add_argument('--converttype', default='RESIZE', help='how to convert imgs')
  parser.add_argument('--dsth',type=int, default=96, help='which size convert imgs')
  parser.add_argument('--dstw',type=int, default=96, help='which size convert imgs')
  #parser.add_argument('--bn-mom', type=float, default=0.9, help='bn mom')
  
  args = parser.parse_args()
  return args

def getsobelimg(srcimg)
  grayimg = cv2.cvtColor(srcimg, cv2.COLOR_BGR2GRAY)
  x = cv2.Sobel(grayimg,cv2.CV_16S,1,0)
  y = cv2.Sobel(grayimg,cv2.CV_16S,0,1)
  absX = cv2.convertScaleAbs(x)
  absY = cv2.convertScaleAbs(y)
  dst = cv2.addWeighted(absX,0.5,absY,0.5,0)
  return dst
  
def convertimg(srcimg,args,dstdir):
  if args.converttype=='HSV':
    dstimg = cv2.cvtColor(srcimg, cv2.COLOR_BGR2HSV＿FULL)
  elif args.converttype=='RESIZE':
    dstimg=cv2.resize(srcimg, (args.dsth,args.dstw))
  elif args.converttype=='SOBEL':
    dstimg=getsobelimg(srcimg)
  savedir=os.path.join(dstdir,jpgname)
  cv2.imencode('.jpg',dstimg)[1].tofile(savedir) #python3 
    #cv2.imwrite(savedir,HSV)
    #cv2.imshow('HSV',HSV)
    #cv2.waitKey(0)
args = parse_args()  

srcdir=args.srcdir

if not os.path.exists(srcdir):
    print('can not find:',srcdir)
    sys.exit(1)




if args.converttype=='HSV':
    dstdir=args.dstdir+'hsvres'
    if not os.path.exists(dstdir):
        os.makedirs(dstdir)
elif args.converttype=='RESIZE':
    dstdir=args.dstdir+'RESIZE'
    if not os.path.exists(dstdir):
        os.makedirs(dstdir)
elif args.converttype=='SOBEL':
    dstdir=args.dstdir+'SOBEL'
    if not os.path.exists(dstdir):
        os.makedirs(dstdir)
passnum=0
allimgs=os.listdir(srcdir)
totallen=len(allimgs)
for index,jpgname in enumerate(allimgs):
    jpgnamedir=os.path.join(srcdir,jpgname)
    src = cv2.imdecode(np.fromfile(jpgnamedir,dtype = np.uint8),-1)
    #src=cv2.imread(jpgnamedir)
    #print(jpgnamedir)
    if src is None:
        print('can not read img:',jpgnamedir)
        continue
    #print(src.shape)
    convertimg(src,args,dstdir)

    #dst=src[51:99,51:99]
    #dst=src[24:72,24:72]


    if index%200==0:
        print('total:',totallen,'current:',index)