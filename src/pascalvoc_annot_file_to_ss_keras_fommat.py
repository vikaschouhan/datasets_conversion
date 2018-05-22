#!/usr/bin/env python3

import os, sys
import argparse
import numpy as np
from   matplotlib import pyplot as plt
import glob
import xml.etree.ElementTree as ET
import shutil
import argparse

def generate_pascalvoc_database_for_ssd_keras(pascalvoc_dir, class_list=['background', 'face', 'aeroplane', 'sofa'], target_images_dir=None, target_csv_file=None):
    images_dir        = '{}/JPEGImages/'.format(pascalvoc_dir)
    annotations_dir   = '{}/Annotations/'.format(pascalvoc_dir)
    target_images_dir = './new_pascalvoc' if target_images_dir == None else target_images_dir
    target_csv_file   = './new_pascalvoc.csv' if target_csv_file == None else target_csv_file
    row_list = []

    print('Using {} as target dir for image files.'.format(target_images_dir))
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
    
    # Generate csv file
    print('Generating csv file {}'.format(target_csv_file))
    with open(target_csv_file, 'w') as f_out:
        for row_t in row_list:
            f_out.write('{},{},{},{},{},{}\n'.format(row_t[0], row_t[1], row_t[2], row_t[3], row_t[4], row_t[5]))
        # endfor
    # endwith

    # Make dir if not present
    if not os.path.isdir(target_images_dir):
        os.mkdir(target_images_dir)
    # endif
    # Copy relevant images to tgt dir
    print('Copying relevant images from {} to {}'.format(images_dir, target_images_dir))
    for row_t in row_list:
        shutil.copy('{}/{}'.format(images_dir, row_t[0]), '{}/{}'.format(target_images_dir, row_t[0]), follow_symlinks=True)
    # endfor

    print('Classes = {}'.format(class_list))
# endfor

if __name__ == '__main__':
    default_class_list = ['background', 'face', 'aeroplane', 'sofa']
    default_target_dir = './new_pascalvoc'
    default_target_csv = './new_pascalvoc.csv'

    parser  = argparse.ArgumentParser()
    parser.add_argument('--pascalvocdir', help='Pascalvoc dataset root directory', type=str, default=None)
    parser.add_argument('--classes',      help='Class list separated by ","', type=str, default=None)
    parser.add_argument('--targetdir',    help='Target directory for copying relevant images.', type=str, default=None)
    parser.add_argument('--targetcsv',    help='Target csv file.', type=str, default=None)
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
    if args.__dict__['targetcsv'] == None:
        print('--targetcsv is None. Using default target csv = {}'.format(default_target_csv))
        target_csv = default_target_csv
    else:
        target_csv = args.__dict__['targetcsv']
    # endif

    pascalvoc_dir = args.__dict__['pascalvocdir']

    # Call function
    generate_pascalvoc_database_for_ssd_keras(pascalvoc_dir, class_list, target_dir, target_csv)
# endif
