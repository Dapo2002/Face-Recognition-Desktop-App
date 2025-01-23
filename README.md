Documentation

 1. Overview

This project is a Student Attendance System using Face Recognition. It includes functionalities for capturing student data, viewing student records, and capturing attendance using face recognition. The system uses Python, PyQt5 for the GUI, and SQLite for the database.

 2. Files and Modules

 2.1 main.py

This is the main file that launches the application. It sets up the GUI, integrates different functionalities, and handles database creation.

Modules Imported:
- `sys`, `os`: For system-level operations and path management.
- `sqlite3`: To interact with the SQLite database.
- `cv2`: OpenCV for image capturing and processing.
- `PyQt5.QtWidgets`: To build the GUI with buttons, forms, and layouts.
- `PyQt5.QtGui`: For customizing fonts and colors.
- `PyQt5.QtCore`: For handling basic core features like constants.
- `CaptureStudentData`, `ViewStudents`, `AttendanceCapture`, `ViewAttendanceHistory`: Custom modules for specific functionalities.

Key Components:

1. resource_path(relative_path): A helper function to get the absolute path to resources, compatible with development and PyInstaller builds.

2. create_database(): Initializes the SQLite database with three tables: `students`, `student_images`, and `attendance`.

3. AttendanceSystem (QMainWindow): The main GUI class that sets up the interface and connects buttons to their corresponding actions.

   - Buttons:
     - Capture Student Data: Opens the student data capture dialog.
     - Start Attendance Capture: Initiates attendance capture using the webcam.
     - View Student Records: Opens a dialog to view existing student records.
     - View Attendance History: Displays the attendance records.

4. setup_fonts_and_palette(): Configures the application’s fonts and color palette for a consistent look.

Execution Flow:
- When the script is run, the application starts by creating the database (if not already created).
- The main window of the attendance system is launched.

 2.2 capture_student.py

This module handles the capture of student data including their personal information and images.

Modules Imported:
- `sqlite3`: To interact with the SQLite database.
- `cv2`: For image capturing using the webcam.
- `PyQt5.QtWidgets`: For GUI elements like dialogs, forms, and buttons.

Key Components:

1. resource_path(relative_path): Retrieves the absolute path to resources, considering both development and PyInstaller contexts.

2. CaptureStudentData (QDialog): The dialog window used for capturing student data.

   - Input Fields:
     - Name: Student's name.
     - Matric Number: Student's unique identification number.
     - Department: Student's department.
     - Level: Student's academic level.
     - Image Status: Displays the number of images captured.

   - Buttons:
     - Capture Images with Webcam: Activates the webcam to capture student images.
     - Save Record: Saves the student data into the database.

   - Key Methods:
     - validate_name(name): Validates the name input, ensuring it's alphabetic and within character limits.
     - validate_department(department): Ensures the department input is alphabetic.
     - validate_level(level): Checks if the level is one of the allowed values (100, 200, 300, 400, 500, 600).
     - capture_images(): Captures images using the webcam, saves them to the student's specific directory, and updates the database.
     - save_record(): Validates all fields and saves the student's information along with the image paths to the database.

2.3 view_students.py

This module allows viewing, managing, and displaying student records stored in the database.

Modules Imported:
- `sqlite3`: To connect and interact with the SQLite database.
- `PyQt5.QtWidgets`: To create dialogs, tables, and other UI elements.
- `PyQt5.QtGui`, `PyQt5.QtCore`: For handling image display and table customization.

Key Components:

1. ViewStudents (QDialog): A dialog to display all student records in a tabular format.

   - Table Columns:
     - Matric Number: Displays the student's matriculation number.
     - Name: Displays the student's name.
     - Department: Displays the department name.
     - Level: Shows the student's academic level.
     - Image: Shows a thumbnail of the first captured image.
     - Action: Button to perform actions such as deleting a record.

   - Key Methods:
     - resource_path(relative_path): Retrieves the correct path to the database file for consistency in accessing resources.
     - load_student_data(): Fetches student records from the database and populates the table. Retrieves the first image for each student from their saved images.

3. Database Structure

- students: Stores basic information about each student (matric number, name, department, level, image path).
- student_images: Keeps paths to all images captured for each student, allowing multiple images per student.
- attendance: Logs each attendance record with a timestamp, ensuring each entry is unique per session.

4. Usage

1. Starting the Application:
   - Run `main.py` to launch the main application window.
   - Ensure all required .dat models and database files are correctly placed as specified by `resource_path`.

2. Capturing Student Data:
   - Click the "Capture Student Data" button to open the data capture dialog.
   - Fill in the student's details and use the webcam to capture images.
   - Save the record once all validations are passed.

3. Viewing Student Records:
   - Click the "View Student Records" button to see all saved student information.
   - Use the table's action buttons to manage each student’s record.

4. Capturing Attendance:
   - Use the "Start Attendance Capture" button to begin capturing attendance via webcam.

5. Viewing Attendance History:
   - Click the "View Attendance History" button to check recorded attendance details.

5. Dependencies

- Python 3.x
- PyQt5
- OpenCV (cv2)
- SQLite3

Ensure all dependencies are installed and compatible with your environment setup.

6. Conclusion

This documentation provides an overview of the functionalities, structure, and flow of the Student Attendance System using Face Recognition. The project leverages the power of PyQt5 for the GUI, OpenCV for capturing and processing images, and SQLite for managing data, creating an integrated system for managing student attendance effectively.