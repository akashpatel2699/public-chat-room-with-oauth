# define bot
import requests
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), 'sql.env')
load_dotenv(dotenv_path)

OPEN_WEATHER_API_KEY = os.environ['OPEN_WEATHER_API_KEY']

NAME = "sugerBot"
FUN_TRANSLATE_BASE_URL = "https://api.funtranslations.com/translate/chef.json?text="
OPEN_WEATHER_API_BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
PREDICT_AGE_BASED_ON_API = "https://api.agify.io?name={}&country_id=US"

def about():
    return "I am <strong>%s</strong>, my job is to reply to message that have !! follow by available commands. To see the available \
        commands: type <br>!! help" % NAME

def help():
    return "I recognize following commands and should be type exact for better conversation: \
    <br>!! about \
    <br>!! help \
    <br>!! funtranslate {message} \
    <br>!! weather {city name} \
    <br>!! predict_age {name}"
def funtranslate(message):
    URL = FUN_TRANSLATE_BASE_URL+ message
    reply = requests.get(URL)
    translated_message  = reply.json()
    print(translated_message)
    try: 
        return translated_message['contents']['translated']
    except KeyError:
        return "Unable to translate your message \'{}\'.".format(message)
def weather(city):
    URL = OPEN_WEATHER_API_BASE_URL + "q=" + city + "&units=imperial&appid=" + OPEN_WEATHER_API_KEY
    response  = requests.get(URL) 
    response = response.json()
    try:
        return str(response['main']['temp']) + ' F'
    except KeyError:
        return 'Maybe invalid city name. Try valid city name like jersey city or new york city'

def predict_age(name):
    URL = PREDICT_AGE_BASED_ON_API.format(name)
    response = requests.get(URL)
    response = response.json()
    try:
        return "%s your predicted age is %d" % (name,response['age'])
    except KeyError: 
        return "Try some other name than %s" %name