import pandas as pd
import os
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
from FacialEmotion.open_face.au_events import AuEvents, au_list

raw_data_path = 'raw_data/'


def extract_file(file_path, au_res, label, person):
    df = pd.read_csv(file_path)
    df = df.rename(columns=lambda x: x.strip())
    df = df[au_list]

    for au in au_list:
        au_res[au]['mean'].append(df[au].mean())
        au_res[au]['std'].append(df[au].std())

        events = AuEvents(au, label, person)
        e1, e2, e3 = events.process(np.array(df[au]))
        events.plot_events()

        au_res[au]['e1'].append(e1)
        au_res[au]['e2'].append(e2)
        au_res[au]['e3'].append(e3)


result_df = pd.DataFrame(columns=['label', 'au', 'mean', 'std'])
res = defaultdict(
    lambda: defaultdict(lambda: {'mean': [], 'std': [], 'e1': [], 'e2': [], 'e3': []}))

for file_name in os.listdir(raw_data_path):
    person = file_name.split('_')[0]
    label = file_name.split('_')[1]
    if label == 'fear':
        extract_file(os.path.join(raw_data_path, file_name), res[label], label, person)

for label in res:
    for au in res[label]:
        mean = np.mean(np.array(res[label][au]['mean']))
        std = np.mean(np.array(res[label][au]['std']))
        result_df = result_df.append({'label': label,
                                      'au': au,
                                      'mean': mean,
                                      'std': std}, ignore_index=True)

print(result_df)
