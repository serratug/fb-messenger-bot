from urllib2 import Request, urlopen, URLError
import json
import urllib2

def getresult(words):
    url ="http://partners.api.skyscanner.net/apiservices/browseroutes/v1.0/anywhere/usd/tr-TR/%s/%s/%s/?apikey=prtl6749387986743898559646983194" % (words[1], words[2], words[0])
    
    response = urllib2.urlopen(url)
    data = json.load(response)
    print data 
    return [data]
