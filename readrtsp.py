#!/bin/python
#### in rtsp server:
####  ffserver -f /etc/ffserver.conf &
#### ffmpeg -f v4l2 -i /dev/video0  -s 640x480 -r 24 -vcodec libx264 -an http://127.0.0.1:8090/feed1.ffm
import cv2
import os
from MTCNN_CAFFE.mtcnn_detector_new import MTCNN_face_detector
mtcnn_detector = MTCNN_face_detector()  

if __name__ == "__main__":
  cap = cv2.VideoCapture("rtsp://192.168.0.110/ch1")
  saveimgdir='face'
  if not os.path.exists(saveimgdir):
    os.makedirs(saveimgdir)
  if cap.isOpened() :
    ret,frame=cap.read()
#    print "==== ret ===="
#    print ret
#    print "====print dir(frame)===="
#    print dir(frame)
#    print "====print frame.shape===="
#    print frame.shape
#    print "====print (frame.shape[0], frame.shape[1], frame.shape[2])===="
#    print (frame.shape[0], frame.shape[1], frame.shape[2])
#    print "====print frame.size===="
#    print frame.size
#    print "====print frame.data===="
#    #print frame.data
#    #print type(frame.data)
#    print "====print frame.copy===="
#    print frame.copy
#    print type(frame.copy)
#    print "====print frame.ctypes===="      
    #-------------------------------------------------------------------------------------------

    #-------------------------------------------------------------------------------------------
    print(frame.ctypes)
    print(type(frame.ctypes))       
    print("====print frame.imag====")
    #print frame.imag
    #print type(frame.imag)
    print("====print frame.tobytes====")
    print(frame.tobytes)
    print(type(frame.tobytes))
  
  ##cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH,640)
  ##cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT,480)
  saveindex=0
  while cap.isOpened():
    ret,frame=cap.read()
    ret,frame=cap.read()
    ret,frame=cap.read()
    ret,frame=cap.read()
    print(src)
    src=cv2.resize(frame,(360,640))
    boundingboxes, points = mtcnn_detector.run_detect_face(src,80)
    if(len(boundingboxes)==1):
        
        saveindex=saveindex+1
        
        savedirjpg=os.path.join(saveimgdir,str(saveindex)+'ir.jpg')
        print(savedirjpg)
        cv2.imwrite(savedirjpg,src)
        
    #cv2.imwrite("test.jpg",frame)
    #print((frame.shape[0], frame.shape[1], frame.shape[2]))
#    print ret
#    print dir(frame)
#    print frame.shape
#    print frame.size
#    print frame.data
    #cv2.namedWindow("frame",0) 
   # cv2.imshow("frame",frame)
    #cv2.waitKey(10)
#cv2.destroyWindow("frame")