import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from pinchos import PinchOS
from overlay import Overlay

options = vision.HandLandmarkerOptions(
    base_options=python.BaseOptions(model_asset_path='hand_landmarker.task'),
    running_mode=vision.RunningMode.VIDEO
)

detector = vision.HandLandmarker.create_from_options(options)
cap = cv2.VideoCapture(0)

pinch = PinchOS()
overlay = Overlay()


while cap.isOpened() and overlay.running:
    overlay.mainloop()
    success, image = cap.read()

    if not success:
        break

    cv2.namedWindow("Pinch OS", cv2.WINDOW_NORMAL)
    image = cv2.flip(image, 1)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image)
    frame_timestamp = int(cap.get(cv2.CAP_PROP_POS_MSEC))

    detection_result = detector.detect_for_video(mp_image, frame_timestamp)

    x, y, w, h = cv2.getWindowImageRect("Pinch OS")
    if len(detection_result.hand_landmarks):
        pinch.draw_hands(detection_result, image)
        pinch.draw_overlay(w, h)
    cv2.imshow("Pinch OS", image)
    if cv2.waitKey(1) & 0xff == ord("q"):
        break

overlay.quit()
cap.release()
cv2.destroyAllWindows()
