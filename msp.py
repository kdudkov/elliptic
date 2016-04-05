#!/usr/bin/env python
# coding: utf-8

import logging
import os
import time

import serial

log = logging.getLogger(__name__)


def find_mac_port():
    for f in os.listdir('/dev'):
        if f.startswith('tty.uart-'):
            log.info('found port /dev/%s', f)
            return '/dev/' + f


class Stepper(object):
    def __init__(self, m, port=None, fn=None):
        self.steps = 0
        self.m = m
        self.port = port or find_mac_port()
        self.fn = fn

    def start(self):
        self.steps = 0
        self.time = 0
        self.last_step = 0
        self.w = 0
        self.kal = 0
        self.start_time = time.time()

    def process_data(self, s):
        if ';' not in s:
            return
        now = time.time()
        dt = 0
        if self.last_step != 0:
            dt = now - self.last_step
            self.time += dt
        else:
            self.start_time = now
        self.last_step = now

        self.lvl, dts = [int(x) for x in s.split(';', 2)]
        # self.lvl = 4
        self.steps += 2
        rpm = 60000. / dts
        p = rpm / 4 * self.lvl
        self.w += p * dt
        cal = self.w / 3600 * 860.42
        data = dict(steps=self.steps, time=int(now), level=self.lvl, rpm=rpm, p=p, w=self.w, cal=cal)
        if self.fn:
            self.fn(data)

    def run(self):
        log.info('start')
        self.start()
        if not self.port:
            print 'port not found!'
            return
        ser = serial.Serial(self.port, 9600)
        while 1:
            s = ser.readline().strip()
            log.debug('got: %s', s)
            try:
                self.process_data(s)
            except:
                log.exception('error')

def p(d):
    print d

if __name__ == '__main__':
    Stepper(102, fn=p).run()
