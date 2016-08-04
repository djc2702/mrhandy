import os
import random
import soundcloud


client = soundcloud.Client(client_id = os.environ.get("SOUNDCLOUD_CLIENT_ID"))

def get_random_quandary_track():
	tracks = client.get('/users/187896/tracks')
	playtrack = tracks[1].permalink_url
	random_track = random.randint(0, (len(tracks) - 1))
	playtrack = tracks[random_track].permalink_url
	return playtrack