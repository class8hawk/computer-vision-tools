import json
import cv2
import os
import numpy as np
import math

jsonfile=open('train_no_poly.json','r')
load_dict = json.load(jsonfile)
jsonfile.close()
picdir='restricted'

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
for bboxstr in load_dict['annotations']:
  bboximg_id=bboxstr['image_id']
  #picbboxs
  if bboximg_id in picbboxs:
    picbboxs[bboximg_id].append([bboxstr['bbox'],bboxstr['category_id']])
  else:
    picbboxs[bboximg_id]=[[bboxstr['bbox'],bboxstr['category_id']]]

for key in picbboxs:
  img=cv2.imread(os.path.join(picdir,picid[key]))
  rotateimg=rotate_image(img,45)
  for eachbox in picbboxs[key]:
    print(eachbox)
    lefttopx=int(eachbox[0][0])
    lefttopy=int(eachbox[0][1])
    rightbottomx=int(eachbox[0][0]+eachbox[0][2])
    rightbottomy=int(eachbox[0][1]+eachbox[0][3])
    cv2.rectangle(img,(lefttopx,lefttopy),(rightbottomx,rightbottomy),(255,255,0),3)
    rotatex,rotatey,rotatew,rotateh=rotate_xml(img,lefttopx,lefttopy,rightbottomx,rightbottomy,45)
    cv2.rectangle(rotateimg,(rotatex,rotatey),(rotatex+rotatew,rotatey+rotateh),(255,255,0),3)
  cv2.imshow("rotateimg",rotateimg)
  cv2.imshow("show",img)
  cv2.waitKey(0)
  #print(type(bboxstr['bbox']))
  
  
  
#{'bbox': [512.0, 426.0, 177.0, 110.0], 'area': [], 'iscrowd': 0, 'id': 5075, 'segmentation': [], 'category_id': 5, 'image_id': 1459}  
for each in load_dict['annotations']:
  #print(each)
  pass