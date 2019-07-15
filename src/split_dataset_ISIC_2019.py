# Author : Vikas Chouhan (presentisgood@gmail.com)
import os
import sys
import argparse
import csv
import copy
import random
import numpy as np
import PIL
import shutil
import random
from   common import *

def split_dataset(metadata_file, split_ratio, image_dir, output_dir):
    metadata_file  = rp(metadata_file)
    assert(sum(split_ratio) == 100)

    # Get list of all unique images
    row_l        = parse_csv_file(metadata_file)
    label_map    = {}
    distr_map    = {}

    # Populate label_map and distr_map
    for row_indx_t, row_t in enumerate(row_l):
        try:
            file_name_t  = row_t[0]
            label_num_t  = int(row_t[1])
            label_name_t = row_t[2]
        except:
            continue
        # endtry

        # Populate label map
        if label_name_t not in label_map:
            label_map[label_name_t] = label_num_t
        else:
            assert label_map[label_name_t] == label_num_t, \
                    'Inconsistent label mismatch at row {}. Previous label num acquired = {}, new label num found = {}'.format(row_indx_t,
                            label_map[label_name_t], label_num_t)
        # endif

        # Populate distrmap
        if label_name_t not in distr_map:
            distr_map[label_name_t] = []
        # endif
        distr_map[label_name_t].append(file_name_t)
    # endfor

    # Some prints
    distr_len_map = {x:len(y) for x,y in distr_map.items()}
    print('Distr count map before applying split = {}'.format(distr_len_map))


    # Split the distribution into training and validation maps
    # Use [newer (mapped) labels => image files] map for this
    train_distr_map = {}
    val_distr_map   = {}
    test_distr_map  = {}
    for lbl_t in distr_map:
        random.shuffle(distr_map[lbl_t])  # shuffle file list
        tot_imgs_t = len(distr_map[lbl_t])
        train_end_indx = int(split_ratio[0]/sum(split_ratio) * tot_imgs_t)
        val_end_indx   = int((split_ratio[0] + split_ratio[1])/sum(split_ratio) * tot_imgs_t)

        train_distr_map[lbl_t] = distr_map[lbl_t][0:train_end_indx]
        val_distr_map[lbl_t]   = distr_map[lbl_t][train_end_indx:val_end_indx]
        test_distr_map[lbl_t]  = distr_map[lbl_t][val_end_indx:]
    # endfor

    # Print train,val,test distr maps
    print('Train distr count map = {}'.format({x:len(y) for x,y in train_distr_map.items()}))
    print('Val distr count map   = {}'.format({x:len(y) for x,y in val_distr_map.items()}))
    print('Test distr count map  = {}'.format({x:len(y) for x,y in test_distr_map.items()}))

    def _write_split(split_name, split_distr_map, label_map, out_dir):
        split_dir = '{}/{}'.format(out_dir, split_name)
        out_image_dir = '{}/images'.format(split_dir)
        out_annot_file = '{}/annot.csv'.format(split_dir)
        out_label_file = '{}/labels.csv'.format(split_dir)
        metadata = []
        print('Writing split {} in {}'.format(split_name, split_dir))

        # Make directory
        mkdir(out_image_dir)

        for lbl_t in split_distr_map:
            for file_t in split_distr_map[lbl_t]:
                src_file = '{}/{}'.format(image_dir, file_t)
                dst_file = '{}/{}'.format(out_image_dir, file_t)
                #shutil.copy(src_file, dst_file)
                soft_link(src_file, dst_file)

                metadata.append([file_t, label_map[lbl_t]])
            # endfor
        # endfor

        # Write metadata
        write_csv(metadata, out_annot_file)
        # Write label file
        write_csv([[x, y] for x,y in label_map.items()], out_label_file)
    # enddef

    _write_split('train', train_distr_map, label_map, output_dir)
    _write_split('val', val_distr_map, label_map, output_dir)
    _write_split('test', test_distr_map, label_map, output_dir)
# enddef


if __name__ == '__main__':
    parser  = argparse.ArgumentParser()
    parser.add_argument('--image_dir',      help='Input image dir',                      type=str, default=None)
    parser.add_argument('--metadata',       help='Input metadata csv file in format [file_name, label_num, label_name]',
                                                                                         type=str, default=None)
    parser.add_argument('--split_ratio',    help='Dataset split ratio (separated by :)', type=str, default='80:20')
    parser.add_argument('--out_dir',        help='Output directory.',                    type=str, default=None)
    args    = parser.parse_args()

    if args.__dict__['metadata'] == None or args.__dict__['image_dir'] == None or \
            args.__dict__['out_dir'] == None:
        print('All options are mandatory.Please use --help for more information.')
        sys.exit(-1)
    # endif

    image_dir    = rp(args.__dict__['image_dir'])
    output_dir   = rp(args.__dict__['out_dir'])
    metadata     = rp(args.__dict__['metadata'])
    try:
        split_ratio  = [int(x) for x in args.__dict__['split_ratio'].split(':')]
    except:
        print('split ratio should be in form of tr:va:te or tr:va where each of tr,va and te are integers.')
        sys.exit(-1)
    # endtry
    if len(split_ratio) == 3:
        print('Test split is not supported by this script at the moment !!')
        sys.exit(-1)
    # endif

    split_dataset(metadata, split_ratio, image_dir, output_dir)
# endif
