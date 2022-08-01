import subprocess
import os

video_path = "../../video"
open_face_path = "C:/Users/t-deangeckt/Documents/dev/HU/chb_project/OpenFace_2.2.0_win_x64/OpenFace_2.2.0_win_x64"
open_face_cmd = f"{open_face_path}/FeatureExtraction.exe"
output_path = 'processed/'

for f in os.listdir(video_path):
    print(f)
    if os.path.exists(os.path.join(output_path, f.split('.')[0] + '.csv')):
        print('exist')
        continue
    full_file_path = os.path.join(video_path, f)
    subprocess.run([open_face_cmd, "-f", full_file_path])
