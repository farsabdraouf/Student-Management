from config.database import DatabaseConnection
from models.student import Student

class StudentRepository:
    def __init__(self):
        self.db = DatabaseConnection()
    
    def add_student(self, student):
        connection = self.db.get_connection()
        if connection:
            try:
                cursor = connection.cursor()
                query = """INSERT INTO students (name, age, major) 
                          VALUES (%s, %s, %s)"""
                cursor.execute(query, (student.name, student.age, student.major))
                connection.commit()
                return True
            except Exception as e:
                print(f"Error adding student: {e}")
                return False
            finally:
                connection.close()
    
    def get_all_students(self):
        connection = self.db.get_connection()
        if connection:
            try:
                cursor = connection.cursor(dictionary=True)
                cursor.execute("SELECT * FROM students")
                results = cursor.fetchall()
                return [Student(
                    student_id=row['id'],
                    name=row['name'],
                    age=row['age'],
                    major=row['major']
                ) for row in results]
            except Exception as e:
                print(f"Error fetching students: {e}")
                return []
            finally:
                connection.close()

    def get_student_by_id(self, student_id):
        connection = self.db.get_connection()
        if connection:
            try:
                cursor = connection.cursor(dictionary=True)
                cursor.execute("SELECT * FROM students WHERE id = %s", (student_id,))
                row = cursor.fetchone()
                if row:
                    return Student(
                        student_id=row['id'],
                        name=row['name'],
                        age=row['age'],
                        major=row['major']
                    )
                return None
            except Exception as e:
                print(f"Error fetching student: {e}")
                return None
            finally:
                connection.close()

    def update_student(self, student):
        connection = self.db.get_connection()
        if connection:
            try:
                cursor = connection.cursor()
                query = """UPDATE students 
                          SET name = %s, age = %s, major = %s 
                          WHERE id = %s"""
                cursor.execute(query, (student.name, student.age, 
                                     student.major, student.student_id))
                connection.commit()
                return True
            except Exception as e:
                print(f"Error updating student: {e}")
                return False
            finally:
                connection.close()

    def delete_student(self, student_id):
        connection = self.db.get_connection()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("DELETE FROM students WHERE id = %s", (student_id,))
                connection.commit()
                return True
            except Exception as e:
                print(f"Error deleting student: {e}")
                return False
            finally:
                connection.close()

    def search_students(self, search_term):
        connection = self.db.get_connection()
        if connection:
            try:
                cursor = connection.cursor(dictionary=True)
                query = """SELECT * FROM students 
                          WHERE name LIKE %s 
                          OR major LIKE %s"""
                search_pattern = f"%{search_term}%"
                cursor.execute(query, (search_pattern, search_pattern))
                results = cursor.fetchall()
                return [Student(
                    student_id=row['id'],
                    name=row['name'],
                    age=row['age'],
                    major=row['major']
                ) for row in results]
            except Exception as e:
                print(f"Error searching students: {e}")
                return []
            finally:
                connection.close()

