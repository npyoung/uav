#!/usr/bin/env python

import sys
import pprint
import requests
import xmltodict
from asciimatics.screen import Screen
from time import sleep

class HuaweiE3372(object):
    BASE_URL = 'http://{host}'
    COOKIE_URL = '/html/index.html'
    session = None

    def __init__(self, host='192.168.0.1'):
        self.host = host
        self.base_url = self.BASE_URL.format(host=host)
        self.session = requests.Session()
        # get a session cookie by requesting the COOKIE_URL
        r = self.session.get(self.base_url + self.COOKIE_URL)

    def get(self, path):
        return xmltodict.parse(self.session.get(self.base_url + path).text).get('response',None)

def main(screen):
    e3372 = HuaweiE3372()
    while True:
        for idx, (key, value) in enumerate(e3372.get('/api/device/signal').items()):
            screen.print_at(f"{key}:",
                            0, idx)
            screen.print_at(f"{value}",
                            12, idx)
        ev = screen.get_key()
        if ev in (ord('Q'), ord('q')):
            return
        screen.refresh()
        sleep(1)

if __name__ == "__main__":
    Screen.wrapper(main)
