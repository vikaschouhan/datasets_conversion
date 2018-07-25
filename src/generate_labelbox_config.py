#!/usr/bin/env python3

import argparse
import sys
import os
import re
import unidecode
import json

def rp(x):
    return os.path.expanduser(x)
# enddef

def gen_json(in_file, out_file, json_file=None):
    color_l    = [ "navy", "green", "orange", "pink", "red" ]

    in_file    = rp(in_file)
    out_file   = rp(out_file)
    json_d     = None
    color_ctr  = 0
    max_ctr    = len(color_l)

    if json_file:
        json_file  = rp(json_file)
        json_d     = json.load(open(json_file, 'r'))
        if "tools" not in json_d:
            print('Wrong json passed in {}'.format(json_file))
            sys.exit(-1)
        # endif
        if not isinstance(json_d["tools"], list):
            print('Wrong json passed in {}'.format(json_file))
            sys.exit(-1)
        # endif
    # endif

    if json_d == None:
        out_dict = {}
        out_dict["tools"] = []
        color_ctr = 0
    else:
        out_dict = json_d
        color_ctr = color_l.index(json_d["tools"][-1]["color"])
        if color_ctr == max_ctr - 1:
            color_ctr = 0
        else:
            color_ctr = color_ctr + 1
        # endif
        print(color_ctr)
    # endif
    
    with open(in_file, 'r') as f_read:
        for line_t in f_read:
            ascii_str = unidecode.unidecode(line_t)
            match  = re.search('^\s+\d+\.\s+([\w\s\d\'\.]+)', ascii_str)
            if match:
                #print(match.groups()[0].rstrip())
                if color_ctr == max_ctr:
                    color_ctr = 0
                # endif
                key = match.groups()[0].rstrip()
                out_dict["tools"].append({
                        "name"    : key,
                        "color"   : color_l[color_ctr],
                        "tool"    : "rectangle"
                    })
                color_ctr = color_ctr + 1
        # endfor
    # endwith

    # Write final json
    with open(out_file, 'w') as f_out:
        json.dump(out_dict, f_out, indent=4)
    # endif
# enddef

if __name__ == '__main__':
    parser  = argparse.ArgumentParser()
    parser.add_argument('--in',     help='Input text file',          type=str, default=None)
    parser.add_argument('--out',    help='Output json file',          type=str, default=None)
    parser.add_argument('--ext',    help='External file to prepended.', type=str, default=None)
    args    = parser.parse_args()

    if args.__dict__['in'] == None or args.__dict__['out'] == None:
        print('All options are mandatory.Please use --help for more information.')
        sys.exit(-1)
    # endif

    gen_json(args.__dict__['in'], args.__dict__['out'], args.__dict__['ext'])
# endif
