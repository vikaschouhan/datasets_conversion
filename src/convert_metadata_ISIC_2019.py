import pandas as pd
from   sklearn import preprocessing

col_map = {    'MEL'  : 'Melanoma',
               'NV'   : 'Melanocytic nevus',
               'BCC'  : 'Basal cell carcinoma',
               'AK'   : 'Actinic keratosis',
               'BKL'  : 'Benign keratosis',
               'DF'   : 'Dermatofibroma',
               'VASC' : 'Vascular lesion',
               'SCC'  : 'Squamous cell carcinoma',
               'UNK'  : 'None of the others'
          }

dframe = pd.read_csv('ISIC_2019_Training_GroundTruth.csv')
dframe = dframe.rename(columns=col_map)
dframe = dframe.set_index('image')
categ  = dframe.idxmax(axis=1)
lenc   = preprocessing.LabelEncoder()
labeln = lenc.fit_transform(categ.values)
dframe = pd.DataFrame({'image' : categ.index, 'label' : labeln, 'label name' : categ.values})
dframe = dframe.set_index('image')
dframe.to_csv('ISIC_2019_Training_GroundTruth_processed.csv')
