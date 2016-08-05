import achewood
import bot_ability
import os
import random
import time
import scloud
from slackclient import SlackClient

### OOP rewrite of mrhandy slackbot

#starterbot's id as an environment variable
BOT_ID = os.environ.get("STARTER_BOT_ID")

#constants
AT_BOT = "<@" + BOT_ID + ">:"

#instantiate slack and twilio clients
slack_client = SlackClient(os.environ.get('STARTER_BOT_TOKEN'))

#list of available ability objects
ability_list = [bot_ability.Generator]

#empty dict of command names and their objects
command_dict = {'generate':bot_ability.Generator()}





def handle_command(command, channel):
	response = "I'm not sure what you mean, sir."
	for word in list(command_dict.keys()):
		if word in command:
			bot_function = command_dict.get(word)
			if all(keywords in command for keywords in bot_function.command_keywords):
				response = choose_polite_prefix() + ' ' + \
						   bot_function.initialize_action(command)
				break
	slack_client.api_call("chat.postMessage", channel=channel, text=response,
		as_user=True)


# Pick a polite prefix.
def choose_polite_prefix():
	prefix_list = open(os.path.join(
					   os.path.curdir, 'files', 'polite_prefixes.txt')) \
					   .readlines()
	return prefix_list[random.randint(0, len(prefix_list) - 1)]


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