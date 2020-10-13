# define bot
import requests

NAME = "sugerBot"
BASE_URL = "https://api.funtranslations.com/translate/asian-accent.json?text={}"

def about():
    return "I am %s, my job is to reply to message that have !! follow by available commands. To see the available \
        commands: tppe !! help" % NAME

def help():
    return "I recognize following commands and should be type exact PLEASE: \
        !! about or !! help or !! funtranslate <message>"
def funtranslate(message):
    payload = {'text':message}
    reply = requests.post("https://api.funtranslations.com/translate/asian-accent.json?text=%s", data=payload)
    translated_message  = reply.json()
    try: 
        return translated_message['contents']['translated']
    except KeyError:
        return "Unable to translate your message \'{}\'.".format(message)
    