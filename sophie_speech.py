#!/usr/bin/env python

from pocketsphinx.pocketsphinx import *
from sphinxbase.sphinxbase import *

import os
import pyaudio
import wave
import audioop
from collections import deque
import time
import math
from light import Light
from song import Song
import speech_recognition as sr
import wiki
import speaker
"""
Written by Sophie Li, 2016
http://blog.justsophie.com/python-speech-to-text-with-pocketsphinx/
"""

class SpeechDetector:
    def __init__(self):
        # Microphone stream config.
        self.CHUNK = 1024  # CHUNKS of bytes to read each time from mic
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 16000

        self.SILENCE_LIMIT = 1  # Silence limit in seconds. The max ammount of seconds where
                           # only silence is recorded. When this time passes the
                           # recording finishes and the file is decoded

        self.PREV_AUDIO = 0.5  # Previous audio (in seconds) to prepend. When noise
                          # is detected, how much of previously recorded audio is
                          # prepended. This helps to prevent chopping the beginning
                          # of the phrase.

        self.THRESHOLD = 3500
        self.num_phrases = -1

        self.MODULES = ["light", "time", "alarm", "remind", "song", "article"]
        self.STATES = ["tell", "on", "off", "set", "unset", "play", "stop", "use"]
        self.light = Light()    
        self.song = Song()
        self.speaker = speaker.Speaker()
        # These will need to be modified according to where the pocketsphinx folder is
        MODELDIR = "en-adapt"

        # Create a decoder with certain model
        config = Decoder.default_config()
        config.set_string('-hmm', os.path.join(MODELDIR, 'en-us-adapt'))
        config.set_string('-lm', os.path.join(MODELDIR, 'alfred/alfred.lm'))
        config.set_string('-dict', os.path.join(MODELDIR, 'alfred/alfred.dic'))

        # Creaders decoder object for streaming data.
        self.decoder = Decoder(config)

    def setup_mic(self, num_samples=100):
        """ Gets average audio intensity of your mic sound. You can use it to get
            average intensities while you're talking and/or silent. The average
            is the avg of the .2 of the largest intensities recorded.
        """
        print "Getting intensity values from mic."
        p = pyaudio.PyAudio()
        stream = p.open(format=self.FORMAT, 
                        channels=self.CHANNELS,
                        rate=self.RATE, 
                        input=True, 
                        frames_per_buffer=self.CHUNK)

        values = [math.sqrt(abs(audioop.avg(stream.read(self.CHUNK), 4)))
                  for x in range(num_samples)]
        values = sorted(values, reverse=True)
        r = sum(values[:int(num_samples * 0.1)]) / int(num_samples * 0.1)
        print " Finished "
        print " Average audio intensity is ", r
        stream.close()
        p.terminate()

        if r < 5000:
            self.THRESHOLD = 5500
        else:
            self.THRESHOLD = r + 1000

    def save_speech(self, data, p):
        """
        Saves mic data to temporary WAV file. Returns filename of saved
        file
        """
        filename = 'output_'+str(int(time.time()))
        # writes data to WAV file
        data = ''.join(data)
        wf = wave.open(filename + '.wav', 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(self.RATE)  # TODO make this value a function parameter?
        wf.writeframes(data)
        wf.close()
        return filename + '.wav'

    def google_decode(self, filename):
        r = sr.Recognizer()

        with sr.AudioFile(filename) as source:
            audio = r.record(source)

        try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
            text_from_speech = r.recognize_google(audio)
            print("Google Speech Recognition thinks you said " + text_from_speech)
            return text_from_speech
            #process_text(text_from_speech)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
        return None

    def mic_listen(self):
        """
        Listens to Microphone, extracts phrases from it and calls pocketsphinx
        to decode the sound
        """
        #self.setup_mic()

        #Open stream
        print(1)
        p = pyaudio.PyAudio()
        stream = p.open(format=self.FORMAT, 
                        channels=self.CHANNELS, 
                        rate=self.RATE, 
                        input=True, 
                        frames_per_buffer=self.CHUNK)
        print "* Mic set up and listening. "

        audio2send = []
        cur_data = ''  # current chunk of audio data
        rel = self.RATE/self.CHUNK
        slid_win = deque(maxlen=self.SILENCE_LIMIT * rel)
        #Prepend audio from 0.5 seconds before noise was detected
        prev_audio = deque(maxlen=self.PREV_AUDIO * rel)
        started = False

        while True:
            cur_data = stream.read(self.CHUNK)
            slid_win.append(math.sqrt(abs(audioop.avg(cur_data, 4))))
            if sum([x > self.THRESHOLD for x in slid_win]) > 0:
                if started == False:
                    print "Tell what you want to search"
                    started = True
                audio2send.append(cur_data)

            elif started:
                print "Finished recording, decoding phras"
                filename = self.save_speech(list(prev_audio) + audio2send, p)
                r = self.google_decode(filename)
                
                os.remove(filename)
                
                stream.close()
                p.terminate()
                
                return r

            else:
                prev_audio.append(cur_data)

    def decode_phrase(self, wav_file):
        self.decoder.start_utt()
        stream = open(wav_file, "rb")
        while True:
          buf = stream.read(1024)
          if buf:
            self.decoder.process_raw(buf, False, False)
          else:
            break
        self.decoder.end_utt()
        words = []
        [words.append(seg.word) for seg in self.decoder.seg()]
        return words

    def remove_element(self, obj, array):
        pos = array.index(obj)
        array.pop(pos)

    def clean_transcribed_data(self, data) :
        new_data = []
        for tag in data:
            if tag == "<sil>":
                continue

            elif tag == "<s>":
                continue

            elif tag == "[SPEECH]":
                continue

            elif tag == "</s>":
                continue

            elif tag == "[NOISE]":
                continue

            else:
                new_data.insert(len(new_data), tag)

        for tag in new_data:
            start_pos = tag.find("(")

            if start_pos == -1:
                continue

            pos = new_data.index(tag)
            tag = tag[:-3]
            new_data[pos] = tag

        for word in new_data:
            temp = word
            word = word.lower()
            pos = new_data.index(temp)

            new_data[pos] = word

        return new_data

    def load_module(self, tag, data):
        print(tag)
        if tag == "light":
            self.light.check_command(data)
        elif tag == "song":
            self.song.check_command(data)
        elif tag == "article":
            val = wiki.check_command(data, self.speaker)
            if val == True:
                r = self.mic_listen()
                if r == None :
                    self.speaker.say("repeat the query")
                    return 
                wiki.handle(r, self.speaker)


    def check_for_modules(self, data):
        modules = self.MODULES

        for tag in data:
            if tag in modules:
                self.load_module(tag, data)

    def key_phrase_checker(self, data):
        data = self.clean_transcribed_data(data)
        print(data)

        if "alfred" in data :
            self.remove_element("alfred", data)
            self.check_for_modules(data)

    def run(self):
        """
        Listens to Microphone, extracts phrases from it and calls pocketsphinx
        to decode the sound
        """
        self.setup_mic()

        #Open stream
        p = pyaudio.PyAudio()
        stream = p.open(format=self.FORMAT, 
                        channels=self.CHANNELS, 
                        rate=self.RATE, 
                        input=True, 
                        frames_per_buffer=self.CHUNK)
        print "* Mic set up and listening. "

        audio2send = []
        cur_data = ''  # current chunk of audio data
        rel = self.RATE/self.CHUNK
        slid_win = deque(maxlen=self.SILENCE_LIMIT * rel)
        #Prepend audio from 0.5 seconds before noise was detected
        prev_audio = deque(maxlen=self.PREV_AUDIO * rel)
        started = False

        while True:
            cur_data = stream.read(self.CHUNK)
            slid_win.append(math.sqrt(abs(audioop.avg(cur_data, 4))))
            if sum([x > self.THRESHOLD for x in slid_win]) > 0:
                if started == False:
                    print "Starting recording of phrase"
                    started = True
                audio2send.append(cur_data)

            elif started:
                print "Finished recording, decoding phrase"
                filename = self.save_speech(list(prev_audio) + audio2send, p)
                r = self.decode_phrase(filename)

                self.key_phrase_checker(r)

                # Removes temp audio file
                os.remove(filename)
                # Reset all
                started = False
                slid_win = deque(maxlen=self.SILENCE_LIMIT * rel)
                prev_audio = deque(maxlen=0.5 * rel)
                audio2send = []
                print "Listening ..."

            else:
                prev_audio.append(cur_data)

        print "* Done listening"
        stream.close()
        p.terminate()

if __name__ == "__main__":
    sd = SpeechDetector()
    sd.run()