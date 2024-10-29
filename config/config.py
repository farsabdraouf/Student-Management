class Config:
    """
    إعدادات التطبيق
    """
    SECRET_KEY = ''  # يجب تغييره في الإنتاج
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''
    MYSQL_DB = 'student_management'
    
    # إعدادات Flask
    DEBUG = True  # يجب تغييره إلى False في الإنتاج
    JSON_AS_ASCII = False  # لدعم اللغة العربية

