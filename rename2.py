import cv2
import os
import numpy as np

orgfiledir='normal'
renamefiledir='renamefilename'

jpgpaths=os.listdir(orgfiledir)

for index,jgpfile in enumerate(jpgpaths):
	jpgname=os.path.join(orgfiledir,jgpfile)
	img=cv2.imread(jpgname)
	if img is None:
		print(jpgname)
		continue

	
	savename=str(index)+'-人员'+str(index)+'.jpg'
	savejpgname=os.path.join(renamefiledir,savename)
	print(savejpgname)
	cv2.imencode('.jpg',img)[1].tofile(savejpgname)
	#cv2.imwrite(savejpgname,bigimg)
	#cv2.imshow("bigimg",bigimg)
	#cv2.waitKey(0)
	#print(bigimg.dtype)
