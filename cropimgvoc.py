import xml.etree.ElementTree as ET
import os
import json
import cv2
image_set = set()
category_set = dict()

category_item_id = -1

image_id = 20180000000


def addImgItem(file_name, size):
    global image_id
    if file_name is None:
        raise Exception('Could not find filename tag in xml file.')
    if size['width'] is None:
        raise Exception('Could not find width tag in xml file.')
    if size['height'] is None:
        raise Exception('Could not find height tag in xml file.')
    image_id += 1
    image_item = dict()
    image_item['id'] = image_id
    image_item['file_name'] = file_name
    image_item['width'] = size['width']
    image_item['height'] = size['height']
    #coco['images'].append(image_item)
    image_set.add(file_name)
    return image_id


def addCatItem(name):
    global category_item_id
    category_item = dict()
    category_item['supercategory'] = 'none'
    category_item_id += 1
    category_item['id'] = category_item_id
    category_item['name'] = name
    #coco['categories'].append(category_item)
    category_set[name] = category_item_id
    return category_item_id
    
    

if __name__ == '__main__':
    extname=''
    #imgx=360  #station4
    #imgy=190
    #imgx=470
    #imgy=208   #station5
    #imgx=655
    #imgy=565   #station10 patr1
    
    
    imgx=696
    imgy=302   #station10 part2
    extname='part2'
    
    
    
    cropsize=512

    jpgdir='testimg'
    xml_path = 'testxml'
    save_crop_jpgdir="crop_jpg"
    save_crop_xml_path='crop_xml'
    if not os.path.exists(save_crop_xml_path):
        os.makedirs(save_crop_xml_path)
    if not os.path.exists(save_crop_jpgdir):
        os.makedirs(save_crop_jpgdir)
    
    for f in os.listdir(xml_path):
        if not f.endswith('.xml'):
            continue
        bndbox = dict()
        size = dict()
        current_image_id = None
        current_category_id = None
        file_name = None
        size['width'] = None
        size['height'] = None
        size['depth'] = None

        xml_file = os.path.join(xml_path, f)
        print(xml_file)
 
        tree = ET.parse(xml_file)
        root = tree.getroot()
        if root.tag != 'annotation':
            raise Exception('pascal voc xml root element should be annotation, rather than {}'.format(root.tag))
        bbboxcount=0
        
        

        
        for elem in root:
            current_parent = elem.tag
            current_sub = None
            object_name = None

            if elem.tag=='size':
                for subelem in elem:
                    if subelem.tag=='width':
                        subelem.text=str(cropsize)
                    if subelem.tag=='height':
                        subelem.text=str(cropsize)                  

            if elem.tag == 'object':
                for subelem in elem:
                    if subelem.tag=='bndbox':
                        
                        
                        for point in subelem:
                            
                            if point.tag=='xmin':
                                xmin=int(point.text)
                                xmin-=imgx
                                #point.text=str(xmin)
                            if point.tag=='ymin':
                                ymin=int(point.text)
                                ymin-=imgy
                                #point.text=str(ymin)
                            if point.tag=='xmax':
                                xmax=int(point.text)
                                xmax-=imgx
                                #point.text=str(xmax)
                            if point.tag=='ymax':
                                ymax=int(point.text)
                                ymax-=imgy
                                #point.text=str(ymax)
                        
                        removenode=0
                        procwdith=xmax-xmin
                        procheight=ymax-ymin
                        if xmin<0:
                            if abs(xmin)>procwdith/2:
                                print('remove:',f,xmin,ymin,xmax,ymax)
                                removenode=1
                            else:
                                xmin=0
                                
                        if ymin<0:
                            if abs(ymin)>procheight/2:
                                print('remove:',f,xmin,ymin,xmax,ymax)
                                removenode=1
                            else:
                                ymin=0
                        if xmax>cropsize-1:
                            if (xmax-cropsize+1)>procwdith/2:
                                print('remove:',f,xmin,ymin,xmax,ymax)
                                removenode=1
                            else:
                                xmax=cropsize-1
                        if ymax>cropsize-1:
                            if (ymax-cropsize+1)>procheight/2:
                                print('remove:',f,xmin,ymin,xmax,ymax)
                                removenode=1
                            else:
                                ymax=cropsize-1
                       
                        
                        if removenode==0:
                            bbboxcount+=1
                            for point in subelem:
                            
                                if point.tag=='xmin':
                                    point.text=str(xmin)
                                if point.tag=='ymin':
                                    point.text=str(ymin)
                                if point.tag=='xmax':
                                    point.text=str(xmax)
                                if point.tag=='ymax':
                                    point.text=str(ymax)
                        else:
                            root.remove(elem)
                #
                        
                

        if bbboxcount>0:
            
            jpgname=os.path.splitext(f)[0]+'.jpg'
            img=cv2.imread(os.path.join(jpgdir,jpgname))
            cropimg=img[imgy:imgy+cropsize,imgx:imgx+cropsize,:]
            jpgname=os.path.splitext(jpgname)[0]+extname+'.jpg'
            cv2.imwrite(os.path.join(save_crop_jpgdir,jpgname),cropimg)
            f=os.path.splitext(f)[0]+extname+'.xml'
            tree.write(os.path.join(save_crop_xml_path , f))


                        
        #tree.write(os.path.join(save_crop_xml_path , f))
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        