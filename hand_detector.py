import cv2
import mediapipe as mp


class HandDetector:
    def __init__(self):
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )
        self.mpDraw = mp.solutions.drawing_utils

    def find_hands(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb)

        landmarks = []

        if results.multi_hand_landmarks:
            for hand in results.multi_hand_landmarks:

                self.mpDraw.draw_landmarks(
                    frame,
                    hand,
                    self.mpHands.HAND_CONNECTIONS
                )

                h, w, c = frame.shape

                for id, lm in enumerate(hand.landmark):
                    cx = int(lm.x * w)
                    cy = int(lm.y * h)

                    landmarks.append((id, cx, cy))

        return frame, landmarks