import csv
import os
import sys
import glob
import shutil
import argparse
import xml.etree.ElementTree as ET

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

def parse_xml(xml_file):
    xml_tree = ET.parse(xml_file)
    file_name = xml_tree.find('filename').text

    def toint(x):
        return int(float(x))
    # enddef

    # count object
    objs_list = []
    for obj_t in xml_tree.findall('object'):
        obj_name = obj_t.find('name').text
        xmin     = toint(obj_t.find('bndbox').find('xmin').text)
        ymin     = toint(obj_t.find('bndbox').find('ymin').text)
        xmax     = toint(obj_t.find('bndbox').find('xmax').text)
        ymax     = toint(obj_t.find('bndbox').find('ymax').text)

        objs_list.append((obj_name, xmin, ymin, xmax, ymax))
    # endfor
    return [ file_name, objs_list ]
# enddef


def parse_all(pascal_voc_root, dst_root):
    # resolve
    pascal_voc_root = rp(pascal_voc_root)
    dst_root        = rp(dst_root)

    annot_dir = pascal_voc_root + '/Annotations'
    image_dir = pascal_voc_root + '/JPEGImages'
    out_image_dir   = dst_root + '/images'
    out_annot_file  = dst_root + '/annot.csv'
    out_label_file  = dst_root + '/labels.csv'

    # Check if dirs exist
    chkdir(annot_dir)
    chkdir(image_dir)
    
    ## glob for xmls
    xml_list  = glob.glob1(annot_dir, '*.xml')
    label_map = {}

    if len(xml_list) == 0:
        print('no xmls found in {}'.format(annot_dir))
        sys.exit(-1)
    # endif

    # Make dir
    mkdir(dst_root)
    mkdir(out_image_dir)

    with open(out_annot_file, 'w') as f_annot_out:
        for xml_t in xml_list:
            xml_path     = annot_dir + '/' + xml_t
            obj_data     = parse_xml(xml_path)
            obj_list     = obj_data[1]
            file_name    = obj_data[0]
            for obj_t in obj_list:
                obj_name = obj_t[0]
                obj_xmin = obj_t[1]
                obj_ymin = obj_t[2]
                obj_xmax = obj_t[3]
                obj_ymax = obj_t[4]

                # Add object to label map if not already present
                if obj_name not in label_map:
                    label_map[obj_name] = len(label_map)
                # endif

                # Copy image file
                sys.stdout.write('\r-> {}      '.format(file_name))
                sys.stdout.flush()
                shutil.copy('{}/{}'.format(image_dir, file_name), '{}/{}'.format(out_image_dir, file_name))
                # Write annot file
                f_annot_out.write('{},{},{},{},{},{},{}\n'.format(file_name, \
                        label_map[obj_name], obj_xmin, obj_ymin, obj_xmax, obj_ymax, obj_name))
            # endfor
        # endfor
    # endwith

    # Write label file
    print('Writing label file..')
    with open(out_label_file, 'w') as f_label_out:
        for key in label_map:
            f_label_out.write('{},{}\n'.format(key, label_map[key]))
        # endfor
    # endwith
# enddef

if __name__ == '__main__':
    parser  = argparse.ArgumentParser()
    parser.add_argument('--pascal_voc_root',  help='Pascal VOC Root directory',          type=str, default=None)
    parser.add_argument('--out_dir',          help='Output Directory.',                  type=str, default=None)
    args    = parser.parse_args()

    if args.__dict__['pascal_voc_root'] == None or args.__dict__['out_dir'] == None:
        print('All options are mandatory.Please use --help for more information.')
        sys.exit(-1)
    # endif

    # Parse all xmls
    parse_all(args.__dict__['pascal_voc_root'], args.__dict__['out_dir'])
# endif
