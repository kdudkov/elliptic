
import pygame

LIGHT_BLUE = (13, 177, 232)
DARK_BLUE = (0, 89, 116)
ORANGE = (253, 176, 18)
GREEN = (139, 193, 117)

b1 = 0, 156, 204
b2 = 0, 78, 102

o1 = 255, 172, 0
o2 = 153, 103, 0

g1 = 155, 204, 139
g2 = 77, 102, 69

r1 = 230, 46, 46
r2 = 153, 31, 31

gray = 100, 100, 100


def mid_text(surf, font, text, color, bgcolor, btw=2):
    s1 = font.render('A', 1, color)
    h1 = s1.get_height()
    y = (surf.get_height() - len(text) * h1 - (len(text) - 1) * btw) / 2
    if y < 0:
        y = btw
    for s in text:
        s1 = font.render(s, 1, color, bgcolor)
        x = max((surf.get_width() - s1.get_width()) / 2, btw)

        surf.blit(s1, (x, y))
        y += s1.get_height() + btw


class Widget(object):
    bg_color = (10, 10, 10)
    x = 0
    y = 0
    data = {}
    last_data = None

    def __init__(self, w=256, h=256):
        self.w = w
        self.h = h

    def get_data(self):
        return None

    def draw(self, force=False):
        val = self.get_data()
        if force or val != self.last_data:
            self.last_data = val
            return self.get_surface(val)
        return None

    def get_surface(self, val):
        pass

    def put(self, scr):
        surf = self.draw()
        if surf:
            scr.blit(surf, (self.x, self.y))


class Digit(Widget):
    color = DARK_BLUE

    def __init__(self, key, frm, label=None, w=256, h=256):
        self.key = key
        self.frm = frm
        self.label = label
        self.font = pygame.font.Font('fonts/trench100free.ttf', 72)
        Widget.__init__(self, w, h)

    def get_data(self):
        return self.frm % self.data[self.key] if self.key in self.data else '?'

    def get_surface(self, val):
        s = pygame.Surface((self.w, self.h))
        s.fill(self.bg_color)
        mid_text(s, self.font, [self.label or self.key, val], self.color, self.bg_color)
        return s


class TimeDigit(Widget):
    color = DARK_BLUE

    def __init__(self, w=256, h=256):
        self.font = pygame.font.Font('fonts/trench100free.ttf', 72)
        Widget.__init__(self, w, h)

    def get_data(self):
        t = self.data['sum_time']
        return '%d:%02d' % (int(t / 60), t % 60)

    def get_surface(self, val):
        s = pygame.Surface((self.w, self.h))
        s.fill(self.bg_color)
        mid_text(s, self.font, ['Time', val], self.color, self.bg_color)
        return s


class LevelBar(Widget):

    bg_color = (0, 0, 0)

    def __init__(self, w=256, h=256):
        self.font = pygame.font.Font('fonts/trench100free.ttf', 128)
        Widget.__init__(self, w, h)

    def get_data(self):
        return self.data.get('level', 1)

    def get_surface(self, val):
        s = pygame.Surface((self.w, self.h))
        s.fill(self.bg_color)

        margin = 10
        btw = 4

        h = (self.h - 2 * margin + btw) / 16 - btw
        w = 3 * h

        x = margin * 4
        y = self.h - margin - h
        for i in range(16):
            c1, c2 = [(b1, b2), (g1, g2), (o1, o2), (r1, r2)][int(i / 4)]
            if i < val:
                pygame.draw.rect(s, c2, (x, y, w, h), 0)
                pygame.draw.rect(s, c1, (x, y, w, h), 1)
            else:
                pygame.draw.rect(s, gray, (x, y, w, h), 1)

            y -= h + btw
        _, c2 = [(b1, b2), (g1, g2), (o1, o2), (r1, r2)][int((val - 1) / 4)]
        s1 = self.font.render(str(val), 1, c2, self.bg_color)
        x += w + margin * 2
        y = (self.h - s1.get_height()) / 2
        s.blit(s1, (x, y))

        return s
