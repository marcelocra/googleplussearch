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
sys.path.append("../sent_keyword_classification")
sys.path.append("../")
from LanguageCheck import Trigram
from spellchecker import spellCheck
from sent import SentiWordNetReader, SentiSynset
from smileys import Smileys


global apiList
global apiKey
global apiOffset
global requestCount
apiList = ["AIzaSyDZFITATgwsWzuw4JpaXbWK0BV6Yd292mg", "AIzaSyBS5eCOxTHbB7AK4ypduCpqiW-RyQIaG3Y", "AIzaSyB24XShYV2CK7K5auqUEWcOYLi6nr_Au8A"]
apiOffset = 0
apiKey = "AIzaSyDZFITATgwsWzuw4JpaXbWK0BV6Yd292mg"
requestCount = 0
spellChecker = spellCheck()

SWN = SentiWordNetReader("../sent_keyword_classification/SENTIWORDNET.txt")
SMILEYS = Smileys("../sent_keyword_classification/SMILEYS.csv")

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
    global apiList
    global apiKey
    global apiOffset
    global requestCount
    requestCount += 1
    if requestCount >= 3000:
        apiOffset += 1
        if apiOffset > 2:
            sys.stdout.write("No more api keys available. aborting")
            sys.exit(0)
        
        sys.stdout.write("Reached query limit, switching to next next apiKey: %s - %s" % (apiKey, apiList[apiOffset])) 
        apiKey = apiList[apiOffset]
        requestCount = 0
        
    url = "https://www.googleapis.com/plus/v1/people/%s?key=%s" % (googleID, apiKey)
    search_data = urllib2.urlopen(url)
    search_data = search_data.read()
    overviewData = json.JSONDecoder().decode(search_data)
    fpu.write(json.JSONEncoder().encode(overviewData) + "\n")
    
    getOverview(googleID)

# Find all the comments corresponding with a given postID
def getComments(activityID):
    global apiList
    global apiKey
    global apiOffset
    global requestCount
    nextPage = True
    pageToken = ""
    while nextPage:
        time.sleep(2)
        requestCount += 1
        if requestCount >= 3000:
            apiOffset += 1
            if apiOffset > 2:
                sys.stdout.write("No more api keys available. aborting")
                sys.exit(0)
        
            sys.stdout.write("Reached query limit, switching to next next apiKey: %s - %s" % (apiKey, apiList[apiOffset])) 
            apiKey = apiList[apiOffset]
            requestCount = 0
    
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
            cleanContent = SMILEYS.removeSmileys(cleanContent)
            output['cleanContent'] = cleanContent

            print cleanContent
            print spellChecker.spellcheck(cleanContent)

            # Check if text is english
            languageDetector = Trigram(cleanContent)
            isEnglish = languageDetector.isEnglish()
            print "Post is in English: %s" % isEnglish
            if isEnglish:
                sent_score = SWN.get_sentiment(content)
                sent_emotions = SMILEYS.findEmotions(content)
                output['sentiment_score'] = sent_score
                output['sentiment_emotions'] = sent_emotions
                
                fpp.write(json.JSONEncoder().encode(output) + "\n")

        if len(overviewData['items']) <= 0 or 'nextPageToken' not in overviewData:
            nextPage = False
        else:
            pageToken = overviewData['nextPageToken']

# Find posts made by users given a search term
def getSearchResults(searchQuery):
    nextPage = True
    pageToken = ""
    global apiList
    global apiKey
    global apiOffset
    global requestCount    
    while nextPage:
        time.sleep(2)
        global requestCount
        requestCount += 1
        if requestCount >= 3000:
            apiOffset += 1
            if apiOffset > 2:
                sys.stdout.write("No more api keys available. aborting")
                sys.exit(0)
        
            sys.stdout.write("Reached query limit, switching to next next apiKey: %s - %s" % (apiKey, apiList[apiOffset])) 
            apiKey = apiList[apiOffset]
            requestCount = 0
        
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
            cleanContent = SMILEYS.removeSmileys(cleanContent)
            output['cleanContent'] = cleanContent
    
            print cleanContent
            

            # Check if text is english
            languageDetector = Trigram(cleanContent)
            isEnglish = languageDetector.isEnglish()
            print "Post is in English: %s" % isEnglish
            if isEnglish:
                sent_score = SWN.get_sentiment(content)
                sent_emotions = SMILEYS.findEmotions(content)
                output['sentiment_score'] = sent_score
                output['sentiment_emotions'] = sent_emotions
                
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
    global apiList
    global apiKey
    global apiOffset
    global requestCount
    nextPage = True
    pageToken = ""
    overviewCount = 0
    while nextPage and overviewCount <= 2:
        time.sleep(2)
        overviewCount += 1
        requestCount += 1
        if requestCount >= 3000:
            apiOffset += 1
            if apiOffset > 2:
                sys.stdout.write("No more api keys available. aborting")
                sys.exit(0)
        
            sys.stdout.write("Reached query limit, switching to next next apiKey: %s - %s" % (apiKey, apiList[apiOffset])) 
            apiKey = apiList[apiOffset]
            requestCount = 0
    
        url = "https://www.googleapis.com/plus/v1/people/%s/activities/public?pageToken=%s&key=%s" % (googleID, pageToken, apiKey)
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
            cleanContent = SMILEYS.removeSmileys(cleanContent)
            output['cleanContent'] = cleanContent
            
            print cleanContent
            
            # Check if text is english
            languageDetector = Trigram(cleanContent)
            isEnglish = languageDetector.isEnglish()
            print "Post is in English: %s" % isEnglish
            if isEnglish:
                sent_score = SWN.get_sentiment(content)
                sent_emotions = SMILEYS.findEmotions(content)
                output['sentiment_score'] = sent_score
                output['sentiment_emotions'] = sent_emotions
                
                fpp.write(json.JSONEncoder().encode(output) + "\n")
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

getSearchResults("iPhone")
