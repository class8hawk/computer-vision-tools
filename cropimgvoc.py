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
    
def getcropimg(extname,imgx,imgy,jpgdir,xml_path):
    
    cropsize=512

    #jpgdir='4station'
    #xml_path = '4station'
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
        #treecp=ET.parse(xml_file)
        root = tree.getroot()
        #rootcp=treecp.getroot()
        
        
        
        #print(len(rootcp))
        
        print('root tpye:',type(root))
        if root.tag != 'annotation':
            raise Exception('pascal voc xml root element should be annotation, rather than {}'.format(root.tag))
        bbboxcount=0
        testcountbbox=0;
        

        print('len:',len(root))
        #for elem in root:
            #print('before:',elem.tag)
        
        for elem in root:
            
            if elem.tag=='size':
                for subelem in elem:
                    if subelem.tag=='width':
                        subelem.text=str(cropsize)
                    if subelem.tag=='height':
                        subelem.text=str(cropsize)                  
            #print('after:',elem.tag)
            if elem.tag == 'filename':
                elem.text+=extname
            
            
        subElement3=root.findall('object')
        #for each in subElement3:
            #rootcp.remove(each)
        for elem in subElement3:
            if elem.tag == 'object':
                testcountbbox+=1
                for subelem in elem:
                    if subelem.tag=='bndbox':
                        
                        
                        for point in subelem:
                            #print(str(testcountbbox),point.tag,point.text)
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
                                #print('remove:',f,xmin,ymin,xmax,ymax)
                                removenode=1
                            else:
                                xmin=0
                        
                        if ymin<0:
                            if abs(ymin)>procheight/2:
                                #print('remove:',f,xmin,ymin,xmax,ymax)
                                removenode=1
                            else:
                                ymin=0
                        if xmax>cropsize-1:
                            if (xmax-cropsize+1)>procwdith/2:
                                #print('remove:',f,xmin,ymin,xmax,ymax)
                                removenode=1
                            else:
                                xmax=cropsize-1
                        if ymax>cropsize-1:
                            if (ymax-cropsize+1)>procheight/2:
                                #print('remove:',f,xmin,ymin,xmax,ymax)
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
                            print('remove:',xmin,ymin,xmax,ymax)
                            root.remove(elem)
                #
                        
                
        print("testcountbbox:",testcountbbox)
        if bbboxcount>0:
            
            jpgname=os.path.splitext(f)[0]+'.jpg'
            img=cv2.imread(os.path.join(jpgdir,jpgname))
            cropimg=img[imgy:imgy+cropsize,imgx:imgx+cropsize,:]
            jpgname=os.path.splitext(jpgname)[0]+extname+'.jpg'
            cv2.imwrite(os.path.join(save_crop_jpgdir,jpgname),cropimg)
            f=os.path.splitext(f)[0]+extname+'.xml'
            tree.write(os.path.join(save_crop_xml_path , f))
            
            
            
def gettypeimg(extname,jpgdir,xml_path):
    
  

    #jpgdir='4station'
    #xml_path = '4station'
    save_crop_jpgdir="save_jpg"
    save_crop_xml_path='save_xml'
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
        #treecp=ET.parse(xml_file)
        root = tree.getroot()
        #rootcp=treecp.getroot()
        
        
        
        #print(len(rootcp))
        
        print('root tpye:',type(root))
        if root.tag != 'annotation':
            raise Exception('pascal voc xml root element should be annotation, rather than {}'.format(root.tag))
        bbboxcount=0
        testcountbbox=0;
        

        print('len:',len(root))
        #for elem in root:
            #print('before:',elem.tag)

            
            
        subElement3=root.findall('object')
        #for each in subElement3:
            #rootcp.remove(each)
        for elem in subElement3:
            if elem.tag == 'object':
                testcountbbox+=1
                for subelem in elem:
                    if subelem.tag=='bndbox':
                        
                        
                        for point in subelem:
                            #print(str(testcountbbox),point.tag,point.text)
                            if point.tag=='xmin':
                                xmin=int(point.text)
  
                                #point.text=str(xmin)
                            if point.tag=='ymin':
                                ymin=int(point.text)
 
                                #point.text=str(ymin)
                            if point.tag=='xmax':
                                xmax=int(point.text)
        
                                #point.text=str(xmax)
                            if point.tag=='ymax':
                                ymax=int(point.text)
     
                                #point.text=str(ymax)
                        
                        removenode=0
                        procwdith=xmax-xmin
                        procheight=ymax-ymin
                        
          
                 
        jpgname=os.path.splitext(f)[0]+'.jpg'
        img=cv2.imread(os.path.join(jpgdir,jpgname))
        cropimg=img[imgy:imgy+cropsize,imgx:imgx+cropsize,:]
        jpgname=os.path.splitext(jpgname)[0]+extname+'.jpg'
        cv2.imwrite(os.path.join(save_crop_jpgdir,jpgname),cropimg)



if __name__ == '__main__':
    extname=''
    #imgx=360  #4station
    #imgy=190
    #jpgdir='4station'
    #xml_path = '4station'
    
    #imgx=470
    #imgy=208   #5station
    #jpgdir='5station'
    #xml_path = '5station'
    
    #imgx=655
    #imgy=565   #10station19201080 patr1
    #jpgdir='10station19201080'
    #xml_path = '10station19201080'    
    
    #imgx=696
    #imgy=302   #10station19201080 part2
    #extname='part2'
    #jpgdir='10station19201080'
    #xml_path = '10station19201080'    
    getcropimg('',360,190,'4station','4station')
    getcropimg('',470,208,'5station','5station')
    getcropimg('',655,565,'10station19201080','10station19201080')
    getcropimg('part2',696,302,'10station19201080','10station19201080')

                        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        