# app.py
from os.path import join, dirname
from dotenv import load_dotenv
import os
import flask
import flask_sqlalchemy
import flask_socketio
import random
from datetime import datetime
import pytz

SEND_ALL_MESSAGES_NEW_USER_CHANNEL = 'joinuser'
ADD_NEW_USER_CHANNEL = 'addNewUser'
REMOVE_DISCONNECTED_USER_CHANNEL = 'removeUser'
RECIEVE_NEW_MESSAGE = 'new message'

# Convert datetime to local time zone
tz_NY = pytz.timezone('America/New_York') 

app = flask.Flask(__name__)

socketio = flask_socketio.SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")

dotenv_path = join(dirname(__file__), 'sql.env')
load_dotenv(dotenv_path)


database_uri = os.environ['DATABASE_URL']

app.config['SQLALCHEMY_DATABASE_URI'] = database_uri

db = flask_sqlalchemy.SQLAlchemy(app)
db.init_app(app)
db.app = app

import models

db.create_all()
db.session.commit()


#Add newly connected user to currently connected users in postgres
def add_new_connected_user(channel, socket_sid):
    new_user  = models.Connected_users(socket_id=socket_sid)
    db.session.add(new_user)
    db.session.commit()

    socketio.emit(channel, {'addNewUser': socket_sid},skip_sid=socket_sid)
    
# Remove disconnected user from connected users list in postgres 
def remove_disconnected_user(channel,socket_sid):
    db.session.query(models.Connected_users).filter_by(socket_id=socket_sid).delete()
    db.session.commit()
    
    socketio.emit(channel, {'removeUser': socket_sid},include_self=False)

def emit_all_messages(channel,socket_sid):
    # TODO - content.jsx looking for all addresses, we want to emit to all address
    all_connected_users = [ \
        db_users.socket_id for db_users in \
        db.session.query(models.Connected_users).all()
    ]
    all_message_objects = [ \
        {'username':db_message.username,'message':db_message.message,\
        'created_at':str(pytz.utc.localize(db_message.created_at,is_dst=None).astimezone(tz_NY))} \
        for db_message in \
        db.session.query(models.Messages).order_by(models.Messages.created_at).all()
    ]
    
    socketio.emit(channel, {
        'message_objects':all_message_objects,
        'username': socket_sid,
        'usersConnected':all_connected_users
    },room=socket_sid)   

def add_new_message(channel,socket_sid,message):
    created_at = pytz.utc.localize(datetime.now(),is_dst=None).astimezone(tz_NY)
    new_message = models.Messages(username=socket_sid,message=message,created_at=created_at)
    db.session.add(new_message)
    db.session.commit()

    socketio.emit(channel,{
        'newMessage': {'username':socket_sid,'message':message,'created_at': str(created_at)}
    })

@socketio.on('connect')
def on_connect():
    socket_sid = flask.request.sid
    username = socket_sid
    emit_all_messages(SEND_ALL_MESSAGES_NEW_USER_CHANNEL,username)
    add_new_connected_user(ADD_NEW_USER_CHANNEL, socket_sid)
    

@socketio.on('disconnect')
def on_disconnect():
    # Socket ID of disconnected user to be remove from connected_users table in postgres
    socket_sid = flask.request.sid 
    remove_disconnected_user(REMOVE_DISCONNECTED_USER_CHANNEL,socket_sid)


@socketio.on('new message')
def on_new_address(data):
    socket_sid = flask.request.sid 
    add_new_message(RECIEVE_NEW_MESSAGE,socket_sid,data['chat'])

@app.route('/')
def index():
    return flask.render_template("index.html")

if __name__ == '__main__': 
    socketio.run(
        app,
        host=os.getenv('IP', '0.0.0.0'),
        port=int(os.getenv('PORT', 8080)),
        debug=True
    )