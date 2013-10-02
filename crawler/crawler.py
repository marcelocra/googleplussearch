#!/usr/bin/python
##########################################################################################
#                   Requests for the Google+ API
# Find posts of a specific user: GET https://www.googleapis.com/plus/v1/people/{GID}/activities/public?key={YOUR_API_KEY}
# Find comments made to a specific post: GET https://www.googleapis.com/plus/v1/activities/{activityID}/comments?key={YOUR_API_KEY}
# Find user information: https://www.googleapis.com/plus/v1/people/{GID}?key={YOUR_API_KEY}
#
##########################################################################################

import MySQLdb
from optparse import OptionParser
import simplejson as json
import urllib2, cookielib

apiKey = "AIzaSyA9DEz-LYeT7f_WRchuUZerCinK_zv4cFI"

#Install cookiejar
cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
urllib2.install_opener(opener)

#Parse options
parser = OptionParser()
parser.add_option("-p", "--post", dest="post", help="Downloads specific post data", default=None)
(options, args) = parser.parse_args()

#Create DB connection
#db = MySQLdb.connect(
#    host="localhost",
#    user="root",
#    passwd="google",
#    db="googlep")
#cur = db.cursor() 
#query = "SELECT * FROM Ncards WHERE Nname LIKE '%%%s%%'" % options.cardname
#cur.execute(query)
#card_info = cur.fetchone()

def getUserInfo(googleID):
    url = "https://www.googleapis.com/plus/v1/people/%s?key=%s" % (googleID, apiKey)
    search_data = urllib2.urlopen(url)
    search_data = search_data.read()
    overviewData = json.JSONDecoder().decode(search_data)
    print overviewData

def getComments(activityID):
    nextPage = True
    pageToken = ""
    while nextPage:
        url = "https://www.googleapis.com/plus/v1/activities/%s/comments?pageToken=%s&key=%s" % (activityID, pageToken, apiKey)
        search_data = urllib2.urlopen(url)
        search_data = search_data.read()
        overviewData = json.JSONDecoder().decode(search_data)
        for item in overviewData['items']:
            print "User: %s(%s)" % (item['actor']['displayName'], item['actor']['id'])
            print item['object']['content']

        if len(overviewData['items']) <= 0 or 'nextPageToken' not in overviewData:
            nextPage = False
        else:
            pageToken = overviewData['nextPageToken']



def getOverview(googleID):
    nextPage = True
    pageToken = ""
    while nextPage:
        url = "https://www.googleapis.com/plus/v1/people/%s/activities/public?pageToken=%s&key=%s" % (googleID, pageToken, apiKey)
        search_data = urllib2.urlopen(url)
        search_data = search_data.read()
        overviewData = json.JSONDecoder().decode(search_data)
        for item in overviewData['items']:
            print item['id']
            print item['object']['content']
            print "Replies: %s" % item['object']['replies']['totalItems']
            print "Activity ID: %s" % item['id']
            if item['object']['replies']['totalItems'] > 0:
                print "\nComments:"
                getComments(item['id'])
            print "---------------------------------------------------"
        if len(overviewData['items']) <= 0:
            nextPage = False
        else:
            pageToken = overviewData['nextPageToken']

getUserInfo("112006633193431967926")
getOverview("+LadyGaga")
