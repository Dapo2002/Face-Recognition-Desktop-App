from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView, QPushButton, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import sqlite3
import os
import sys

class ViewStudents(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("View Student Records")
        self.setGeometry(300, 100, 900, 500)  # Adjust size if needed

        # Layout setup
        layout = QVBoxLayout()

        # Table Widget
        self.table = QTableWidget()
        self.table.setColumnCount(6)  # Extra column for delete button
        self.table.setHorizontalHeaderLabels(["Matric Number", "Name", "Department", "Level", "Image", "Action"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        layout.addWidget(self.table)
        self.setLayout(layout)

        # Load data into the table
        self.load_student_data()

    def resource_path(self, relative_path):
        """ Get the absolute path to the resource, works for development and PyInstaller. """
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)

    def load_student_data(self):
        try:
            # Connect to the database using resource_path
            db_path = self.resource_path('student_attendance.db')
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            # Fetch distinct student records
            cursor.execute("SELECT matric_number, name, department, level FROM students")
            student_rows = cursor.fetchall()

            self.table.setRowCount(len(student_rows))

            # Populate the table with data
            for row_index, student in enumerate(student_rows):
                matric_number, name, department, level = student

                # Query to fetch the first image path associated with the student's matric number
                cursor.execute("SELECT image_path FROM student_images WHERE matric_number = ? ORDER BY rowid LIMIT 1", (matric_number,))
                image_row = cursor.fetchone()
                image_path = image_row[0] if image_row else ""

                # Add student details to table
                self.table.setItem(row_index, 0, QTableWidgetItem(matric_number))
                self.table.setItem(row_index, 1, QTableWidgetItem(name))
                self.table.setItem(row_index, 2, QTableWidgetItem(department))
                self.table.setItem(row_index, 3, QTableWidgetItem(level))

                # Display the first image
                if image_path and os.path.exists(image_path):
                    pixmap = QPixmap(image_path)
                    pixmap = pixmap.scaled(100, 100, Qt.KeepAspectRatio)
                    image_label = QLabel()
                    image_label.setPixmap(pixmap)
                    self.table.setCellWidget(row_index, 4, image_label)
                else:
                    self.table.setItem(row_index, 4, QTableWidgetItem("No Image"))

                # Action button
                delete_button = QPushButton("Delete")
                delete_button.clicked.connect(lambda _, matric_number=matric_number: self.delete_student(matric_number))
                self.table.setCellWidget(row_index, 5, delete_button)

            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred while loading data: {str(e)}")

    def delete_student(self, matric_number):
        try:
            # Connect to the database using resource_path
            db_path = self.resource_path('student_attendance.db')
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            # Delete the student record and associated images
            cursor.execute("DELETE FROM students WHERE matric_number = ?", (matric_number,))
            cursor.execute("DELETE FROM student_images WHERE matric_number = ?", (matric_number,))

            conn.commit()
            conn.close()

            QMessageBox.information(self, "Success", "Student record deleted successfully.")
            self.load_student_data()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred while deleting the student record: {str(e)}")
