#!/usr/bin/env python
import html2text
from config import Config
from feedgen.feed import FeedGenerator
from datetime import datetime, timezone

from studip_sync.config import CONFIG
from studip_sync.logins import LoginError
from studip_sync.session import Session, SessionError
from studip_sync.parsers import ParserError

ACTIVITY_URL = Config.BASE_URL + '/studip/api.php/user/' + Config.USER_ID + '/activitystream'
PAYLOAD = {'filtertype': Config.SELECTED_FILTERS}


def main():
    session = create_session()
    print("Fetching stream...")

    activities = fetch_activitystream(session)
    generate_feed(activities)


def create_session():
    with Session(base_url=CONFIG.base_url) as studip_sync_session:
        print("Logging in...")
        try:
            studip_sync_session.login(CONFIG.auth_type, CONFIG.auth_type_data, CONFIG.username,
                          CONFIG.password)
        except (LoginError, ParserError) as e:
            print("Login failed!")
            print(e)
            return 1

    return studip_sync_session.session


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


def fetch_activitystream(session):
    with session.get(ACTIVITY_URL, params=PAYLOAD) as response:
        if not response.ok:
            raise SessionError("Could not fetch activities!")

        return response.json()


if __name__ == '__main__':
    main()
