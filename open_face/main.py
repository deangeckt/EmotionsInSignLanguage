import pandas as pd
import os
from collections import defaultdict
import numpy as np


raw_data_path = 'raw_data/'

au_list = ['AU01_r', 'AU02_r', 'AU04_r', 'AU05_r', 'AU06_r', 'AU07_r', 'AU09_r', 'AU10_r',
           'AU12_r', 'AU15_r', 'AU17_r', 'AU01_c', 'AU02_c', 'AU04_c', 'AU05_c', 'AU06_c', 'AU07_c',
           'AU09_c', 'AU10_c', 'AU12_c', 'AU14_c', 'AU15_c', 'AU17_c', 'AU28_c']

intensity_threshold = 0
binary_threshold = 0


def extrac_file(file_path, au_res):
    df = pd.read_csv(file_path)
    df = df.rename(columns=lambda x: x.strip())
    df = df[au_list]

    for au in au_list:
        au_res[au]['mean'].append(df[au].mean())
        au_res[au]['std'].append(df[au].std())


result_df = pd.DataFrame(columns=['label', 'au', 'mean', 'std'])
res = defaultdict(lambda: defaultdict(lambda: {'mean': [], 'std': []}))

for file_name in os.listdir(raw_data_path):
    person = file_name.split('_')[0]
    label = file_name.split('_')[1]
    extrac_file(os.path.join(raw_data_path, file_name), res[label])

for label in res:
    for au in res[label]:
        mean = np.mean(np.array(res[label][au]['mean']))
        std = np.mean(np.array(res[label][au]['std']))
        result_df = result_df.append({'label': label,
                                      'au': au,
                                      'mean': mean,
                                      'std': std}, ignore_index=True)

print(result_df)