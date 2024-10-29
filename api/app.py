from flask import Flask, request, jsonify
from repositories.student_repository import StudentRepository
from services.student_service import StudentService
from models.student import Student
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app = Flask(__name__)
repository = StudentRepository()
service = StudentService(repository)

@app.route('/api/students', methods=['GET'])
def get_students():
    """
    الحصول على قائمة الطلاب
    يمكن استخدام معامل search للبحث
    """
    search_term = request.args.get('search', '')
    if search_term:
        students = service.search_students(search_term)
    else:
        students = service.get_all_students()
    
    return jsonify([{
        'id': student.student_id,
        'name': student.name,
        'age': student.age,
        'major': student.major
    } for student in students])

@app.route('/api/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    """
    الحصول على بيانات طالب محدد
    """
    student = service.get_student_by_id(student_id)
    if student:
        return jsonify({
            'id': student.student_id,
            'name': student.name,
            'age': student.age,
            'major': student.major
        })
    return jsonify({'error': 'Student not found'}), 404

@app.route('/api/students', methods=['POST'])
def add_student():
    """
    إضافة طالب جديد
    """
    data = request.get_json()
    
    if not all(key in data for key in ['name', 'age', 'major']):
        return jsonify({'error': 'Missing required fields'}), 400
    
    success = service.add_student(
        name=data['name'],
        age=data['age'],
        major=data['major']
    )
    
    if success:
        return jsonify({'message': 'Student added successfully'}), 201
    return jsonify({'error': 'Failed to add student'}), 400

@app.route('/api/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    """
    تحديث بيانات طالب
    """
    data = request.get_json()

    if not all(key in data for key in ['name', 'age', 'major']):
        return jsonify({'error': 'Missing required fields'}), 400

    success = service.update_student(
        student_id=student_id,
        name=data['name'],
        age=data['age'],
        major=data['major']
    )

    if success:
        return jsonify({'message': 'Student updated successfully'})
    return jsonify({'error': 'Failed to update student'}), 400


@app.route('/api/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    """
    حذف طالب
    """
    success = service.delete_student(student_id)
    
    if success:
        return jsonify({'message': 'Student deleted successfully'})
    return jsonify({'error': 'Failed to delete student'}), 400

@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """
    الحصول على إحصائيات عن الطلاب
    """
    students = service.get_all_students()
    
    # حساب الإحصائيات
    total_students = len(students)
    avg_age = sum(student.age for student in students) / total_students if total_students > 0 else 0
    
    # حساب عدد الطلاب في كل تخصص
    majors = {}
    for student in students:
        majors[student.major] = majors.get(student.major, 0) + 1
    
    return jsonify({
        'total_students': total_students,
        'average_age': round(avg_age, 2),
        'students_by_major': majors
    })

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response