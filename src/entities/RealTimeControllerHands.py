import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# HANDS_MOVE_THRESHOLD = 50


class HandTracker:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)

        self.pose = mp_hands.Hands(
            model_complexity=0,
            max_num_hands=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.4
        )

        self.prev_finger_x = None
        self.prev_finger_y = None

    def get_movement(self):
        ret, frame = self.cap.read()

        if not ret:
            return None

        height, width, _ = frame.shape

        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image_rgb.flags.writeable = False

        results = self.pose.process(image_rgb)

        image_rgb.flags.writeable = True
        frame = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)

        movement = None

        if results.multi_hand_landmarks:

            for hand_landmarks in results.multi_hand_landmarks:

                landmarks = hand_landmarks.landmark

                finger = landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP]

                finger_x = int(finger.x * width)
                finger_y = int(finger.y * height)
                HANDS_MOVE_THRESHOLD = height *0.05
                if self.prev_finger_y is not None:

                    if -(self.prev_finger_y - finger_y) > HANDS_MOVE_THRESHOLD:
                        movement = "Flap"
                        
                        cv2.putText(
                            frame,
                            "Flap Detected!",
                            (50, 100),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1,
                            (0, 255, 0),
                            2
                        )

                self.prev_finger_x = finger_x
                self.prev_finger_y = finger_y

                cv2.circle(frame, (finger_x, finger_y), 8, (0, 0, 255), -1)

                mp_drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS
                )

        cv2.imshow("Hand Tracking", frame)

        if cv2.waitKey(1) & 0xFF == 27:
            return "QUIT"

        return movement

    def release(self):
        self.pose.close()
        self.cap.release()
        cv2.destroyAllWindows()