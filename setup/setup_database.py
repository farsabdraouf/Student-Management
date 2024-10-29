import mysql.connector
from mysql.connector import Error

def setup_database():
    try:
        # إنشاء اتصال بدون تحديد قاعدة بيانات
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password=""
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # إنشاء قاعدة البيانات
            cursor.execute("CREATE DATABASE IF NOT EXISTS student_management")
            
            # استخدام قاعدة البيانات
            cursor.execute("USE student_management")
            
            # إنشاء جدول الطلاب
            create_table_query = """
            CREATE TABLE IF NOT EXISTS students (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                age INT,
                major VARCHAR(50)
            )
            """
            cursor.execute(create_table_query)
            
            print("تم إعداد قاعدة البيانات بنجاح!")
            
    except Error as e:
        print(f"حدث خطأ أثناء إعداد قاعدة البيانات: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    setup_database()

