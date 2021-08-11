import numpy as np 
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

import config
import json_to_midi
from visualize_segments import visualize_segments

# spotify API python client
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=config.CLIENT_ID,client_secret=config.CLIENT_SECRET))

TRAVIS = '0Y5tJX1MQlPlqiwlOH1tJY'
GATTI = '40mjsnRjCpycdUw3xhS20g'
BACH = '4srKxNDkB0veyOkXDw7KoF'
OPUS ='3v2oAQomhOcYCPPHafS3KV'
BACH_B = '2B6a59WZSJ5oIUrIWfnkhT'
MAX = '54Hw7R909mkcRNpqW2VnaD'

analysis = sp.audio_analysis(OPUS)
segments = analysis['segments']
json_to_midi.convert(analysis, 'opus 2021 b')

#visualize_segments(segments, 'Opus')