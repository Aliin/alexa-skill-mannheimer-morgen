import feedparser

def getFeed(url):
    NewsFeed = feedparser.parse(url)
    return NewsFeed.entries[1]

def printEntry(entry):
    print(entry.keys())
    print(entry["dachzeile"])
    print(entry["description"])

def runTest(url):
    feed = getFeed(url)
    printEntry(feed)

def printFirstArticleContent(url):
    feed = getFeed(url)
    return entry["description"]

# runTest("https://xmedias2.morgenweb.de/feed/202-alexa-advanced-de-kall.xml")
