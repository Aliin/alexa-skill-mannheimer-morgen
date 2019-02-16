import feedparser
from html.parser import HTMLParser
import json

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

class Article:
    def __init__(self, entry, fields):
        self.entry = entry
        self.fields = fields

    def normalize(self, html):
        s = StolenFromStackoverflow()
        try:
            s.feed(html)
            return s.get_data()
        except TypeError:
            return html

    def get_object(self):
        article = {}
        for field in self.fields:
            if field not in self.entry.keys():
                next
            elif field == 'tags':
                article[field] = self.tags()
            else:
                article[field] = self.normalize(self.entry[field])
        return article

    def tags(self):
        tags = ""
        for tag in self.entry["tags"]:
            tags += tag["term"]
        return tags

class FeedReader:
    fields = ['title', 'summary', 'tags']

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

    def __init__(self, category, numberArticles):
        self.category = category
        self.numberArticles = numberArticles
        self.feed_url = self.overall_feeds.get(category, False) or self.regional_feeds.get(category, False)

    def getFeed(self):
        return feedparser.parse(self.feed_url)

    def getEntries(self):
        return self.getFeed().entries[:self.numberArticles]

    def getArticleList(self):
        articleList = []
        for entry in self.getEntries():
            articleList.append(self.article(entry))
        return articleList

    def article(self, entry):
        return Article(entry, self.fields).get_object()

    def runTest(self):
        print(self.results())

    def results(self):
        return self.getArticleList()
