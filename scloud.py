import os
import random
import soundcloud

# instantiate a soundcloud client
client = soundcloud.Client(client_id = os.environ.get("SOUNDCLOUD_CLIENT_ID"))

# get a random track by doc quan
def get_random_track():
	tracks = client.get('/tracks', genres='reggaeton')
	random_track = random.randint(0, (len(tracks) - 1))
	playtrack = tracks[random_track].permalink_url
	return playtrack

def get_tasty_groove():
	tracks = client.get('/tracks', genres='funk')
	random_track = random.randint(0, (len(tracks) - 1))
	playtrack = tracks[random_track].permalink_url
	return playtrack

# search for an artist and play a random track by them
def random_track_by_user_search(artist_name):
	# search for the artist name
	users = client.get('/users', q=artist_name)

	if len(users) != 0:
		#helper variables
		index = 0
		hasNoTracks = True
		#iterate over results til we find a user that has tracks
		while hasNoTracks:
			# find the current top result
			topresult = users[index]
			# get the users tracks
			tracks = client.get('/users/' + str(topresult.id) + '/tracks')
			# if the user has no tracks, increment the index
			if len(tracks) is None or len(tracks) == 0:
				index += 1
			else:
				hasNoTracks = False
		# choose a random track
		random_track = random.randint(0, (len(tracks) - 1))
		playtrack = tracks[random_track].permalink_url
		# send the track and the artists name
		return [str(playtrack), str(topresult.username)]
	else:
		return ["I'm terribly sorry, sir, but there seem to be no users with that name."]