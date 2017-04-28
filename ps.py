from os import environ, path
from pocketsphinx.pocketsphinx import *
from sphinxbase.sphinxbase import *

modeldir = ""

config = Decoder.default_config()
config.set_string('-hmm', path.join(modeldir, 'en-adapt/en-us'))
config.set_string('-lm', path.join(modeldir, 'en-adapt/en-us.lm.bin'))
config.set_string('-dict', path.join(modeldir, 'en-adapt/cmudict-en-us.dict'))
decoder = Decoder(config)
decoder.start_utt()
stream = open(path.join("", '1.wav'), 'rb')

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