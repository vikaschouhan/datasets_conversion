import os
import csv
import locale

def rp(dir):
    '''Resolve relative path to absolute path'''
    if dir == None:
        return None
    # endif
    if dir[0] == '.':
        return os.path.normpath(os.getcwd() + '/' + dir)
    else:
        return os.path.normpath(os.path.expanduser(dir))
# enddef

def mkdir(dir):
    '''Make directory.'''
    if dir == None:
        return None
    # endif
    if not os.path.isdir(dir):
        os.makedirs(dir, exist_ok=True)
    # endif
# enddef

def soft_link(src, dst):
    '''Create softlink from src to dst.'''
    if os.path.islink(dst):
        return
    if os.path.isfile(src) and os.path.isdir(dst):
        dst = dst + '/' + os.path.basename(src)
    # endif
    os.symlink(src, dst)
# enddef

def parse_csv_file(csv_file, encoding='iso-8859-1'):
    '''Parse csv file into list of rows, each row itself being a list of columns.'''
    encoding   = locale.getpreferredencoding() if encoding == None else encoding
    csv_reader = csv.reader(open(csv_file, 'r', encoding=encoding))
    row_list   = [ x for x in csv_reader ]
    return row_list
# enddef

def write_csv(row_list, csv_file, is_header=False, encoding='iso-8859-1'):
    '''Write row list to csv file.'''
    # NOTE: is_header is ignore at this time
    with open(csv_file, 'w', encoding=encoding) as out_csv:
        csv_writer = csv.writer(out_csv)
        csv_writer.writerows(row_list)
    # endwith
# enddef

