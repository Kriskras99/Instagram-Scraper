from flask import Flask, render_template, abort, redirect, url_for, request
from flask_socketio import SocketIO, join_room, leave_room

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

import os

from instagram_scraper.config import Config
from instagram_scraper.instagram import Instagram
from instagram_scraper.ps import PSBuildingblock, PS

scheduler = BackgroundScheduler()

config = Config()

app = Flask(__name__,
            static_url_path='',
            static_folder='web/')
socketio = SocketIO(app)

ps = PS([])
for bb in os.listdir('/config/buildingblocks'):
    with open(bb, 'r') as f:
        ps.merge(PS.from_json(json.load(f)))

instagram = Instagram(
    ps,
    config
)

scheduler.add_job(instagram.investigate_users, IntervalTrigger(minutes=config['app']['time_between_scans'], jitter=30, coalesce=True, max_instances=1))

@app.route('/')
def index():
    return redirect("/index.html", code=301)

@app.route('/hello')
def hello():
    return 'Hello, World!'

@socketio.on('set_settings')
def set_settings(data):
    # save settings
    """
    instagram: username, password, totp
    app: time between scans (15m), time between follower check (24h?), degrees of seperation
    """
    config.set_all(data)


@socketio.on('get_settings')
def get_settings():
    # save settings
    """
    instagram: username, password, totp
    app: time between scans (15m), time between follower check (24h?), degrees of seperation
    """
    return config.get_all()

@socketio.on('false_positive')
def unmark_post(data):
    # post is not relevant, delete from storage
    os.rm('/data/%s.jpeg' % data)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')
