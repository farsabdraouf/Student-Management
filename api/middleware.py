from functools import wraps
from flask import request, jsonify
import jwt
import datetime

SECRET_KEY = ""  # يجب تغييره في الإنتاج

def create_token(user_id):
    """
    إنشاء token للمصادقة
    """
    token = jwt.encode({
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
    }, SECRET_KEY, algorithm='HS256')
    return token

def token_required(f):
    """
    middleware للتحقق من صحة token
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        try:
            token = token.split()[1]  # Remove 'Bearer' prefix
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        except:
            return jsonify({'error': 'Invalid token'}), 401
        
        return f(*args, **kwargs)
    
    return decorated
