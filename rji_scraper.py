# https://www.rjionline.org/rss
import feedparser
import json
import re

def main():
    feed = feedparser.parse('https://www.rjionline.org/rss')
    json = parse(feed)

    with open('news.json', 'w') as output:
        output.write(str(json))

def parse(feed):
    feed_list = []
    for item in feed.entries:
        title = item.title.strip()
        updated = item.updated.strip()
        if(item.link):
            link = item.link.strip()
        if(item.summary):
            summary = item.summary.strip()
        if(item.tags):
            for tag in item.tags:
                tags = tag.term.strip()

        feed_item = {
            'title': title,
            'updated': updated,
            'link': link,
            'summary': summary,
            'tags': tags
        }
        feed_list.append(str(clean_feed_item(feed_item)))
        clean_feed = cleanup(feed_list)
    return clean_feed

def cleanup(feed_list):
    clean_list = re.sub(r'\\', r'', str(feed_list))
    cleaner_list = re.sub(r'\'{', r'"{', str(clean_list))
    cleanest_list = re.sub(r'\}\'', r'}"', str(cleaner_list))
    return cleanest_list
def clean_feed_item(feed_item):
    clean_item = re.sub(r'\"', r'\'', str(feed_item))
    return clean_item

if __name__ == '__main__':
    main()
