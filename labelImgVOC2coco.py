# =========================================================
# @purpose: 把labelImg标注的voc格式数据转换成coco格式数据
# @date：   2019/8
# @version: v1.0
# @author： Xu Huasheng
# @github： https://github.com/xuhuasheng/labelImg_voc2coco
# ==========================================================

import json
import os, sys
import xml.etree.ElementTree as ET

PROJECT_DIR   =  '/home/watson/Documents/mask_THzDatasets/'
ANN_DIR        = PROJECT_DIR + 'annotations/'

#==================== 需要修改 train or val ========================
COCO_JSON_FILE = ANN_DIR + 'mask_THz_val.json'  # json save path
VOC_XMLS_DIR = '/home/watson/Documents/mask_THzDatasets/val_xmls/'
#==================================================================

if not os.path.exists(ANN_DIR):
    os.makedirs(ANN_DIR)

# coco images 的列表
images = []

# coco annotations 的列表
annotations = []

# coco categories 的列表
# If necessary, pre-define category and its id
PRE_DEFINE_CATEGORIES = {"gun": 1, "phone": 2}
categories = [
    {
        'id': 1,
        'name': 'gun',
        'supercategory': 'object',
    },
    {
        'id': 2,
        'name': 'phone',
        'supercategory': 'object',
    }
]

# coco 存储格式的字典
coco_json = {
    "images":images,  
    "annotations": annotations,                
    "categories": categories
    }




'''
purpose: voc 的xml 转 coco 的json
'''
def labelImg_voc2coco():
    voc_xmls_list = os.listdir(VOC_XMLS_DIR)
    converted_num = 0
    image_id = 0
    bbox_id = 0

    for xml_fileName in voc_xmls_list:
        
        # 进度输出
        converted_num += 1
        sys.stdout.write('\r>> Processing %s, Converting xml %d/%d' % (xml_fileName, converted_num, len(voc_xmls_list)))
        sys.stdout.flush()

        # 解析xml
        xml_fullName = os.path.join(VOC_XMLS_DIR, xml_fileName)
        tree = ET.parse(xml_fullName) # 解析xml元素树
        root = tree.getroot()         # 获得树的根节点
        
        # image: file_name
        filename = get_element(root, 'filename').text.split('.')[0] + '.jpg' # 读xml文件里的文件名
        # filename = xml_fileName                                                 # 读文件名
        
        # image: id
        image_id = image_id + 1
        
        # image: width & height
        size = get_element(root, 'size')
        img_width = int(get_element(size, 'width').text)
        img_height = int(get_element(size, 'height').text)

        # images
        image = {
            'file_name': filename, 
            'id':image_id,
            'width': img_width,
            'height': img_height
            }

        coco_json['images'].append(image)


        for obj in get_elements(root, 'object'):
            # annotation: category_id
            category = get_element(obj, 'name').text
            if category not in PRE_DEFINE_CATEGORIES:
                new_id = len(PRE_DEFINE_CATEGORIES) + 1
                PRE_DEFINE_CATEGORIES[category] = new_id
            category_id = PRE_DEFINE_CATEGORIES[category]

            # annotation: id
            bbox_id += 1

            # annotation: bbox
            bndbox = get_element(obj, 'bndbox')
            xmin = int(get_element(bndbox, 'xmin').text)
            ymin = int(get_element(bndbox, 'ymin').text)
            xmax = int(get_element(bndbox, 'xmax').text)
            ymax = int(get_element(bndbox, 'ymax').text)
            assert(xmax > xmin)
            assert(ymax > ymin)
            bbox_width = abs(xmax - xmin)
            bbox_height = abs(ymax - ymin)

            # annotation: segmentation
            seg = list(eval(get_element(obj, 'segmentation').text))

            annotation = {
                'id': bbox_id,
                'image_id': image_id,
                'category_id': category_id,
                'segmentation': [seg],
                'area': bbox_width * bbox_height, 
                'bbox':[xmin, ymin, bbox_width, bbox_height],
                'iscrowd': 0
                }

            coco_json['annotations'].append(annotation)

    print('\r')
    print("Num of categories: %s" % len(categories))
    print("Num of images: %s" % len(images))
    print("Num of annotations: %s" % len(annotations))
    print(PRE_DEFINE_CATEGORIES)
    # coco格式字典写入json
    with open(COCO_JSON_FILE, 'w') as outfile:  
        outfile.write(json.dumps(coco_json))

'''
input：
    @root: 根节点  
    @childElementName: 字节点tag名称
output：
    @elements:根节点下所有符合的子元素对象    
''' 
def get_elements(root, childElementName):
    elements = root.findall(childElementName)
    return elements


'''
input：
    @root: 根节点  
    @childElementName: 字节点tag名称
output：
    @elements:根节点下第一个符合的子元素对象    
''' 
def get_element(root, childElementName):
    element = root.find(childElementName)
    return element


if __name__ == '__main__':
    print('start convert')
    labelImg_voc2coco()
    print('\nconvert finished!')