#
# Site looksy 
# -----------
#
# author		: Kevin Jump ( @kevinjump)
# description	: Go through a list of sites, get the html 
#				  and search it for things 	
#

import os 
import urllib2
import urllib 
import time


#
# GetContent : Gets the HTML from a URL
#
def GetContent(url):

	try:
		response = urllib2.urlopen(url, timeout=10)
		return response.read()
		
	except:
		#print 'error getting site {0}'.format(url) 
		return ''


def FindTheString(url, html, search):

	substring = html.lower().find(search.lower())
	if ( substring > 0 ) :
		print '' 
		print '{0} found {1}'.format(url, search),  
		
#
# Main Application
#
# guessy
#		
#	takes website urls and looks for beta. new. alpha.
#
		

# file
websites_file = 'CouncilDomains.txt'
guess = "new"

f = open(websites_file, 'r')
all_lines = f.read().splitlines()

total = len(all_lines)
current = 0

for website in all_lines:
	current = current + 1

	if website[0] <> '#' : #not a comment 
	
		website_info = website.split(',')
		
		if len(website_info) == 2:
		
			website_name = website_info[0]
			website_url = website_info[1]

			html = GetContent( 'http://{0}{1}'.format(guess, website_url))
			if html.__len__() > 10 :
				print 'http://{0}{1}'.format(guess, website_url) 
				
			#print '[{0}]'.format(current) ,
 
f.close() 