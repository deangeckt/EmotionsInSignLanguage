import cv2
from media_pipe_extractor import MediaPipeExtractor, Solution


def extract_from_file(full_path):
    pose_ex = MediaPipeExtractor(Solution.POSE)
    face_de_ex = MediaPipeExtractor(Solution.FACE_DETECTION)
    face_mesh_ex = MediaPipeExtractor(Solution.FACE_MESH)

    vid = cv2.VideoCapture(full_path)
    _, img = vid.read()
    while True:
        success, img = vid.read()
        if not success:
            print(f'err in file {full_path}')
            break

        face_mesh_ex.process(img)
        pose_ex.process(img)
        face_de_ex.process(img)

        cv2.imshow("Vid", img)
        if cv2.waitKey(75) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()


extract_from_file('../../video/עצב02.mp4')
