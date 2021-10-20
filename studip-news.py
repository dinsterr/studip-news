#!/usr/bin/env python
import re

from bs4 import BeautifulSoup
from config import Config
from feedgen.feed import FeedGenerator
from datetime import datetime, timezone

from studip_sync.config import CONFIG as STUDIP_SYNC_CONFIG
from studip_sync.logins import LoginError
from studip_sync.session import Session, SessionError
from studip_sync.parsers import ParserError

PAYLOAD = {'filtertype': Config.SELECTED_FILTERS}
USER_ID_REGEX = re.compile('STUDIP.ActivityFeed.user_id = \'(.+?)\';')
START_PAGE_URL = STUDIP_SYNC_CONFIG.base_url + "dispatch.php/start"
ACTIVITY_STREAM_URL = STUDIP_SYNC_CONFIG.base_url + "api.php/user/{0}/activitystream"


def main():
    session = create_session()
    activities = fetch_activity_stream(session)
    generate_feed(activities)


def create_session():
    with Session(base_url=STUDIP_SYNC_CONFIG.base_url) as studip_sync_session:
        print("Logging in...")
        try:
            studip_sync_session.login(STUDIP_SYNC_CONFIG.auth_type, STUDIP_SYNC_CONFIG.auth_type_data,
                                      STUDIP_SYNC_CONFIG.username,
                                      STUDIP_SYNC_CONFIG.password)
        except (LoginError, ParserError) as e:
            print("Login failed!")
            print(e)
            return 1

    return studip_sync_session.session


def extract_user_id(session):
    if Config.USER_ID:
        return Config.USER_ID

    with session.get(START_PAGE_URL) as response:
        if not response.ok:
            raise SessionError("Could not open page for user id extraction!")

    match = USER_ID_REGEX.search(response.text)
    if match:
        return match.group(1)
    else:
        raise ParserError("Could not extract userid!")


def generate_feed(json):
    print("Generating feed...")
    fg = FeedGenerator()
    fg.id(STUDIP_SYNC_CONFIG.base_url)
    fg.title('STUD.IP Activities')

    for entry in json:
        fe = fg.add_entry()
        fe.id(entry['id'])
        fe.title(entry['title'])
        fe.content(BeautifulSoup(entry['content']).get_text())
        fe.link({'href': STUDIP_SYNC_CONFIG.base_url + list(entry['object_url'].keys())[0]})
        fe.published(datetime.fromtimestamp(int(entry['mkdate']), timezone.utc))

    fg.atom_file("/dev/stdout", pretty=True)


def generate_user_id_url(session):
    return ACTIVITY_STREAM_URL.format(extract_user_id(session))


def fetch_activity_stream(session):
    print("Fetching activity stream...")
    with session.get(generate_user_id_url(session), params=PAYLOAD) as response:
        if not response.ok:
            raise SessionError("Could not fetch activities!")

        return response.json()


if __name__ == '__main__':
    main()
