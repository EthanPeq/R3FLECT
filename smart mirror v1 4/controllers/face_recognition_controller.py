import face_recognition
import pickle
import time
import cv2

class FaceRecognition:
    def __init__(self, vision_state, update_name_callback, timeout_duration=60):
        self.vision_state = vision_state
        self.update_name_callback = update_name_callback
        self.timeout_duration = timeout_duration
        self.known_encodings, self.known_names = self.load_known_faces()

    def load_known_faces(self):
        with open("smart mirror v1 4/faces data/known_faces.pkl", "rb") as f:
            
            return pickle.load(f)

    def process_face_recognition(self, rgb_small, original_frame):
        small_frame = cv2.resize(rgb_small, (0, 0), fx=0.25, fy=0.25)
        face_locations = face_recognition.face_locations(small_frame)

        if face_locations:
            encodings = face_recognition.face_encodings(small_frame, face_locations)
            for face_encoding in encodings:
                matches = face_recognition.compare_faces(self.known_encodings, face_encoding)
                name = "Unknown"
                if True in matches:
                    match_index = matches.index(True)
                    name = self.known_names[match_index]

                if name != self.vision_state.recognized_name:
                    self.vision_state.recognized_name = name
                    self.vision_state.last_detected_time = time.time()
                    self.update_name_callback(name)
                else:
                    # Face still detected, just update the timestamp
                    self.vision_state.last_detected_time = time.time()
        else:
            # No face detected in frame
            if (
                self.vision_state.recognized_name is not None and
                self.vision_state.last_detected_time is not None and
                time.time() - self.vision_state.last_detected_time > self.timeout_duration
            ):
                self.vision_state.recognized_name = None
                self.vision_state.last_detected_time = None
                self.update_name_callback("")  # Reset to default like "R3FLECT"

    def start(self, camera):
        frame_count = 0
        while True:
            start_time = time.time()
            frame = camera.get_frame()
            frame_count += 1

            if frame is not None and frame_count % 2 == 0:  # Process every other frame
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                self.process_face_recognition(rgb_frame, frame)

            elapsed = time.time() - start_time
            time.sleep(0.2)
