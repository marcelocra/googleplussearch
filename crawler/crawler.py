#!/usr/bin/python
##########################################################################################
#                   Requests for the Google+ API
# Find posts of a specific user: GET https://www.googleapis.com/plus/v1/people/{GID}/activities/public?key={YOUR_API_KEY}
# Find comments made to a specific post: GET https://www.googleapis.com/plus/v1/activities/{activityID}/comments?key={YOUR_API_KEY}
# Find user information: https://www.googleapis.com/plus/v1/people/{GID}?key={YOUR_API_KEY}
#
##########################################################################################

#import MySQLdb
from optparse import OptionParser
import simplejson as json
import urllib2, cookielib
import sys
import re
from nltk.util import clean_html
import HTMLParser

sys.path.append("../LanguageDetection")
from LanguageCheck import Trigram

apiKey = "AIzaSyDZFITATgwsWzuw4JpaXbWK0BV6Yd292mg"

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

# Find all the comments corresponding with a given postID
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
            content = clean_html(item['object']['content'])
            print content

        if len(overviewData['items']) <= 0 or 'nextPageToken' not in overviewData:
            nextPage = False
        else:
            pageToken = overviewData['nextPageToken']

# Find posts made by users given a search term
def getSearchResults(searchQuery):
    nextPage = True
    pageToken = ""
    re_hashtag_find = re.compile("<a class=\"ot-hashtag\".*?>(.*?)</a>")
    while nextPage:
        url = "https://www.googleapis.com/plus/v1/activities?query=%s&pageToken=%s&key=%s" % (searchQuery, pageToken, apiKey)
        search_data = urllib2.urlopen(url)
        search_data = search_data.read()
        overviewData = json.JSONDecoder().decode(search_data)
        fp = open("output.txt", "a+")
        for item in overviewData['items']:
            output = {}
            print item['id']
            output['postID'] = item['id']
            output['userID'] = item['actor']['id']
            output['replyCount'] = item['object']['replies']['totalItems']
            output['userName'] = item['actor']['displayName']
            output['content'] = clean_html(item['object']['content'])
#            getUserInfo(item['actor']['id'])

            output['hashtags'] = re_hashtag_find.findall(item['object']['content'])
            content = HTMLParser.HTMLParser().unescape(clean_html(item['object']['content']))
            print content
            fp.write(json.JSONEncoder().encode(output) + "\n")
            # Check if text is english
            languageDetector = Trigram(content)
            isEnglish = languageDetector.isEnglish()
            print "Post is in English: %s" % isEnglish
            # Iterate over comments
            print "Replies: %s" % output['replyCount']
            print "Activity ID: %s" % output['postID']
            if item['object']['replies']['totalItems'] > 0:
                print "\nComments:"
#                getComments(item['id'])
            print "---------------------------------------------------"
        fp.close()

        if len(overviewData['items']) <= 0:
            nextPage = False
        else:
            pageToken = overviewData['nextPageToken']
    
# get all the posts made publicly by someone given a googleID
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

getSearchResults("iPhone")
#getUserInfo("112006633193431967926")
#getOverview("+LadyGaga")
