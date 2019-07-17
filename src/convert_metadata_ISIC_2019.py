import pandas as pd
from   sklearn import preprocessing
import argparse
import os
import sys

col_map_isic2019 = {
        'MEL'  : 'Melanoma',
        'NV'   : 'Melanocytic nevus',
        'BCC'  : 'Basal cell carcinoma',
        'AK'   : 'Actinic keratosis',
        'BKL'  : 'Benign keratosis',
        'DF'   : 'Dermatofibroma',
        'VASC' : 'Vascular lesion',
        'SCC'  : 'Squamous cell carcinoma',
        'UNK'  : 'None of the others'
    }
col_map_isic2018 = {
        'MEL'  : 'Melanoma',
        'NV'   : 'Melanocytic nevus',
        'BCC'  : 'Basal cell carcinoma',
        'AKIEC': 'Actinic keratosis',
        'BKL'  : 'Benign keratosis',
        'DF'   : 'Dermatofibroma',
        'VASC' : 'Vascular lesion'
    }

col_map = {
        '2018' : col_map_isic2018,
        '2019' : col_map_isic2019,
    }

def process_csv(csv_file, isic_year):
    assert isic_year in ['2018', '2019'], 'invalid isic year.'
    col_map_t = col_map[isic_year]

    dframe = pd.read_csv(csv_file)
    dframe = dframe.rename(columns=col_map_t)
    dframe = dframe.set_index('image')
    categ  = dframe.idxmax(axis=1)
    lenc   = preprocessing.LabelEncoder()
    labeln = lenc.fit_transform(categ.values)
    dframe = pd.DataFrame({'image' : ['{}.jpg'.format(x) for x in categ.index], 'label' : labeln, 'label name' : categ.values})
    dframe = dframe.set_index('image')

    dst_file = os.path.splitext(csv_file)[0] + '_processed.csv'
    print('Generating {}'.format(dst_file))
    dframe.to_csv(dst_file)
# enddef

if __name__ == '__main__':
    parser  = argparse.ArgumentParser()
    parser.add_argument('--in_csv', help='Input csv metadata file.', type=str, default=None)
    parser.add_argument('--isic_year', help='ISIC Dataset year', type=str, default='2019')
    args    = parser.parse_args()

    if args.__dict__['in_csv'] is None:
        print('--in_csv is required !!')
        sys.exit(-1)
    # endif
   
    process_csv(args.__dict__['in_csv'], args.__dict__['isic_year'])
