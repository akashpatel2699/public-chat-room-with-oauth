# models.py
import flask_sqlalchemy
from app import db
from datetime import datetime
from enum import Enum

class Messages(db.Model):
    __tablename__ = 'messages'
    
    username = db.Column(db.String(100),primary_key=True, nullable=False)
    message  = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime,primary_key=True, nullable=False, default=datetime.utcnow)
    def __init__(self, username,message,created_at):
        self.username = username
        self.message = message
        self.created_at = created_at
    def __repr__(self):
        return '<message: %s by %s>' % self.message,self.username
    
class Connected_users(db.Model):
    __tablename__ = 'connected_users'
    
    sid = db.Column(db.String(50), primary_key=True)
    auth_type = db.Column(db.String(120))
    name = db.Column(db.String(120))
    email = db.Column(db.String(120))
    profile_url = db.Column(db.Text)

    def __init__(self, sid,auth_type,name,email,profile_url):
        assert type(auth_type) is AuthUserType
        self.sid = sid
        self.name = name
        self.email= email
        self.auth_type = auth_type.value
        self.profile_url = profile_url
        
    def __repr__(self):
        return '<Connected_users: %s has %s>' % self.socket_id,self.username
        
class AuthUserType(Enum):
    GOOGLE = "google"
    FACEBOOK = "facebook"
    GITHUB = "github"