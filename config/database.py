from mysql.connector import connect, Error

class DatabaseConnection:
    def __init__(self):
        self.config = {
            'host': 'localhost',
            'user': 'root',
            'password': '',
            'database': 'student_management'
        }
    
    def get_connection(self):
        try:
            connection = connect(**self.config)
            return connection
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            return None