import bot_ability
import inspect
import lxml.html
import os
import random
import soundcloud
import urllib.request
from urllib.parse import quote


##### TO DO
### - full width mode
### - kick it with a dope verse / drop fire bars
### - certified hot flames / hot fire


# instantiate a soundcloud client
client = soundcloud.Client(client_id = os.environ.get("SOUNDCLOUD_CLIENT_ID"))

class ComicPost():

	#change this once we have more comics, if ever
	command_name = 'achewood'
	command_keywords = ['achewood']
	command_helptext = '`Achewood:` Post a random Achewood strip, or '\
								'search for strip containing "dialog in quotes."'
	command_manpage = "To be implemented later."

	def __init__(self):
		pass
	
	def initialize_action(self, command):
		if 'achewood' in command and '"' not in command:
			response = self.get_achewood()
		elif 'achewood' in command and '"' in command:
			response = self.get_achewood(command[command.find('"'):command.rfind('"')])
		return response

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



## Class for the generator bot function
class Generator():

	command_name = 'generate'
	command_keywords = ['generate']
	command_helptext = "`Generate code phrases:` use the " \
								"keywords 'generate' and 'code' to generate " \
								"top-secret code phrases. *TO DO:* expand to generate " \
								"names, etc."
	command_manpage = "To be implemented later."

	def initialize_action(self, command):
		
		codephrase = self.generate_codephrase()
		return "Your code phrase is " + codephrase + "."

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
	command_helptext = "`Help:` displays information on available commands."
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
	command_helptext = "`Who's the nerd:` tells the channel who the nerd currently is." \
					   " *TO DO:* Build the Nerd Accumulator and SCoring Algorithm Response" \
					   " (N.A.S.C.A.R.)"

	def initialize_action(self, command):
		#basic who is the nerd support
		chance = random.randint(0,100)
		if chance >= 98:
			the_nerd = "Shaquille O'Neal is the nerd now, sir."
		else:
			## fix later eg make work
			# users = list(slack_client.api_call("users.list").get('members'))
			# the_nerd = users[random.randint(0, len(users) - 1)].get('real_name')
			the_nerd = "Kyle Tierce"
			return the_nerd + " is the nerd now, sir."


class SoundCloud():

	##need to fix these
	command_name = 'kick it'
	command_keywords = ['kick it']
	command_helptext = "`Kick it:` Kick it with a tasty groove. "\
						"*TO DO:* Make... better. "
	command_manpage = 'To be implemented later.'

	def initialize_action(self, command):
		tracks = client.get('/playlists/46223708/tracks')
		random_track = random.randint(0, (len(tracks) - 1))
		playtrack = tracks[random_track].permalink_url
		return playtrack