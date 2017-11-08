# https://www.rjionline.org/rss
import feedparser
import json
import boto3
from time import mktime
from dateutil import parser as parsedate

def main():
    feed = feedparser.parse('https://www.rjionline.org/rss')
    feed_list = parse(feed)

    with open('news.json', 'w') as output:
        json.dump(feed_list, output)

    save_to_dynamodb(feed_list)

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
            "title": title,
            "updated": updated,
            "link": link,
            "summary": summary,
            "tags": tags
        }
        feed_list.append(feed_item)
    return feed_list

def parsetime(updated_time):
    dt_obj = parsedate.parse(updated_time)
    epoch_time = int(mktime(dt_obj.timetuple()))
    return epoch_time

def save_to_dynamodb(feed_list):
        # create a boto3 session (should load your stored credentials from env)
        session = boto3.Session()

        # create a client for interacting with dynamodb
        dynamodb = session.resource('dynamodb')
        # get the election_results dynamodb table
        table = dynamodb.Table('DYNAMO_DB_RESULTS_TABLE')

        for item in feed_list:
            item_to_save = {
                "updated": parsetime(item['updated']),
                "tags": item['tags'],
                "article": item
            }

            table.put_item(Item=item_to_save)


if __name__ == '__main__':
    main()
