import os
from xml.dom import minidom
import cv2

txtdirs=r'E:/img/labelhs'
imgdirs=r'E:/img/Horizontalscreen'  #use / for split
xmldirs=r'E:/img/xml'


dom=minidom.Document()
root_node=dom.createElement('annotation')
dom.appendChild(root_node)


folder=dom.createElement('folder')
folder_text=dom.createTextNode('')
root_node.appendChild(folder)
folder.appendChild(folder_text)
folder_text.data=imgdirs.split('/')[-1]


filename_xml=dom.createElement('filename')
root_node.appendChild(filename_xml)
filename_xml_text=dom.createTextNode('')
filename_xml.appendChild(filename_xml_text)


path_xml=dom.createElement('path')
root_node.appendChild(path_xml)
path_xml_text=dom.createTextNode('')
path_xml.appendChild(path_xml_text)


source_xml=dom.createElement('source')
root_node.appendChild(source_xml)
database_xml=dom.createElement('database')
source_xml.appendChild(database_xml)
sourc_xml_text=dom.createTextNode('fromdarknet')
database_xml.appendChild(sourc_xml_text)


size_xml=dom.createElement('size')
root_node.appendChild(size_xml)
width_xml=dom.createElement('width')
size_xml.appendChild(width_xml)
width_xml_text=dom.createTextNode('')
width_xml.appendChild(width_xml_text)
height_xml=dom.createElement('height')
size_xml.appendChild(height_xml)
height_xml_text=dom.createTextNode('')
height_xml.appendChild(height_xml_text)
depth_xml=dom.createElement('depth')
size_xml.appendChild(depth_xml)
depth_xml_text=dom.createTextNode('')
depth_xml.appendChild(depth_xml_text)


segmented_xml=dom.createElement('segmented')
root_node.appendChild(segmented_xml)
segmented_xml_text=dom.createTextNode('0')
segmented_xml.appendChild(segmented_xml_text)

object_xml=dom.createElement('object')
root_node.appendChild(object_xml)

name_xml=dom.createElement('name')
object_xml.appendChild(name_xml)
name_xml_text=dom.createTextNode('peaper')
name_xml.appendChild(name_xml_text)

pose_xml=dom.createElement('pose')
object_xml.appendChild(pose_xml)
pose_xml_text=dom.createTextNode('Unspecified')
pose_xml.appendChild(pose_xml_text)

truncated_xml=dom.createElement('truncated')
object_xml.appendChild(truncated_xml)
truncated_xml_text=dom.createTextNode('0')
truncated_xml.appendChild(truncated_xml_text)

difficult_xml=dom.createElement('difficult')
object_xml.appendChild(difficult_xml)
difficult_xml_text=dom.createTextNode('0')
difficult_xml.appendChild(difficult_xml_text)

bndbox_xml=dom.createElement('bndbox')
object_xml.appendChild(bndbox_xml)

xmin_xml=dom.createElement('xmin')
bndbox_xml.appendChild(xmin_xml)
xmin_xml_text=dom.createTextNode('')
xmin_xml.appendChild(xmin_xml_text)

ymin_xml=dom.createElement('ymin')
bndbox_xml.appendChild(ymin_xml)
ymin_xml_text=dom.createTextNode('')
ymin_xml.appendChild(ymin_xml_text)

xmax_xml=dom.createElement('xmax')
bndbox_xml.appendChild(xmax_xml)
xmax_xml_text=dom.createTextNode('')
xmax_xml.appendChild(xmax_xml_text)

ymax_xml=dom.createElement('ymax')
bndbox_xml.appendChild(ymax_xml)
ymax_xml_text=dom.createTextNode('')
ymax_xml.appendChild(ymax_xml_text)


txtfilenames=os.listdir(txtdirs)
print('label total:',len(txtfilenames))
for index,txtfilename in enumerate(txtfilenames):
    jpgname=os.path.splitext(txtfilename)[0]+'.jpg'
    xmlname=os.path.splitext(txtfilename)[0]+'.xml'
    filename_xml_text.data=jpgname
    fulljpgname=imgdirs+'/'+jpgname
    path_xml_text.data=fulljpgname
    
    img=cv2.imread(fulljpgname)
    if img is None:
        continue
    h,w,c=img.shape
    width_xml_text.data=str(w)
    height_xml_text.data=str(h)
    depth_xml_text.data=str(c)
    
    txtfile=open(os.path.join(txtdirs,txtfilename),'r')
    lines=txtfile.readlines()
    line=lines[0].strip().split(' ')
    name_xml_text.data='class'+line[0]
    
    xcent=float(line[1])
    ycent=float(line[2])
    wscaler=float(line[3])
    hscaler=float(line[4])
    
    xmin=int(xcent*w-wscaler*w/2)
    ymin=int(ycent*h-hscaler*h/2)
    xmax=int(xcent*w+wscaler*w/2)
    ymax=int(ycent*h+hscaler*h/2)
    
    xmin_xml_text.data=str(xmin)
    ymin_xml_text.data=str(ymin)
    xmax_xml_text.data=str(xmax)
    ymax_xml_text.data=str(ymax)
    
    xmlsavename=os.path.join(xmldirs,xmlname)
    with open(os.path.join(xmldirs,xmlname),'w',encoding='UTF-8') as fh:
        dom.writexml(fh,indent='',addindent='\t',newl='\n',encoding='UTF-8')

