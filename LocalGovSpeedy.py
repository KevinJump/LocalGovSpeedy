#
# LocalgovSpeedy - a page speed mesuring device
# ---------------------------------------------
# autho: Kevin Jump (@kevinjump)
# decription: just a bit of fun, asking google page insights about 
#               local goverment websites.
#
import os
import urllib 
import urllib2
import json
import time  

import base64


pageSpeedApikey = ''
pageSpeedUrl = ''
 
# load our settings.
#dir_path = os.path.dirname(os.path.abspath(__file__))
#speedy_config = os.path.join( dir_path, 'speed_config.json' ) 
with open('speed_config.json') as config_file:    
    config = json.load(config_file)
    pageSpeedApiKey = config['apikey']
    

# go to google and get the pagespeed info for a site
#
def GetPageSpeedJson(url, site_type):  

    try:
	
		# build the pagespeed url
		api_key = pageSpeedApiKey          
		url_args = { 'url': url, 'strategy': site_type, 'key' : api_key, 'screenshot' : 'true'}        
		encoded_args = urllib.urlencode(url_args)
		ps_url = 'https://www.googleapis.com/pagespeedonline/v1/runPagespeed?{0}'.format(encoded_args)
		
		response = urllib2.urlopen(ps_url, timeout = 30)
		return response.read()
	
    except:
	    print "Unexpected error:", sys.exc_info()[0]

#
# read the bytes value from the json - if it's not set
# return 0
def psGetBytes(ps_json, bytes_property):
    
    try:
        bytes_value = ps_json[bytes_property]
        if bytes_value:
            return bytes_value
        else:
            return '0'
    except:
        return '0'

#
# save the json so we can use it again
#
def saveJson(council_name, response, site_type):
    file_name = './results/' + council_name + '_' + site_type + '.json' 
    js = open(file_name, 'w')
    js.write(response)
    js.close()
    
def saveScreenshot(council_name, site_type, ps_json):
    
    try:
        file_name = './results/screenshots/' + council_name + '_' + site_type + ".jpg"
        jpg = open(file_name, 'wb')
    
        data = json.loads(ps_json)
        screenshot_section = data['screenshot']
        jpg_data = screenshot_section['data'].replace('_', '/').replace('-', '+')


        # The google pagespeed service is returning an invalid base64. 
        # To correct it replace all '_' with '/' and all '-' with '+'.
        jpg.write(base64.b64decode(jpg_data))
        jpg.close()
    except:
        return
    
    
    
def printCouncilScores(council_name, council_site, ps_json):
    try:
        data = json.loads(ps_json)
        ps_score = data['score']
        print ps_score ,
        
        ps_json = data['pageStats']
        
        ps_htmlb = psGetBytes(ps_json, 'htmlResponseBytes')
        ps_cssb = psGetBytes(ps_json, 'cssResponseBytes')
        ps_imgb = psGetBytes(ps_json, 'imageResponseBytes')
        ps_jsb = psGetBytes(ps_json, 'javascriptResponseBytes')
        ps_othb = psGetBytes(ps_json, 'otherResponseBytes')
        
        total_bytes = int(ps_htmlb) + int(ps_cssb) + int(ps_imgb) + int(ps_jsb) + int(ps_othb)   
        
        print ',{0},{1},{2},{3},{4},{5},'.format(ps_htmlb, ps_cssb, ps_imgb, ps_jsb, ps_othb, total_bytes) ,

    except:
        print 'error,0,0,0,0,0,'
    

def GetAndProcessResults(council_name, council_site, site_type):
    try:
        council_result = GetPageSpeedJson(council_site, site_type)
    
        if council_result.__len__() > 10 :
            saveJson(council_name, council_result, site_type)
            printCouncilScores(council_name, council_site, council_result)
            saveScreenshot(council_name, site_type, council_result)
    except:
        return 

#
# Main code ---
#
#
#council_file = 'CouncilSites.txt'
council_file = 'betasites_june.txt'

f = open(council_file, 'r')
all_lines = f.read().splitlines()

total = len(all_lines)
current = 0

for council in all_lines:
    current = current + 1 
    
    if council[0] <> '#': # not a comment
        council_info = council.split(',')
        
        if len(council_info) == 2:
            council_name = council_info[0]
            council_site = council_info[1]
            
            print '{0},{1},'.format(council_name, council_site) ,
            GetAndProcessResults(council_name, council_site, 'desktop')
            time.sleep(1)
            GetAndProcessResults(council_name, council_site, 'mobile')
            print ''
            time.sleep(1)