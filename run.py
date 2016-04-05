#!/usr/bin/env python
# coding: utf-8

import logging
import os
import threading
import time
from datetime import datetime as dt

import pygame

from msp import Stepper
from widgets import Digit, TimeDigit, LevelBar

log = logging.getLogger(__name__)


class Main(object):
    running = True
    widgets = []
    x = 0
    y = 0
    file = None
    keys = 'time,level,steps,rpm,p,w,cal'.split(',')

    def __init__(self):
        self.screen = pygame.display.set_mode((1024, 768))
        self.data = {'sum_time': 0}
        self.last_data = 0
        if not os.path.exists('data'):
            os.makedirs('data')
        pygame.init()
        pygame.font.init()

        self.stepper = Stepper(102, fn=self.got_data)

        self.add_new(LevelBar())
        self.add_new(Digit('rpm', '%.1f', label='RPM'))
        self.add_new(TimeDigit())

        self.add_new_row(Digit('steps', '%.d', label='Steps'))
        self.add_new(Digit('p', u'%.1f', label='Wt'))
        self.add_new(Digit('cal', u'%.0f'))

    def add_new(self, widget):
        self.widgets.append(widget)
        widget.data = self.data
        if self.x + widget.w > self.screen.get_width():
            self.x = 0
            self.y += widget.h
        widget.x = self.x
        widget.y = self.y
        self.x += widget.w

    def add_new_row(self, widget):
        self.widgets.append(widget)
        self.x = 0
        self.y += widget.h
        widget.data = self.data
        widget.x = self.x
        widget.y = self.y
        self.x += widget.w

    def got_data(self, d):
        log.debug('got data %s', d)
        self.data.update(d)
        now = time.time()
        if now - self.last_data < 5:
            self.data['sum_time'] = self.data['sum_time'] + (now - self.last_data)
        self.last_data = now
        if self.file:
            self.file.write(','.join((str(self.data.get(x, '')) for x in self.keys)) + '\n')

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
