# define bot
"""
    Bot replies define here
"""
import os
from os.path import join, dirname
import requests
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), "sql.env")
load_dotenv(dotenv_path)

OPEN_WEATHER_API_KEY = os.environ["OPEN_WEATHER_API_KEY"]

NAME = "sugerBot"
FUN_TRANSLATE_BASE_URL = "https://api.funtranslations.com/translate/chef.json?text="
OPEN_WEATHER_API_BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
PREDICT_AGE_BASED_ON_API = "https://api.agify.io?name={}&country_id=US"


def about():
    """
    simple about method that replies to !! about command
    """
    return (
        "I am <strong>%s</strong>, my job is to reply to message that have"
        " !! follow by available commands. To see the available "
        "commands: type <br>!! help" % NAME
    )


def help_command():
    """
    simple help method that replies to !! help command and informs available commands
    """
    return (
        "I recognize following commands and should be type exact for better conversation: "
        "<br>!! about "
        "<br>!! help "
        "<br>!! funtranslate {message} "
        "<br>!! weather {city name} "
        "<br>!! predict_age {name}"
    )


def funtranslate(message):
    """
        simple funtranslate method that replies to !!"\
        " funtranslate <message> command after making an API call
    """
    url = FUN_TRANSLATE_BASE_URL + message
    reply = requests.get(url)
    translated_message = reply.json()
    try:
        return translated_message["contents"]["translated"]
    except KeyError:
        return "Unable to translate your message '{}'.".format(message)


def weather(city):
    """
        simple weather method that replies to !!"\
        " weather <city> command after making API call to openweathermap open free API
    """
    url = (
        OPEN_WEATHER_API_BASE_URL
        + "q="
        + city
        + "&units=imperial&appid="
        + OPEN_WEATHER_API_KEY
    )
    response = requests.get(url)
    response = response.json()
    try:
        return str(response["main"]["temp"]) + " F"
    except KeyError:
        return "Maybe invalid city name. Try valid city name like jersey city or new york city"


def predict_age(name):
    """
        simple predict_age method that replies to !!"\
        " predict_age <age> command after fetching response from open source API
    """
    url = PREDICT_AGE_BASED_ON_API.format(name)
    response = requests.get(url)
    response = response.json()
    try:
        return "%s your predicted age is %d" % (name, response["age"])
    except KeyError:
        return "Try some other name than %s" % name
