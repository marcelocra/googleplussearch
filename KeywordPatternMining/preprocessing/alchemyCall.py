from alchemyapi import AlchemyAPI
import json
import codecs

APIendpoint = "http://access.alchemyapi.com/"
userKeywords = {}
def getKeywords(uID, inputText):
    alchemyapi = AlchemyAPI()
    #alchemyapi.loadAPIKey("api_key.txt")
    response = alchemyapi.keywords('text',inputText)
    print inputText
    if response['status'] == 'OK':
        #print('## Response Object ##')
        #print(json.dumps(response, indent=4))


        #print('')
        #print('## Keywords ##')
        keywords = []
        posts = uID + " : "
        for keyword in response['keywords']:
                keywords.append(keyword['text'])
                posts = posts + keyword['text'] + "|"
        userKeywords[uID] = keywords
        posts = posts + "\n"
        with codecs.open("outNew.txt", "a") as f:
            f.write(posts.encode("UTF-8"))
        return True
    else:
        print('idError: ', uID)
        with codecs.open("keywordOut2.txt", "a") as f:
            text = uID + "\n"
            f.write(text.encode("UTF-8"))
        return False
    
def getKeywordPerPost():
    reader = open('output_sony_posts.txt')
    all_json_posts = reader.read().splitlines()
    alchemyapi = AlchemyAPI()
    counter = 0
    for p in all_json_posts:
        print str(counter)
        if counter < 1000:
            counter = counter + 1
            continue
        #elif counter > 2000:
        #    break
        else:
            counter = counter + 1
        content = json.loads(p)["cleanContent"]   
        response = alchemyapi.keywords('text',content.encode("UTF-8"))
    
        if response['status'] == 'OK':
            keywords = []
            posts = ""
            for keyword in response['keywords']:
                    keywords.append(keyword['text'])
                    posts = posts + keyword['text'] + ","
            posts = posts[:-1] + "\n"
            if posts <> "\n":
                with codecs.open("keyPerPost.txt", "a") as f:
                    f.write(posts.encode("UTF-8"))
        else:
            print "error" + str(counter)
        

def runAll():
    reader = open('keywordOut.txt')
    all_users = reader.read().splitlines()
    counter = 0
    for u in all_users:
        if (counter % 100) == 0:
            print str(counter) + " user processed"
        text = open("datas/" + u + ".txt").read()
        if getKeywords(u, text):
            counter = counter + 1

#text = open("datas/100163937996899435598.txt").read()
#getKeywords(text)
runAll()
#getKeywordPerPost()
