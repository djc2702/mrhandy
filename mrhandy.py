import achewood
import os
import random
import time
import scloud
from slackclient import SlackClient

### TO DO
### Use dictionaries to hold commands, and for help/instructions
### full width mode
### kick it with a dope verse / drop fire bars
### say who the nerd is

#starterbot's id as an environment variable
BOT_ID = os.environ.get("STARTER_BOT_ID")

#constants
AT_BOT = "<@" + BOT_ID + ">:"
AT_BOT_COLON = "<@" + BOT_ID + ">:"
GENERATE_COMMAND = "generate"
SOUNDCLOUD_COMMAND = "play"


#instantiate slack and twilio clients
slack_client = SlackClient(os.environ.get('STARTER_BOT_TOKEN'))


def handle_command(command, channel):
	"""
		Receives command directed at the bot and determines if they 
		are valid commands. If so, then acts on the commands. 
		If not, returns back what it needs for clarification.
	"""
	response = "I'm not sure what you mean, sir."
	if 'code word' in command or 'codeword' in command:
		#generate a secret code phrase
		codeword = generate_code_words()
		prefix = choose_polite_prefix()
		response = prefix + " Your code word is " + codeword \
					+ "."
	elif 'achewood' in command and '"' not in command:
		response = choose_polite_prefix() + '\n' \
		+ achewood.get_achewood()
	elif 'achewood' in command and '"' in command:
		response = choose_polite_prefix() + '\n' \
		+ achewood.get_achewood(command[command.find('"'):command.rfind('"')])
	elif 'down with the sickness' in command:
		response = "Ooh wa ah ah ah, sir."
	elif SOUNDCLOUD_COMMAND in command and 'by' in command:
		# 
		artist_query = command[command.find('"') + 1:command.rfind('"')]
		# run the search method
		result = scloud.random_track_by_user_search(artist_query)
		if len(result) > 1:
			# get the artist's name
			artist = result[1] 
			# get the track url
			trackurl = result[0] 
			# set the response
			response = choose_polite_prefix() + ' Playing a song by ' + \
			artist + '. \n' + trackurl
		else:
			response = result[0]
	elif SOUNDCLOUD_COMMAND in command and 'by' not in command:
		# get a random track 
		trackurl = scloud.get_random_track()
		response = choose_polite_prefix() + '\n' + trackurl
	elif 'kick it' in command:
		trackurl = scloud.get_tasty_groove()
		response = "I shall kick it with a tasty groove, sir. " + '\n' + trackurl
	if 'm8' in command:
		response = response.replace('sir', 'm8').replace('you', 'u').replace('too', '2').replace('right', 'rite')
	slack_client.api_call("chat.postMessage", channel=channel, text=response,
		as_user=True)	



def parse_slack_output(slack_rtm_output):
	"""
		The Slack real time messaging api is an events firehose.
		this parsing function returns None unless a message is 
		directed at the Bot, based on its ID.
	"""
	output_list = slack_rtm_output
	if output_list and len(output_list) > 0:
		for output in output_list:
			if output and 'text' in output and AT_BOT in output['text']:
				#return text after the @ mention, whitespace removed
				return output['text'].split(AT_BOT)[1].strip().lower(), \
					   output['channel']
	return None, None



# Pick a polite prefix.
def choose_polite_prefix():
	prefix_list = open(os.path.join(
					   os.path.curdir, 'files', 'polite_prefixes.txt')) \
					   .readlines()
	return prefix_list[random.randint(0, len(prefix_list) - 1)]



# Generate code words.
def generate_code_words():

	#flip a coin to see if we're making two- or three-word code phrases
	#to do - multiple codephrases at once, fix magic numbers
	coin = random.randint(0,1)

	# get the first list of code words, using system-agnostic path
	# delimiters
	list1 = open(os.path.join(os.path.curdir, 'files', 'code1.txt')) \
				.read().split()

	# pick a random word
	firstword = list1[random.randint(0,48)]

	#lather, rinse, repeat
	list2 = open(os.path.join(os.path.curdir, 'files', 'code2.txt')) \
				.read().split()

	secondword = list2[random.randint(0,52)]

	thirdword = list2[random.randint(0,52)]

	if coin == 0:
		return firstword + ' ' + secondword
	else:
		return firstword + ' ' + secondword + ' ' + thirdword


# the loop
if __name__ == "__main__":
	READ_WEBSOCKET_DELAY = 1 # one second delay between reading from firehose
	if slack_client.rtm_connect():
		print("Mr. Handy is connected and running!")
		while True:
			command, channel = parse_slack_output(slack_client.rtm_read())
			if command and channel:
				handle_command(command, channel)
			time.sleep(READ_WEBSOCKET_DELAY)
	else:
		print("Connection has failed. Invalid Slack token or bot ID?")

