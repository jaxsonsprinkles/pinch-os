import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import numpy as np

HAND_CONNECTIONS = [
    (0,1),(1,2),(2,3),(3,4),       # Thumb
    (0,5),(5,6),(6,7),(7,8),       # Index
    (5,9),(9,10),(10,11),(11,12),  # Middle chain from base
    (9,13),(13,14),(14,15),(15,16),
    (13,17),(17,18),(18,19),(19,20),
    (0,17)
]

options = vision.HandLandmarkerOptions(
    base_options=python.BaseOptions(model_asset_path='hand_landmarker.task'),
    running_mode=vision.RunningMode.VIDEO
)

detector = vision.HandLandmarker.create_from_options(options)


cap = cv2.VideoCapture(0)

def draw_hands(result, image):
    height, width = image.shape[:2]
    if not len(result.hand_landmarks):
        return False
    
    points = []
    for lm in result.hand_landmarks:
        for nlm in lm:
            x,y = int(nlm.x*width), int(nlm.y*height)
            points.append((x,y))
            cv2.circle(image, (x, y), 5, (255,255,255))
    for (start, end) in HAND_CONNECTIONS:
        if start < len(points) and end < len(points):
            cv2.line(image, points[start], points[end], (255, 255, 255), 2)

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