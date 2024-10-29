from api.app import app
from api.error_handlers import register_error_handlers
from config.config import Config

def setup_app():
    # تطبيق الإعدادات
    app.config.from_object(Config)
    
    # تسجيل معالجات الأخطاء
    register_error_handlers(app)
    
    return app

if __name__ == "__main__":
    app = setup_app()
    app.run(debug=True)