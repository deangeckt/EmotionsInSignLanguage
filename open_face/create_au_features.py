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


def extract_file(file_path):
    df = pd.read_csv(file_path)
    df = df.rename(columns=lambda x: x.strip())
    df = df[au_list]

    file_res = defaultdict(dict)

    for au in au_list:
        file_res[au]['mean'] = df[au].mean()
        file_res[au]['std'] = df[au].std()

        vid_id = os.path.basename(file_path).split('.')[0]
        events = AuEvents(au, vid_id)
        events_resp = events.process(np.array(df[au]))
        events.plot_events()

        for event_key in events_resp:
            file_res[au][event_key] = events_resp[event_key]

    return file_res


features = ['mean', 'std', 'e0_i', 'e1_i', 'e2_i', 'e0_a', 'e1_a', 'e2_a']
df_features = ['label', 'au'].extend(features)

all_vid_res = defaultdict(lambda: defaultdict(lambda: default_au_features()))
per_vid_res = defaultdict(dict)
os.makedirs("results", exist_ok=True)

for file_name in os.listdir(raw_data_path):
    print(file_name)
    label = file_name.split('_')[1]
    file_res = extract_file(os.path.join(raw_data_path, file_name))

    per_vid_res_df = pd.DataFrame(columns=df_features)
    for au in file_res:
        res_obj = {'label': label, 'au': au}
        for feature in features:
            val = file_res[au].get(feature, 0)
            all_vid_res[label][au][feature].append(val)
            res_obj[feature] = val
        per_vid_res_df = per_vid_res_df.append(res_obj, ignore_index=True)

    # save result per video / file
    per_vid_res_df.to_csv(f'results/{file_name}')


all_vid_res_df = pd.DataFrame(columns=df_features)
for label in all_vid_res:
    for au in all_vid_res[label]:
        res_obj = {'label': label, 'au': au}
        for feature in features:
            feature_mean = np.mean(np.array(all_vid_res[label][au][feature]))
            res_obj[feature] = feature_mean
        all_vid_res_df = all_vid_res_df.append(res_obj, ignore_index=True)

all_vid_res_df.to_csv('results/all_results.csv')
