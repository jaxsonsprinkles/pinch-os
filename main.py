import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import numpy as np
import math

HAND_CONNECTIONS = [
    (0, 1), (1, 2), (2, 3), (3, 4),
    (0, 5), (5, 6), (6, 7), (7, 8),
    (5, 9), (9, 10), (10, 11), (11, 12),
    (9, 13), (13, 14), (14, 15), (15, 16),
    (13, 17), (17, 18), (18, 19), (19, 20),
    (0, 17)
]
THUMB_TIP_IDX = 4
INDEX_TIP_IDX = 8


options = vision.HandLandmarkerOptions(
    base_options=python.BaseOptions(model_asset_path='hand_landmarker.task'),
    running_mode=vision.RunningMode.VIDEO
)

detector = vision.HandLandmarker.create_from_options(options)


cap = cv2.VideoCapture(0)


def detect_pinch(threshold, image, points):
    pinch_state = False

    thumb_x, thumb_y = points[THUMB_TIP_IDX]
    index_x, index_y = points[INDEX_TIP_IDX]
    distance = math.sqrt((thumb_x-index_x)**2+(thumb_y-index_y)**2)
    if distance <= threshold:

        pinch_state = True

        cv2.putText(image, "Pinch detected", (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    elif distance > threshold+10:
        pinch_state = False


def draw_hands(result, image):

    height, width = image.shape[:2]
    if not len(result.hand_landmarks):
        return False

    points = []
    # cv2.putText(image, f"{result.handedness[0][0].display_name} hand", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)

    for i, lm in enumerate(result.hand_landmarks[0]):
        x, y = int(lm.x*width), int(lm.y*height)
        points.append((x, y))
        cv2.circle(image, (x, y), 5, (255, 255, 255))
        cv2.putText(image, str(
            HAND_CONNECTIONS[i][1]-1), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    for (start, end) in HAND_CONNECTIONS:
        if start < len(points) and end < len(points):
            cv2.line(image, points[start], points[end], (255, 255, 255), 2)

    if len(points) > max(THUMB_TIP_IDX, INDEX_TIP_IDX):
        detect_pinch(40, image, points)


while cap.isOpened():
    success, image = cap.read()

    if not success:
        break

    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image)
    frame_timestamp = int(cap.get(cv2.CAP_PROP_POS_MSEC))

    detection_result = detector.detect_for_video(mp_image, frame_timestamp)
    if len(detection_result.hand_landmarks):
        draw_hands(detection_result, image)

    cv2.imshow("Pinch OS", image)
    if cv2.waitKey(1) & 0xff == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
