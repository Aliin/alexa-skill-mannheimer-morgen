import feedparser

NewsFeed = feedparser.parse("https://xmedias2.morgenweb.de/feed/202-alexa-advanced-de-kall.xml")
entry = NewsFeed.entries[1]

print(entry.keys())
print(entry["dachzeile"])
print(len(NewsFeed.entries))
print(entry["description"])
