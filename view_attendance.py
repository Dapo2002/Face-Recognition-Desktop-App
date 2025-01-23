# view_attendance.py
import sys
import sqlite3
import os
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QPushButton, QTableWidget,
    QTableWidgetItem, QLabel, QDateEdit, QMessageBox, QComboBox
)
from PyQt5.QtCore import QDate, QDateTime
from PyQt5.QtGui import QIcon

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores the path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class ViewAttendanceHistory(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("View Attendance History")
        self.setGeometry(200, 200, 800, 600)

        # Layout
        layout = QVBoxLayout()
        filter_layout = QFormLayout()

        # Date range filters
        self.start_date_edit = QDateEdit()
        self.start_date_edit.setDate(QDate.currentDate())
        self.end_date_edit = QDateEdit()
        self.end_date_edit.setDate(QDate.currentDate())

        filter_layout.addRow(QLabel("Start Date:"), self.start_date_edit)
        filter_layout.addRow(QLabel("End Date:"), self.end_date_edit)

        # Dropdown for delete date range
        self.delete_range_combo = QComboBox()
        self.delete_range_combo.addItems([
            "Select Date Range", "Last 15 minutes", "Last hour",
            "Last 24 hours", "Last 7 days", "Last 4 weeks", "All time"
        ])

        filter_layout.addRow(QLabel("Delete Attendance History:"), self.delete_range_combo)

        # Buttons
        self.filter_button = QPushButton("Filter Records")
        self.delete_button = QPushButton("Delete Records")
        self.close_button = QPushButton("Close")

        # Table to display attendance records
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Matric Number", "Name", "Date", "Time"])

        # Add widgets to layout
        layout.addLayout(filter_layout)
        layout.addWidget(self.filter_button)
        layout.addWidget(self.delete_button)
        layout.addWidget(self.table)
        layout.addWidget(self.close_button)

        self.setLayout(layout)

        # Connect buttons to functions
        self.filter_button.clicked.connect(self.filter_records)
        self.delete_button.clicked.connect(self.delete_records)
        self.close_button.clicked.connect(self.close)

        self.update_table()

    def filter_records(self):
        start_date = self.start_date_edit.date().toString("yyyy-MM-dd")
        end_date = self.end_date_edit.date().toString("yyyy-MM-dd")
        self.update_table(start_date, end_date)

    def update_table(self, start_date=None, end_date=None):
        conn = sqlite3.connect(resource_path('student_attendance.db'))
        cursor = conn.cursor()

        if start_date and end_date:
            cursor.execute("""
                SELECT matric_number, name, date(timestamp) as date, time(timestamp) as time
                FROM attendance
                WHERE timestamp BETWEEN ? AND ?
                ORDER BY timestamp DESC
            """, (f"{start_date} 00:00:00", f"{end_date} 23:59:59"))
        else:
            cursor.execute("""
                SELECT matric_number, name, date(timestamp) as date, time(timestamp) as time
                FROM attendance
                ORDER BY timestamp DESC
            """)

        records = cursor.fetchall()
        conn.close()

        self.table.setRowCount(len(records))
        for row_num, row_data in enumerate(records):
            for col_num, data in enumerate(row_data):
                self.table.setItem(row_num, col_num, QTableWidgetItem(str(data)))

    def delete_records(self):
        selected_range = self.delete_range_combo.currentText()
        conn = sqlite3.connect(resource_path('student_attendance.db'))
        cursor = conn.cursor()

        # Determine time range for deletion
        if selected_range == "Last 15 minutes":
            time_range = QDateTime.currentDateTime().addSecs(-15 * 60)
        elif selected_range == "Last hour":
            time_range = QDateTime.currentDateTime().addSecs(-60 * 60)
        elif selected_range == "Last 24 hours":
            time_range = QDateTime.currentDateTime().addDays(-1)
        elif selected_range == "Last 7 days":
            time_range = QDateTime.currentDateTime().addDays(-7)
        elif selected_range == "Last 4 weeks":
            time_range = QDateTime.currentDateTime().addDays(-28)
        elif selected_range == "All time":
            cursor.execute("DELETE FROM attendance")
            conn.commit()
            QMessageBox.information(self, "Success", "All attendance records have been deleted.")
            conn.close()
            self.update_table()
            return
        else:
            QMessageBox.warning(self, "Error", "Please select a valid date range.")
            return

        if selected_range != "All time":
            cursor.execute("""
                DELETE FROM attendance 
                WHERE timestamp >= ?
            """, (time_range.toString("yyyy-MM-dd HH:mm:ss"),))
            conn.commit()
            QMessageBox.information(self, "Success", f"Attendance records from {selected_range} have been deleted.")

        conn.close()
        self.update_table()
