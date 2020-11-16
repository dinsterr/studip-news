#!/usr/bin/env python
import requests
import html2text
from config import Config
from feedgen.feed import FeedGenerator
from datetime import datetime, timezone

ACTIVITY_URL = Config.BASE_URL + '/studip/api.php/user/' + Config.USER_ID + '/activitystream'
PAYLOAD = {'filtertype': Config.SELECTED_FILTERS}


def main():
    activities = fetch_activitystream()
    generate_feed(activities)


def generate_feed(json):
    fg = FeedGenerator()
    fg.id(ACTIVITY_URL)
    fg.title('StudIp Activities')

    for entry in json:
        fe = fg.add_entry()
        fe.id(entry['id'])
        fe.title(entry['title'])
        fe.content(html2text.html2text(entry['content']))
        fe.link({'href':  Config.BASE_URL + list(entry['object_url'].keys())[0]})
        fe.published(datetime.fromtimestamp(int(entry['mkdate']), timezone.utc))

    fg.atom_file("/dev/stdout")


def fetch_activitystream():
    r = requests.get(ACTIVITY_URL, params=PAYLOAD, cookies=Config.AUTH_COOKIES)
    return r.json()


if __name__ == '__main__':
    main()
