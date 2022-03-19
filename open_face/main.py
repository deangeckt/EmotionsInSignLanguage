import pandas as pd
import os
from collections import defaultdict
import numpy as np
from FacialEmotion.open_face.au_events import AuEvents, au_list

raw_data_path = 'raw_data/'


def default_au_features():
    au_features = {}
    for f in features:
        au_features[f] = []
    return au_features


def extract_file(file_path, au_res):
    df = pd.read_csv(file_path)
    df = df.rename(columns=lambda x: x.strip())
    df = df[au_list]

    for au in au_list:
        au_res[au]['mean'].append(df[au].mean())
        au_res[au]['std'].append(df[au].std())

        vid_id = os.path.basename(file_path).split('.')[0]
        events = AuEvents(au, vid_id)
        e1, e2, e3 = events.process(np.array(df[au]))
        # events.plot_events()

        au_res[au]['e1'].append(e1)
        au_res[au]['e2'].append(e2)
        au_res[au]['e3'].append(e3)


features = ['mean', 'std', 'e1', 'e2', 'e3']
df_features = ['label', 'au'].extend(features)
result_df = pd.DataFrame(columns=df_features)

res = defaultdict(lambda: defaultdict(lambda: default_au_features()))

for file_name in os.listdir(raw_data_path):
    print(file_name)
    person = file_name.split('_')[0]
    label = file_name.split('_')[1]
    extract_file(os.path.join(raw_data_path, file_name), res[label])

for label in res:
    for au in res[label]:
        res_obj = {'label': label, 'au': au}
        for feature in features:
            feature_mean = np.mean(np.array(res[label][au][feature]))
            res_obj[feature] = feature_mean
        result_df = result_df.append(res_obj, ignore_index=True)

# print(result_df)
result_df.to_csv('non_bin.csv')
