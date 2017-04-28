import pyttsx
from gtts import gTTS
import vlc
import time
import wave
import contextlib

class Mic:
    def __init__(self):
        self.engine = pyttsx.init()

    def say(self, text_to_say):
        self.engine(text_to_say)
        self.engine.runAndWait()

    def stop(self):
        self.engine.stop()

    def check_runtime(self, fname):
        with contextlib.closing(wave.open(fname,'r')) as f:
            frames = f.getnframes()
            rate = f.getframerate()
            duration = frames / float(rate)
            return duration

    def google_say(self, text_to_say, fname="1.mp3"):

        tts = gTTS(text=text_to_say, lang="en")
        tts.save(fname)

        runtime = self.check_runtime(fname)
        self.player = vlc.MediaPlayer(fname)
        self.player.play()

        time.sleep(runtime)

        self.player.stop()
        os.remove(fname)