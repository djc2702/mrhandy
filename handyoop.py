import inspect
import bot_ability
import os
import random
import time
from slackclient import SlackClient

### OOP rewrite of mrhandy slackbot

#starterbot's id as an environment variable
BOT_ID = os.environ.get("STARTER_BOT_ID")

#constants
AT_BOT = "<@" + BOT_ID + ">:"

#instantiate slack and twilio clients
slack_client = SlackClient(os.environ.get('STARTER_BOT_TOKEN'))

#list of available ability objects, received using reflection to inspect
# the bot_ability module for classes
ability_list = [x[1] for x in inspect.getmembers(bot_ability, inspect.isclass)]

#empty dict of command names and their objects
command_dict = {}

#populate the dictionary with the ability names and their instances
for ability in ability_list:
	command_dict[ability.command_name] = ability()


def handle_command(command, channel):
	response = "I'm not sure what you mean, sir."
	# for every word in the command list... 
	for word in list(command_dict.keys()):
		if word in command.lower():
			bot_function = command_dict.get(word)
			# get the response by calling the relevant bot function's 
			# 'initialize action' method
			response = bot_function.initialize_action(command)
			break
	# check for m8 status
	if 'm8' in command:
		response = response.replace('sir', 'm8').replace('you', 'u').replace('too', '2').replace('right', 'rite')
	# Post the message using the client api
	slack_client.api_call("chat.postMessage", channel=channel, text=response,
		as_user=True)

# getter method for the bot_ability module
def get_slack_client():
	return slack_client


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
				return output['text'].split(AT_BOT)[1].strip(), \
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