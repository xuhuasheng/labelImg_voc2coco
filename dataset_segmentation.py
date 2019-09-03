# =========================================================
# @purpose: 将数据集按比例分割成训练集和测试集
# @date：   2019/9
# @version: v1.0
# @author： Xu Huasheng
# @github： https://github.com/xuhuasheng/train_test_dataset_segmentation
# ==========================================================
import os
import shutil
import random

ALL_DATA_PATH = '/home/watson/Documents/aug_THzDatasets/All_Data/'
ALL_XMLS_PATH = ALL_DATA_PATH + 'xmls/'
ALL_IMGS_PATH = ALL_DATA_PATH + 'imgs/'

OUTPUT_PATH = '/home/watson/Documents/aug_THzDatasets/'
TRAIN_PATH = OUTPUT_PATH + 'train/'
VAL_PATH  = OUTPUT_PATH + 'val/'
TRAIN_XMLS_PATH = OUTPUT_PATH + 'train_xmls/'
VAL_XMLS_PATH = OUTPUT_PATH + 'val_xmls/'

imgs_list = os.listdir(ALL_IMGS_PATH)
xmls_list = os.listdir(ALL_XMLS_PATH)

TRAIN_TEST_RATIO = 0.8 # 分割比例
all_dataset_num = len(imgs_list) # 1792
trainset_num = round(all_dataset_num * TRAIN_TEST_RATIO) # 1434
testset_num = all_dataset_num - trainset_num # 358

trainset_cnt = 0
testset_cnt = 0

random.seed(0) #设置随机种子，保证每次随机生成一致
random.shuffle(imgs_list) # 打乱文件列表

# 训练集分割
for img_fileName in imgs_list[:trainset_num]:
    img_fullFileName = os.path.join(ALL_IMGS_PATH + img_fileName) # 路径拼接，获得图片绝对路径
    img_name = img_fileName.split('.')[0] # 去掉后缀名，获得图片名字
    
    xml_name = img_name
    xml_fileName = xml_name + '.xml'
    xml_fullFileName = os.path.join(ALL_XMLS_PATH + xml_fileName)

    # 判断对应xml文件是否存在
    if xml_fileName not in xmls_list:
        print('WARNING:' + xml_fileName + 'is not exist in' + ALL_XMLS_PATH)
        continue

    print(' trainset copying... ' + img_name)
    shutil.copy(img_fullFileName, TRAIN_PATH)
    shutil.copy(xml_fullFileName, TRAIN_XMLS_PATH)
    trainset_cnt += 1

# 测试集分割
for img_fileName in imgs_list[trainset_num :]:
    img_fullFileName = os.path.join(ALL_IMGS_PATH + img_fileName) # 路径拼接，获得图片绝对路径
    img_name = img_fileName.split('.')[0] # 去掉后缀名，获得图片名字
    
    xml_name = img_name
    xml_fileName = xml_name + '.xml'
    xml_fullFileName = os.path.join(ALL_XMLS_PATH + xml_fileName)

    # 判断对应xml文件是否存在
    if xml_fileName not in xmls_list:
        print('WARNING:' + xml_fileName + 'is not exist in' + ALL_XMLS_PATH)
        continue

    print('testset copying... ' + img_name)
    shutil.copy(img_fullFileName, VAL_PATH)
    shutil.copy(xml_fullFileName, VAL_XMLS_PATH)
    testset_cnt += 1

print('trainset_cnt: %d' % (trainset_cnt))
print('testset_cnt: %d' % (testset_cnt))
print('ratio: %f' % (trainset_cnt/all_dataset_num))
print('dataset segmentation finished!')



