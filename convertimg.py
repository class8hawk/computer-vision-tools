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
  parser.add_argument('--converttype', default='HSV', help='how to convert imgs')
  #parser.add_argument('--bn-mom', type=float, default=0.9, help='bn mom')
  
  args = parser.parse_args()
  return args

  
def convertimg(srcimg,args):
  if args.converttype=='HSV':
    dstdirhsv=args.dstdir+'hsvres'
    HSV = cv2.cvtColor(srcimg, cv2.COLOR_BGR2HSV＿FULL)
    savedir=os.path.join(dstdirhsv,jpgname)
    cv2.imencode('.jpg',HSV)[1].tofile(savedir) #python3 
    #cv2.imwrite(savedir,HSV)
    #cv2.imshow('HSV',HSV)
    #cv2.waitKey(0)
args = parse_args()  

srcdir=args.srcdir

if not os.path.exists(srcdir):
    print('can not find:',srcdir)
    sys.exit(1)




if args.converttype=='HSV':
    dstdirhsv=args.dstdir+'hsvres'
    if not os.path.exists(dstdirhsv):
        os.makedirs(dstdirhsv)

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
    convertimg(src,args)

    #dst=src[51:99,51:99]
    #dst=src[24:72,24:72]


    if index%200==0:
        print('total:',totallen,'current:',index)