#!/usr/bin/env python
# @File : voc_window_file.py
import os, sys
import xml.etree.ElementTree as ET

reload(sys)
sys.setdefaultencoding('utf-8')

def parse_rec(filename):
    """ Parse a PASCAL VOC xml file """

    tree = ET.parse(filename)
    objects = []

    for pic in tree.findall('size'):
        pic_struct = {}
        pic_struct['width'] = int(pic.find('width').text)
        pic_struct['height'] = int(pic.find('height').text)
        pic_struct['depth'] = int(pic.find('depth').text)
        objects.append(pic_struct)

    for obj in tree.findall('object'):
        obj_struct = {}
        obj_struct['name'] = obj.find('name').text
        # obj_struct['difficult'] = int(obj.find('difficult').text)
        bbox = obj.find('bndbox')
        obj_struct['bbox'] = [int(float(bbox.find('xmin').text)),
                              int(float(bbox.find('ymin').text)),
                              int(float(bbox.find('xmax').text)),
                              int(float(bbox.find('ymax').text))]
        objects.append(obj_struct)
    return objects

def main():

    vocdevkit = '/media/DT_Moyan/Data/VOC/VOCdevkit'
    VOCopts_classes=['aeroplane', 'bicycle', 'bird', 'boat', 'bottle',
                     'bus', 'car', 'cat', 'chair', 'cow', 'diningtable',
                     'dog', 'horse', 'motorbike', 'person', 'pottedplant',
                     'sheep', 'sofa', 'train', 'tvmonitor']
    years = ['2007', '2012']
    split = ['trainval', 'test']
    fileName = 'window_file_voc2007_trainval.txt'
    fid = open(fileName, 'wt')

    # just running
    print ("VOC years: %s" %(years[0]))
    txt_ = os.path.join(vocdevkit, 'VOC' + years[0], 'ImageSets', 'Main' , split[0] + '.txt')
    f = open(txt_); idList = f.readlines() ; f.close()
    print len(idList)

    idCount = 0

    for u in range(len(idList)):
        nm = idList[u].strip() + '.jpg'
        xm = idList[u].strip() + '.xml'
        imgFullName = os.path.join('VOC' + years[0], 'JPEGImages', nm)
        # imgPath = os.path.join(vocdevkit, 'VOC' + years[0], 'JPEGImages', nm)
        xmlPath = os.path.join(vocdevkit, 'VOC' + years[0], 'Annotations', xm)
        nObjs = parse_rec(xmlPath)

        chw1 = nObjs[0]['depth']
        chw2 = nObjs[0]['height']
        chw3 = nObjs[0]['width']
        fid.write('# %d\n' % u)
        fid.write('%s\n' % imgFullName)
        fid.write('%d\n%d\n%d\n' % (chw1, chw2, chw3))
        fid.write('%d\n' % (len(nObjs) - 1))
        for j in range(1, len(nObjs)):

            clsIds = nObjs[j]['name']
            xmin = nObjs[j]['bbox'][0]
            ymin = nObjs[j]['bbox'][1]
            xmax = nObjs[j]['bbox'][2]
            ymax = nObjs[j]['bbox'][3]
            if (xmax <= xmin) | (ymax <= ymin):
                continue
            clsId = VOCopts_classes.index(clsIds) + 1
            t_lines = str(clsId) + ' 0' + ' 0' + ' ' + str(xmin) + ' ' + str(ymin) + ' ' + str(xmax) + ' ' + str(ymax)
            fid.write('%s\n' % t_lines)
            # print t_lines
        fid.write('%d\n' % 0)
        idCount += 1

    fid.close()

if __name__ == "__main__":
    main()