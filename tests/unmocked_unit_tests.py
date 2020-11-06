"""
    app.py and bot.py 
    
    This file tests unmocked unit tests from app, models, and bot
"""

import sys
import os
import datetime
import unittest.mock as mock
from os.path import dirname, join

# pylint: disable=C0413
sys.path.append(join(dirname(__file__), "../"))
import unittest
from app import check_for_bot_command, check_for_valid_url
from bot import NAME
from models import Messages, MessageType, Connected_users, AuthUserType

KEY_INPUT = "input"
KEY_EXPECTED = "expected"
KEY_NAME = "name"
KEY_MESSAGE = "message"
KEY_MESSAGE_TYPE = "message_type"
KEY_DATE = "created_at"
KEY_SOCKET_ID = "sid"
KEY_EMAIL = "email"
KEY_PROFILE_URL = "profile_url"
KEY_AUTH_TYPE = "auth_type"


class Unmocked_unit_tests(unittest.TestCase):
    '''
        test all function that doesn't required any
        part of it to be mocked for response 
    '''
    def setUp(self):
        '''
            setup before test functions are called that why its called setup
        '''
        self.check_about_bot_command = [
            {
                KEY_INPUT: "!! about",
                KEY_EXPECTED: "I am <strong>{}</strong>, my job is to reply to message that have !! follow by available commands. "
                "To see the available commands: type <br>!! help".format(NAME),
            }
        ]
        self.check_edge_case_for_about_bot_command = [
            {
                KEY_INPUT: "!! something about",
                KEY_EXPECTED: "I am <strong>{}</strong>, my job is to reply to message that have !! follow by available commands. "
                "To see the available commands: type <br>!! help".format(NAME),
            }
        ]
        self.check_help_bot_command = [
            {
                KEY_INPUT: "!! help",
                KEY_EXPECTED: "I recognize following commands and should be type exact for better conversation: "
                "<br>!! about "
                "<br>!! help "
                "<br>!! funtranslate {message} "
                "<br>!! weather {city name} "
                "<br>!! predict_age {name}",
            }
        ]
        self.check_edge_case_for_help_bot_command = [
            {
                KEY_INPUT: "!! help",
                KEY_EXPECTED: "I recognize following commands and should be type exact for better conversation: "
                "<br>!! about "
                "<br>!! help "
                "<br>!! funtranslate {message} "
                "<br>!! weather {city name} "
                "<br>!! predict_age {name}",
            }
        ]
        self.check_bot_command_failure = [
            {
                KEY_INPUT: "!! unknown",
                KEY_EXPECTED: "Unrecognized command. Please use !! help to see available commands.",
            },
            {
                KEY_INPUT: "!! corona cases",
                KEY_EXPECTED: "Unrecognized command. Please use !! help to see available commands.",
            },
        ]
        self.check_for_valid_url_success = [
            {KEY_INPUT: "http://google.com", KEY_EXPECTED: True},
            {KEY_INPUT: "http:google.com", KEY_EXPECTED: True},
        ]
        self.check_for_valid_url_failure = [
            {KEY_INPUT: "www.google.com", KEY_EXPECTED: ValueError}
        ]
        self.check_models_Messages_init_success = [
            {
                KEY_EXPECTED: {
                    KEY_NAME: "akash",
                    KEY_MESSAGE: "testing message",
                    KEY_MESSAGE_TYPE: MessageType.TEXT_MESSAGE,
                    KEY_DATE: datetime.datetime.now(),
                }
            }
        ]
        self.check_models_Messages_repr_success = [
            {KEY_EXPECTED: "<message: {} by {}>"}
        ]
        self.check_models_Connected_users_init_success = [
            {
                KEY_EXPECTED: {
                    KEY_NAME: "akash",
                    KEY_EMAIL: "akash@gmail.com",
                    KEY_SOCKET_ID: "12345",
                    KEY_AUTH_TYPE: AuthUserType.FACEBOOK,
                    KEY_PROFILE_URL: "htts://profileULR.com",
                }
            }
        ]
        self.message_object = Messages(
            "akash",
            "testing message",
            MessageType.TEXT_MESSAGE,
            datetime.datetime.now(),
        )
        self.connected_user_object = Connected_users(
            "12345",
            AuthUserType.FACEBOOK,
            "akash",
            "akash@gmail.com",
            "https://profileURL.com",
        )

    def test_check_about_bot_command_success(self):
        '''
            test !! about command of bot
        '''
        for test_case in self.check_about_bot_command:
            response = check_for_bot_command(test_case[KEY_INPUT])
            expected = test_case[KEY_EXPECTED]

            self.assertEqual(response, expected)

    def test_edge_case_about_bot_command_success(self):
        '''
            check if !! something about still works that same 
            as !! about
        '''
        for test_case in self.check_edge_case_for_about_bot_command:
            response = check_for_bot_command(test_case[KEY_INPUT])
            expected = test_case[KEY_EXPECTED]

            self.assertEqual(response, expected)

    def test_check_help_bot_command_success(self):
        '''
            check !! help command 
        '''
        for test_case in self.check_help_bot_command:
            response = check_for_bot_command(test_case[KEY_INPUT])
            expected = test_case[KEY_EXPECTED]

            self.assertEqual(response, expected)

    def test_edge_case_help_bot_command_success(self):
        '''
            check !! something help command 
            and works same as !! help
        '''
        for test_case in self.check_edge_case_for_help_bot_command:
            response = check_for_bot_command(test_case[KEY_INPUT])
            expected = test_case[KEY_EXPECTED]

            self.assertEqual(response, expected)

    def test_check_bot_command_failure(self):
        '''
            check command that are not expected 
            such as !! not known command or !! hi
        '''
        for test_case in self.check_bot_command_failure:
            response = check_for_bot_command(test_case[KEY_INPUT])
            expected = test_case[KEY_EXPECTED]

            self.assertEqual(response, expected)

    def test_check_for_valid_url(self):
        '''
            test that valid url indentifies 
            an url to be a URL and also
            check when it raises an exception
        '''
        for test_case in self.check_for_valid_url_success:
            response = check_for_valid_url(test_case[KEY_INPUT])
            expected = test_case[KEY_EXPECTED]

            self.assertEqual(response, expected)

        with self.assertRaises(Exception) as context:
            response = check_for_valid_url(
                self.check_for_valid_url_failure[0][KEY_INPUT]
            )
            expected = self.check_for_valid_url_failure[0][KEY_EXPECTED]
            self.assertTrue(expected in str(context.exception))
            self.assertNotEqual(response, expected)

    def test_models_Messages_init(self):
        ''' 
            test models Messages constructor for correctness
        '''
        expected = self.check_models_Messages_init_success[0][KEY_EXPECTED]
        message_object = self.message_object
        self.assertEqual(expected[KEY_NAME], message_object.username)
        self.assertEqual(expected[KEY_MESSAGE], message_object.message)
        self.assertEqual(expected[KEY_MESSAGE_TYPE].value, message_object.message_type)

    def test_models_Messages_repr(self):
        '''
            check models Messages method that
            represents the object
        '''
        self.assertEqual(
            self.check_models_Messages_repr_success[0][KEY_EXPECTED].format(
                "testing message", "akash"
            ),
            self.message_object.__repr__(),
        )

    def test_models_Connected_users_init(self):
        '''
            test Connected_users constructor
        '''
        expected = self.check_models_Connected_users_init_success[0][KEY_EXPECTED]
        connected_user_object = self.connected_user_object
        self.assertEqual(expected[KEY_NAME], connected_user_object.name)
        self.assertEqual(expected[KEY_EMAIL], connected_user_object.email)
        self.assertEqual(expected[KEY_AUTH_TYPE].value, connected_user_object.auth_type)

    def test_models_Connected_users_repr(self):
        '''
            test method that represents the object
        '''
        self.assertEqual(
            "<Connected_users: {} has {}>".format("12345", "akash"),
            self.connected_user_object.__repr__(),
        )


if __name__ == "__main__":
    unittest.main()
