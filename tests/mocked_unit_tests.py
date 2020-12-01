"""
    app.py and bot.py 
    
    This file tests mocked unit tests from app and bot
"""

import sys
import unittest.mock as mock
from unittest.mock import Mock
from dotenv import load_dotenv
import os
import datetime
from os.path import join, dirname
import requests
import pytz
import unittest

# pylint: disable=C0413
sys.path.append(join(dirname(__file__), "../"))
from app import tz_NY
from app import (
    SEND_ALL_MESSAGES_NEW_USER_CHANNEL,
    ADD_NEW_USER_CHANNEL,
    REMOVE_DISCONNECTED_USER_CHANNEL,
    RECIEVE_NEW_MESSAGE,
    AUTHENTICATED_CHANNEL,
)
from app import database_uri, google_client_id, github_client_id, github_client_secret
from app import (
    check_for_bot_command,
    check_for_valid_image,
    add_new_connected_user,
    remove_disconnected_user,
    emit_all_messages,
    add_new_message,
    on_connect,
    on_disconnect,
    on_new_message,
    on_new_facebook_user,
    on_new_google_user,
)
from bot import (
    NAME,
    FUN_TRANSLATE_BASE_URL,
    OPEN_WEATHER_API_BASE_URL,
    PREDICT_AGE_BASED_ON_API,
)
from bot import OPEN_WEATHER_API_KEY
from bot import funtranslate
from models import AuthUserType, MessageType

KEY_INPUT = "input"
KEY_EXPECTED = "expected"
KEY_CHANNEL = "channel"
KEY_SOCKET_ID = "socket_sid"
KEY_NAME = "name"
KEY_EMAIL = "email"
KEY_AUTH_TYPE = "auth_type"
KEY_PROFILE_URL = "profile_url"
KEY_MESSAGE = "message"
KEY_MESSAGE_TYPE = "message_type"
KEY_CHAT = "chat"
KEY_ID_TOKEN = "id_token"


class HeaderObject:
    def __init__(self, content_type):
        self.headers = {"content-type": content_type}


class UserObject:
    all_objects = []

    def __init__(self, email, sid, auth_type, name, profile_url):
        self.email = email
        self.sid = sid
        self.auth_type = auth_type.value
        self.name = name
        self.profile_url = profile_url
        self.all_objects.append(self)

    def filter_by(self, email):
        return self

    def first(self):
        return self.all_objects[0]

    def get(self, sid):
        for each in self.all_objects:
            if each.sid == sid:
                return each

    def all(self):
        return self.all_objects

    def order_by(self, created_at):
        return MessageObject(
            "akashpatel",
            "This is a message object",
            MessageType.TEXT_MESSAGE,
            datetime.datetime.now(),
        )


class MessageObject:
    all_messages = []

    def __init__(self, username, message, message_type, created_at):
        self.username = username
        self.message = message
        self.message_type = message_type.value
        self.created_at = created_at
        self.all_messages.append(self)

    def first(self):
        return self.all_messages[0]

    def all(self):
        return self.all_messages


class mocked_unit_tests(unittest.TestCase):
    def setUp(self):
        self.check_fun_translate_bot_command_success = [
            {KEY_INPUT: "!! funtranslate hello", KEY_EXPECTED: "hellu"}
        ]
        self.check_edge_case_fun_translate_failure = [
            {
                KEY_INPUT: "!! funtranslate authentication error",
                KEY_EXPECTED: "Unable to translate your message 'authentication error'.",
            },
            {
                KEY_INPUT: "!! funtranslate",
                KEY_EXPECTED: "Incorrect funtranslate format. Try !! help to see the correct format",
            },
        ]
        self.check_weather_bot_command_success = [
            {KEY_INPUT: "!! weather jersey city", KEY_EXPECTED: "67 F"},
            {KEY_INPUT: "!! weather pluto", KEY_EXPECTED: "67 F"},
        ]
        self.check_weather_bot_command_failure = [
            {
                KEY_INPUT: "!! weather unkown city",
                KEY_EXPECTED: "Maybe invalid city name. Try valid city name like jersey city or new york city",
            },
            {
                KEY_INPUT: "!! weather",
                KEY_EXPECTED: "Incorrect weather format. Try !! help to see the correct format",
            },
        ]
        self.check_predict_age_bot_command_success = [
            {
                KEY_INPUT: "!! predict_age name",
                KEY_EXPECTED: "name your predicted age is 43",
            }
        ]
        self.check_predict_age_bot_command_failure = [
            {
                KEY_INPUT: "!! predict_age",
                KEY_EXPECTED: "Incorrect predict_age format. Try !! help to see the correct format",
            },
            {KEY_INPUT: "!! predict_age ", KEY_EXPECTED: "Try some other name than "},
        ]
        self.check_for_valid_image_success = [
            {
                KEY_INPUT: "https://images.pexels.com/photos/5074815/pexels-photo-5074815.jpeg?"
                "auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260",
                KEY_EXPECTED: True,
            }
        ]
        self.check_for_valid_image_failure = [
            {
                KEY_INPUT: "https://images.pexels.com/photos/5074815/pexels-photo-5074815?"
                "auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260",
                KEY_EXPECTED: False,
            }
        ]
        self.add_new_connected_user_success = [
            {
                KEY_INPUT: {
                    KEY_CHANNEL: ADD_NEW_USER_CHANNEL,
                    KEY_SOCKET_ID: "12345",
                    KEY_NAME: "akashpatel",
                    KEY_EMAIL: "akashpatel@gmail.com",
                    KEY_AUTH_TYPE: AuthUserType.GOOGLE,
                    KEY_PROFILE_URL: "https://profileURL.com",
                }
            },
            {
                KEY_INPUT: {
                    KEY_CHANNEL: ADD_NEW_USER_CHANNEL,
                    KEY_SOCKET_ID: "0000",
                    KEY_NAME: "akashpatel",
                    KEY_EMAIL: "akashpatel@gmail.com",
                    KEY_AUTH_TYPE: AuthUserType.GOOGLE,
                    KEY_PROFILE_URL: "https://profileURL.com",
                }
            },
            {
                KEY_INPUT: {
                    KEY_CHANNEL: ADD_NEW_USER_CHANNEL,
                    KEY_SOCKET_ID: "0000",
                    KEY_NAME: "akashpatel",
                    KEY_EMAIL: "akashpatel@gmail.com",
                    KEY_AUTH_TYPE: AuthUserType.GOOGLE,
                    KEY_PROFILE_URL: "https://profileURL.com",
                }
            },
            {
                KEY_INPUT: {
                    KEY_CHANNEL: ADD_NEW_USER_CHANNEL,
                    KEY_SOCKET_ID: "1234",
                    KEY_NAME: "akashpatel",
                    KEY_EMAIL: "akash@gmail.com",
                    KEY_AUTH_TYPE: AuthUserType.FACEBOOK,
                    KEY_PROFILE_URL: "https://profileURL.com",
                }
            },
        ]
        self.remove_disconnected_user_success = [
            {
                KEY_INPUT: {
                    KEY_CHANNEL: REMOVE_DISCONNECTED_USER_CHANNEL,
                    KEY_SOCKET_ID: "12345",
                }
            }
        ]
        self.emit_all_messages_success = [
            {
                KEY_INPUT: {
                    KEY_CHANNEL: SEND_ALL_MESSAGES_NEW_USER_CHANNEL,
                    KEY_SOCKET_ID: "12345",
                    KEY_NAME: "akashpatel",
                    KEY_EMAIL: "akashpatel@gmail.com",
                    KEY_AUTH_TYPE: AuthUserType.GOOGLE,
                    KEY_PROFILE_URL: "https://profileURL.com",
                }
            }
        ]
        self.add_new_message_success = [
            {
                KEY_INPUT: {
                    KEY_CHANNEL: RECIEVE_NEW_MESSAGE,
                    KEY_SOCKET_ID: "12345",
                    KEY_MESSAGE: "this is new message",
                    KEY_MESSAGE_TYPE: MessageType.TEXT_MESSAGE,
                    KEY_NAME: "akashpatel",
                    KEY_EMAIL: "akashpatel@gmail.com",
                }
            }
        ]
        self.on_new_message_success = [
            {
                KEY_INPUT: {
                    KEY_CHAT: "this is a new chat",
                    KEY_EMAIL: "akashpatel@gmail.com",
                },
                KEY_EXPECTED: {
                    KEY_NAME: "",
                    KEY_EMAIL: "akashpatel@gmail.com",
                    KEY_CHAT: "this is a new chat",
                    KEY_MESSAGE_TYPE: MessageType.TEXT_MESSAGE,
                },
            },
            {
                KEY_INPUT: {KEY_CHAT: "!! about", KEY_EMAIL: "bot@gmail.com"},
                KEY_EXPECTED: {
                    KEY_NAME: NAME,
                    KEY_EMAIL: "bot@gmail.com",
                    KEY_CHAT: "!! about",
                    KEY_MESSAGE_TYPE: MessageType.BOT_MESSAGE,
                },
            },
            {
                KEY_INPUT: {
                    KEY_CHAT: "https://google.com",
                    KEY_EMAIL: "akashpatel@gmail.com",
                },
                KEY_EXPECTED: {
                    KEY_NAME: "",
                    KEY_EMAIL: "akashpatel@gmail.com",
                    KEY_CHAT: "https://google.com",
                    KEY_MESSAGE_TYPE: MessageType.URL_LINKS,
                },
            },
            {
                KEY_INPUT: {
                    KEY_CHAT: "https://google.com/image",
                    KEY_EMAIL: "akashpatel@gmail.com",
                },
                KEY_EXPECTED: {
                    KEY_NAME: "",
                    KEY_EMAIL: "akashpatel@gmail.com",
                    KEY_CHAT: "https://google.com/image",
                    KEY_MESSAGE_TYPE: MessageType.IMAGE_URL,
                },
            },
        ]
        self.on_new_facebook_user_success = [
            {
                KEY_INPUT: {
                    KEY_NAME: "akashpatel",
                    KEY_EMAIL: "akashpatel@gmail.com",
                    "url": "https://profileURL.com",
                },
                KEY_EXPECTED: {
                    KEY_NAME: "akashpatel",
                    KEY_EMAIL: "akashpatel@gmail.com",
                    "url": "https://profileURL.com",
                    KEY_SOCKET_ID: "12345",
                },
            }
        ]
        self.on_new_google_user_success = [
            {
                KEY_INPUT: {KEY_ID_TOKEN: "1234567890"},
                KEY_EXPECTED: {
                    KEY_NAME: "akashpatel",
                    KEY_EMAIL: "akashpatel@gmail.com",
                    KEY_PROFILE_URL: "https://profileURL.com",
                    KEY_SOCKET_ID: "12345",
                },
            }
        ]

    def mocked_fun_translate_API_call_success(self, URL):
        class MockResponse:
            def __init__(self, json_data):
                self.json_data = json_data

            def json(self):
                return self.json_data

        return MockResponse({"contents": {"translated": "hellu"}})

    def mocked_API_call_failure(self, URL):
        class MockResponse:
            def __init__(self, json_data):
                self.json_data = json_data

            def json(self):
                return self.json_data

        return MockResponse(
            {"error": {"code": 400, "message": "Bad Request: text is missing."}}
        )

    def test_check_fun_translate_bot_command_success(self):
        for test_case in self.check_fun_translate_bot_command_success:
            with mock.patch("requests.get", self.mocked_fun_translate_API_call_success):

                response = check_for_bot_command(test_case[KEY_INPUT])
                expected = test_case[KEY_EXPECTED]

                self.assertEqual(response, expected)

    def test_check_fun_translate_bot_command_failure(self):
        for test_case in self.check_edge_case_fun_translate_failure:
            with mock.patch("requests.get", self.mocked_API_call_failure):

                response = check_for_bot_command(test_case[KEY_INPUT])
                expected = test_case[KEY_EXPECTED]

                self.assertEqual(response, expected)

    def mocked_weather_API_call_success(self, URL):
        class MockResponse:
            def __init__(self, json_data):
                self.json_data = json_data

            def json(self):
                return self.json_data

        return MockResponse({"main": {"temp": 67}})

    def test_check_weather_bot_command_success(self):
        for test_case in self.check_weather_bot_command_success:
            with mock.patch("requests.get", self.mocked_weather_API_call_success):

                response = check_for_bot_command(test_case[KEY_INPUT])
                expected = test_case[KEY_EXPECTED]

                self.assertEqual(response, expected)

    def test_check_weather_bot_command_failure(self):
        for test_case in self.check_weather_bot_command_failure:
            with mock.patch("requests.get", self.mocked_API_call_failure):

                response = check_for_bot_command(test_case[KEY_INPUT])
                expected = test_case[KEY_EXPECTED]

                self.assertEqual(response, expected)

    def mocked_predict_age_API_call_success(self, URL):
        class MockResponse:
            def __init__(self, json_data):
                self.json_data = json_data

            def json(self):
                return self.json_data

        return MockResponse({"age": 43})

    def test_check_predict_age_bot_command_success(self):
        for test_case in self.check_predict_age_bot_command_success:
            with mock.patch("requests.get", self.mocked_predict_age_API_call_success):

                response = check_for_bot_command(test_case[KEY_INPUT])
                expected = test_case[KEY_EXPECTED]

                self.assertEqual(response, expected)

    def test_check_predict_age_bot_command_failure(self):
        for test_case in self.check_predict_age_bot_command_failure:
            with mock.patch("requests.get", self.mocked_API_call_failure):

                response = check_for_bot_command(test_case[KEY_INPUT])
                expected = test_case[KEY_EXPECTED]

                self.assertEqual(response, expected)

    @mock.patch("requests.head", return_val=Mock())
    def test_check_for_image_url(self, my_mocked_request_dot_head):
        my_mocked_request_dot_head.side_effect = [
            HeaderObject("image/jpg"),
            HeaderObject("text/html"),
        ]
        success_response = check_for_valid_image(self.check_for_valid_image_success[0])
        failure_response = check_for_valid_image(self.check_for_valid_image_failure[0])
        self.assertEqual(
            success_response, self.check_for_valid_image_success[0][KEY_EXPECTED]
        )
        self.assertEqual(
            failure_response, self.check_for_valid_image_failure[0][KEY_EXPECTED]
        )

    @mock.patch("app.db.session.add")
    @mock.patch("app.models.Connected_users")
    @mock.patch("app.db.session.commit", return_value=None)
    @mock.patch("app.socketio.emit", return_value=None)
    @mock.patch(
        "app.db.session.query",
        return_value=UserObject(
            "akashpatel@gmail.com",
            "12345",
            AuthUserType.FACEBOOK,
            "akashpatel",
            "https://profileURL.com",
        ),
    )
    def test_add_new_user_that_exist_in_db(
        self,
        mocked_db_query,
        mocked_socketio_emit,
        mocked_db_session_commit,
        mocked_models_Connected_users,
        mocked_db_session_add,
    ):
        for test_case in self.add_new_connected_user_success:
            input = test_case[KEY_INPUT]
            add_new_connected_user(
                input[KEY_CHANNEL],
                input[KEY_SOCKET_ID],
                input[KEY_NAME],
                input[KEY_EMAIL],
                input[KEY_AUTH_TYPE],
                input[KEY_PROFILE_URL],
            )
            if input[KEY_SOCKET_ID] != "0000" or input[KEY_AUTH_TYPE].value != "google":
                mocked_socketio_emit.assert_called_with(
                    input[KEY_CHANNEL],
                    {
                        "addNewUser": input[KEY_NAME],
                        "auth_type": input[KEY_AUTH_TYPE].value,
                        "profile_url": input[KEY_PROFILE_URL],
                    },
                    skip_sid=input[KEY_SOCKET_ID],
                )
            if input[KEY_EMAIL] == "akash@gmail.com":
                mocked_models_Connected_users.assert_called_with(
                    sid=input[KEY_SOCKET_ID],
                    auth_type=input[KEY_AUTH_TYPE],
                    name=input[KEY_NAME],
                    email=input[KEY_EMAIL],
                    profile_url=input[KEY_PROFILE_URL],
                )
                mocked_db_session_add.called_once()

    @mock.patch("app.db.session.delete")
    @mock.patch("app.db.session.commit", return_value=None)
    @mock.patch("app.socketio.emit", return_value=None)
    @mock.patch(
        "app.db.session.query",
        return_value=UserObject(
            "akashpatel@gmail.com",
            "12345",
            AuthUserType.FACEBOOK,
            "akashpatel",
            "https://profileURL.com",
        ),
    )
    def test_remove_disconnected_user(
        self,
        mocked_db_query,
        mocked_socketio_emit,
        mocked_db_session_commit,
        mocked_db_session_delete,
    ):
        for test_case in self.remove_disconnected_user_success:
            input = test_case[KEY_INPUT]
            remove_disconnected_user(input[KEY_CHANNEL], input[KEY_SOCKET_ID])
            mocked_socketio_emit.assert_called_with(
                input[KEY_CHANNEL], {"removeUser": "akashpatel"}, include_self=False
            )
            mocked_db_session_commit.called_once()
            mocked_db_session_delete.called_once()

    @mock.patch("app.socketio.emit", return_value=None)
    @mock.patch(
        "app.db.session.query",
        return_value=UserObject(
            "akashpatel@gmail.com",
            "12345",
            AuthUserType.FACEBOOK,
            "akashpatel",
            "https://profileURL.com",
        ),
    )
    def test_emit_all_messages(self, mocked_db_query, mocked_socketio_emit):
        for test_case in self.emit_all_messages_success:
            input = test_case[KEY_INPUT]
            emit_all_messages(
                input[KEY_CHANNEL],
                input[KEY_SOCKET_ID],
                input[KEY_NAME],
                input[KEY_EMAIL],
            )
            mocked_all_message_objects = [
                {
                    "username": db_message.username,
                    "message": db_message.message,
                    "created_at": str(
                        pytz.utc.localize(
                            db_message.created_at, is_dst=None
                        ).astimezone(tz_NY)
                    ),
                    "message_type": db_message.message_type,
                }
                for db_message in mocked_db_query().order_by("not useful").all()
            ]
            mocked_all_connected_users = [
                {
                    "username": db_user.name,
                    "auth_type": db_user.auth_type,
                    "profile_url": db_user.profile_url,
                }
                for db_user in mocked_db_query().all()
            ]
            mocked_all_message_objects.pop()
            mocked_socketio_emit.assert_called_with(
                input[KEY_CHANNEL],
                {
                    "message_objects": mocked_all_message_objects,
                    "user": {"username": input[KEY_NAME], "email": input[KEY_EMAIL]},
                    "usersConnected": mocked_all_connected_users,
                },
                room=input[KEY_SOCKET_ID],
            )
            mocked_socketio_emit.called_once()

    @mock.patch("app.db.session.commit")
    @mock.patch("app.db.session.add")
    @mock.patch("app.models.Messages")
    @mock.patch("app.socketio.emit", return_value=None)
    @mock.patch(
        "app.db.session.query",
        return_value=UserObject(
            "akashpatel@gmail.com",
            "12345",
            AuthUserType.FACEBOOK,
            "akashpatel",
            "https://profileURL.com",
        ),
    )
    def test_add_new_message(
        self,
        mocked_db_query,
        mocked_socketio_emit,
        mocked_models_Messages,
        mocked_session_add,
        mocked_session_commit,
    ):
        for test_case in self.add_new_message_success:

            input = test_case[KEY_INPUT]
            add_new_message(
                input[KEY_CHANNEL],
                input[KEY_SOCKET_ID],
                input[KEY_MESSAGE],
                input[KEY_MESSAGE_TYPE],
                input[KEY_NAME],
                input[KEY_EMAIL],
            )

            mocked_models_Messages.called_once()
            mocked_session_add.called_once()
            mocked_session_commit.called_once()
            mocked_db_query.side_effect = 'raise Exception("AttributeError")'
            add_new_message(
                input[KEY_CHANNEL],
                input[KEY_SOCKET_ID],
                input[KEY_MESSAGE],
                input[KEY_MESSAGE_TYPE],
                "",
                input[KEY_EMAIL],
            )
            mocked_session_commit.called_once()

    @mock.patch("app.user_authenticated")
    def test_on_connect(self, mocked_user_authenticated):
        mocker = mock.MagicMock()
        mocker.sid = "12345"
        with mock.patch("app.flask.request",mocker):
            on_connect()
            mocked_user_authenticated.assert_called_with(
                AUTHENTICATED_CHANNEL, False, mocker.sid
            )

    @mock.patch("app.user_authenticated")
    @mock.patch("app.remove_disconnected_user")
    def test_on_disconnect(
        self,
        mocked_remove_disconnected_user,
        mocked_user_authenticated,
    ):
        mocker = mock.MagicMock()
        mocker.sid = "12345"
        with mock.patch("app.flask.request",mocker):
            on_disconnect()
            mocked_remove_disconnected_user.assert_called_with(
                REMOVE_DISCONNECTED_USER_CHANNEL, mocker.sid
            )
            mocked_user_authenticated.assert_called_with(
                AUTHENTICATED_CHANNEL, False, mocker.sid
            )

    @mock.patch("app.check_for_bot_command")
    @mock.patch("app.check_for_valid_image")
    @mock.patch("app.add_new_message")
    def test_on_new_message(
        self,
        mocked_add_new_message,
        mocked_check_for_valid_image,
        mocked_check_for_bot_command,
    ):
        mocked_check_for_valid_image.side_effect = [False, True]
        mocker = mock.MagicMock()
        mocker.sid = "12345"
        with mock.patch("app.flask.request",mocker):
            for test_case in self.on_new_message_success:
                mocked_check_for_bot_command.return_value = "!! about"
                input = test_case[KEY_INPUT]
                expected = test_case[KEY_EXPECTED]
                on_new_message(input)
                if expected[KEY_NAME] == NAME:
                    self.assertEqual(mocked_add_new_message.call_count, 3)
                else:
                    mocked_add_new_message.assert_called_with(
                        RECIEVE_NEW_MESSAGE,
                        mocker.sid,
                        expected[KEY_CHAT],
                        expected[KEY_MESSAGE_TYPE],
                        expected[KEY_NAME],
                        expected[KEY_EMAIL],
                    )

    @mock.patch("app.user_authenticated")
    @mock.patch("app.emit_all_messages")
    @mock.patch("app.add_new_connected_user")
    def test_on_new_facebook_user(
        self,
        mocked_add_new_connected_user,
        mocked_emit_all_messages,
        mocked_user_authenticated,
    ):
        mocker = mock.MagicMock()
        mocker.sid = "12345"
        with mock.patch("app.flask.request",mocker):
            for test_case in self.on_new_facebook_user_success:
                input = test_case[KEY_INPUT]
                expected = test_case[KEY_EXPECTED]
    
                on_new_facebook_user(input)
    
                mocked_add_new_connected_user.assert_called_with(
                    ADD_NEW_USER_CHANNEL,
                    mocker.sid,
                    expected[KEY_NAME],
                    expected[KEY_EMAIL],
                    AuthUserType.FACEBOOK,
                    expected["url"],
                )
                mocked_emit_all_messages.called_once()
                mocked_user_authenticated.assert_called_with(
                    AUTHENTICATED_CHANNEL, True, expected[KEY_SOCKET_ID]
                )

    @mock.patch("app.user_authenticated")
    @mock.patch("app.emit_all_messages")
    @mock.patch("app.add_new_connected_user")
    @mock.patch("app.id_token.verify_oauth2_token")
    def test_on_new_google_user(
        self,
        mocked_google_verify_token,
        mocked_add_new_connected_user,
        mocked_emit_all_messages,
        mocked_user_authenticated,
    ):
        mocker = mock.MagicMock()
        mocker.sid = "12345"
        with mock.patch("app.flask.request",mocker):
            for test_case in self.on_new_google_user_success:
                input = test_case[KEY_INPUT]
                expected = test_case[KEY_EXPECTED]
                mocked_google_verify_token.return_value = {
                    "sub": "1111",
                    KEY_NAME: "akashpatel",
                    KEY_EMAIL: "akashpatel@gmail.com",
                    "picture": "https://profileURL.com",
                }
                on_new_google_user(input)
    
                mocked_add_new_connected_user.assert_called_with(
                    ADD_NEW_USER_CHANNEL,
                    mocker.sid,
                    expected[KEY_NAME],
                    expected[KEY_EMAIL],
                    AuthUserType.GOOGLE,
                    expected[KEY_PROFILE_URL],
                )
                mocked_emit_all_messages.called_once()
                mocked_user_authenticated.assert_called_with(
                    AUTHENTICATED_CHANNEL, True, expected[KEY_SOCKET_ID]
                )


if __name__ == "__main__":
    unittest.main()
