import csv
import os
import sys
import glob
import shutil
import argparse
import uuid

def mkdir(dir):
    if not os.path.isdir(dir):
        os.mkdir(dir)
    # endif
# enddef

def chkdir(dir):
    if not os.path.isdir(dir):
        print('{} does not exist !!'.format(dir))
        sys.exit(-1)
    # endif
# enddef

def rp(dir):
    return os.path.expanduser(dir)
# enddef

def parse_all(dataset_root, dst_root):
    # resolve
    dataset_root    = rp(dataset_root)
    dst_root        = rp(dst_root)
    img_sufx_list   = [ '*.png', '*.jpg', '*.jpeg', '*.bmp', '*.tiff' ]
    img_sufx_list   = img_sufx_list + [ x.upper() for x in img_sufx_list ]

    # Check if dirs exist
    chkdir(dataset_root)
    mkdir(dst_root)
    
    ## glob
    dirs = glob.glob1(dataset_root, '*')
    label_dict = {}
    for dir_t in dirs:
        dir_this = '{}/{}'.format(dataset_root, dir_t)
        if dir_t not in label_dict:
            label_dict[dir_t] = []
        # endif
        pic_list = []
        for img_sufx_t in img_sufx_list:
            pic_list = pic_list + glob.glob1(dir_this, img_sufx_t)
        # endfor
        # Add to dictionary
        label_dict[dir_t] = pic_list
    # endfor

    # Copy images
    dst_img_dir    = '{}/{}'.format(dst_root, 'images')
    dst_img_annot  = '{}/{}'.format(dst_root, 'annot.csv')
    dst_img_labels = '{}/{}'.format(dst_root, 'labels.csv')
    # Create image dir
    mkdir(dst_img_dir)

    # Generate labels
    label_to_num_map = {}
    for k_t in label_dict:
        label_to_num_map[k_t] = len(label_to_num_map)
    # endfor

    # Copy files & write annot file
    with open(dst_img_annot, 'w') as annot_fout:
        for k_t in label_dict:
            for pic_t in label_dict[k_t]:
                dst_pic  = str(uuid.uuid4()) + os.path.splitext(pic_t)[1]
                src_file = '{}/{}/{}'.format(dataset_root, k_t, pic_t)
                dst_file = '{}/{}'.format(dst_img_dir, dst_pic)
                print('{} -> {}      '.format(pic_t, dst_pic), end='\r')
                # Copy
                shutil.copy(src_file, dst_file)
                # Write annot
                annot_fout.write('{},{}\n'.format(dst_pic, label_to_num_map[k_t]))
            # endfor
        # endfor
    # endwith

    # Write label file
    print('Writing labels..', end='\r')
    with open(dst_img_labels, 'w') as f_label_out:
        for key in label_to_num_map:
            f_label_out.write('{},{}\n'.format(key, label_to_num_map[key]))
        # endfor
    # endwith
# enddef

if __name__ == '__main__':
    parser  = argparse.ArgumentParser()
    parser.add_argument('--dataset_root',     help='Dataset Root directory',             type=str, default=None)
    parser.add_argument('--out_dir',          help='Output Directory.',                  type=str, default=None)
    args    = parser.parse_args()

    if args.__dict__['dataset_root'] == None or args.__dict__['out_dir'] == None:
        print('All options are mandatory.Please use --help for more information.')
        sys.exit(-1)
    # endif

    dataset_root = args.__dict__['dataset_root']
    out_dir      = args.__dict__['out_dir']

    parse_all(dataset_root, out_dir)
# endif
