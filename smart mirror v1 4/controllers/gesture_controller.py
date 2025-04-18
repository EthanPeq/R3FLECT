import mediapipe as mp
import time
import cv2

class GestureControl:
    def __init__(self, vision_state, gesture_callback):
        self.vision_state = vision_state
        self.gesture_callback = gesture_callback
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
        self.mp_drawing = mp.solutions.drawing_utils
        self.swipe_threshold = 80
        self.swipe_delay = 1
        self.last_swipe_time = 0

    def process_gesture_detection(self, rgb_frame, frame):
        results = self.hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

                if self.is_one_gesture(hand_landmarks):
                    self.vision_state.swipe_mode_active = True
                    cv2.putText(frame, "1 Gesture Active", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                else:
                    self.vision_state.swipe_mode_active = False
                    cv2.putText(frame, "1 Gesture Not Detected", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

                if self.vision_state.swipe_mode_active:
                    index_x = int(hand_landmarks.landmark[8].x * frame.shape[1])
                    if self.vision_state.prev_index_x is not None:
                        current_time = time.time()
                        if current_time - self.vision_state.prev_time < 0.5:
                            movement = index_x - self.vision_state.prev_index_x
                            if abs(movement) > self.swipe_threshold:
                                if current_time - self.last_swipe_time >= self.swipe_delay:
                                    direction = "right" if movement > 0 else "left"
                                    self.gesture_callback(direction)
                                    self.last_swipe_time = current_time
                    self.vision_state.prev_index_x = index_x
                    self.vision_state.prev_time = time.time()

    def is_one_gesture(self, hand_landmarks):
        index_tip = hand_landmarks.landmark[8].y
        index_mcp = hand_landmarks.landmark[5].y
        middle_tip = hand_landmarks.landmark[12].y
        middle_mcp = hand_landmarks.landmark[9].y
        ring_tip = hand_landmarks.landmark[16].y
        ring_mcp = hand_landmarks.landmark[13].y
        pinky_tip = hand_landmarks.landmark[20].y
        pinky_mcp = hand_landmarks.landmark[17].y

        index_raised = index_tip < index_mcp
        middle_down = middle_tip > middle_mcp
        ring_down = ring_tip > ring_mcp
        pinky_down = pinky_tip > pinky_mcp

        return index_raised and middle_down and ring_down and pinky_down

    def start(self, camera):
        while True:
            frame = camera.get_frame()
            if frame is not None:
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                self.process_gesture_detection(rgb_frame, frame)
