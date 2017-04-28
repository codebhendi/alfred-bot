import pyaudio
import wave
import time
import tempfile
import audioop

from os import environ, path
import pocketsphinx as ps
from sphinxbase.sphinxbase import *

def init() :

    modeldir = "en-adapt"

    config = ps.Decoder.default_config();

    config.set_string('-hmm', path.join(modeldir, 'en-us-alfred/'))
    config.set_string('-lm', path.join(modeldir, 'alfred.lm'))
    config.set_string('-dict', path.join(modeldir, 'alfred.dict'))
    
    decoder = ps.Decoder(config)

    audio = pyaudio.PyAudio();

    activeListen(audio, decoder, THRESHOLD=None)

def getScore(data):
    rms = audioop.rms(data, 2)
    score = rms / 3
    return score


def fetchThreshold(audio):
    # TODO: Consolidate variables from the next three functions
    THRESHOLD_MULTIPLIER = 1.8
    RATE = 16000
    CHUNK = 1024

    # number of seconds to allow to establish threshold
    THRESHOLD_TIME = 1

    # prepare recording stream
    stream = audio.open(format=pyaudio.paInt16,
                              channels=1,
                              rate=RATE,
                              input=True,
                              frames_per_buffer=CHUNK)

    # stores the audio data
    frames = []

    # stores the lastN score values
    lastN = [i for i in range(20)]

    # calculate the long run average, and thereby the proper threshold
    for i in range(0, RATE / CHUNK * THRESHOLD_TIME):

        data = stream.read(CHUNK)
        frames.append(data)

        # save this data point as a score
        lastN.pop(0)
        lastN.append(getScore(data))
        average = sum(lastN) / len(lastN)

    stream.stop_stream()
    stream.close()

    # this will be the benchmark to cause a disturbance over!
    THRESHOLD = average * THRESHOLD_MULTIPLIER

    print(THRESHOLD)
    return THRESHOLD

def transcribe(fp, decoder):
    """
    Performs STT, transcribing an audio file and returning the result.

    Arguments:
        fp -- a file object containing audio data
    """

    fp.seek(44)

    # FIXME: Can't use the Decoder.decode_raw() here, because
    # pocketsphinx segfaults with tempfile.SpooledTemporaryFile()
    data = fp.read()
    decoder.start_utt()
    decoder.process_raw(data, False, True)
    decoder.end_utt()

    result = decoder.hyp()


    transcribed = [result]
    print(transcribed[0])
    return transcribed

def activeListen(audio, decoder, THRESHOLD):
    RATE = 16000
    CHUNK = 1024
    LISTEN_TIME = 12

    # check if no threshold provided
    if THRESHOLD is None:
        THRESHOLD = fetchThreshold(audio)

    # self.speaker.play(jasperpath.data('audio', 'beep_hi.wav'))

    # prepare recording stream
    stream = audio.open(format=pyaudio.paInt16,
                              channels=1,
                              rate=RATE,
                              input=True,
                              frames_per_buffer=CHUNK)

    frames = []
    # increasing the range # results in longer pause after command
    # generation
    lastN = [THRESHOLD * 1.2 for i in range(30)]

    for i in range(0, RATE / CHUNK * LISTEN_TIME):

        data = stream.read(CHUNK)
        frames.append(data)
        score = getScore(data)

        lastN.pop(0)
        lastN.append(score)

        average = sum(lastN) / float(len(lastN))

        # TODO: 0.8 should not be a MAGIC NUMBER!
        if average < THRESHOLD * 0.8:
            break

    # self.speaker.play(jasperpath.data('audio', 'beep_lo.wav'))

    # save the audio data
    stream.stop_stream()
    stream.close()

    with tempfile.SpooledTemporaryFile(mode='w+b') as f:
        wav_fp = wave.open(f, 'wb')
        wav_fp.setnchannels(1)
        wav_fp.setsampwidth(pyaudio.get_sample_size(pyaudio.paInt16))
        wav_fp.setframerate(RATE)
        wav_fp.writeframes(''.join(frames))
        wav_fp.close()
        f.seek(0)
        transcribe(f, decoder)

init()