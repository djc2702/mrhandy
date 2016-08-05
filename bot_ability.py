
import lxml.html
import os
import random
import urllib.request
from urllib.parse import quote


## Class for the generator bot function
class Generator():

	command_name = 'generate'

	def __init__(self):
		self.command_keywords = ['generate', 'code']
		self.command_helptext = "`Generate code phrases:` use the " \
								"keywords 'generate' and 'code' to generate " \
								"top-secret code phrases. *TO DO:* expand to generate " \
								"names, etc."
		self.command_manpage = "To be implemented later."

	


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

	def __init__(self):
		self.command_kewyords = 'help'
		self.command_helptext = "`Help:` displays information on available commands."
		self.command_manpage = "To be implemented later."

	def initialize_action(self, command, ability_list):
		response = ''
		for item in ability_list:
			response += item.command_helptext + '\n'
		return response

class ComicPost():

	#change this once we have more comics, if ever
	command_name = 'achewood'

	def __init__(self):
		self.command_keywords = ['achewood']
		self.command_helptext = '`Achewood:` Post a random Achewood strip, or '\
								'search for strip containing "dialog in quotes."'
		self.command_manpage = "To be implemented later."

	
	def initialize_action(self, command):
		if 'achewood' in command and '"' not in command:
			response = self.get_achewood()
		elif 'achewood' in command and '"' in command:
			print(command)
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