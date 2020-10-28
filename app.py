# app.py
"""
    Main server file that handles all client requests
    including socket calls and communication with
    postgres sql to store or fetch data like
    message and connected users in the public chat
"""
import os
from os.path import join, dirname
from datetime import datetime
from dotenv import load_dotenv
import flask
import flask_sqlalchemy
import flask_socketio
import pytz
import requests as req
from rfc3987 import parse
from google.oauth2 import id_token
from google.auth.transport import requests

import models
import bot

SEND_ALL_MESSAGES_NEW_USER_CHANNEL = "joinuser"
ADD_NEW_USER_CHANNEL = "addNewUser"
REMOVE_DISCONNECTED_USER_CHANNEL = "removeUser"
RECIEVE_NEW_MESSAGE = "new message"
AUTHENTICATED_CHANNEL = "authenticate"

# Convert datetime to local time zone
tz_NY = pytz.timezone("America/New_York")

app = flask.Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = flask_sqlalchemy.SQLAlchemy(app)


socketio = flask_socketio.SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")

dotenv_path = join(dirname(__file__), "sql.env")
load_dotenv(dotenv_path)

database_uri = os.environ["DATABASE_URL"]
google_client_id = os.environ["GOOGLE_CLIENT_ID"]
github_client_id = os.environ["GITHUB_CLIENT_ID"]
github_client_secret = os.environ["GITHUB_CLIENT_SECRET"]


app.config["SQLALCHEMY_DATABASE_URI"] = database_uri

# pylint: disable=no-member,too-many-arguments
def init_db(init_app):
    """
    Initialize the databse with app
    """
    db.init_app(init_app)
    db.app = init_app
    db.create_all()
    db.session.commit()


def add_new_connected_user(channel, socket_sid, name, email, auth_type, profile_url):
    """
    Newly connected user check they already connected from other device
    if there just update their socket id or their authentication type
    if don't exist add them to the connected users' table and send
    everyone else his profile picture and user name to be display
    """
    user_exist_in_db = (
        db.session.query(models.Connected_users).filter_by(email=email).first()
    )
    if user_exist_in_db and (
        email == user_exist_in_db.email
        and auth_type.value != user_exist_in_db.auth_type
    ):
        user_exist_in_db.auth_type = auth_type.value
    elif user_exist_in_db and (
        email == user_exist_in_db.email and socket_sid != user_exist_in_db.sid
    ):
        user_exist_in_db.sid = socket_sid
        db.session.commit()
        return
    elif user_exist_in_db and (
        email == user_exist_in_db.email
        and auth_type.value == user_exist_in_db.auth_type
    ):
        return
    else:
        new_user = models.Connected_users(
            sid=socket_sid,
            auth_type=auth_type,
            name=name,
            email=email,
            profile_url=profile_url,
        )
        db.session.add(new_user)
    db.session.commit()
    socketio.emit(
        channel,
        {"addNewUser": name, "auth_type": auth_type.value, "profile_url": profile_url},
        skip_sid=socket_sid,
    )


# Remove disconnected user from connected users list in postgres
def remove_disconnected_user(channel, socket_sid):
    """
    check that they exist before removing from connected users' table
    """
    user_to_remove = db.session.query(models.Connected_users).get(socket_sid)
    if user_to_remove:
        username = user_to_remove.name
        db.session.delete(user_to_remove)
        db.session.commit()
        socketio.emit(channel, {"removeUser": username}, include_self=False)


def emit_all_messages(channel, socket_sid, username, email):
    """
    Send all messages thats in the public chat to the newly connected user only
    """
    all_connected_users = [
        {
            "username": db_user.name,
            "auth_type": db_user.auth_type,
            "profile_url": db_user.profile_url,
        }
        for db_user in db.session.query(models.Connected_users).all()
    ]
    all_message_objects = [
        {
            "username": db_message.username,
            "message": db_message.message,
            "created_at": str(
                pytz.utc.localize(db_message.created_at, is_dst=None).astimezone(tz_NY)
            ),
            "message_type": db_message.message_type,
        }
        for db_message in db.session.query(models.Messages)
        .order_by(models.Messages.created_at)
        .all()
    ]

    socketio.emit(
        channel,
        {
            "message_objects": all_message_objects,
            "user": {"username": username, "email": email},
            "usersConnected": all_connected_users,
        },
        room=socket_sid,
    )


def add_new_message(channel, socket_sid, message, message_type, username, email):
    """
    Get username of the new message sender and add new message with recieve
    parameters to the Messages table and also send this message to
    all clients in the public room including the sender
    """
    created_at = pytz.utc.localize(datetime.now(), is_dst=None).astimezone(tz_NY)
    try:
        username = (
            db.session.query(models.Connected_users).filter_by(email=email).first().name
            if len(username) == 0
            else username
        )
        new_message = models.Messages(
            username=username,
            message=message,
            message_type=message_type,
            created_at=created_at,
        )
        db.session.add(new_message)
        db.session.commit()
    except AttributeError:
        user_authenticated(AUTHENTICATED_CHANNEL, False, socket_sid)
        return
    socketio.emit(
        channel,
        {
            "newMessage": {
                "username": username,
                "message": message,
                "message_type": message_type.value,
                "created_at": str(created_at),
            }
        },
    )


def check_for_bot_command(message):
    """
    check what bot command it is about confirmed by caller of the function that its a bot cmd
    Based on what bot command it is, call the appropriate function from the bot.py file
    if the commnd doesn't match any available command then return Invalid command message
    """
    bot_reply = ""
    if "about" in message:
        bot_reply = bot.about()
    elif "help" in message:
        bot_reply = bot.help_command()
    elif "funtranslate" in message:
        tmp = message.find("funtranslate")
        try:
            message_to_translate = message[tmp + message[tmp:].index(" ") + 1 :]
            bot_reply = bot.funtranslate(message_to_translate)
        except ValueError:
            bot_reply = (
                "Incorrect funtranslate format. Try !! help to see the correct format"
            )
    elif "weather" in message:
        tmp = message.find("weather")
        try:
            weather_city = message[tmp + message[tmp:].index(" ") + 1 :]
            bot_reply = bot.weather(weather_city)
        except ValueError:
            bot_reply = (
                "Incorrect weather format. Try !! help to see the correct format"
            )
    elif "predict_age" in message:
        tmp = message.find("predict_age")
        try:
            name = message[tmp + message[tmp:].index(" ") + 1 :]
            bot_reply = bot.predict_age(name)
        except ValueError:
            bot_reply = (
                "Incorrect predict_age format. Try !! help to see the correct format"
            )
    else:
        bot_reply = (
            "Unrecognized command. Please use !! help to see available commands."
        )
    return bot_reply


def check_for_valid_url(message):
    """
    check of the message is a valid URL
    """
    try:
        parse(message, rule="IRI")
        return True
    except ValueError:
        return False


def check_for_valid_image(image_url):
    """
    confirm if the valid url is an image url
    """
    image_formats = ("image/png", "image/jpeg", "image/jpg")
    response = req.head(image_url)
    if response.headers["content-type"] in image_formats:
        return True
    return False


def user_authenticated(channel, boolean, socket_sid):
    """
    Simply send the client whether they are authenticated or not
    """
    socketio.emit(
        channel,
        {
            "isAuthenticated": boolean,
        },
        room=socket_sid,
    )


@socketio.on("connect")
def on_connect():
    """
    when user vists the homepage send them unauthenticated response
    so the login page is displayed before allowing to messaging page
    """
    socket_sid = flask.request.sid
    user_authenticated(AUTHENTICATED_CHANNEL, False, socket_sid)


@socketio.on("disconnect")
def on_disconnect():
    """
    when disconnect event is sent remove that user using their socket id
    from the connected_users to required them to login in again
    """
    socket_sid = flask.request.sid
    remove_disconnected_user(REMOVE_DISCONNECTED_USER_CHANNEL, socket_sid)
    user_authenticated(AUTHENTICATED_CHANNEL, False, socket_sid)


@socketio.on("new message")
def on_new_message(data):
    """
    when new message arrives, check for what kind of message it is
    and based on the message type call functions accordingly
    """
    socket_sid = flask.request.sid
    message = data["chat"]
    email = data["email"]
    if check_for_valid_url(message):
        if check_for_valid_image(message):
            message_type = models.MessageType.IMAGE_URL
        else:
            message_type = models.MessageType.URL_LINKS

    else:
        message_type = models.MessageType.TEXT_MESSAGE

    add_new_message(RECIEVE_NEW_MESSAGE, socket_sid, message, message_type, "", email)

    if message.startswith("!! ", 0, 3):
        message = check_for_bot_command(message)
        message_type = models.MessageType.BOT_MESSAGE
        add_new_message(RECIEVE_NEW_MESSAGE, "", message, message_type, bot.NAME, email)


@socketio.on("new github user")
def on_new_github_user(data):
    """
    when user tries to log in with Github button
    send requests to Github server for access_token
    and based on the response validate new user
    """
    socket_sid = flask.request.sid
    response = req.post(
        "https://github.com/login/oauth/access_token",
        {
            "client_id": github_client_id,
            "client_secret": github_client_secret,
            "code": data["code"],
        },
    )
    try:
        access_token = response.text.split("&")[0].split("=")[1]
        response = req.get("https://api.github.com/user", auth=("token", access_token))
        response = response.json()
        name = response["login"]
        avatar_url = response["avatar_url"]
        if response["email"] is None:
            email = name + "@null.com"
        else:
            email = response["email"]

        add_new_connected_user(
            ADD_NEW_USER_CHANNEL,
            socket_sid,
            name,
            email,
            models.AuthUserType.GITHUB,
            avatar_url,
        )
        emit_all_messages(SEND_ALL_MESSAGES_NEW_USER_CHANNEL, socket_sid, name, email)
        user_authenticated(AUTHENTICATED_CHANNEL, True, socket_sid)

    except KeyError:
        return


@socketio.on("new facebook user")
def on_new_facebook_user(data):
    """
    user tries to login with Facebook
    take their name, email, url and then
    add it the connected users table
    and don't need to request for access_token
    as that taken care by front-end
    """
    socket_sid = flask.request.sid
    name = data["name"]
    email = data["email"]
    profile_url = data["url"]

    add_new_connected_user(
        ADD_NEW_USER_CHANNEL,
        socket_sid,
        name,
        email,
        models.AuthUserType.FACEBOOK,
        profile_url,
    )
    emit_all_messages(SEND_ALL_MESSAGES_NEW_USER_CHANNEL, socket_sid, name, email)
    user_authenticated(AUTHENTICATED_CHANNEL, True, socket_sid)


@socketio.on("new google user")
def on_new_google_user(data):
    """
    when user successfully get id_token and send to server
    take that id token and request for their access token
    to fetch name,email,profile picture and then
    add to conencted users and send all the messages to
    the newly connected user and let others know about it
    """
    socket_sid = flask.request.sid
    try:
        idinfo = id_token.verify_oauth2_token(
            data["id_token"], requests.Request(), google_client_id
        )
        name = idinfo["name"]
        email = idinfo["email"]
        profile_url = idinfo["picture"]

        add_new_connected_user(
            ADD_NEW_USER_CHANNEL,
            socket_sid,
            name,
            email,
            models.AuthUserType.GOOGLE,
            profile_url,
        )
        emit_all_messages(SEND_ALL_MESSAGES_NEW_USER_CHANNEL, socket_sid, name, email)
        user_authenticated(AUTHENTICATED_CHANNEL, True, socket_sid)

    except ValueError:
        # Invalid token
        pass


@app.route("/")
def index():
    """
    when user first visits the page
    render index page
    """
    return flask.render_template("index.html")


if __name__ == "__main__":
    init_db(app)
    socketio.run(
        app,
        host=os.getenv("IP", "0.0.0.0"),
        port=int(os.getenv("PORT", "8080")),
        debug=True,
    )
