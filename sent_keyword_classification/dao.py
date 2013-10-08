##
from models import Post

def buildPost(post):
    print "-------------------------HASHTAGS--"
    output = Post(post)
    print output.hashtags
    return output

def buildPosts(posts):
    return map(buildPost, posts)

