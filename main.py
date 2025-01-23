# main.py
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.QtCore import Qt
from capture_student import CaptureStudentData
from view_students import ViewStudents
from attendance_capture import AttendanceCapture
from view_attendance import ViewAttendanceHistory
import os
import sys
import sqlite3

def resource_path(relative_path):
    """Get the absolute path to a resource, works for both development and PyInstaller."""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Path to the .dat file
shape_predictor_path = resource_path('face_recognition_models/models/shape_predictor_68_face_landmarks.dat')
shape_predictor_path_1 = resource_path('face_recognition_models/models/shape_predictor_5_face_landmarks.dat')
shape_predictor_path_2 = resource_path('face_recognition_models/models/mmod_human_face_detector.dat')
shape_predictor_path_3 = resource_path('face_recognition_models/models/dlib_face_recognition_resnet_model_v1.dat')

# Database creation logic
def create_database():
    db_path = resource_path('student_attendance.db')
    conn = sqlite3.connect(db_path)  # Create or connect to the database
    cursor = conn.cursor()

    # Create the students table
    cursor.execute('''CREATE TABLE IF NOT EXISTS students (
                        matric_number TEXT PRIMARY KEY,
                        name TEXT,
                        department TEXT,
                        level TEXT,
                        image_path TEXT
                      )''')

    # Create the student_images table to store individual image paths for each student
    cursor.execute('''CREATE TABLE IF NOT EXISTS student_images (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        matric_number TEXT,
                        image_path TEXT,
                        FOREIGN KEY (matric_number) REFERENCES students (matric_number)
                      )''')

    # Create the attendance table to log attendance, ensuring unique records per session
    cursor.execute('''CREATE TABLE IF NOT EXISTS attendance (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        matric_number TEXT,
                        name TEXT,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        UNIQUE (matric_number, timestamp),
                        FOREIGN KEY (matric_number) REFERENCES students (matric_number)
                      )''')

    conn.commit()
    conn.close()

class AttendanceSystem(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up window title and geometry
        self.setWindowTitle("Face Recognition Attendance System by Abdulbadie")
        self.setGeometry(100, 100, 800, 600)

        # Set up layout
        layout = QVBoxLayout()

        # Customize colors and fonts for the main window
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f4f7;
            }
        """)

        # Buttons with stylish designs
        self.capture_button = QPushButton("Capture Student Data")
        self.attendance_button = QPushButton("Start Attendance Capture")
        self.view_records_button = QPushButton("View Student Records")
        self.view_attendance_button = QPushButton("View Attendance History")

        # Apply styling to buttons
        button_style = """
            QPushButton {
                background-color: #1e88e5;
                color: white;
                font-size: 16px;
                font-weight: bold;
                padding: 12px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #1565c0;
            }
            QPushButton:pressed {
                background-color: #0d47a1;
            }
        """

        # Apply button styles
        for button in [self.capture_button, self.attendance_button, self.view_records_button, self.view_attendance_button]:
            button.setStyleSheet(button_style)

        # Add buttons to the layout
        layout.addWidget(self.capture_button)
        layout.addWidget(self.attendance_button)
        layout.addWidget(self.view_records_button)
        layout.addWidget(self.view_attendance_button)

        # Set main widget and layout
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Connect buttons to functions
        self.capture_button.clicked.connect(self.open_capture_dialog)
        self.view_records_button.clicked.connect(self.open_view_students)
        self.attendance_button.clicked.connect(self.start_attendance_capture)
        self.view_attendance_button.clicked.connect(self.open_view_attendance_history)

        # Set up font and palette for overall UI enhancements
        self.setup_fonts_and_palette()

    def setup_fonts_and_palette(self):
        # Set a general font for the application
        app_font = QFont("Arial", 12)
        QApplication.setFont(app_font)

        # Set up color palette for the window
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor("#f0f4f7"))
        palette.setColor(QPalette.WindowText, Qt.black)
        palette.setColor(QPalette.Button, QColor("#1e88e5"))
        palette.setColor(QPalette.ButtonText, Qt.white)
        self.setPalette(palette)

    def open_capture_dialog(self):
        # Open the capture student data form
        self.capture_dialog = CaptureStudentData()
        self.capture_dialog.exec_()

    def open_view_students(self):
        # Open the view student records dialog
        self.view_students_dialog = ViewStudents()
        self.view_students_dialog.exec_()

    def start_attendance_capture(self):
        # Initialize and start the attendance capture process
        attendance = AttendanceCapture()
        attendance.start_attendance_capture()

    def open_view_attendance_history(self):
        # Open the view attendance history dialog
        self.view_attendance_dialog = ViewAttendanceHistory()
        self.view_attendance_dialog.exec_()

if __name__ == "__main__":
    create_database()  # Ensure the database is created
    app = QApplication(sys.argv)
    window = AttendanceSystem()
    window.show()
    sys.exit(app.exec_())
