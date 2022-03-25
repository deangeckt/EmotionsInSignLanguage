import os

src_dir = '../video'

for f in os.listdir(src_dir):
    label = ''
    if 'כעס' in f:
        label = 'angry'
    elif 'ניי' in f:
        label = 'neutral'
    elif 'עצב' in f:
        label = 'sad'
    elif 'שמחה' in f:
        label = 'happy'
    else:
        label = 'fear'
    file_idx = f.split(' ')[1].split('.')[0]
    new_name = f"per1_{label}_{file_idx}.mp4"
    print(new_name)

    old_file = os.path.join(src_dir, f)
    new_file = os.path.join(src_dir, new_name)
    os.rename(old_file, new_file)
