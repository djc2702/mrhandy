import urllib.request
from urllib.parse import quote
import lxml.html


def get_achewood(*arg):
	# If no search argument is supplied, grab a random strip using urllib and lxml
	if len(arg) == 0:
		page = urllib.request.urlopen('http://www.ohnorobot.com/random.pl?comic=636')
		doc = lxml.html.parse(page)
		imgurl = doc.xpath('//img/@src')
		return 'http://www.achewood.com' + imgurl[1]
	else:
		# if there's a search term, first turn it into a searchable string
		search = ' '.join(arg)
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
