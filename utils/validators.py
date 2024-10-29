def validate_student_data(name, age, major):
    """
    التحقق من صحة بيانات الطالب
    """
    # التحقق من الاسم
    if not name or not isinstance(name, str):
        print("الاسم غير صالح")
        return False
    
    name = name.strip()
    if len(name) < 2 or len(name) > 100:
        print("يجب أن يكون طول الاسم بين 2 و 100 حرف")
        return False
    
    # التحقق من العمر
    try:
        age = int(age)
        if age < 16 or age > 100:
            print("العمر يجب أن يكون بين 16 و 100")
            return False
    except (ValueError, TypeError):
        print("العمر يجب أن يكون رقماً صحيحاً")
        return False
    
    # التحقق من التخصص
    if not major or not isinstance(major, str):
        print("التخصص غير صالح")
        return False
    
    major = major.strip()
    if len(major) < 2 or len(major) > 50:
        print("يجب أن يكون طول التخصص بين 2 و 50 حرف")
        return False
    
    return True

def validate_student_id(student_id):
    """
    التحقق من صحة رقم الطالب
    """
    try:
        student_id = int(student_id)
        if student_id <= 0:
            print("رقم الطالب يجب أن يكون أكبر من 0")
            return False
        return True
    except (ValueError, TypeError):
        print("رقم الطالب يجب أن يكون رقماً صحيحاً")
        return False
