from hackernews import HackerNews
from urllib2 import urlopen, URLError
import time


def internet_on():
    try:
        urlopen('http://216.58.192.142', timeout=4)
        return True
    except URLError as err: 
        return False

class HN:
    def __init__(self, speaker):
        self.speaker = speaker
        self.hn = HackerNews()

    def get_top_stories(self):
        ids = self.hn.top_stories(limit=10)

        for id in ids:
            item = self.hn.get_item(id)
            print(item.title)
            self.speaker.say(item.title)

            #time.sleep(5)

    def check_command(self, data):
        if "news" in data:
            if internet_on() == False:
                self.speaker.say("no internet connection try later")
                return false

            if "check" in data:
                self.get_top_stories()