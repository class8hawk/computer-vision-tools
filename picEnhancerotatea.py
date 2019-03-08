import json
import cv2
import os
import numpy as np
import math
import random

jsonfile=open('train_no_poly.json','r')
load_dict = json.load(jsonfile)
jsonfile.close()
picdir='restricted'
bgdir='normal'
addnormalsrcdir='addnormal'
if not os.path.exists(addnormalsrcdir):
  os.makedirs(addnormalsrcdir)

bgimagenames=os.listdir(bgdir)
itbgimagenames=iter(bgimagenames)

def rotate_image( src, angle, scale=1.):
  w = src.shape[1]
  h = src.shape[0]
  # convet angle into rad
  rangle = np.deg2rad(angle)  # angle in radians
  # calculate new image width and height
  nw = (abs(np.sin(rangle)*h) + abs(np.cos(rangle)*w))*scale
  nh = (abs(np.cos(rangle)*h) + abs(np.sin(rangle)*w))*scale
  # ask OpenCV for the rotation matrix
  rot_mat = cv2.getRotationMatrix2D((nw*0.5, nh*0.5), angle, scale)
  # calculate the move from the old center to the new center combined
  # with the rotation
  rot_move = np.dot(rot_mat, np.array([(nw-w)*0.5, (nh-h)*0.5, 0]))
  # the move only affects the translation, so update the translation
  # part of the transform
  rot_mat[0, 2] += rot_move[0]
  rot_mat[1, 2] += rot_move[1]
  # map
  return cv2.warpAffine(
    src, rot_mat, (int(math.ceil(nw)), int(math.ceil(nh))),
    flags=cv2.INTER_LANCZOS4)

def rotate_xml( src, xmin, ymin, xmax, ymax, angle, scale=1.):
  w = src.shape[1]
  h = src.shape[0]
  rangle = np.deg2rad(angle)  # angle in radians
  # now calculate new image width and height
   # get width and heigh of changed image
  nw = (abs(np.sin(rangle)*h) + abs(np.cos(rangle)*w))*scale
  nh = (abs(np.cos(rangle)*h) + abs(np.sin(rangle)*w))*scale
  # ask OpenCV for the rotation matrix
  rot_mat = cv2.getRotationMatrix2D((nw*0.5, nh*0.5), angle, scale)
  # calculate the move from the old center to the new center combined
  # with the rotation
  rot_move = np.dot(rot_mat, np.array([(nw-w)*0.5, (nh-h)*0.5, 0]))
  # the move only affects the translation, so update the translation
  # part of the transform
  rot_mat[0, 2] += rot_move[0]
  rot_mat[1, 2] += rot_move[1]
  # rot_mat: the final rot matrix
 # get the four center of edges in the initial martix，and convert the coord
  point1 = np.dot(rot_mat, np.array([(xmin+xmax)/2, ymin, 1]))
  point2 = np.dot(rot_mat, np.array([xmax, (ymin+ymax)/2, 1]))
  point3 = np.dot(rot_mat, np.array([(xmin+xmax)/2, ymax, 1]))
  point4 = np.dot(rot_mat, np.array([xmin, (ymin+ymax)/2, 1]))
  #point1 = np.dot(rot_mat, np.array([xmin, ymin, 1]))
  #point2 = np.dot(rot_mat, np.array([xmax, ymin, 1]))
  #point3 = np.dot(rot_mat, np.array([xmin, ymax, 1]))
  #point4 = np.dot(rot_mat, np.array([xmax, ymax, 1]))
  # concat np.array
  concat = np.vstack((point1, point2, point3, point4))
  # change type
  concat = concat.astype(np.int32)
  #print(concat)
  rx, ry, rw, rh = cv2.boundingRect(concat)
  return rx, ry, rw, rh




for key in load_dict:
  print(key)
    #print(keyl2)
#print(load_dict['annotations'])
#{'license': 1, 'height': 347, 'flickr_url': '', 'file_name': '190127_151952_00178855.jpg', 'width': 465, 'data_captured': '', 'id': 1457, 'coco_url': ''}
picid={}
for each in load_dict['images']:
  picid[each['id']]=each['file_name']

picbboxs={}
maximgid=0
maxid=0
categorydict={1:0,2:0,3:0,4:0,5:0}
for bboxstr in load_dict['annotations']:
  bboximg_id=bboxstr['image_id']
  categorydict[bboxstr['category_id']]+=1
  #print(next(itbgimagenames))
  if(maximgid<bboximg_id):
    maximgid=bboximg_id
  if maxid<bboxstr['id']:
    maxid=bboxstr['id']
  #picbboxs
  if bboximg_id in picbboxs:
    picbboxs[bboximg_id].append([bboxstr['bbox'],bboxstr['category_id'],bboxstr['id']])
  else:
    picbboxs[bboximg_id]=[[bboxstr['bbox'],bboxstr['category_id'],bboxstr['id']]]
print(maximgid,maxid)
print(categorydict)
isbreak=0


for key in picbboxs:
  if isbreak:
    break
  img=cv2.imread(os.path.join(picdir,picid[key]))
  imgh,imgw,c=img.shape
  for eachbox in picbboxs[key]:
    if isbreak:
      break
    repeattime=0
    if eachbox[1]==1:
      repeattime=2
    if eachbox[1]==3 or eachbox[1]==5:
      repeattime=1
    
    for i in range(repeattime):
      
      lefttopx=int(eachbox[0][0])
      lefttopy=int(eachbox[0][1])
      rightbottomx=int(eachbox[0][0]+eachbox[0][2])
      rightbottomy=int(eachbox[0][1]+eachbox[0][3])
      w=eachbox[0][2]
      h=eachbox[0][3]
      roilefttopx=lefttopx-int(w*0.12)
      roilefttopy=lefttopy-int(h*0.12)
      roirightbottomx=rightbottomx+int(w*0.12)
      roirightbottomy=rightbottomy+int(h*0.12)
      
      roilefttopx=roilefttopx if roilefttopx>0 else 0
      roilefttopy=roilefttopy if roilefttopy>0 else 0
      roirightbottomx=roirightbottomx if roirightbottomx<imgw-1 else imgw-1
      roirightbottomy=roirightbottomy if roirightbottomy<imgh-1 else imgh-1
      
      #print('w:',w,'h:',h)
      roiimg=img[roilefttopy:roirightbottomy,roilefttopx:roirightbottomx]
      
      newxmin=lefttopx-roilefttopx
      newymin=lefttopy-roilefttopy
      newxmax=newxmin+w
      newymax=newymin+h
      
      try:
        bgjpgname=next(itbgimagenames)
        
        
      except StopIteration:
        isbreak=1
        break
      bgimg=cv2.imread(os.path.join(bgdir,bgjpgname))
      bgh,bgw,bgc=bgimg.shape
      roiimgh=roirightbottomy-roilefttopy
      roiimgw=roirightbottomx-roilefttopx
      if bgh<(roiimgh)*1.3 or bgw<(roiimgw)*1.3:
        continue
      bgroiminx=random.randint(0,bgw-roiimgw)
      bgroiminy=random.randint(0,bgh-roiimgh)
      bgroimaxx=bgroiminx+roiimgw
      bgroimaxy=bgroiminy+roiimgh
      bgimg[bgroiminy:bgroimaxy,bgroiminx:bgroimaxx]=roiimg
        
      resminx=bgroiminx+newxmin
      resminy=bgroiminy+newymin
      resmaxx=resminx+w
      resmaxy=resminy+h
      #cv2.rectangle(roiimg,(newxmin,newymin),(newxmax,newymax),(255,255,0),3)
      #cv2.rectangle(bgimg,(resminx,resminy),(resmaxx,resmaxy),(255,255,0),3)
      #cv2.imshow("bgimg",bgimg)
      #cv2.waitKey(0)
      cv2.imwrite(os.path.join(addnormalsrcdir,bgjpgname),bgimg)
        
        # imgjson
      imagepartjson={}
      imagepartjson["coco_url"]=''
      imagepartjson["data_captured"]=''
      imagepartjson["file_name"]=bgjpgname
      imagepartjson["flickr_url"]=''
      maximgid+=1
      imagepartjson["id"]=maximgid
        
      imagepartjson["height"]=bgh
      imagepartjson["width"]=bgw
      imagepartjson["license"]=1
        
        
        #bboxjson
      bboxjson={}
      maxid+=1
      bboxjson["id"]=maxid
      bboxjson["image_id"]=maximgid
      bboxjson["category_id"]=eachbox[1]
      bboxjson["iscrowd"]=0
      bboxjson["segmentation"]=[]
      bboxjson["area"]=[]
      bboxjson["bbox"]=[resminx,resminy,resmaxx-resminx,resmaxy-resminy]
      bboxjson["minAreaRect"]=[]
      
      load_dict['images'].append(imagepartjson)
      load_dict['annotations'].append(bboxjson)
      
      
      #print(imagepartjson)
      #print(bboxjson)
jsonData = json.dumps(load_dict)
fileObject = open('newaddbg.json', 'w')
fileObject.write(jsonData)
fileObject.close()
      #cv2.rectangle(roiimg,(newxmin,newymin),(newxmax,newymax),(255,255,0),3)
      #cv2.imshow("show",roiimg)
      #cv2.waitKey(0)
      #{"coco_url": "", "data_captured": "", "file_name": "190125_181308_00174698.jpg", "flickr_url": "", "id": 466, "height": 345, "width": 802, "license": 1}
#{"id": 5314, "image_id": 980, "category_id": 4, "iscrowd": 0, "segmentation": [], "area": [], "bbox": [170, 60, 55, 93], "minAreaRect": [[205, 155], [166, 61], [186, 53], [225, 147]]}
#{'bbox': [512.0, 426.0, 177.0, 110.0], 'area': [], 'iscrowd': 0, 'id': 5075, 'segmentation': [], 'category_id': 5, 'image_id': 1459}  
'''
for key in picbboxs:
  img=cv2.imread(os.path.join(picdir,picid[key]))
  rotatea=90
  rotateimg=rotate_image(img,rotatea)
  for eachbox in picbboxs[key]:
    print(eachbox)
    lefttopx=int(eachbox[0][0])
    lefttopy=int(eachbox[0][1])
    rightbottomx=int(eachbox[0][0]+eachbox[0][2])
    rightbottomy=int(eachbox[0][1]+eachbox[0][3])
    cv2.rectangle(img,(lefttopx,lefttopy),(rightbottomx,rightbottomy),(255,255,0),3)
    rotatex,rotatey,rotatew,rotateh=rotate_xml(img,lefttopx,lefttopy,rightbottomx,rightbottomy,rotatea)
    cv2.rectangle(rotateimg,(rotatex,rotatey),(rotatex+rotatew,rotatey+rotateh),(255,255,0),3)
  cv2.imshow("rotateimg",rotateimg)
  cv2.imshow("show",img)
  cv2.waitKey(0)
  #print(type(bboxstr['bbox']))
'''

for each in load_dict['annotations']:
  #print(each)
  pass