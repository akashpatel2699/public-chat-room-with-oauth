# models.py
'''
    Define Class that mapes to SQL table using flask SQLALCHEMY
'''
from datetime import datetime
from enum import Enum
from flask_sqlalchemy import Model
from sqlalchemy import Column, String,Text, DateTime

# pylint: disable=no-member,too-few-public-methods,invalid-name,too-many-arguments
class Messages(Model):
    '''
        Define Messages table using flask SQLALCHEMY
    '''
    __tablename__ = "messages"

    username = Column(String(100), primary_key=True, nullable=False)
    message = Column(Text, nullable=False)
    message_type = Column(String(50), nullable=False, default="text message")
    created_at = Column(
        DateTime, primary_key=True, nullable=False, default=datetime.utcnow
    )

    def __init__(self, username, message, message_type, created_at):
        assert isinstance(message_type,MessageType)
        self.username = username
        self.message = message
        self.message_type = message_type.value
        self.created_at = created_at

    def __repr__(self):
        return "<message: {} by {}>".format(self.message, self.username)


class Connected_users(Model):
    '''
        Define Connected_users table using flask SQLALCHEMY
    '''
    __tablename__ = "connected_users"

    sid = Column(String(50), primary_key=True)
    auth_type = Column(String(120))
    name = Column(String(120))
    email = Column(String(120))
    profile_url = Column(Text)

    def __init__(self, sid, auth_type, name, email, profile_url):
        assert isinstance(auth_type,AuthUserType)
        self.sid = sid
        self.name = name
        self.email = email
        self.auth_type = auth_type.value
        self.profile_url = profile_url

    def __repr__(self):
        return "<Connected_users: {} has {}>".format(self.sid, self.name)


class AuthUserType(Enum):
    '''
        Enum class for different Auth types
    '''
    GOOGLE = "google"
    FACEBOOK = "facebook"
    GITHUB = "github"


class MessageType(Enum):
    '''
        Enum class for different Message types
    '''
    TEXT_MESSAGE = "text message"
    URL_LINKS = "url link"
    IMAGE_URL = "image url"
    BOT_MESSAGE = "bot message"
