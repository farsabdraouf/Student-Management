from models.student import Student
from utils.validators import validate_student_data

class StudentService:
    def __init__(self, repository):
        self.repository = repository
    
    def add_student(self, name, age, major):
        if validate_student_data(name, age, major):
            student = Student(name=name, age=age, major=major)
            return self.repository.add_student(student)
        return False
    
    def get_all_students(self):
        return self.repository.get_all_students()
    
    def get_student_by_id(self, student_id):
        return self.repository.get_student_by_id(student_id)
    
    def update_student(self, student_id, name, age, major):
        if validate_student_data(name, age, major):
            student = Student(student_id=student_id, name=name, 
                            age=age, major=major)
            return self.repository.update_student(student)
        return False
    
    def delete_student(self, student_id):
        return self.repository.delete_student(student_id)
    
    def search_students(self, search_term):
        return self.repository.search_students(search_term)

# utils/validators.py
def validate_student_data(name, age, major):
    if not name or len(name.strip()) < 2:
        print("Invalid name")
        return False
    
    try:
        age = int(age)
        if age < 16 or age > 100:
            print("Invalid age")
            return False
    except ValueError:
        print("Age must be a number")
        return False
    
    if not major or len(major.strip()) < 2:
        print("Invalid major")
        return False
    
    return True
