import cv2
from gesture_controller import GestureControl  # Or paste your GestureControl class directly here

class DummyCamera:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)

    def get_frame(self):
        ret, frame = self.cap.read()
        return frame if ret else None

    def release(self):
        self.cap.release()

class DummyVisionState:
    def __init__(self):
        self.swipe_mode_active = False
        self.prev_index_x = None
        self.prev_time = 0

def gesture_callback(direction):
    print(f"Swipe detected: {direction}")

def main():
    vision_state = DummyVisionState()
    gesture_control = GestureControl(vision_state, gesture_callback)
    camera = DummyCamera()

    try:
        while True:
            frame = camera.get_frame()
            if frame is None:
                continue
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            gesture_control.process_gesture_detection(rgb_frame, frame)

            # Display the frame
            cv2.imshow("Gesture Tester", frame)

            # Exit on 'q' key press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        camera.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
