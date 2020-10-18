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
import bot

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
def add_new_connected_user(channel, socket_sid,username):
    new_user  = models.Connected_users(socket_id=socket_sid,username=username)
    db.session.add(new_user)
    db.session.commit()

    socketio.emit(channel, {'addNewUser': username},skip_sid=socket_sid)
    
# Remove disconnected user from connected users list in postgres 
def remove_disconnected_user(channel,socket_sid):
    user_to_remove = db.session.query(models.Connected_users).get(socket_sid)
    # user_to_remove = db.session.query(models.Connected_users).filter_by(socket_id=socket_sid).first()
    username = user_to_remove.username
    db.session.delete(user_to_remove)
    db.session.commit()
    
    socketio.emit(channel, {'removeUser': username},include_self=False)

def emit_all_messages(channel,socket_sid,username):

    all_connected_users = [ \
        db_users.username for db_users in \
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
        'username': username,
        'usersConnected':all_connected_users
    },room=socket_sid)   

def add_new_message(channel,socket_sid,message,username):
    created_at = pytz.utc.localize(datetime.now(),is_dst=None).astimezone(tz_NY)
    username =  db.session.query(models.Connected_users).get(socket_sid).username if len(username) == 0  else username
    new_message = models.Messages(username=username,message=message,created_at=created_at) 
    db.session.add(new_message)
    db.session.commit()

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

        
@socketio.on('connect')
def on_connect():
    print("hello")
    socket_sid = flask.request.sid
    username = generate_username()[0]
    emit_all_messages(SEND_ALL_MESSAGES_NEW_USER_CHANNEL, socket_sid,username)
    add_new_connected_user(ADD_NEW_USER_CHANNEL,socket_sid,username)
    

@socketio.on('disconnect')
def on_disconnect():
    # Socket ID of disconnected user to be remove from connected_users table in postgres
    socket_sid = flask.request.sid 
    remove_disconnected_user(REMOVE_DISCONNECTED_USER_CHANNEL,socket_sid)


@socketio.on('new message')
def on_new_address(data):
    socket_sid = flask.request.sid 
    message = data['chat']
    add_new_message(RECIEVE_NEW_MESSAGE,socket_sid,message, "")
    if message.startswith('!! ', 0 , 3):
        message =  check_for_bot_command(message)
        add_new_message(RECIEVE_NEW_MESSAGE,"",message, bot.NAME)

@socketio.on('new github user')
def on_new_github_user(data):
    print("Got an event for new github user input with data:", data)
    response = req.post("https://github.com/login/oauth/access_token", 
        {
            'client_id': github_client_id,
            'client_secret': github_client_secret,
            'code' : data['code']
        }
    )
    access_token = response.text.split('&')[0].split('=')[1]
    response = req.get("https://api.github.com/user", auth=('token', access_token))
    response = response.json()
    name = response['login']
    if response['email'] == None:
        email = name + "@null.com"
    else: 
        email = response['email']
    push_new_user_to_db(name, email ,models.AuthUserType.GITHUB)

@socketio.on('new facebook user')
def on_new_facebook_user(data):
    print("Got an event for new facebook user input with data:", data)
    print('name for facebook: {} email is {}'.format(data['name'],data['email']))
    push_new_user_to_db(data['name'], data['email'],models.AuthUserType.FACEBOOK)

@socketio.on('new google user')
def on_new_google_user(data):
    try:
        idinfo = id_token.verify_oauth2_token(data['id_token'], requests.Request(), google_client_id)
        userid = idinfo['sub']
        username = idinfo['name']
        email = idinfo['email']
        print("Username: {} Email: {}".format(username,email))
        push_new_user_to_db(username, email ,models.AuthUserType.GOOGLE)
    except ValueError:
        # Invalid token
        pass
    # TODO


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
