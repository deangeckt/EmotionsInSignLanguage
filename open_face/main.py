import pandas as pd
import os

raw_data_path = 'raw_data/'

au_list = ['AU01_r', 'AU02_r', 'AU04_r', 'AU05_r', 'AU06_r', 'AU07_r', 'AU09_r', 'AU10_r',
           'AU12_r', 'AU15_r', 'AU17_r', 'AU01_c', 'AU02_c', 'AU04_c', 'AU05_c', 'AU06_c', 'AU07_c',
           'AU09_c', 'AU10_c', 'AU12_c', 'AU14_c', 'AU15_c', 'AU17_c', 'AU28_c']


def extrac_file(file_path, person, label):
    print(f"Processing person: {person} with label: {label}")
    df = pd.read_csv(file_path)
    df = df.rename(columns=lambda x: x.strip())
    df = df[au_list]
    print(df.head())


file_name = 'per1_angry_01.csv'
person = file_name.split('_')[0]
label = file_name.split('_')[1]
extrac_file(os.path.join(raw_data_path, file_name), person, label)