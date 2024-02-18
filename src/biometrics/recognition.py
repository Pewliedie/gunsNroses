import json

import cv2
import face_recognition
import numpy as np

__all__ = ('recognizer', 'biometric_auth')


class Recognizer:
    def __init__(self):
        self.known_face_encodings = []
        self.known_face_names = []

        self.frame_resizing = 0.25

    def encode_image(self, image_path):
        img = cv2.imread(image_path)
        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_encoding = face_recognition.face_encodings(rgb_img)[0]
        json_encoding = json.dumps(img_encoding.tolist())
        return json_encoding

    def detect_known_faces(self, frame):
        small_frame = cv2.resize(
            frame, (0, 0), fx=self.frame_resizing, fy=self.frame_resizing
        )

        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(
            rgb_small_frame, face_locations
        )

        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(
                self.known_face_encodings, face_encoding
            )
            name = "unknown"

            face_distances = face_recognition.face_distance(
                self.known_face_encodings, face_encoding
            )
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = self.known_face_names[best_match_index]
            face_names.append(name)

        face_locations = np.array(face_locations)
        face_locations = face_locations / self.frame_resizing
        return face_locations.astype(int), face_names


def biometric_auth(face_encodings, id):
    recognizer = Recognizer()

    image_encoding = np.array(json.loads(face_encodings))

    recognizer.known_face_encodings.append(image_encoding)
    recognizer.known_face_names.append(id)

    cap = cv2.VideoCapture(0)

    while True:
        _, frame = cap.read()

        face_locations, face_names = recognizer.detect_known_faces(frame)
        for face_loc, name in zip(face_locations, face_names):

            y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]

            cv2.putText(
                frame, name, (x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 2
            )
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 200), 4)

            return name == id

        key = cv2.waitKey(1)
        if key == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


recognizer = Recognizer()
