
import os
import json
import numpy as np
import shutil
import pandas as pd
import cv2

defect_name2label = {'background': 0, 'mask': 1}

CLASSES = ('mask')

class Fabric2COCO:

    def __init__(self, mode="val"):
        self.images = []
        self.annotations = []
        self.categories = []
        self.img_id = 0
        self.ann_id = 0
        self.mode =mode
        if not os.path.exists("/media/hasx/DATA5/code/pytorch/CenterNet/CenterNet/data/coco/images/{}".format(self.mode + '2017')):
            os.makedirs("/media/hasx/DATA5/code/pytorch/CenterNet/CenterNet/data/coco/images/{}".format(self.mode + '2017'))

    def to_coco(self, anno_file_dir, img_dir):
        self._init_categories()
        annoFiles = os.listdir(anno_file_dir)
        for annoFile in annoFiles:
            if not annoFile.endswith(".json"):
                continue
            # anno_result= pd.read_json(open(anno_file,"r"))
            annoFilepath = os.path.join(anno_file_dir, annoFile)
            jsonFile = open(annoFilepath,encoding='GBK').read()
            anno_result = json.loads(jsonFile)
            # print(anno_result["shape"])
            # print(type(anno_result["name"]))
            # exit()
            imageName = anno_result["imagePath"]
            width = anno_result["imageWidth"]
            shapes_list=anno_result["shapes"]
            height = anno_result["imageHeight"]
            keypoints = []
            bboxs = []
            # print(name_list)
            # print(len(name_list))
            # exit()
            for shapes in shapes_list:
                shapeType = shapes["shape_type"]
                Label = shapes["label"]
                # groupId = shapes["group_id"]
                # ncount = 0 # same ID need count twice

                if shapeType == "polygon" and Label == "1":
                    keypoint_ = []
                    Points = shapes["points"]
                    for Point in Points:
                        keypoint_.append(round(Point[0], 2))
                        keypoint_.append(round(Point[1], 2))
                        keypoint_.append(2)        
                    #print(keypoint_)
                    # preGroupId = groupId
                    keypoints.append(keypoint_)

                    # ncount += 1

                if shapeType == "rectangle" and Label == "1":
                    bbox_ = []
                    Bboxs = shapes["points"]
                    for Bbox in Bboxs:
                        bbox_.append(Bbox[0])
                        bbox_.append(Bbox[1])
                    # ncount += 1
                    bboxs.append(bbox_)
                # print('ncount', ncount)
                # if ncount == 2:  # same ID need count twice
                #
                #     keypoints.append(keypoint)
                #     bboxs.append(bbox)
            if len(bboxs) == 0:
                len2 = len(keypoints)
                for i in range(len2):
                    keypoints_ = np.array(keypoints[i])
                    bbox_x = keypoints_[::3]
                    bbox_y = keypoints_[1::3]
                    x1 = min(bbox_x)
                    y1 = min(bbox_y)
                    x2 = max(bbox_x)
                    y2 = max(bbox_y)
                    bbox_ = [x1, y1, x2, y2]
                    bboxs.append(bbox_)

            # print(bboxs)
            # exit()

            img_path = os.path.join(img_dir, imageName)

            # if os.path.isfile(img_path) == False:
            #     print('skip(False):', img_path)
            #     continue
            print(annoFilepath)
            #print('len(keypoints)', len(keypoints))
            #print('len(bboxs)', len(bboxs))
            # assert len(keypoints[0]) == 18
            if len(bboxs) != len(keypoints):
                continue

            count = 0

            for bbox, keypoint in zip(bboxs, keypoints):
                label = 1
                print('len(keypoint)', len(keypoint))
                print('len(bbox)', len(bbox))
                if len(keypoint) != 12:
                    continue
                if len(bbox) != 4:
                    continue

                annotation, area = self._annotation(label, bbox, keypoint)
                # if area < 400:
                #     print('skip(area small):', img_path)
                #     continue
                count += 1
                print('count:', count)

                self.annotations.append(annotation)
                self.ann_id += 1

                # img = cv2.imread(img_path)
                # h, w, c = img.shape

            self.images.append(self._image(img_path, height, width))
            self.img_id += 1
            self._cp_img(img_path)

        instance = {}
        instance['info'] = 'mask_defect'
        instance['license'] = ['none']
        instance['images'] = self.images
        instance['annotations'] = self.annotations
        instance['categories'] = self.categories
        return instance

    def _init_categories(self):
        for v in range(1, 2):
            print(v)
            category = {}
            category['id'] = v
            category['name'] = 'mask'
            category['supercategory'] = 'mask'
            category['keypoints'] = ['left_up', 'right_up', 'right_down', 'left_down']
            category['skeleton'] = [[1, 2], [2, 3], [3, 4], [4, 1]] # coco关键点从1开始
            self.categories.append(category)
        # for k, v in defect_name2label.items():
        #     category = {}
        #     category['id'] = v
        #     category['name'] = k
        #     category['supercategory'] = 'defect_name'
        #     self.categories.append(category)

    def _image(self, path, h, w):
        image = {}
        image['height'] = h
        image['width'] = w
        image['id'] = self.img_id
        image['file_name'] = os.path.basename(path)
        return image

    def _annotation(self,label, bbox, keypoints):
        area=(bbox[2]-bbox[0])*(bbox[3]-bbox[1])
        points=[[bbox[0],bbox[1]],[bbox[2],bbox[1]],[bbox[2],bbox[3]],[bbox[0],bbox[3]]]
        annotation = {}
        annotation['id'] = self.ann_id
        annotation['image_id'] = self.img_id
        annotation['category_id'] = label
        # annotation['segmentation'] = [np.asarray(points).flatten().tolist()]
        annotation['segmentation'] = []
        annotation['bbox'] = self._get_box(points)
        annotation['iscrowd'] = 0
        annotation['area'] = round(area, 2)
        annotation['num_keypoints'] = len(keypoints)/3
        annotation['keypoints'] = keypoints
        return annotation, area

    def _cp_img(self, img_path):
        shutil.copy(img_path, os.path.join("/media/hasx/DATA5/code/pytorch/CenterNet/CenterNet/data/coco/images/{}".format(self.mode + '2017'), os.path.basename(img_path)))

    def _get_box(self, points):
        min_x = min_y = np.inf
        max_x = max_y = 0
        for x, y in points:
            min_x = min(min_x, x)
            min_y = min(min_y, y)
            max_x = max(max_x, x)
            max_y = max(max_y, y)
        '''coco,[x,y,w,h]'''
        return [round(min_x, 2), round(min_y, 2), round(max_x - min_x, 2), round(max_y - min_y, 2)]

    def save_coco_json(self, instance, save_path):
        import json
        with open(save_path, 'w') as fp:
            json.dump(instance, fp, indent=1, separators=(',', ': '),ensure_ascii=False)


def background(l1, l2, sufix):
    jsonpath = "./annotations.json"
    jsonFile = open(jsonpath).read()
    data_list = json.loads(jsonFile)
    ## d['title']中的'title'是自己json格式文件里面的names
    categories = data_list['categories']
    annotations = data_list['annotations']
    df_annotations = pd.DataFrame(annotations)
    # print(df_annotations.index)
    newDfcategories = pd.DataFrame(categories).drop(5)
    newDfcategories = newDfcategories.sort_values(by='id', ascending=True)
    data_list['categories'] = newDfcategories.to_dict(orient='record')
    # print(data_list['categories'])
    # print(df_annotations['category_id'].value_counts())

    # newDfannotations = df_annotations[~df_annotations['category_id'].isin([0])] # 反选不包含0类别的
    # newDfannotations = pd.DataFrame(annotations).drop('category_id'==0)
    # newDfannotations = df_annotations[df_annotations['bbox'].isin([0])] # 反选不包含0类别的
    newDfannotations = df_annotations['bbox'].tolist() # 反选不包含0类别的
    # newDfannotations = [newDfannotations[ind] for ind, bool in enumerate([l1 <min(d[2:])<l2 for d in newDfannotations]) if bool == True]
    index = [ind for ind, bool in enumerate([l1 <min(d[2:])<l2 for d in newDfannotations]) if bool == True] #筛选出符合条件的index
    # newDfannotations = [newDfannotations[ind] for ind in index]
    # df_annotations = (df_annotations.iloc[ind] for ind in index)
    df_annotations = df_annotations.iloc[index]

    data_list['annotations'] = df_annotations.to_dict(orient='record')
    print(len(data_list['annotations']))
    # print(newDfannotations)
    # print(len(newDfannotations))
    # df_annotations['bbox'] = newDfannotations

    # print(df_annotations)
    # print(newDfannotations[:, 2:])

    # print(newDfannotations['category_id'].value_counts())
    # data_list['annotations'] = newDfannotations.to_dict(orient='record')

    # print(type(data_list))
    # final_json = json.dumps(data_list, ensure_ascii=False)
    final_json = json.dumps(data_list)
    with open("./annotations_%s.json"%sufix,mode='w'
                ) as file:
        file.write(final_json)

    # print(df_annotations)

def rmllow():
    jsonpath = "./result.json"
    jsonFile = open(jsonpath).read()
    data_list = json.loads(jsonFile)
    annotations = data_list['annotations']
    df_annotations = pd.DataFrame(annotations)
    newDfannotations = df_annotations['score'].tolist()  # 反选不包含0类别的
    index = [ind for ind, bool in enumerate([d > 0.05 for d in newDfannotations]) if bool == True] #筛选出符合条件的index
    df_annotations = df_annotations.iloc[index]
    data_list['annotations'] = df_annotations.to_dict(orient='record')
    print(len(data_list['annotations']))
    final_json = json.dumps(data_list, indent = 4, separators=(',', ': '))
    with open(
            "./annotations_%s.json" % "new",
            mode='w'
            ) as file:
        file.write(final_json)


if __name__ == '__main__':
    # TODO 当一个json包含多个目标,且标注顺序不对应是结果可能会有误

    '''转换有瑕疵的样本为coco格式'''
    # name = '5env_00_crop.json'
    img_dir = "pic"
    anno_dir="pic"
    mode = "train"
    fabric2coco = Fabric2COCO(mode=mode)
    train_instance = fabric2coco.to_coco(anno_dir, img_dir)
    if not os.path.exists("/media/hasx/DATA5/code/pytorch/CenterNet/CenterNet/data/coco/annotations/"):
        os.makedirs("/media/hasx/DATA5/code/pytorch/CenterNet/CenterNet/data/coco/annotations/")
    fabric2coco.save_coco_json(train_instance, "/media/hasx/DATA5/code/pytorch/CenterNet/CenterNet/data/coco/annotations/"+'person_keypoints_{}2017.json'.format(mode))
    # l1, l2 = 0, 0
    # # sufixes = ['under40s', 'beyond40s']
    # sufixes = ['all']
    # for sufix in sufixes:
    #     if sufix == 'under40s':
    #         l1 = 0
    #         l2 = 40
    #     else:
    #         l1 = 0
    #         l2 = 44420
    #     background(l1, l2, sufix)
    # rmllow()

