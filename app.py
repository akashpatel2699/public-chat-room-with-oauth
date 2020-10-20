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
from random_username.generate import generate_username
import requests as req
import bot
from rfc3987 import parse

from google.oauth2 import id_token
from google.auth.transport import requests

SEND_ALL_MESSAGES_NEW_USER_CHANNEL = 'joinuser'
ADD_NEW_USER_CHANNEL = 'addNewUser'
REMOVE_DISCONNECTED_USER_CHANNEL = 'removeUser'
RECIEVE_NEW_MESSAGE = 'new message'
AUTHENTICATED_CHANNEL = 'authenticate'

# Convert datetime to local time zone
tz_NY = pytz.timezone('America/New_York') 

app = flask.Flask(__name__)

socketio = flask_socketio.SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")

dotenv_path = join(dirname(__file__), 'sql.env')
load_dotenv(dotenv_path)


database_uri = os.environ['DATABASE_URL']
google_client_id = os.environ['GOOGLE_CLIENT_ID']
github_client_id = os.environ['GITHUB_CLIENT_ID']
github_client_secret = os.environ['GITHUB_CLIENT_SECRET']

app.config['SQLALCHEMY_DATABASE_URI'] = database_uri

db = flask_sqlalchemy.SQLAlchemy(app)
db.init_app(app)
db.app = app

import models


# db = flask_sqlalchemy.SQLAlchemy(app)
# def init_db(app):
#     db.init_app(app)
#     db.app = app     # May not be necessary, but I had some issues without it I think
#     import models
#     db.create_all()
#     db.session.commit()
    
#Add newly connected user to currently connected users in postgres
def add_new_connected_user(channel,socket_sid,name,email,auth_type, profile_url):
    user_exist_in_db = db.session.query(models.Connected_users).filter_by(email=email).first()
    if user_exist_in_db and (email == user_exist_in_db.email and auth_type.value != user_exist_in_db.auth_type):
        user_exist_in_db.auth_type = auth_type
    elif user_exist_in_db and socket_sid != user_exist_in_db.sid:
        user_exist_in_db.sid = socket_sid
        db.session.commit()
        return
    elif user_exist_in_db and auth_type == user_exist_in_db.auth_type:
        return
    else:
        new_user  = models.Connected_users(sid=socket_sid,auth_type=auth_type,name=name,email=email,profile_url=profile_url)
        db.session.add(new_user)
    db.session.commit()
    socketio.emit(channel, {'addNewUser': name,'auth_type': auth_type.value, 'profile_url': profile_url},skip_sid=socket_sid)
    
# Remove disconnected user from connected users list in postgres 
def remove_disconnected_user(channel,socket_sid):
    user_to_remove = db.session.query(models.Connected_users).get(socket_sid)
    # user_to_remove = db.session.query(models.Connected_users).filter_by(socket_id=socket_sid).first()
    if user_to_remove: 
        username = user_to_remove.name
        db.session.delete(user_to_remove)
        db.session.commit()
        socketio.emit(channel, {'removeUser': username},include_self=False)

def emit_all_messages(channel,socket_sid,username, email, profile_url):

    all_connected_users = [ \
        {'username':db_user.name,'auth_type': db_user.auth_type, 'profile_url': db_user.profile_url} for db_user in \
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
        'user': {'username': username,'email': email},
        'usersConnected':all_connected_users
    },room=socket_sid)   

def add_new_message(channel,socket_sid,message,username, email):
    created_at = pytz.utc.localize(datetime.now(),is_dst=None).astimezone(tz_NY)
    try:
        username =  db.session.query(models.Connected_users).filter_by(email=email).first().name if len(username) == 0  else username
        new_message = models.Messages(username=username,message=message,created_at=created_at) 
        db.session.add(new_message)
        db.session.commit()
    except AttributeError:
        user_authenticated(AUTHENTICATED_CHANNEL, False,socket_sid)
        return

    socketio.emit(channel,{
        'newMessage': {'username':username,'message':message,'created_at': str(created_at)}
    })
    
def check_for_bot_command(message):
    # check for valid bot command and act accordingly
    bot_reply= ''
    if 'about' in message:
        bot_reply = bot.about()
    elif 'help' in message:
        bot_reply = bot.help()
    elif 'funtranslate' in message:
        tmp = message.find('funtranslate')
        try:
            message_to_translate = message[tmp + message[tmp:].index(' ')+1:]
            bot_reply = bot.funtranslate(message_to_translate)
        except ValueError:
            bot_reply = "Incorrect format. Try !! help to see the correct format"
    elif 'weather' in message:
        tmp = message.find('weather')
        try:
            weather_city = message[tmp + message[tmp:].index(' ')+1:]
            bot_reply = bot.weather(weather_city)
        except ValueError:
            bot_reply = "Incorrect format. Try !! help to see the correct format"
    elif 'predict_age' in message:
        tmp = message.find('predict_age')
        try:
            name = message[tmp + message[tmp:].index(' ')+1:]
            bot_reply = bot.predict_age(name)
        except ValueError:
            bot_reply = "Incorrect format. Try !! help to see the correct format"
    else:
        bot_reply= "Unrecognized command. Please use !! help to see available commands."
    return bot_reply
    
def check_for_valid_url(message):
    try:
        parse(message,rule="IRI")
        return True
    except ValueError:
        return False

def check_for_valid_image(image_url):
    print("image url func")
    image_formats = ("image/png", "image/jpeg", "image/jpg")
    r = req.head(image_url)
    if r.headers["content-type"] in image_formats:
        return True
    return False

def user_authenticated(channel, boolean,socket_sid):
    socketio.emit(channel, {
        'isAuthenticated': boolean,
    },room=socket_sid)
    
@socketio.on('connect')
def on_connect():
    socket_sid = flask.request.sid
    user_authenticated(AUTHENTICATED_CHANNEL,False,socket_sid)
    

@socketio.on('disconnect')
def on_disconnect():
    # Socket ID of disconnected user to be remove from connected_users table in postgres
    print("disconnected")
    socket_sid = flask.request.sid 
    print(socket_sid)
    remove_disconnected_user(REMOVE_DISCONNECTED_USER_CHANNEL,socket_sid)
    user_authenticated(AUTHENTICATED_CHANNEL,False,socket_sid)

@socketio.on('new message')
def on_new_address(data):
    socket_sid = flask.request.sid 
    message = data['chat']
    email = data['email']
    if check_for_valid_url(message):
        if check_for_valid_image(message):
            message = "<img src={} alt='failed to load and image' style='width:400px;height:500px;object-fit:cover;'>".format(message)
        else:
            message = "<a href={} target='_blank'>{}</a>".format(message,message)
        
        add_new_message(RECIEVE_NEW_MESSAGE,socket_sid,message, "", email)
    elif not check_for_valid_url(message):
        add_new_message(RECIEVE_NEW_MESSAGE,socket_sid,message, "", email)
    
    if message.startswith('!! ', 0 , 3):
        message =  check_for_bot_command(message)
        add_new_message(RECIEVE_NEW_MESSAGE,"",message, bot.NAME, email)

@socketio.on('new github user')
def on_new_github_user(data):
    socket_sid = flask.request.sid 
    print("Got an event for new github user input with data:", data)
    response = req.post("https://github.com/login/oauth/access_token", 
        {
            'client_id': github_client_id,
            'client_secret': github_client_secret,
            'code' : data['code']
        }
    )
    try:
        access_token = response.text.split('&')[0].split('=')[1]
        response = req.get("https://api.github.com/user", auth=('token', access_token))
        response = response.json()
        name = response['login']
        avatar_url = response['avatar_url']
        if response['email'] == None:
            email = name + "@null.com"
        else: 
            email = response['email']
        
        add_new_connected_user(ADD_NEW_USER_CHANNEL,socket_sid,name,email,models.AuthUserType.GITHUB,avatar_url)
        emit_all_messages(SEND_ALL_MESSAGES_NEW_USER_CHANNEL, socket_sid, name, email, avatar_url)
        user_authenticated(AUTHENTICATED_CHANNEL,True,socket_sid)
        
    except KeyError: 
        return

@socketio.on('new facebook user')
def on_new_facebook_user(data):
    socket_sid = flask.request.sid 
    name = data['name']
    email = data['email']
    profile_url = data['url']
    print("Got an event for new facebook user input with data:", data)
    print('name for facebook: {} email is {}'.format(data['name'],data['email']))
    
    add_new_connected_user(ADD_NEW_USER_CHANNEL,socket_sid,name,email,models.AuthUserType.FACEBOOK,profile_url)
    emit_all_messages(SEND_ALL_MESSAGES_NEW_USER_CHANNEL, socket_sid, name, email, profile_url)
    user_authenticated(AUTHENTICATED_CHANNEL,True,socket_sid)

@socketio.on('new google user')
def on_new_google_user(data):
    socket_sid = flask.request.sid 
    try:
        idinfo = id_token.verify_oauth2_token(data['id_token'], requests.Request(), google_client_id)
        userid = idinfo['sub']
        name = idinfo['name']
        email = idinfo['email']
        profile_url = idinfo['picture']
        print(profile_url)
        print("Username: {} Email: {}".format(name,email))
        
        add_new_connected_user(ADD_NEW_USER_CHANNEL,socket_sid,name,email,models.AuthUserType.GOOGLE,profile_url)
        emit_all_messages(SEND_ALL_MESSAGES_NEW_USER_CHANNEL, socket_sid, name, email,profile_url)
        user_authenticated(AUTHENTICATED_CHANNEL,True,socket_sid)
        
    except ValueError:
        # Invalid token
        pass


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
