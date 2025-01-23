# capture_student.py
import re
from PyQt5.QtWidgets import QDialog, QLineEdit, QFormLayout, QPushButton, QLabel, QMessageBox
import sqlite3
import cv2
import os
import sys

def resource_path(relative_path):
    """Get the absolute path to a resource, works for both development and PyInstaller."""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class CaptureStudentData(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Capture Student Data")
        self.setGeometry(200, 200, 400, 300)

        # Form layout for input fields
        layout = QFormLayout()

        self.name_input = QLineEdit(self)
        self.matric_input = QLineEdit(self)
        self.department_input = QLineEdit(self)
        self.level_input = QLineEdit(self)
        self.image_path_label = QLabel("No images captured yet.")

        # Buttons
        self.capture_image_button = QPushButton("Capture Images with Webcam")
        self.save_button = QPushButton("Save Record")

        # Adding input fields and buttons to the form
        layout.addRow("Name:", self.name_input)
        layout.addRow("Matric Number:", self.matric_input)
        layout.addRow("Department:", self.department_input)
        layout.addRow("Level:", self.level_input)
        layout.addRow("Image Status:", self.image_path_label)
        layout.addRow(self.capture_image_button)
        layout.addRow(self.save_button)

        self.setLayout(layout)

        # Connect buttons to functions
        self.capture_image_button.clicked.connect(self.capture_images)
        self.save_button.clicked.connect(self.save_record)

    def validate_matric(self, matric):
        # Regular expression to validate the matric number format
        pattern = r"^\d{2}/\d{2}[A-Za-z]{2}\d{3}$"
        return bool(re.match(pattern, matric))

    def sanitize_matric(self, matric):
        # Replace "/" with a safe character for file paths (e.g., "_")
        return matric.replace("/", "_")

    def validate_name(self, name):
        # Check if the name contains only alphabets and is between 3 and 40 characters
        return name.replace(" ", "").isalpha() and 3 <= len(name) <= 40

    def validate_department(self, department):
        # Check if the department contains only alphabets
        return department.replace(" ", "").isalpha()

    def validate_level(self, level):
        # Validate level to be one of the specified values
        valid_levels = {'100', '200', '300', '400', '500', '600'}
        return level in valid_levels

    def capture_images(self):
        # Retrieve the matric number to use as a folder name for saving images
        matric = self.matric_input.text()
        if not matric:
            QMessageBox.warning(self, "Error", "Please enter the Matric Number before capturing images.")
            return
        if not self.validate_matric(matric):
            QMessageBox.warning(self, "Error", "Matric number must be in the format '19/52HA054")
            return

        sanitized_matric = self.sanitize_matric(matric)

        # Create a directory for the student's images if it doesn't exist
        image_directory = os.path.join("student_images", sanitized_matric)
        os.makedirs(image_directory, exist_ok=True)

        # Initialize the webcam
        cap = cv2.VideoCapture(0)
        cv2.namedWindow("Capture Images")

        img_count = 0  # Counter for captured images

        notification_timer = 0  # Timer for notification display duration

        # Connect to the database using resource_path
        db_path = resource_path('student_attendance.db')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Convert the frame to grayscale for better recognition compatibility
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Apply CLAHE to enhance contrast in low-light conditions
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            enhanced_frame = clahe.apply(gray_frame)

            # Display notification text for a brief period after each capture
            if notification_timer > 0:
                cv2.putText(frame, f"Image {img_count} captured", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                notification_timer -= 1  # Decrement timer on each frame

            # Display instruction to press 'q' to quit at the top right side
            text = "Press 'q' to quit"
            (text_width, text_height), baseline = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
            cv2.putText(frame, text, (frame.shape[1] - text_width - 10, text_height + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

            # Display the enhanced frame
            cv2.imshow("Capture Images", frame)

            key = cv2.waitKey(1)

            if key % 256 == 32:  # SPACE key
                # Save the captured enhanced image with a unique name
                img_name = os.path.join(image_directory, f"{sanitized_matric}_{img_count}.jpg")  # Saving as .jpg
                cv2.imwrite(img_name, enhanced_frame)

                # Insert the image path into the database
                cursor.execute("INSERT INTO student_images (matric_number, image_path) VALUES (?, ?)", (matric, img_name))
                conn.commit()

                img_count += 1
                self.image_path_label.setText(f"{img_count} images captured.")
                notification_timer = 30  # Set timer to display the notification for a short duration

            elif key % 256 == ord('q'):  # 'q' key to quit
                break

        cap.release()
        cv2.destroyAllWindows()
        conn.close()

    def save_record(self):
        # Get the data from input fields
        name = self.name_input.text()
        matric = self.matric_input.text()
        department = self.department_input.text()
        level = self.level_input.text()
        sanitized_matric = self.sanitize_matric(matric)
        image_path = os.path.join("student_images", sanitized_matric)

        # Validate input fields
        if not matric:
            QMessageBox.warning(self, "Error", "Please fill in the blank spaces.")
            return
        if not self.validate_matric(matric):
            QMessageBox.warning(self, "Error", "Matric number must be in the format '19/52HA054'.")
            return
        if not self.validate_name(name):
            QMessageBox.warning(self, "Error", "Name must be between 3 and 40 characters and contain only alphabets.")
            return
        if not self.validate_department(department):
            QMessageBox.warning(self, "Error", "Department cannot be empty and cannot contain numbers.")
            return
        if not self.validate_level(level):
            QMessageBox.warning(self, "Error", "Level must be one of the following: 100, 200, 300, 400, 500, 600.")
            return
        if not os.path.exists(image_path):
            QMessageBox.warning(self, "Error", "Please capture images before saving the record.")
            return

        # Save the record to the database
        if name and matric and department and level and os.path.exists(image_path):
            # Connect to the database using resource_path
            db_path = resource_path('student_attendance.db')
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO students (matric_number, name, department, level, image_path) VALUES (?, ?, ?, ?, ?)",
                               (matric, name, department, level, image_path))
                conn.commit()
                QMessageBox.information(self, "Success", "Record saved successfully!")
            except sqlite3.IntegrityError:
                QMessageBox.warning(self, "Error", "Matric number already exists.")
            finally:
                conn.close()
        else:
            QMessageBox.warning(self, "Error", "Please fill in all fields and capture images.")