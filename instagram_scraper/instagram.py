from datetime import datetime, MINYEAR
import os

from instagrapi import Client
from fcache.cache import FileCache
from mintotp import totp

import socketio

from instagram_scraper.image_to_terms import OCR
from instagram_scraper.PS import PS
from instagram_scraper.Config import Config

MIN_DATE = datetime(MINYEAR, 1, 1)

class Instagram:
    def __init__(self, ps: PS, config: Config):
        self.ps = ps
        self.client = Client()
        self.client.login(
            config['instagram']['username'], 
            config['instagram']['password'],
            totp(config['instagram']['totp']))
        else:
            self.client.login(username, password)
        self.cache = FileCache('Instagram-Scraper', flag='cs', app_cache_dir='/data')
        self.ocr = OCR()

    def username_to_userid(self, username: str) -> int:
        try:
            return self.cache.get('username_userid', {})[username]
        except KeyError:
            userid = self.client.user_id_from_username(username)
            self.cache.get('username_userid', {})[username] = userid
            self.cache.get('userid_username', {})[userid] = username
            return userid
    
    def last_investigated(self, userid: int) -> datetime:
        return self.cache.get('investigated', {}).get(userid, MIN_DATE)

    def investigate_user(self, username: str):
        userid = self.username_to_userid(username)
        dt_now = datetime.now()
        dt_last = self.last_investigated(userid)
        stories = user_stories(userid)
        for story in stories:
            # only check story if it is newer than last time we checked the user and if it is not a video
            if story.taken_at > dt_last and story.video_url is None:
                story_download(story.pk, "story.jpeg", "/tmp/")
                terms = self.ocr.image_to_terms('/tmp/story.jpeg')
                matches = self.ps.match(terms)
                if matches:
                    os.rename('/tmp/story.jpeg', '/data/%s.jpeg' % story.pk)
                    socketio.emit('new_image', story.pk)
                else:
                    os.rm('/tmp/story.jpeg')
    
    def investigate_users(self):
        for user in self.config['users']:
            investigate_user(user)
            if self.config['users'][user]:
                for user2 in self.config['users'][user]:
                    investigate_user(user2)

