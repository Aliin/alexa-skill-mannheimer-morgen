import feedparser
from html.parser import HTMLParser

class StolenFromStackoverflow(HTMLParser):
    def __init__(self):
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = StolenFromStackoverflow()
    s.feed(html)
    return s.get_data()

overall_feeds = {
        'Das Wichtigste': 'http://www.morgenweb.de/feed/146-rss-das-wichtigste.xml',
        'Sport': 'http://www.morgenweb.de/feed/50-rss-sport.xml',
        'Politik': 'http://www.morgenweb.de/feed/55-politik-rss-feed.xml',
        'Wirtschaft': 'http://www.morgenweb.de/feed/56-wirtschaft-rss-feed.xml',
        'Kultur': 'http://www.morgenweb.de/feed/57-kultur-rss-feed.xml',
        'Aus aller Welt': 'http://www.morgenweb.de/feed/58-vermischtes-rss-feed.xml',
        'Wissenschaft': 'http://www.morgenweb.de/feed/68-rss-wissenschaft.xml',
        'Kommentare': 'http://www.morgenweb.de/feed/69-rss-kommentare.xml',
        'Freizeit': 'http://www.morgenweb.de/feed/70-rss-freizeit.xml',
        'Reise': 'http://www.morgenweb.de/feed/71-rss-reise.xml',
        'Auto': 'http://www.morgenweb.de/feed/72-rss-auto.xml'
}

regional_feeds = {
        'Unternehmen der Region': 'http://www.morgenweb.de/feed/59-rss-feed-unternehmen-der-region.xml',
        'Die Adler Mannheim': 'http://www.morgenweb.de/feed/51-rss-adler-mannheim.xml',
        'Rhein-Neckar Löwen': 'http://www.morgenweb.de/feed/52-rss-loewen.xml',
        'SV Waldhof 07 ': 'http://www.morgenweb.de/feed/53-rss-sv-waldhof.xml',
        'TSG 1899 Hoffenheim': 'http://www.morgenweb.de/feed/54-rss-hoffenheim.xml'
}

def getFeed(url):
    NewsFeed = feedparser.parse(url)
    return NewsFeed.entries[1]

def printEntry(entry):
    print(entry.keys())
    print(strip_tags(entry["summary"]))

def runTest(url):
    feed = getFeed(url)
    printEntry(feed)

def printFirstArticleContent(url):
    feed = getFeed(url)
    return entry["description"]

runTest(overall_feeds['Das Wichtigste'])