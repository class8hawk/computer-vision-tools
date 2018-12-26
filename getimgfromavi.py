import os
import sys
import cv2

vediodir='2018-03-30'

distdir='phoneimg'

index=0

if len(sys.argv)==3:
    vediodir=sys.argv[1]
    distdir=sys.argv[2]
    
if len(sys.argv)==4:
    vediodir=sys.argv[1]
    distdir=sys.argv[2]
    index==sys.argv[3]

l1srcdirs=os.listdir(vediodir)
    
if not os.path.exists(distdir):
    os.mkdir(distdir)

for l1srcdir in l1srcdirs:

    if not (l1srcdir.split('.')[-1]=='avi' or l1srcdir.split('.')[-1]=='mp4'):
        print('hh')
        continue
    if os.path.exists(os.path.join(distdir,l1srcdir)):
        continue
    os.mkdir(os.path.join(distdir,l1srcdir))
    videoname=os.path.join(vediodir,l1srcdir)
    cap = cv2.VideoCapture(videoname)
    
    while 1:
    
        ret, frame = cap.read()
        for i in range(10):
            ret, frame = cap.read()

        if frame is None:
            break
         
        jpgsavename=os.path.join(distdir,l1srcdir,str(index)+'.jpg')
        cv2.imencode('.jpg',frame)[1].tofile(jpgsavename)

        index+=1
        if index%100==0:
            print(videoname,':',index)
    cap.release()
    