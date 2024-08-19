import cv2
import face_recognition
import numpy as np

def load_known_faces():
    """Load known face images and encode them."""
    known_face_encodings = []
    known_face_names = []

    # Load known faces
    known_image = face_recognition.load_image_file("known_face.jpg")
    known_face_encoding = face_recognition.face_encodings(known_image)[0]

    known_face_encodings.append(known_face_encoding)
    known_face_names.append("Known Person")

    return known_face_encodings, known_face_names

def detect_and_recognize_faces(frame, known_face_encodings, known_face_names):
    """Detect and recognize faces in the frame."""
    rgb_frame = frame[:, :, ::-1]  # Convert BGR to RGB

    # Find all face locations and face encodings in the frame
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    face_names = []
    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"

        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]

        face_names.append(name)

    return face_locations, face_names

def draw_face_boxes(frame, face_locations, face_names):
    """Draw rectangles and labels around detected faces."""
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up the face locations since the frame was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

def main():
    # Load known faces
    known_face_encodings, known_face_names = load_known_faces()

    # Initialize video capture
    video_capture = cv2.VideoCapture(0)

    while True:
        ret, frame = video_capture.read()

        if not ret:
            print("Error: Unable to capture video.")
            break

        # Detect and recognize faces
        face_locations, face_names = detect_and_recognize_faces(frame, known_face_encodings, known_face_names)

        # Draw boxes and labels around detected faces
        draw_face_boxes(frame, face_locations, face_names)

        # Display the resulting frame
        cv2.imshow('Video', frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the capture and close the windows
    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
