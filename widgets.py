
import pygame

LIGHT_BLUE = (13, 177, 232)
DARK_BLUE = (0, 89, 116)
ORANGE = (253, 176, 18)
GREEN = (139, 193, 117)


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

    def __init__(self, x=0, y=0, w=256, h=256):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def draw(self):
        pass

    def put(self, scr):
        scr.fill(self.bg_color, (self.x, self.y, self.w, self.h))
        surf = self.draw()
        if surf:
            scr.blit(surf, (self.x, self.y))


class Digit(Widget):
    color = DARK_BLUE

    def __init__(self, data, key, frm, x=0, y=0, w=256, h=256):
        self.data = data
        self.key = key
        self.frm = frm
        self.font = pygame.font.Font('fonts/trench100free.ttf', 72)
        Widget.__init__(self, x, y, w, h)

    def draw(self):
        x = 5
        y = 5
        s = pygame.Surface((self.w, self.h))
        if self.key in self.data:
            val = self.frm % self.data[self.key]
        else:
            val = '?'
        s.fill(self.bg_color)
        mid_text(s, self.font, [self.key, val], self.color, self.bg_color)
        return s


class TimeDigit(Widget):
    color = DARK_BLUE

    def __init__(self, data, x=0, y=0, w=256, h=256):
        self.data = data
        self.font = pygame.font.Font('fonts/trench100free.ttf', 72)
        Widget.__init__(self, x, y, w, h)

    def draw(self):
        x = 5
        y = 5
        s = pygame.Surface((self.w, self.h))
        t = self.data['sum_time']
        s.fill(self.bg_color)
        mid_text(s, self.font, ['Time', '%d:%02d' % (int(t/60), t % 60)], self.color, self.bg_color)
        return s


class LevelBar(Widget):

    bg_color = (0, 0, 0)

    def __init__(self, data, x=0, y=0, w=256, h=256):
        self.data = data
        self.font = pygame.font.Font('fonts/trench100free.ttf', 128)
        Widget.__init__(self, x, y, w, h)

    def draw(self):
        margin = 10
        btw = 4

        h = (self.h - 2 * margin + btw) / 16 - btw
        w = 3 * h

        x = margin * 4
        y = self.h - margin - h

        val = self.data.get('level', 1)
        s = pygame.Surface((self.w, self.h))
        s.fill(self.bg_color)
        for i in range(16):
            if i < val:
                pygame.draw.rect(s, DARK_BLUE, (x, y, w, h), 0)
            pygame.draw.rect(s, LIGHT_BLUE, (x, y, w, h), 1)
            y -= h + btw
        s1 = self.font.render(str(val), 1, DARK_BLUE, self.bg_color)
        x += w + margin * 2
        y = (self.h - s1.get_height()) / 2
        s.blit(s1, (x, y))

        return s
