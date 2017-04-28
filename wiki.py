import re
from urllib2 import Request, urlopen, URLError
import json

def handle(text, speaker):
    # method to get the wiki summary
    get_wiki(text, speaker)


def get_wiki(title, speaker):
    # get the user voice input as string
    # make a call to the Wikipedia API
    request = Request('https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro=&explaintext=&titles='+title)
    try:
        response = urlopen(request)
        data = json.load(response)
        # Parse the JSON to just get the extract. Always get the first summary.
        output = data["query"]["pages"]
        final = output[output.keys()[0]]["extract"]
        speaker.say(final)
    except URLError, e:
        speaker.say("Unable to reach dictionary API.")


def isValid(text):
    wiki= bool(re.search(r'\bWiki\b',text, re.IGNORECASE))
    # Add 'Wicky' because the STT engine recognizes it quite often
    wicky= bool(re.search(r'\bwicky\b',text, re.IGNORECASE))
    article= bool(re.search(r'\barticle\b',text, re.IGNORECASE))

    if wicky or wiki or article:
        return True
    else:
        return False

def check_command(data, speaker):
    if "check" in data :
        speaker.say("What would you like to learn about?")
        return True
    else :
        return False