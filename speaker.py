import talkey
from gtts import gTTS
import vlc
import time
import wave
import contextlib

class Speaker:
    def __init__(self):
        self.engine =talkey.Talkey()

    def say(self, text_to_say):
        self.engine.say(text_to_say)

    def google_say(self, text_to_say, fname="1.mp3"):

        tts = gTTS(text=text_to_say, lang="en")
        tts.save(fname)

        self.player = vlc.MediaPlayer(fname)
        self.player.play()

        self.player.stop()
        os.remove(fname)
