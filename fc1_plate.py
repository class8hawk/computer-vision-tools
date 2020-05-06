#coding=utf-8 
       
import os
import caffe 
import numpy as np 
deploy='pose_C5.prototxt'    #deploy文件 
caffe_model='pos_C5_RGB_fixgamma.caffemodel'  #训练好的 caffemodel 
import cv2
 
import os



imgdir='71.bmp'   #随机找的一张待测图片 
 
def Test(img):
      
    net = caffe.Net(deploy,caffe_model,caffe.TEST)   #加载model和network 
       
    #图片预处理设置 
    transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})  #设定图片的shape格式(1,3,28,28) 
    transformer.set_transpose('data', (2,0,1))    #改变维度的顺序，由原始图片(28,28,3)变为(3,28,28) 
    #transformer.set_mean('data', np.load(mean_file).mean(1).mean(1))    #减去均值，前面训练模型时没有减均值，这儿就不用
    #transformer.set_mean('data',  np.array([128,128,128]))
    transformer.set_raw_scale('data', 255)    # 缩放到【0，255】之间 
    #transformer.set_channel_swap('data', (2,1,0))   #交换通道，将图片由RGB变为BGR 
    #transformer.set_input_scale('data',1/128)
    #transformer.set_input_scale('data',0.017)
    im=caffe.io.load_image(imgdir)                   #加载图片 
    net.blobs['data'].data[...] = transformer.preprocess('data',im)      #执行上面设置的图片预处理操作，并将图片载入到blob中 
       
    #执行测试 
    #net.params['bn_data'][0].data=np.array([1,1,1],dtype='float32')
    #net.layers('bn_data').params(0).getdata
    #net.params['bn_data_scale'][0].data[...]=np.array([1,1,1],dtype='float32')
    filters = net.params['bn_data_scale'][0].data[...]
    print("bn_data_scale:",filters)
    #print("blobs {}\nparams {}".format(net.blobs.keys(), net.params.keys()))
    #net.save('pos_C5_RGB_fixgamma.caffemodel');
    out = net.forward() 
    datamiddle= net.blobs['data'].data[0]
    print(datamiddle)
    fmiddle= net.blobs['bn_data'].data[0]
    print(fmiddle.shape,fmiddle)
    fcout= net.blobs['fc1'].data[0]#.flatten()
    print(fcout)
    #取出最后一层（prob）属于某个类别的概率值，并打印,'prob'为最后一层的名称
    #points=fcout.reshape(-1,2)
    #src=cv2.imread(imgdir)
    
    
    
    #print( net.blobs['Dense3'].data[0])
    #print(points) 

Test(imgdir)
