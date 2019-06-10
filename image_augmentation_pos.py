# -*- coding: UTF-8 -*-
"""
	image_augmentation_pos.py
"""

import numpy as np
import cv2
import os
import argparse
import random
import math
from multiprocessing import Process
from multiprocessing import cpu_count


'''
定义裁剪函数，四个参数分别是：
左上角横坐标x0
左上角纵坐标y0
裁剪宽度w
裁剪高度h
'''
crop_image = lambda img, x0, y0, w, h: img[y0:y0 + h, x0:x0 + w]

'''
随机裁剪
area_ratio为裁剪画面占原画面的比例
hw_vari是扰动占原高宽比的比例范围
'''


def random_crop(img, area_ratio, hw_vari):
    h, w = img.shape[:2]
    hw_delta = np.random.uniform(-hw_vari, hw_vari)
    hw_mult = 1 + hw_delta

    # 下标进行裁剪，宽高必须是正整数
    w_crop = int(round(w * np.sqrt(area_ratio * hw_mult)))

    # 裁剪宽度不可超过原图可裁剪宽度
    if w_crop > w:
        w_crop = w

    h_crop = int(round(h * np.sqrt(area_ratio / hw_mult)))
    if h_crop > h:
        h_crop = h

    # 随机生成左上角的位置
    x0 = np.random.randint(0, w - w_crop + 1)
    y0 = np.random.randint(0, h - h_crop + 1)

    return crop_image(img, x0, y0, w_crop, h_crop)


'''
定义旋转函数：
angle是逆时针旋转的角度
crop是个布尔值，表明是否要裁剪去除黑边
'''


def rotate_image(img, angle, crop):
    h, w = img.shape[:2]

    # 旋转角度的周期是360°
    angle %= 360

    # 用OpenCV内置函数计算仿射矩阵
    M_rotate = cv2.getRotationMatrix2D((w / 2, h / 2), angle, 1)

    # 得到旋转后的图像
    img_rotated = cv2.warpAffine(img, M_rotate, (w, h))

    # 如果需要裁剪去除黑边
    if crop:
        angle_crop = angle % 180  # 对于裁剪角度的等效周期是180°
        if angle_crop > 90:  # 并且关于90°对称
            angle_crop = 180 - angle_crop

        theta = angle_crop * np.pi / 180.0  # 转化角度为弧度
        hw_ratio = float(h) / float(w)  # 计算高宽比

        tan_theta = np.tan(theta)  # 计算裁剪边长系数的分子项
        numerator = np.cos(theta) + np.sin(theta) * tan_theta

        r = hw_ratio if h > w else 1 / hw_ratio  # 计算分母项中和宽高比相关的项
        denominator = r * tan_theta + 1  # 计算分母项

        crop_mult = numerator / denominator  # 计算最终的边长系数
        w_crop = int(round(crop_mult * w))  # 得到裁剪区域
        h_crop = int(round(crop_mult * h))
        x0 = int((w - w_crop) / 2)
        y0 = int((h - h_crop) / 2)
        img_rotated = crop_image(img_rotated, x0, y0, w_crop, h_crop)
    return img_rotated


'''
随机旋转
angle_vari是旋转角度的范围[-angle_vari, angle_vari)
p_crop是要进行去黑边裁剪的比例
'''


def random_rotate(img, angle_vari, p_crop):
    angle = np.random.uniform(-angle_vari, angle_vari)
    crop = False if np.random.random() > p_crop else True
    return rotate_image(img, angle, crop)


'''
定义hsv变换函数：
hue_delta是色调变化比例
sat_delta是饱和度变化比例
val_delta是明度变化比例
'''


def hsv_transform(img, hue_delta, sat_mult, val_mult):
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV).astype(np.float)
    img_hsv[:, :, 0] = (img_hsv[:, :, 0] + hue_delta) % 180
    img_hsv[:, :, 1] *= sat_mult
    img_hsv[:, :, 2] *= val_mult
    img_hsv[img_hsv > 255] = 255
    return cv2.cvtColor(np.round(img_hsv).astype(np.uint8), cv2.COLOR_HSV2BGR)


'''
随机hsv变换
hue_vari是色调变化比例的范围
sat_vari是饱和度变化比例的范围
val_vari是明度变化比例的范围
'''


def random_hsv_transform(img, hue_vari, sat_vari, val_vari):
    hue_delta = np.random.randint(-hue_vari, hue_vari)
    sat_mult = 1 + np.random.uniform(-sat_vari, sat_vari)
    val_mult = 1 + np.random.uniform(-val_vari, val_vari)
    return hsv_transform(img, hue_delta, sat_mult, val_mult)


'''
定义gamma变换函数：
gamma就是Gamma
'''


def gamma_transform(img, gamma):
    gamma_table = [np.power(x / 255.0, gamma) * 255.0 for x in range(256)]
    gamma_table = np.round(np.array(gamma_table)).astype(np.uint8)
    return cv2.LUT(img, gamma_table)


'''
随机gamma变换
gamma_vari是Gamma变化的范围[1/gamma_vari, gamma_vari)
'''


def random_gamma_transform(img, gamma_vari):
    log_gamma_vari = np.log(gamma_vari)
    alpha = np.random.uniform(-log_gamma_vari, log_gamma_vari)
    gamma = np.exp(alpha)
    return gamma_transform(img, gamma)


"""
	run_augmentation.py
"""


# 导入image_augmentation.py为一个可调用模块
# import image_augmentation as ia


# 利用Python的argparse模块读取输入输出和各种扰动参数
def parse_args():
    parser = argparse.ArgumentParser(
        description='A Simple Image Data Augmentation Tool',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--input_dir',
                        help='Directory containing images', default='/media/hasx/85bbc910-aa30-46e0-8b9c-158eeace2c9c/home/hasx/Project/Datasets/trainData/unalign_extened_2_2.5/pos_train_part_20190521')
    parser.add_argument('--output_dir',
                        help='Directory for augmented images', default='/media/hasx/85bbc910-aa30-46e0-8b9c-158eeace2c9c/home/hasx/Project/Datasets/trainData/unalign_extened_2_2.5/pos_train_part_20190521_augmentation')
    parser.add_argument('--num',
                        help='Number of images to be augmented',
                        type=int, default=593341)

    parser.add_argument('--num_procs',
                        help='Number of processes for paralleled augmentation',
                        type=int, default=cpu_count())

    parser.add_argument('--p_mirror',
                        help='Ratio to mirror an image',
                        type=float, default=0)

    parser.add_argument('--p_crop',
                        help='Ratio to randomly crop an image',
                        type=float, default=0) #default=0.5

    parser.add_argument('--crop_size',
                        help='The ratio of cropped image size to original image size, in area',
                        type=float, default=1) #default=0.8
    parser.add_argument('--crop_hw_vari',
                        help='Variation of h/w ratio',
                        type=float, default=0.1)

    parser.add_argument('--p_rotate',
                        help='Ratio to randomly rotate an image',
                        type=float, default=1.0)
    parser.add_argument('--p_rotate_crop',
                        help='Ratio to crop out the empty part in a rotated image',
                        type=float, default=1.0)
    parser.add_argument('--rotate_angle_vari',
                        help='Variation range of rotate angle',
                        type=float, default=10.0)

    parser.add_argument('--p_hsv',
                        help='Ratio to randomly change gamma of an image',
                        type=float, default=1.0)
    parser.add_argument('--hue_vari',
                        help='Variation of hue',
                        type=int, default=10)
    parser.add_argument('--sat_vari',
                        help='Variation of saturation',
                        type=float, default=0.1)
    parser.add_argument('--val_vari',
                        help='Variation of value',
                        type=float, default=0.1)

    parser.add_argument('--p_gamma',
                        help='Ratio to randomly change gamma of an image',
                        type=float, default=1.0)
    parser.add_argument('--gamma_vari',
                        help='Variation of gamma',
                        type=float, default=2.0)

    args = parser.parse_args()
    args.input_dir = args.input_dir.rstrip('/')
    args.output_dir = args.output_dir.rstrip('/')

    return args


'''
根据进程数和要增加的目标图片数，
生成每个进程要处理的文件列表和每个文件要增加的数目
'''


def generate_image_list(args):
    # 获取所有文件名和文件总数
    filenames = os.listdir(args.input_dir)
    num_imgs = len(filenames)

    # 计算平均处理的数目并向下取整
    num_ave_aug = int(math.floor(args.num / num_imgs))

    # 剩下的部分不足平均分配到每一个文件，所以做成一个随机幸运列表
    # 对于幸运的文件就多增加一个，凑够指定的数目
    rem = args.num - num_ave_aug * num_imgs
    lucky_seq = [True] * rem + [False] * (num_imgs - rem)
    random.shuffle(lucky_seq)

    # 根据平均分配和幸运表策略，
    # 生成每个文件的全路径和对应要增加的数目并放到一个list里
    img_list = [
        (os.sep.join([args.input_dir, filename]), num_ave_aug + 1 if lucky else num_ave_aug)
        for filename, lucky in zip(filenames, lucky_seq)
    ]

    # 文件可能大小不一，处理时间也不一样，
    # 所以随机打乱，尽可能保证处理时间均匀
    random.shuffle(img_list)

    # 生成每个进程的文件列表，
    # 尽可能均匀地划分每个进程要处理的数目
    length = float(num_imgs) / float(args.num_procs)
    indices = [int(round(i * length)) for i in range(args.num_procs + 1)]
    return [img_list[indices[i]:indices[i + 1]] for i in range(args.num_procs)]


# 每个进程内调用图像处理函数进行扰动的函数
def augment_images(filelist, args):
    # 遍历所有列表内的文件
    for filepath, n in filelist:
        img = cv2.imread(filepath)
        filename = filepath.split(os.sep)[-1]
        dot_pos = filename.rfind('.')

        # 获取文件名和后缀名
        imgname = filename[:dot_pos]
        ext = filename[dot_pos:]

        print('Augmenting {} ...'.format(filename))
        for i in range(n):
            img_varied = img.copy()

            # 扰动后文件名的前缀
            varied_imgname = '{}_{:0>3d}_'.format(imgname, i)

            # 按照比例随机对图像进行镜像
            # if random.random() < args.p_mirror:
            #     # 利用numpy.fliplr(img_varied)也能实现
            #     img_varied = cv2.flip(img_varied, 1)
            #     varied_imgname += 'm'

            # 按照比例随机对图像进行裁剪
            # if random.random() < args.p_crop:
            #     img_varied = random_crop(
            #         img_varied,
            #         args.crop_size,
            #         args.crop_hw_vari)
            #     varied_imgname += 'c'

            # 按照比例随机对图像进行旋转
            # if random.random() < args.p_rotate:
            #     img_varied = random_rotate(
            #         img_varied,
            #         args.rotate_angle_vari,
            #         args.p_rotate_crop)
            #     varied_imgname += 'r'

            #按照比例随机对图像进行HSV扰动
            if random.random() < args.p_hsv:
                img_varied = random_hsv_transform(
                    img_varied,
                    args.hue_vari,
                    args.sat_vari,
                    args.val_vari)
                varied_imgname += 'h'

            # 按照比例随机对图像进行Gamma扰动
            if random.random() < args.p_gamma:
                img_varied = random_gamma_transform(
                    img_varied,
                    args.gamma_vari)
                varied_imgname += 'g'

            # 生成扰动后的文件名并保存在指定的路径
            output_filepath = os.sep.join([
                args.output_dir,
                '{}{}'.format(varied_imgname, ext)])
            cv2.imwrite(output_filepath, img_varied)


# 主函数
def main():
    # 获取输入输出和变换选项
    args = parse_args()
    params_str = str(args)[10:-1]
    print params_str

    # 如果输出文件夹不存在，则建立文件夹
    if not os.path.exists(args.output_dir):
        os.mkdir(args.output_dir)

    print('Starting image data augmentation for {}\n'
          'with\n{}\n'.format(args.input_dir, params_str))

    # 生成每个进程要处理的列表
    sublists = generate_image_list(args)

    # 创建进程
    processes = [Process(target=augment_images, args=(x, args,)) for x in sublists]

    # 并行多进程处理
    for p in processes:
        p.start()

    for p in processes:
        p.join()

    print('\nDone!')


if __name__ == '__main__':
    main()
