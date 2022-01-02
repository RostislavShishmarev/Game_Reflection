import pygame as pg
import pygame.draw as dr
import pygame.transform as tr
from functions import do_nothing, load_image


class BaseWidget:
    def __init__(self, parent, rect):
        self.parent = parent
        x, y, w, h = rect
        self.x, self.y, self.x1, self.y1 = x, y, x + w, y + h
        self.w, self.h = w, h

    def render(self, screen=None):
        pass

    def __contains__(self, coords):
        return coords[0] in range(self.x, self.x1) and\
               coords[1] in range(self.y, self.y1)

    def process_event(self, event, *args, **kwargs):
        pass


class Button(BaseWidget):
    def __init__(self, parent, rect, text, font_size=40,
                 main_color=pg.Color(70, 202, 232),
                 back_color=pg.Color(0, 0, 0), slot=do_nothing, text2=None,
                 key=None, modifier=None):
        super().__init__(parent, rect)
        self.function = slot

        self.text = text
        self.text2 = text2 if text2 is not None else text
        self.current_text = self.text
        self.font_size = font_size

        self.main_color = main_color
        self.light_main_color = pg.Color(min(self.main_color.r + 90, 255),
                                         min(self.main_color.g + 90, 255),
                                         min(self.main_color.b + 90, 255))
        self.current_color = self.main_color
        self.back_color = back_color

        self.key = key
        self.modifier = modifier

    def slot(self, *args, **kwargs):
        # Декорация переданной функции:
        self.current_text = self.text if self.current_text == self.text2\
            else self.text2

        self.function(*args, **kwargs)

    def render(self, screen=None):
        screen = screen if screen is not None else self.parent.screen
        dr.rect(screen, self.back_color,
                (self.x, self.y, self.w, self.h))
        dr.rect(screen, self.current_color,
                (self.x, self.y, self.w, self.h), width=2)
        font = pg.font.Font(None, self.font_size)
        text = font.render(self.current_text, True, self.current_color)
        screen.blit(text, (self.x + self.w // 2 - text.get_width() // 2,
                           self.y + self.h // 2 - text.get_height() // 2))

    def process_event(self, event, *args, **kwargs):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.pos in self:
                self.slot(*args, **kwargs)
        if event.type == pg.KEYDOWN and self.key is not None:
            if event.key == self.key:
                if self.modifier is not None:
                    if event.mod & self.modifier:
                        self.slot(*args, **kwargs)
                else:
                    self.slot(*args, **kwargs)
        if event.type == pg.MOUSEMOTION:
            if event.pos in self:
                self.current_color = self.light_main_color
            else:
                self.current_color = self.main_color


class TextDisplay(BaseWidget):
    def __init__(self, parent, rect, title, text_item,
                 title_font_size=40, item_font_size=70,
                 main_color=pg.Color(239, 242, 46),
                 back_color=pg.Color(0, 0, 0), image=None):
        super().__init__(parent, rect)
        self.item = text_item
        self.title = title
        self.title_font_size = title_font_size
        self.item_font_size = item_font_size
        self.main_color = main_color
        self.back_color = back_color
        self.image = image

    def render(self, screen=None):
        screen = screen if screen is not None else self.parent.screen
        dr.rect(screen, self.back_color,
                (self.x, self.y, self.w, self.h), border_radius=8)
        dr.rect(screen, self.main_color,
                (self.x, self.y, self.w, self.h), width=2, border_radius=8)

        title_font = pg.font.Font(None, self.title_font_size)
        title = title_font.render(self.title, True, self.main_color)
        screen.blit(title, (self.x + self.w // 2 - title.get_width() // 2,
                            self.y + 5))

        item_font = pg.font.Font(None, self.item_font_size)
        item = item_font.render(self.item, True, self.main_color)
        item_x = self.x + self.w // 2 - item.get_width() // 2
        if self.image is not None:
            item_x = self.x + self.w - item.get_width() - self.w // 8
            im = tr.scale(load_image('Platform.png', -1), (5 * self.w // 8,
                                                           item.get_height()))
            screen.blit(im, (self.x + round(self.w // 8),
                        self.y + self.h - item.get_height() - 10))
        screen.blit(item, (item_x, self.y + self.h - item.get_height() - 5))

    def set_item(self, item):
        self.item = item

    def process_event(self, event):
        pass


class TabWidget(BaseWidget):
    def __init__(self, parent, rect, titles, titles_h=40,
                 title_font_size=30,
                 main_color=pg.Color(20, 224, 54),
                 back_color=pg.Color(0, 0, 0)):
        super().__init__(parent, rect)
        self.main_color = main_color
        self.light_main_color = pg.Color(min(self.main_color.r + 90, 255),
                                         min(self.main_color.g + 90, 255),
                                         min(self.main_color.b + 90, 255))
        self.current_color = self.main_color
        self.back_color = back_color

        self.rects_w = 2
        self.bord_rad = 6
        self.text_indent = 10

        self.titles_names = titles
        self.selected_index = 0
        self.titles_h = titles_h
        self.title_font_size = title_font_size
        self.widgets = []
        x, y = self.x + 10, self.y
        for i, ttl in enumerate(self.titles_names):
            title_font = pg.font.Font(None, self.title_font_size)
            title = title_font.render(ttl, True, self.main_color)
            w, h = title.get_width() + self.text_indent * 2, self.titles_h
            self.widgets.append([[], Button(self.parent, (x, y, w, h), ttl,
                                            font_size=self.title_font_size,
                                            main_color=self.main_color,
                                            slot=self.change_selected)])
            x += w + self.rects_w * 2

    def render(self, screen=None):
        screen = screen if screen is not None else self.parent.screen
        dr.rect(screen, self.back_color,
                (self.x, self.y + self.titles_h - self.rects_w // 2,
                 self.w, self.h - self.titles_h + self.rects_w // 2),
                border_radius=self.bord_rad)
        dr.rect(screen, self.main_color,
                (self.x, self.y + self.titles_h - self.rects_w // 2,
                 self.w, self.h - self.titles_h + self.rects_w // 2),
                width=self.rects_w, border_radius=self.bord_rad)
        for i, title in enumerate(self.titles_names):
            self.widgets[i][1].render()
            if i == self.selected_index:
                self.surface = pg.Surface((self.w,
                                           self.h - self.titles_h +\
                                           self.rects_w // 2), pg.SRCALPHA, 32)
                self.surface.fill(pg.Color(0, 0, 0, 1))
                for widget in self.widgets[i][0]:
                    widget.render(screen=self.surface)
                pg.Surface.blit(screen, self.surface, (self.x,
                                                       self.y + self.titles_h -\
                                                       self.rects_w // 2))

    def process_event(self, event):
        for i, title in enumerate(self.titles_names):
            self.widgets[i][1].process_event(event, i)
            for widget in self.widgets[i][0]:
                widget.process_event(event)

    def change_selected(self, index):
        self.selected_index = index
    
    def get_widgets(self, index):
        return self.widgets[index][0]

    def set_widgets(self, index, widgets):
        self.widgets[index][0] = widgets

    def add_widget(self, index, widget):
        self.widgets[index][0].append(widget)
