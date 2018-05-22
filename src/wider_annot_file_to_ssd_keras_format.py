#!/usr/bin/env python3

import os, sys
import argparse

def parse_widerface_annot_file(annot_file_name, new_annot_file_name):
    curr_image = None
    face_indx  = 1

    with open(annot_file_name, 'r') as f_read:
        with open(new_annot_file_name, 'w') as f_write:
            # Write header
            #f_write.write('#{},{},{},{},{},{}\n'.format('file_name', 'face_indx', 'x_min', 'x_max', 'y_min', 'y_max'))

            for l_t in f_read:
                l_contents = l_t.strip('\n').split(' ')
                # Check how many columns
                if len(l_contents) == 1:
                    # Check if it's file_name or number of faces
                    if l_contents[0].split('.')[-1] == 'jpg':
                        curr_image = os.path.basename(l_contents[0])   # Get only file name
                    # endif
                # endif
                if len(l_contents) > 1:
                    # This may be the row for bbox coordinates
                    # Check if curr_image is initialized properly. If not, then skip
                    if curr_image == None:
                        continue
                    # endif
                    x_min = int(l_contents[0])
                    y_min = int(l_contents[1])
                    width = int(l_contents[2])
                    height = int(l_contents[3])
                    x_max = x_min + width
                    y_max = y_min + height
                    f_write.write('{},{},{},{},{},{}\n'.format(curr_image, face_indx, x_min, x_max, y_min, y_max))
                # endif
            # endfor
        # endwith
    # endwith
# enddef

if __name__ == '__main__':
    parser  = argparse.ArgumentParser()
    parser.add_argument("--srcwiderannot", help="Source annotation file for wider database", type=str, default=None)
    parser.add_argument("--dstwiderannot", help="Destination annotation file", type=str, default=None)
    args = parser.parse_args()

    if args.__dict__['srcwiderannot'] == None or args.__dict__['dstwiderannot'] == None:
        print('--srcwiderannot & --dstwiderannot both are required !!')
        sys.exit(-1)
    # endif

    parse_widerface_annot_file(args.__dict__['srcwiderannot'], args.__dict__['dstwiderannot'])
# endif
