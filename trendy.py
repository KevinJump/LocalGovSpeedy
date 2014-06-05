#
# Site trendy - looks for the cool words
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

foundcount = 0 


#
# GetContent : Gets the HTML from a URL
#
def GetContent(url):

	try:
		response = urllib2.urlopen(url, timeout=10)
		return response.read()
		
	except:
		print url, ' error getting site',
		return ''


def FindTheString(url, html, search):

	substring = html.lower().find(search.lower())
	if ( substring > 0 ) :
		print ' found [{0}]'.format(search),  
		return 1 
	
	return 0 
		
#
# Main Application
#
# looksy [string] 
#		
#	looks for the string in a list of sites (council)
#
		

# file
websites_file = 'councilsites.txt'

trends = ['top task', 'straight to', 'residents', 'pay it', 'report it', 'find my nearest', 'popular tasks','highlights','faq','frequently asked','Popular topics','Quick links']
trendcounts = range(len(trends)) 
websites = 0

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

			html = GetContent(website_url) 
			if html.__len__() > 10 :
			
				print '[{0}].{1}'.format(current, website_url),
				websites = websites + 1 
			
				for i in range(len(trends)):
				
					searchstring = trends[i] 
					
					if FindTheString(website_url, html, searchstring) == 1:
						trendcounts[i] = trendcounts[i] + 1
					
				
			print ''
 
f.close() 

print "."

print 'Got Content from {0} websites'.format(websites) 
print '--------------------------------'

for i in range(len(trends)):
	print '{0}   : {1}'.format(trends[i], trendcounts[i])
	