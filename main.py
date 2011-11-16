#!/usr/bin/env python
#coding: utf-8
# Copyright 2011 ZYYX Inc.
#

# import GAE libraries
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.api import channel
from google.appengine.api import mail

# import std libs
import time
import random
import datetime
import pprint
import hashlib

# import application libs
import model

# import 3rd party libs
import tenjin
from tenjin.helpers import *

SERVICE_DOMAIN = "http://link-snap.appspot.com"

class Main(webapp.RequestHandler):
    def get(self):        
        self.response.out.write(tenjin.Template('view/index.tenjin').render())

class PhoneFrame(webapp.RequestHandler):
    def get(self):
        hash = self.request.get('hash')
        if hash.strip() == "":
            self.response.out.write('"hash" parameter missing.')
            return
        
        vars = {"hash": hash}
        self.response.out.write(tenjin.Template('view/phone_frame.tenjin').render(vars))

class Token(webapp.RequestHandler):
    def get(self):
        uname = self.request.get('user')
        token = channel.create_channel(uname)
        self.response.out.write('{"token": "' + token + '"}')

class Update(webapp.RequestHandler):
    def get(self):
        hash = self.request.get('hash')
        if hash.strip() == "":
            self.response.out.write('"hash" parameter missing.')
            return
            
        url = self.request.get('url')
        if url.strip() == "":
            self.response.out.write('"url" paramter missing.')
            return
            
        channel.send_message(hash, '{"url": "' + url + '"}')

class HashGen(webapp.RequestHandler):
    def get(self):
        hash = hashlib.md5(str(random.random()).encode('base64')).hexdigest()
        self.response.out.write('{"hash": "' + hash + '"}')

class MailAddr(webapp.RequestHandler):
    def get(self):
        email = self.request.get('email')
        if email.strip() == "":
            self.response.out.write('"email" parameter missing.')
            return
        hash = self.request.get('hash')
        if hash.strip() == "":
            self.response.out.write('"hash" parameter missing.')
            return
        mail.send_mail(
            sender = "noreply@link-snap.appspotmail.com",
            to = email,
            subject = "LinkSnap 待ち受け画面アドレス",
            body = tenjin.Template('view/mail_body.tenjin').render({
                "domain": SERVICE_DOMAIN,
                "hash": str(hash)
            })
        )
        self.response.out.write('{"result": 1}')

class LinkSnap(webapp.RequestHandler):
    def get(self):
        hash = self.request.get('hash')
        if hash.strip() == "":
            self.response.out.write('"hash" parameter missing.')
            return
        
        vars = {"hash": hash}
        self.response.out.write(tenjin.Template('view/linksnap.tenjin').render(vars))

class Receiver(webapp.RequestHandler):
    def get(self):
        hash = self.request.get('hash')
        if hash.strip() == "":
            self.response.out.write('"hash" parameter missing.')
            return

        vars = {"hash": hash}
        self.response.out.write(tenjin.Template('view/receiver.tenjin').render(vars))

def main():
    application = webapp.WSGIApplication(
        [
            ('/', Main),
            ('/phone_frame', PhoneFrame),
            ('/update', Update),
            ('/token', Token),
            ('/hashgen', HashGen),
            ('/mailaddr', MailAddr),
            ('/linksnap', LinkSnap),
            ('/receiver', Receiver),
        ],
        debug = True
    )
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()
