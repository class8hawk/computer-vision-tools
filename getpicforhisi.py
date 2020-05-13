import os
import cv2
picnum=200
posdir='trainpos'
negdir='trainneg'
savedir="hisi"
if not os.path.exists(savedir):
    os.makedirs(savedir)


posimgnames=os.listdir(posdir)
negimgnames=os.listdir(negdir)

posstep=len(posimgnames)/picnum
negstep=len(negimgnames)/picnum

for i in range(picnum):
    posimg=cv2.imread(os.path.join(posdir,posimgnames[i*posstep]))
    posimgresize=cv2.resize(posimg,(128,128))
    posflip=cv2.flip(posimgresize, 1)
    cv2.imwrite(os.path.join(savedir,str(i*4)+'.jpg'),posimgresize)
    cv2.imwrite(os.path.join(savedir,str(i*4+2)+'.jpg'),posflip)
    negimg=cv2.imread(os.path.join(negdir,negimgnames[i*negstep]))

    negimgresize=cv2.resize(negimg,(128,128))
    negimgflip=cv2.flip(negimgresize, 1)
    cv2.imwrite(os.path.join(savedir,str(i*4+1)+'.jpg'),negimgresize)
    cv2.imwrite(os.path.join(savedir,str(i*4+3)+'.jpg'),negimgflip)
