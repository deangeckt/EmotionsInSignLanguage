import mediapipe as mp
from enum import Enum
import cv2

mp_draw = mp.solutions.drawing_utils
mp_draw_style = mp.solutions.drawing_styles


# when extracting features use None,
# so we won't draw on the image effecting other solution extraction
class Debug(Enum):
    NONE = 0
    DRAW = 1
    PLOT = 2


class Solution(Enum):
    POSE = 0
    FACE_MESH = 1
    FACE_DETECTION = 2


def draw(landmarks, img, sol: Solution):
    if sol == Solution.POSE:
        mp_draw.draw_landmarks(img, landmarks, mp.solutions.pose.POSE_CONNECTIONS)
    elif sol == Solution.FACE_MESH:
        for landmark in landmarks:
            mp_draw.draw_landmarks(
                image=img,
                landmark_list=landmark,
                connections=mp.solutions.face_mesh.FACEMESH_TESSELATION,
                landmark_drawing_spec=None,
                connection_drawing_spec=mp_draw_style.get_default_face_mesh_tesselation_style()
            )
    else:
        for detection in landmarks:
            mp_draw.draw_detection(img, detection)


def init_mp_obj(sol: Solution):
    solutions = {Solution.POSE: mp.solutions.pose,
                 Solution.FACE_MESH: mp.solutions.face_mesh,
                 Solution.FACE_DETECTION: mp.solutions.face_detection}
    mp_sol = solutions[sol]
    if sol == Solution.POSE:
        return mp_sol.Pose()
    elif sol == Solution.FACE_MESH:
        return mp_sol.FaceMesh(
            static_image_mode=True,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5)
    else:
        return mp_sol.FaceDetection(model_selection=1, min_detection_confidence=0.5)


class MediaPipeExtractor:
    def __init__(self, solution=Solution.POSE, debug=Debug.DRAW):
        self.sol = solution
        self.mp_obj = init_mp_obj(solution)
        self.debug = debug

    def process(self, img):
        landmark_keys = {Solution.POSE: 'pose_landmarks',
                         Solution.FACE_MESH: 'multi_face_landmarks',
                         Solution.FACE_DETECTION: 'detections'}
        landmark_key = landmark_keys[self.sol]
        results = self.mp_obj.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        landmarks = getattr(results, landmark_key)
        if landmarks is None:
            return
        if self.debug == Debug.DRAW:
            draw(landmarks, img, self.sol)

