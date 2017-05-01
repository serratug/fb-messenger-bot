#from urllib2 import Request, urlopen, URLError
import json
#import urllib2
import requests

def getresult(words):
    url ="http://partners.api.skyscanner.net/apiservices/browseroutes/v1.0/anywhere/usd/tr-TR/%s/%s/%s/?apikey=prtl6749387986743898559646983194" % (words[1], words[2], words[0])
    
    response = requests.get(url)
    data = response.json()
    #print data
    return [data]
