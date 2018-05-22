#!/usr/bin/env python3

import random
import os, sys
import argparse
import numpy as np
from   matplotlib import pyplot as plt
import glob
import xml.etree.ElementTree as ET
import shutil
import argparse

def generate_pascalvoc_database_for_ssd_keras(pascalvoc_dir, 
                                              class_list=['background', 'face', 'aeroplane', 'sofa'],
                                              target_dir=None,
                                              train_ratio=0.7):
    images_dir        = '{}/JPEGImages/'.format(pascalvoc_dir)
    annotations_dir   = '{}/Annotations/'.format(pascalvoc_dir)
    target_dir        = './new_pascalvoc' if target_dir == None else target_dir
    train_csv         = '{}/train.csv'.format(target_dir)
    val_csv           = '{}/val.csv'.format(target_dir)
    train_dir         = '{}/train_images'.format(target_dir)
    val_dir           = '{}/val_images'.format(target_dir)
    row_list = []

    # All debug info
    print('Pascalvoc image dir           = {}'.format(images_dir))
    print('Pascalvoc annottations dir    = {}'.format(annotations_dir))
    print('Target train csv file         = {}'.format(train_csv))
    print('Target validation csv file    = {}'.format(val_csv))
    print('Target train images dir       = {}'.format(train_dir))
    print('Target validation images dir  = {}'.format(val_dir))

    if train_ratio < 0.0 and train_ratio > 1.0:
        print('train_ratio should be between 0 and 1. Exiting')
        sys.exit(-1)
    # endif

    print('Populating all xml files in {}'.format(annotations_dir))
    xml_list = glob.glob('{}/{}'.format(annotations_dir, '*.xml'))

    print('Populating data.')
    # Iterate over all xml files
    for file_t in xml_list:
        xml_obj = ET.parse(file_t)
        for obj_t in xml_obj.findall('object'):
            obj_name = obj_t.find('name').text
            # Check of object name is to ignored or what !!
            if obj_name not in class_list:
                continue
            # endif
            obj_xmin = int(obj_t.find('bndbox').find('xmin').text)
            obj_ymin = int(obj_t.find('bndbox').find('ymin').text)
            obj_xmax = int(obj_t.find('bndbox').find('xmax').text)
            obj_ymax = int(obj_t.find('bndbox').find('ymax').text)
            filename = '{}.jpg'.format(os.path.splitext(os.path.basename(file_t))[0])
            row_list.append([filename, class_list.index(obj_name), obj_xmin, obj_xmax, obj_ymin, obj_ymax])
        # endfor
    # endfor

    # Shuffle row list and divide between train and validation
    random.shuffle(row_list)
    split_index = int(train_ratio * len(row_list))
    train_row_list = row_list[0:split_index]
    val_row_list   = row_list[split_index:]
   
    # Make dir if not present
    if not os.path.isdir(target_dir):
        os.mkdir(target_dir)
    # endif

    def __repeat(row_l, csv_f, img_dir):
        # Generate csv file
        print('Generating csv file {}'.format(csv_f))
        with open(csv_f, 'w') as f_out:
            for row_t in row_l:
                f_out.write('{},{},{},{},{},{}\n'.format(row_t[0], row_t[1], row_t[2], row_t[3], row_t[4], row_t[5]))
            # endfor
        # endwith

        if not os.path.isdir(img_dir):
            os.mkdir(img_dir)
        # endif

        # Copy relevant images to tgt dir
        print('Copying relevant images from {} to {}'.format(images_dir, img_dir))
        for row_t in row_l:
            shutil.copy('{}/{}'.format(images_dir, row_t[0]), '{}/{}'.format(img_dir, row_t[0]), follow_symlinks=True)
        # endfor
    # enddef

    # Repeat for train and val
    __repeat(train_row_list, train_csv, train_dir)
    __repeat(val_row_list, val_csv, val_dir)

    print('Classes = {}'.format(class_list))
# endfor

if __name__ == '__main__':
    default_class_list = ['background', 'face', 'aeroplane', 'sofa']
    default_target_dir = './new_pascalvoc'

    parser  = argparse.ArgumentParser()
    parser.add_argument('--pascalvocdir', help='Pascalvoc dataset root directory', type=str, default=None)
    parser.add_argument('--classes',      help='Class list separated by ","', type=str, default=None)
    parser.add_argument('--targetdir',    help='Target directory for copying relevant images.', type=str, default=None)
    args = parser.parse_args()

    if args.__dict__['pascalvocdir'] == None:
        print('--pascalvocdir is required !!')
        sys.exit(-1)
    # endif
    if args.__dict__['classes'] == None:
        print('--classes is None. Using default class list = {}'.format(default_class_list))
        class_list = default_class_list
    else:
        class_list = args.__dict__['classes'].split(',')
    # endif
    if args.__dict__['targetdir'] == None:
        print('--targetdir is None. Using default target dir = {}'.format(default_target_dir))
        target_dir = default_target_dir
    else:
        target_dir = args.__dict__['targetdir']
    # endif

    pascalvoc_dir = args.__dict__['pascalvocdir']

    # Call function
    generate_pascalvoc_database_for_ssd_keras(pascalvoc_dir, class_list, target_dir)
# endif
