import os
import os.path
import shutil
 
fileDir_ann = "E:\\voc_year\\VOCdevkit\\VOC2007\\Annotations"
fileDir_img = "E:\\voc_year\\VOCdevkit\\VOC2007\\JPEGImages\\"
saveDir_img = "E:\\voc_year\\VOCdevkit\\VOC2007\\JPEGImages_ssd\\"
 
if not os.path.exists(saveDir_img):
    os.mkdir(saveDir_img)
 
names = locals()
 
for files in os.walk(fileDir_ann):
    for file in files[2]:
        
        print file + "-->start!"
 
        saveDir_ann = "E:\\voc_year\\VOCdevkit\\VOC2007\\Annotations_ssd\\"
        if not os.path.exists(saveDir_ann):
            os.mkdir(saveDir_ann)
 
        fp = open(fileDir_ann + '\\' + file)        
        saveDir_ann = saveDir_ann + file
        fp_w = open(saveDir_ann, 'w')
        classes = ['aeroplane','bicycle','bird','boat','bottle','bus','car','>cat<','chair','cow','diningtable',\
                   'dog','horse','motorbike','pottedplant','sheep','sofa','train','tvmonitor','person']
 
        lines = fp.readlines()
 
        ind_start = []
        ind_end = []
        lines_id_start = lines[:]
        lines_id_end = lines[:]
        
        while "\t<object>\n" in lines_id_start:
            a = lines_id_start.index("\t<object>\n")
            ind_start.append(a)
            lines_id_start[a] = "delete"
 
        while "\t</object>\n" in lines_id_end:
            b = lines_id_end.index("\t</object>\n")
            ind_end.append(b)
            lines_id_end[b] = "delete"
        
        i = 0
        for k in range(0,len(ind_start)):
            for j in range(0,len(classes)):
                if classes[j] in lines[ind_start[i]+1]:
                    a = ind_start[i]
                    names['block%d'%k] = [lines[a],lines[a+1],\
                                          lines[a+2],lines[a+3],lines[a+4],\
                                          lines[a+5],lines[a+6],lines[a+7],\
                                          lines[a+8],lines[a+9],lines[a+10],\
                                          lines[ind_end[i]]]
                    break
            i += 1
 
        classes1 = '\t\t<name>bicycle</name>\n'
        classes2 = '\t\t<name>motorbike</name>\n'
        classes3 = '\t\t<name>bus</name>\n'
        classes4 = '\t\t<name>car</name>\n'
 
        string_start = lines[0:ind_start[0]]
        string_end = [lines[len(lines)-1]]
        
        a = 0
        for k in range(0,len(ind_start)):
            if classes1 in names['block%d'%k]:
                a += 1
                string_start += names['block%d'%k]
            if classes2 in names['block%d'%k]:
                a += 1
                string_start += names['block%d'%k]
            if classes3 in names['block%d'%k]:
                a += 1
                string_start += names['block%d'%k]
            if classes4 in names['block%d'%k]:
                a += 1
                string_start += names['block%d'%k]
 
        string_start += string_end 
        for c in range(0,len(string_start)):
            fp_w.write(string_start[c])
        fp_w.close()
 
        if a == 0:
            os.remove(saveDir_ann)
        else:
            name_img = fileDir_img + os.path.splitext(file)[0] + ".jpg"
            shutil.copy(name_img,saveDir_img)
        fp.close()