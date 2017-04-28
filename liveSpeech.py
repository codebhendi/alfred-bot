# import os
# from pocketsphinx import LiveSpeech

# model_path = "en-adapt"

# speech = LiveSpeech(
#     verbose=False,
#     sampling_rate=16000,
#     buffer_size=2048,
#     no_search=False,
#     full_utt=False,
#     hmm=os.path.join(model_path, 'en-us-alfred'),
#     lm=os.path.join(model_path, 'alfred.lm'),
#     dic=os.path.join(model_path, 'alfred.dict')
# )

# for phrase in speech:
#     print(phrase)

import os
from pocketsphinx import AudioFile, get_model_path, get_data_path

model_path = "en-adapt"
data_path = ""

config = {
    'verbose': False,
    'audio_file': os.path.join(data_path, "test10.wav"),
    'buffer_size': 2048,
    'no_search': False,
    'full_utt': False,
    'hmm': os.path.join(model_path, 'en-us'),
    'lm': os.path.join(model_path, 'alfred.lm'),
    'dict': os.path.join(model_path, 'alfred.dict')
}

audio = AudioFile(**config)
for phrase in audio:
    print(phrase)