# attendance_capture.py
import cv2
import face_recognition
import sqlite3
import os
import sys
from datetime import datetime

class AttendanceCapture:
    def __init__(self):
        # Load student images and their encodings
        self.known_face_encodings = []
        self.known_face_names = []
        self.known_face_matrics = []

        try:
            self.load_known_faces()
        except Exception as e:
            print(f"Error loading known faces: {e}")

        # Dictionary to keep track of attendance
        self.attendance_marked = {}

    def resource_path(self, relative_path):
        """ Get the absolute path to the resource, works for development and PyInstaller. """
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)

    def load_known_faces(self):
        # Load all images from the student_images directory
        db_path = self.resource_path('student_attendance.db')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT matric_number, name, image_path FROM students")
        students = cursor.fetchall()

        for student in students:
            matric, name, image_folder = student
            if not os.path.exists(image_folder):
                continue

            # Iterate through each image in the folder and encode it
            for img_name in os.listdir(image_folder):
                img_path = os.path.join(image_folder, img_name)
                image = face_recognition.load_image_file(img_path)
                encodings = face_recognition.face_encodings(image)

                if encodings:  # Check if encodings are not empty
                    self.known_face_encodings.append(encodings[0])
                    self.known_face_names.append(name)
                    self.known_face_matrics.append(matric)

        conn.close()

    def start_attendance_capture(self):
        # Start webcam feed
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Error: Unable to access the camera.")
            return

        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    print("Error: Failed to capture frame from camera.")
                    break

                # Convert the frame to RGB for face_recognition
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # Find all face locations and encodings in the current frame
                face_locations = face_recognition.face_locations(rgb_frame)
                face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

                # Iterate through each face in the frame
                for face_encoding, face_location in zip(face_encodings, face_locations):
                    matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                    face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
                    best_match_index = face_distances.argmin() if matches else None

                    # Check if a match is found
                    if best_match_index is not None and matches[best_match_index]:
                        name = self.known_face_names[best_match_index]
                        matric = self.known_face_matrics[best_match_index]

                        # Check if the student has already been marked for attendance
                        if matric not in self.attendance_marked:
                            self.mark_attendance(matric, name)

                        # Display the name on the webcam feed
                        top, right, bottom, left = face_location
                        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                        cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                    else:
                        # Display "Unknown" for faces that do not match
                        top, right, bottom, left = face_location
                        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                        cv2.putText(frame, "Unknown", (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

                # Display instruction to press 'q' to quit
                cv2.putText(frame, "Press 'q' to quit", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

                cv2.imshow("Attendance Capture", frame)

                # Press 'q' to exit the capture process
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        except Exception as e:
            print(f"Error during attendance capture: {e}")

        finally:
            # Ensure the resources are released properly
            cap.release()
            cv2.destroyAllWindows()

    def mark_attendance(self, matric, name):
        # Connect to the database and insert the attendance record
        try:
            db_path = self.resource_path('student_attendance.db')
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            # Insert the attendance record based on matric and name
            attendance_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute("INSERT INTO attendance (matric_number, name, timestamp) VALUES (?, ?, ?)",
                           (matric, name, attendance_time))
            conn.commit()

            # Add matric number to the marked attendance list
            self.attendance_marked[matric] = True

        except Exception as e:
            print(f"Error marking attendance: {e}")

        finally:
            conn.close()
