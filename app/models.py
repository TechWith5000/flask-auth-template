from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def set_password(self, password):
        """Hashes password and stores it"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Checks if password matches the stored hash"""
        return check_password_hash(self.password_hash, password)

class TokenBlocklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, unique=True) # JWT Token ID
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())