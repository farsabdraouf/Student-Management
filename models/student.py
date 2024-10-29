class Student:
    def __init__(self, student_id=None, name=None, age=None, major=None):
        self.student_id = student_id
        self.name = name
        self.age = age
        self.major = major
    
    def __str__(self):
        return f"Student(ID: {self.student_id}, Name: {self.name}, Age: {self.age}, Major: {self.major})"