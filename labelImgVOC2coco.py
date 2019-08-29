import json
import os, sys
import xml.etree.ElementTree as ET

PROJECT_DIR   =  '/home/watson/Documents/voc2coco/'

# DATA_DIR       = PROJECT_DIR + 'coco_train2014/' # pic save path
ANN_DIR        = PROJECT_DIR + 'annotations/'
COCO_JSON_FILE = PROJECT_DIR + 'annotations/instances_train2014.json'  # json save path

VOC_XMLS_DIR = '/home/watson/Documents/THzDataset/annotations/train_xml/'
THZ_IMGS_DIR = '/home/watson/Documents/THzDataset/train_img_rgb/'

# if not os.path.exists(PROJECT_DIR): 
#     os.makedirs(PROJECT_DIR)
# if not os.path.exists(DATA_DIR):
#     os.makedirs(DATA_DIR)
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

def get(root, name):
    vars = root.findall(name)
    return vars

def get_and_check(root, name, length):
    vars = root.findall(name)
    if len(vars) == 0:
        raise NotImplementedError('Can not find %s in %s.'%(name, root.tag))
    if length > 0 and len(vars) != length:
        raise NotImplementedError('The size of %s is supposed to be %d, but is %d.'%(name, length, len(vars)))
    if length == 1:
        vars = vars[0]
    return vars

def get_filename(filename):
    try:
        filename = os.path.splitext(filename)[0] # 分离文件名与扩展名；默认返回(fname,fextension)元组，可做分片操作
        return filename # 返回文件名
    except:
        raise NotImplementedError('Filename %s is supposed to be an integer.'%(filename))

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
        filename = get_filename(get_and_check(root, 'filename', 1).text) + '.jpg'
        
        # image: id
        image_id = image_id + 1
        
        # image: width & height
        size = get_and_check(root, 'size', 1)
        img_width = int(get_and_check(size, 'width', 1).text)
        img_height = int(get_and_check(size, 'height', 1).text)

        # images
        image = {
            'file_name': filename, 
            'id':image_id,
            'width': img_width,
            'height': img_height
            }

        coco_json['images'].append(image)


        ## Cruuently we do not support segmentation
        #  segmented = get_and_check(root, 'segmented', 1).text
        #  assert segmented == '0'
        for obj in get(root, 'object'):
            # annotation: category_id
            category = get_and_check(obj, 'name', 1).text
            if category not in PRE_DEFINE_CATEGORIES:
                new_id = len(PRE_DEFINE_CATEGORIES) + 1
                PRE_DEFINE_CATEGORIES[category] = new_id
            category_id = PRE_DEFINE_CATEGORIES[category]

            # annotation: id
            bbox_id += 1

            # annotation: bbox
            bndbox = get_and_check(obj, 'bndbox', 1)
            xmin = int(get_and_check(bndbox, 'xmin', 1).text) - 1
            ymin = int(get_and_check(bndbox, 'ymin', 1).text) - 1
            xmax = int(get_and_check(bndbox, 'xmax', 1).text)
            ymax = int(get_and_check(bndbox, 'ymax', 1).text)
            assert(xmax > xmin)
            assert(ymax > ymin)
            bbox_width = abs(xmax - xmin)
            bbox_height = abs(ymax - ymin)

            # annotation: segmentation
            seg = []
            #left_top
            seg.append(xmin)
            seg.append(ymin)
            #left_bottom
            seg.append(xmin)
            seg.append(ymin + bbox_height)
            #right_bottom
            seg.append(xmin + bbox_width)
            seg.append(ymin + bbox_height)
            #right_top
            seg.append(xmin + bbox_width)
            seg.append(ymin)

            annotation = {
                'id': bbox_id,
                'image_id': image_id,
                'category_id': category_id,
                'area': bbox_width * bbox_height, 
                'bbox':[xmin, ymin, bbox_width, bbox_height],
                'iscrowd': 0, 
                'segmentation': seg
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


if __name__ == '__main__':
    print('start convert')
    labelImg_voc2coco()
    print('\nconvert finished!')