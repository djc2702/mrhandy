
import os
import random



class Generator():

	command_name = 'generate'
	# command_keywords = ['generate', 'code']
	# command_helptext = "`Generate code phrases:` use the " \
	# 					"keywords 'generate' and 'code' to generate" \
	# 					"top-secret code phrases."
	# command_manpage = "To be implemented later."

	def __init__(self):
		# self.command_name = 'generate'
		self.command_keywords = ['generate', 'code']
		self.command_helptext = "`Generate code phrases:` use the " \
								"keywords 'generate' and 'code' to generate" \
								"top-secret code phrases."
		self.command_manpage = "To be implemented later."

	def initialize_action(self, command):
		
		codephrase = generate_codephrase()
		return "Your code phrase is " + codephrase + "."





# Generate codephrase.
def generate_codephrase():
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