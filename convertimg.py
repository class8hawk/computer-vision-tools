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
  #parser.add_argument('--bn-mom', type=float, default=0.9, help='bn mom')
  
  args = parser.parse_args()
  return args

  
args = parse_args()  

srcdir=args.srcdir
dstdir=args.dstdir+'hsvres'

if not os.path.exists(srcdir):
    print('can not find:',srcdir)
    sys.exit(1)

if not os.path.exists(dstdir):
    os.makedirs(dstdir)
passnum=0
for index,jpgname in enumerate(os.listdir(srcdir)):
    jpgnamedir=os.path.join(srcdir,jpgname)
    src = cv2.imdecode(np.fromfile(jpgnamedir,dtype = np.uint8),-1)
    #src=cv2.imread(jpgnamedir)
    print(jpgnamedir)
    if src is None:
        print('can not read img:',jpgnamedir)
        continue
    print(src.shape)
    HSV = cv2.cvtColor(src, cv2.COLOR_BGR2HSV＿FULL)
    #cv2.imshow('HSV',HSV)
    #cv2.waitKey(0)
    #dst=src[51:99,51:99]
    #dst=src[24:72,24:72]
    savedir=os.path.join(dstdir,jpgname)
    cv2.imencode('.jpg',HSV)[1].tofile(savedir)
    #cv2.imwrite(savedir,HSV)
    print(index)