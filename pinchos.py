import cv2
import math
from constants import THUMB_TIP_IDX, INDEX_TIP_IDX

HAND_CONNECTIONS = [
    (0, 1), (1, 2), (2, 3), (3, 4),
    (0, 5), (5, 6), (6, 7), (7, 8),
    (5, 9), (9, 10), (10, 11), (11, 12),
    (9, 13), (13, 14), (14, 15), (15, 16),
    (13, 17), (17, 18), (18, 19), (19, 20),
    (0, 17)
]


class PinchOS():
    def __init__(self):
        self.points = []
        self.pinch_state = False

    def detect_pinch(self, threshold, image):

        thumb_x, thumb_y = self.points[THUMB_TIP_IDX]
        index_x, index_y = self.points[INDEX_TIP_IDX]
        distance = math.sqrt((thumb_x-index_x)**2+(thumb_y-index_y)**2)
        if distance <= threshold:
            self.pinch_state = True

            cv2.putText(image, "Pinch detected", (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        elif distance > threshold+10:
            self.pinch_state = False

    def draw_hands(self, result, image):
        self.points = []
        height, width = image.shape[:2]

        # cv2.putText(image, f"{result.handedness[0][0].display_name} hand", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)

        for i, lm in enumerate(result.hand_landmarks[0]):
            x, y = int(lm.x*width), int(lm.y*height)
            self.points.append((x, y))
            cv2.circle(image, (x, y), 5, (255, 255, 255))
            cv2.putText(image, str(
                HAND_CONNECTIONS[i][1]-1), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        for (start, end) in HAND_CONNECTIONS:
            if start < len(self.points) and end < len(self.points):
                cv2.line(image, self.points[start],
                         self.points[end], (255, 255, 255), 2)

        if len(self.points) > max(THUMB_TIP_IDX, INDEX_TIP_IDX):
            self.detect_pinch(40, image)
