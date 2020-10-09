# app.py
from os.path import join, dirname
from dotenv import load_dotenv
import os
import flask
import flask_sqlalchemy
import flask_socketio
import models 
import random

CHAT_MESSAGE_RECEIVED_CHANNEL = 'addresses received'

app = flask.Flask(__name__)

socketio = flask_socketio.SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")

dotenv_path = join(dirname(__file__), 'sql.env')
load_dotenv(dotenv_path)


database_uri = os.environ['DATABASE_URL']

app.config['SQLALCHEMY_DATABASE_URI'] = database_uri

db = flask_sqlalchemy.SQLAlchemy(app)
# db.init_app(app)
# db.app = app


# db.create_all()
# db.session.commit()

user_data  = []
usernames  = ['Akash','Bansil','Raj','Rohit']
usersConnected = {}


# def emit_all_addresses(channel):
#     # TODO - content.jsx looking for all addresses, we want to emit to all address
#     all_addresses = [ \
#         db_address.address for db_address in \
#         db.session.query(models.Usps).all()
#     ]
    
    
#     socketio.emit(channel, {
#         'allAddresses': all_addresses
#     })   

@socketio.on('connect')
def on_connect():
    print('Someone connected!\n =========\n'+ flask.request.sid +'\n' + str(len(user_data)))
    # socketio.emit('connected', {
    #     'test': 'Connected'
    # })
    socket_sid = flask.request.sid
    # username  = usernames[random.randint(0,len(usernames)-1)]
    username = socket_sid
    usersConnected[socket_sid] = username
    socketio.emit('joinuser', {'username': username, 'messages': user_data,'usersConnected':list(usersConnected.values())},room=socket_sid)
    socketio.emit('addNewUser', {'addNewUser': username},skip_sid=socket_sid)
    # TODO
    

@socketio.on('disconnect')
def on_disconnect():
    removeUser = usersConnected.pop(flask.request.sid)
    socketio.emit('removeUser', {'removeUser': removeUser },include_self=False)
    print ('Someone disconnected!')

@socketio.on('new message')
def on_new_address(data):
    print("Got an event for new address input with data:", data)
    user_data.append(data['chat'])
    # db.session.add(models.Usps(data["address"]));
    # db.session.commit();
    socketio.emit('new messages', {'chat': data['chat']})
    # emit_all_messages(CHAT_MESSAGE_RECEIVED_CHANNEL)

@app.route('/')
def index():
    # emit_all_addresses(ADDRESSES_RECEIVED_CHANNEL)

    return flask.render_template("index.html")

if __name__ == '__main__': 
    socketio.run(
        app,
        host=os.getenv('IP', '0.0.0.0'),
        port=int(os.getenv('PORT', 8080)),
        debug=True
    )
