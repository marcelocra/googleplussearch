#!/usr/bin/python
##########################################################################################
#                   Requests for the Google+ API
# Find posts of a specific user: GET https://www.googleapis.com/plus/v1/people/{GID}/activities/public?key={YOUR_API_KEY}
# Find comments made to a specific post: GET https://www.googleapis.com/plus/v1/activities/{activityID}/comments?key={YOUR_API_KEY}
# Find user information: https://www.googleapis.com/plus/v1/people/{GID}?key={YOUR_API_KEY}
#
##########################################################################################

from optparse import OptionParser
import simplejson as json
import urllib2, cookielib
import sys
import re
from nltk.util import clean_html
import HTMLParser
import time

sys.path.append("../LanguageDetection")
sys.path.append("../")
from LanguageCheck import Trigram
from spellchecker import spellCheck

apiKey = "AIzaSyDZFITATgwsWzuw4JpaXbWK0BV6Yd292mg"
spellChecker = spellCheck()
fpp = open("output_posts.txt", "a+")
fpu = open("output_users.txt", "a+")

re_hashtag_find = re.compile("<a class=\"ot-hashtag\".*?>(.*?)</a>")

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
    fpu.write(json.JSONEncoder().encode(overviewData) + "\n")

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
            output = {}
            print item['id']
            output['postID'] = item['id']
            output['userID'] = item['actor']['id']
            output['userName'] = item['actor']['displayName']
            output['content'] = clean_html(item['object']['content'])
            
            output['hashtags'] = re_hashtag_find.findall(item['object']['content'])
            content = HTMLParser.HTMLParser().unescape(clean_html(item['object']['content']))
            cleanContent = re.sub("http://.*?(?:\s+|$)", "", content)
            output['cleanContent'] = cleanContent

            print cleanContent
            print spellChecker.spellcheck(cleanContent)

            # Check if text is english
            languageDetector = Trigram(cleanContent)
            isEnglish = languageDetector.isEnglish()
            print "Post is in English: %s" % isEnglish
            if isEnglish:
                getUserInfo(item['actor']['id'])
                fpp.write(json.JSONEncoder().encode(output) + "\n")

        if len(overviewData['items']) <= 0 or 'nextPageToken' not in overviewData:
            nextPage = False
        else:
            pageToken = overviewData['nextPageToken']

# Find posts made by users given a search term
def getSearchResults(searchQuery):
    nextPage = True
    pageToken = ""
    
    while nextPage:
        time.sleep(2)
        url = "https://www.googleapis.com/plus/v1/activities?query=%s&maxResults=20&pageToken=%s&key=%s" % (searchQuery, pageToken, apiKey)
        search_data = urllib2.urlopen(url)
        search_data = search_data.read()
        overviewData = json.JSONDecoder().decode(search_data)

        for item in overviewData['items']:
            output = {}
            print item['id']
            output['postID'] = item['id']
            output['userID'] = item['actor']['id']
            output['replyCount'] = item['object']['replies']['totalItems']
            output['userName'] = item['actor']['displayName']
            output['content'] = clean_html(item['object']['content'])

            output['hashtags'] = re_hashtag_find.findall(item['object']['content'])
            content = HTMLParser.HTMLParser().unescape(clean_html(item['object']['content']))
            cleanContent = re.sub("http://.*?(?:\s+|$)", "", content)
            output['cleanContent'] = cleanContent

            print cleanContent
            print spellChecker.spellcheck(cleanContent)

            # Check if text is english
            languageDetector = Trigram(cleanContent)
            isEnglish = languageDetector.isEnglish()
            print "Post is in English: %s" % isEnglish
            if isEnglish:
                fpp.write(json.JSONEncoder().encode(output) + "\n")
                getUserInfo(item['actor']['id'])
            # Iterate over comments
            print "Replies: %s" % output['replyCount']
            print "Activity ID: %s" % output['postID']
            if item['object']['replies']['totalItems'] > 0:
                print "\nComments:"
                getComments(item['id'])

            print "---------------------------------------------------"

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
