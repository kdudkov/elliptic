#!/usr/bin/env python
# coding: utf-8

import time
import os
from datetime import datetime as dt
import threading
import logging

import pygame

from msp import Stepper
from widgets import Digit, TimeDigit, LevelBar

log = logging.getLogger(__name__)


class Main(object):
    running = True
    widgets = []
    file = None
    keys = 'time,level,steps,rpm,p,w,kal'.split(',')

    def __init__(self):
        self.screen = pygame.display.set_mode((1024, 768))
        self.data = {'sum_time': 0}
        self.last_data = 0
        if not os.path.exists('data'):
            os.makedirs('data')
        pygame.init()
        pygame.font.init()

        self.stepper = Stepper(102, fn=self.got_data)

        y = 0
        self.widgets.append(LevelBar(self.data, x=0, y=y))
        self.widgets.append(Digit(self.data, 'rpm', '%.1f', x=256, y=y))

        y += 256
        self.widgets.append(TimeDigit(self.data, x=0, y=y))
        self.widgets.append(Digit(self.data, 'steps', '%.d', x=256, y=y))
        self.widgets.append(Digit(self.data, 'p', u'%.1f Вт', x=512, y=y))

    def got_data(self, d):
        log.debug('got data %s', d)
        self.data.update(d)
        now = time.time()
        if now - self.last_data < 5:
            self.data['sum_time'] = self.data['sum_time'] + (now - self.last_data)
        self.last_data = now
        if self.file:
            self.file.write(','.join((self.data.get(x, '') for x in self.keys)) + '\n')

    def run(self):
        self.thread = threading.Thread(target=self.stepper.run)
        self.thread.daemon = True
        self.thread.start()
        fname = 'data/%s.csv' % dt.now().strftime('%Y%m%d%H%M')
        with open(fname, 'w') as self.file:
            self.file.write(','.join(self.keys) + '\n')
            self.loop()

    def loop(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    self.keypress(event)
            pygame.event.pump()
            self.draw_all()
            time.sleep(0.01)

    def keypress(self, event):
        if event.unicode == u'q':
            self.running = False
        print event.unicode

    def draw_all(self):
        for i in self.widgets:
            i.put(self.screen)
        pygame.display.flip()


if __name__ == '__main__':
    logging.basicConfig(level='INFO')
    Main().run()
