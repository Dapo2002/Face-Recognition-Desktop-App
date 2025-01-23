import sqlite3

# Function to create the database and tables
def create_database():
    conn = sqlite3.connect('student_attendance.db')  # Create or connect to the database
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

# Run the function to create the database and tables when this script is executed directly
if __name__ == "__main__":
    create_database()
