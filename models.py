# models.py
import flask_sqlalchemy
from app import db
from datetime import datetime

class Messages(db.Model):
    __tablename__ = 'messages'
    username = db.Column(db.String(100),primary_key=True, nullable=False)
    message  = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime,primary_key=True, nullable=False,
        default=datetime.now)
    def __init__(self, username,message,created_at):
        self.username = username
        self.message = message
        self.created_at = created_at
    def __repr__(self):
        return '<message: %s by %s>' % self.message,self.username
    
class Connected_users(db.Model):
    __tablename__ = 'connected_users'
    socket_id = db.Column(db.String(100),primary_key=True, nullable=False)
    
    def __init__(self, socket_id):
        self.socket_id = socket_id
    def __repr__(self):
        return '<Connected_users: %s>' % self.socket_id