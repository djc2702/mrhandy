import bot_ability
import mrhandy
import inspect
import lxml.html
import os
import random
import re
import soundcloud
import urllib.request
from urllib.parse import quote


##### TO DO
### - full width mode
### - kick it with a dope verse / drop fire bars
### - certified hot flames / hot fire


# instantiate a soundcloud client
client = soundcloud.Client(client_id = os.environ.get("SOUNDCLOUD_CLIENT_ID"))

#get the slack client from the main bot module
slack_client = mrhandy.get_slack_client()


class ComicPost():

	#change this once we have more comics, if ever
	command_name = 'achewood'
	command_keywords = ['achewood']
	command_helptext = '`Achewood:` Post a random Achewood strip, or '\
								'search for strip containing "dialog in quotes."'
	command_manpage = "To be implemented later."
	
	def initialize_action(self, command):
		if '"' not in command:
			response = self.get_achewood()
		elif '"' in command:
			response = self.get_achewood(command[command.find('"'):command.rfind('"')])
		return bot_ability.choose_polite_prefix() + ' ' + response

	def get_achewood(self, *arg):
		# If no search argument is supplied, grab a random strip using urllib and lxml
		if len(arg) == 0:
			page = urllib.request.urlopen('http://www.ohnorobot.com/random.pl?comic=636')
			doc = lxml.html.parse(page)
			imgurl = doc.xpath('//img/@src')
			return 'http://www.achewood.com' + imgurl[1]
		else:
			# if there's a search term, first turn it into a searchable string
			search = ' '.join(arg)
			search = search.replace('"', '')
			search = quote(search)
			# run the search with ohnorobot
			searchpage = urllib.request.urlopen('http://www.ohnorobot.com/index.php?s=' \
				+ search + '&Search=Search&comic=636')
			doc = lxml.html.parse(searchpage).getroot()
			# get the links from the results page
			links = doc.xpath('//a/@href')
			# if there're no results, say so
			if 'letsbefriends.php' in links[2]:
				return "No strip containing that dialog was found, sir. My apologies."
			else:
				# otherwise return the best result
				best_result = links[2]
				page = urllib.request.urlopen(best_result)
				doc = lxml.html.parse(page)
				imgurl = doc.xpath('//img/@src')
				return 'http://www.achewood.com' + imgurl[1]


class DiceRoller():
	command_name = 'roll'
	command_keywords = ['roll']
	command_helptext = '`Roll:` Use `Roll XdY` to roll dice, where X is the number' \
					   "of dice and Y is the type of dice, e.g. `roll 2d10`."
	command_manpage = "To be implemented later."

	def initialize_action(self, command):
		#  a list of the digit groups in the command using a regular expression
		digits = re.findall("[0-9]{1,3}", command)
		# break the list down into number of dice...
		dice_no = digits[0]
		# and the type (ie sides) of the dice
		dice_type = digits[1]
		response = "Rolling " + dice_no + "d" + dice_type + ": "
		result_list = []
		# for number of dice to roll...
		for i in range(int(dice_no)):
			# roll the y-sided die
			roll = random.randint(1, int(dice_type))
			# append it to the result list for summing the total
			result_list.append(roll)
			# append it to the response string
			response += str(roll)
			# as long as it's not the last die being rolled, also append a comma
			if  i != int(dice_no) - 1:
				response += ", "
		# return the response and the total
		return bot_ability.choose_polite_prefix() + \
			   response + " = " + str(sum(result_list))
 

## Class for the generator bot function
class Generator():

	command_name = 'generate'
	command_keywords = ['generate']
	command_helptext = "`Generate code phrases:` use the " \
								"keywords `generate` and `code` to generate " \
								"top-secret code phrases. *TO DO:* expand to generate " \
								"names, etc."
	command_manpage = "To be implemented later."

	def initialize_action(self, command):
		
		codephrase = self.generate_codephrase()
		return bot_ability.choose_polite_prefix() + ' ' + \
			   "Your code phrase is " + codephrase + "."

	# Generate codephrase.
	def generate_codephrase(self):
	####TO DO - multiple codephrases at once, fix magic numbers
		
		#flip a coin to see if we're making two- or three-word code phrases
		
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


# Class for the help display function
class HelpDisplay():

	command_name = 'help'
	command_keywords = ['help']
	command_helptext = "`Help:` Displays information on available commands."
	command_manpage = "To be implemented later."

	def initialize_action(self, command):
		# use reflection to get list of classes in this module
		ability_objects = [x[1] for x in inspect.getmembers(bot_ability, inspect.isclass)]
		response = []
		# for each item, add its helptext to the response
		for item in ability_objects:
			response.append(item.command_helptext)
		response = sorted(response)
		return '\n'.join(response)


class NerdAlert():

	command_name = 'nerd'
	command_keywords = ['who', 'the nerd']
	command_helptext = "`Who's the nerd:` Ask who the nerd currently is. " \
					   " *TO DO:* Build the Nerd Accumulator and SCoring Algorithm Response" \
					   " (N.A.S.C.A.R.)"

	def initialize_action(self, command):
		#basic who is the nerd support
		chance = random.randint(0,100)
		if chance >= 98:
			the_nerd = "Shaquille O'Neal is the nerd now, sir."
		else:
			users = list(slack_client.api_call("users.list").get('members'))
			the_nerd = users[random.randint(0, len(users) - 1)].get('real_name')
			if the_nerd == 'Mr. Handy':
				return "It would appear I am the nerd now, sir, although I must say "\
						"I'm not pleased with the notion."
			else:
				return the_nerd + " is the nerd now, sir."


class OminousMode():

	command_name = 'ominous'
	command_keywords = ['make', 'ominous']
	command_helptext = '`Make "text" ominous:` Make text very ominous.'
	command_manpage = 'To be implemented later.'

	def initialize_action(self, command):
		normal_text = command[command.find('"') + 1:command.rfind('"')]

		ominous_text = ""
		for c in normal_text:
			if c == ' ':
				ominous_text += "  "
			else:
				# Get the full-width unicode text equivalent of the character
				ominous_text += chr(0xFEE0 + ord(c))
		return ominous_text


# Class for the soundcloud music retriever
class SoundCloud():

	##need to make this better
	command_name = 'kick it'
	command_keywords = ['kick it']
	command_helptext = "`Kick it:` Kick it with a tasty groove. "\
						"*TO DO:* Make... better. "
	command_manpage = 'To be implemented later.'

	def initialize_action(self, command):
		tracks = client.get('/playlists/46223708/tracks')
		random_track = random.randint(0, (len(tracks) - 1))
		playtrack = tracks[random_track].permalink_url
		return bot_ability.choose_polite_prefix() + ' ' + playtrack


# Pick a polite prefix.
def choose_polite_prefix():
	prefix_list = open(os.path.join(
					   os.path.curdir, 'files', 'polite_prefixes.txt')) \
					   .readlines()
	return prefix_list[random.randint(0, len(prefix_list) - 1)]