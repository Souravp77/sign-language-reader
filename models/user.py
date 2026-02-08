from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from database.db_helpers import execute_query

class User(UserMixin):
    """User model for authentication"""
    
    def __init__(self, user_id, username, email, password_hash=None):
        self.id = user_id
        self.user_id = user_id
        self.username = username
        self.email = email
        self.password_hash = password_hash
    
    @staticmethod
    def get(user_id):
        """Get user by ID"""
        query = "SELECT * FROM users WHERE user_id = %s"
        result = execute_query(query, (user_id,), fetch_one=True)
        
        if result:
            return User(
                user_id=result['user_id'],
                username=result['username'],
                email=result['email'],
                password_hash=result['password_hash']
            )
        return None
    
    @staticmethod
    def get_by_email(email):
        """Get user by email"""
        query = "SELECT * FROM users WHERE email = %s"
        result = execute_query(query, (email,), fetch_one=True)
        
        if result:
            return User(
                user_id=result['user_id'],
                username=result['username'],
                email=result['email'],
                password_hash=result['password_hash']
            )
        return None
    
    @staticmethod
    def create(username, email, password):
        """Create a new user"""
        password_hash = generate_password_hash(password)
        
        query = """
        INSERT INTO users (username, email, password_hash)
        VALUES (%s, %s, %s)
        """
        user_id = execute_query(query, (username, email, password_hash))
        
        if user_id:
            return User.get(user_id)
        return None
    
    def check_password(self, password):
        """Check if password matches hash"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """Convert user to dictionary"""
        return {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email
        }