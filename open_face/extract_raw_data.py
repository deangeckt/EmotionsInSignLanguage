import subprocess
import os

video_path = "<FILL>"
open_face_path = "<FILL>"
open_face_cmd = f"{open_face_path}/FeatureExtraction.exe"

for f in os.listdir(video_path):
    print(f)
    full_file_path = os.path.join(video_path, f)
    subprocess.run([open_face_cmd, "-f", full_file_path])
