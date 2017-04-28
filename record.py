import pyaudio
import wave
import time

from os import environ, path
from pocketsphinx.pocketsphinx import *
from sphinxbase.sphinxbase import *


def speech_proces(path_file):
    modeldir = "en-adapt"

    config = Decoder.default_config()

    config.set_string('-hmm', path.join(modeldir, 'en-us-adapt'))
    config.set_string('-lm', path.join(modeldir, 'alfred.lm'))
    config.set_string('-dict', path.join(modeldir, 'alfred.dict'))
    decoder = Decoder(config)
    decoder.start_utt()
    stream = open(path.join("", path_file), 'rb')

    while True:
      buf = stream.read(4096)
      if buf:
        decoder.process_raw(buf, False, False)
      else:
        break
    decoder.end_utt()

    hypothesis = decoder.hyp()
    print ('Best hypothesis: ', hypothesis.hypstr, " model score: ", hypothesis.best_score, " confidence: ", hypothesis.prob)
    print ('Best hypothesis segments: ', [seg.word for seg in decoder.seg()])


CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
RECORD_SECONDS = 3
WAVE_OUTPUT_FILENAME = ".wav"
count = 10;
modeldir = "time_train"

while (count > 0):
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* recording")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    file_name = str(count) + WAVE_OUTPUT_FILENAME
    wf = wave.open(path.join("modeldir", file_name), 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    speech_proces(file_name)
    count -= 1
    time.sleep(5)