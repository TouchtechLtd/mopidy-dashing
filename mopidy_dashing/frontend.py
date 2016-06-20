from __future__ import unicode_literals

import pykka
import urllib2
import logging
import json

from mopidy import core
from time import sleep

logger = logging.getLogger(__name__)

class DashingFrontend(pykka.ThreadingActor, core.CoreListener):
    def __init__(self, config, core):
        super(DashingFrontend, self).__init__()
        self.config = config    
        self.core = core

        self.url = "http://%s:%s%s" % (
            config['dashing']['hostname'], 
            config['dashing']['port'], 
            config['dashing']['widget'],
        )
        self.auth_token = config['dashing']['auth_token']

        self.req = urllib2.Request(self.url)
        self.req.add_header('Content-Type', 'application/json')
    
    def send(self,data):
        self.req = urllib2.Request(self.url)
        self.req.add_header('Content-Type', 'application/json')
        urllib2.urlopen(self.req, data)

    def on_start(self):
        logger.debug(self.url)

    def on_stop(self):
        message = json.dumps({
            "auth_token": self.auth_token,
            "title": "Music stopped",
            "song": "",
            "details": ""
        })

        logger.info(message)
        self.send(message)

    def track_playback_started(self, tl_track):
        self.starting = True
        artists = []
        for artist in tl_track.track.artists:
            artists.append(artist.name)         
        
        try:
            message = json.dumps({ 
                "auth_token": self.auth_token,
                "title" : "Currently playing",
                "song": tl_track.track.name,
                "details": "%s - %s" % ("/".join(artists), tl_track.track.album.name)
            })

            logger.info(message)
            self.send(message)
        except AttributeError:
            logger.info("No track details to send")

            message = json.dumps({ 
                "auth_token": self.auth_token,
                "title" : "Currently playing",
                "song": "Unknown track",
                "details": ""
            })

            logger.info(message)
            self.send(message)

    def track_playback_ended(self, tl_track, time_position):
        sleep(1)
        if not self.starting:
            message = json.dumps({
                "auth_token": self.auth_token,
                "title": "Music stopped",
                "song": "",
                "details": ""
            })
            logger.info(message)
            self.send(message)
        else:
            self.starting = False
        
