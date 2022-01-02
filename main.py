import pygame as pg
import pygame.transform as tr

from functions import load_image
from gamewindow import GameWindow


class Levels:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.x = width
        self.y = height

    def buttons_lvl(self):
        n = 55
        for i in range(2):
            Buttons(self.screen, self.x + n, self.y + n,
                    text='Уровень {}'.format(i + 1),
                    text_color=(255, 91, 0), light_text_color=(255, 181, 90),
                    back_color=(0, 0, 0),
                    light_back_color=(20, 20, 20)).text_btn()
            n += 75

    def window_lvl(self):
        font = pg.font.Font(None, 50)
        text = font.render("Уровни", True, (255, 91, 0))
        w = text.get_width()
        h = text.get_height()
        pg.draw.rect(self.screen, (0, 0, 0),
                         (self.x - 5, self.y - 10, w + 250, h + 490),
                         border_radius=8)
        table = pg.draw.rect(self.screen, (255, 91, 0),
                             (self.x - 5, self.y - 10, w + 250, h + 490), 2,
                             border_radius=8)
        self.screen.blit(text, (self.x + 120, self.y))


class Buttons:
    def __init__(self, screen, width, height, color=None,
                 light_color=None, image_size=None, image=None,
                 light_image=None, text=None,
                 text_color=None, light_text_color=None,
                 back_color=None, light_back_color=None):
        self.screen = screen
        self.x = width
        self.y = height
        if image is not None:
            self.color = color
            self.light_color = light_color
            self.image = image
            self.light_image = light_image
            self.image_size = image_size
        if text is not None:
            self.text = text
            self.text_color = text_color
            self.light_text_color = light_text_color
            self.back_color = back_color
            self.light_back_color = light_back_color

    def image_btn(self):
        settings = tr.scale(load_image(self.image), self.image_size)
        settings1 = tr.scale(load_image(self.light_image), self.image_size)
        w = settings.get_width()
        h = settings.get_height()
        rect = pg.draw.rect(self.screen, self.color,
                                (self.x - 2, self.y - 2, w + 4, h + 4), 2)
        self.screen.blit(settings, (self.x, self.y))
        if rect.collidepoint(pg.mouse.get_pos()):
            pg.draw.rect(self.screen, self.light_color,
                             (self.x - 2, self.y - 2, w + 4, h + 4), 2)
            self.screen.blit(settings1, (self.x, self.y))
        return rect
        # цвет - (100, 255, 100), цвет2 - (70, 202, 232)

    def text_btn(self):
        font = pg.font.Font(None, 50)
        text = font.render(self.text, True, self.text_color)
        text1 = font.render(self.text, True, self.light_text_color)
        w = text.get_width()
        h = text.get_height()
        pg.draw.rect(self.screen, self.back_color,
                         (self.x - 10, self.y - 10, w + 20, h + 25))
        rect = pg.draw.rect(self.screen, self.text_color,
                                (self.x - 10, self.y - 10, w + 20, h + 25), 2)
        self.screen.blit(text, (self.x, self.y))
        if rect.collidepoint(pg.mouse.get_pos()):
                pg.draw.rect(self.screen, self.light_back_color,
                                 (self.x - 10, self.y - 10, w + 20, h + 25))
                pg.draw.rect(self.screen, self.light_text_color,
                                 (self.x - 10, self.y - 10, w + 20, h + 25), 2)
                self.screen.blit(text1, (self.x, self.y))
        return rect


class MainWindow:
    def __init__(self):
        self.size = self.width, self.height = 1240, 700
        self.FPS = 60
        # Флаг
        self.running = True

    def run(self):
        pg.init()
        # Экран
        screen = pg.display.set_mode(self.size)

        # Иконка
        pg.display.set_caption('Отражение')
        pg.display.set_icon(load_image('Reflection_logo.png'))

        # Атрибуты:
        self.fone = tr.scale(load_image('Fone.png'), (1240, 700))
        self.cursor = load_image('Cursor.png')
        self.clock = pg.time.Clock()

        # Виджеты:
        self.settings_button = Buttons(screen, self.width - 105,
                                       self.height - 690,
                                       color=(100, 255, 100),
                                       light_color=(150, 255, 150),
                                       image_size=(90, 90),
                                       image='Settings.png',
                                       light_image='Settings_light.png')
        self.play_button = Buttons(screen, self.width - 220,
                                   self.height - 66, text='Играть',
                                   text_color=(70, 202, 232),
                                   light_text_color=(160, 255, 255),
                                   back_color=(0, 0, 0),
                                   light_back_color=(20, 20, 20))
        self.exit_button = Buttons(screen, self.width - 75,
                                   self.height - 75, color=(70, 202, 232),
                                   light_color=(160, 255, 255),
                                   image_size=(56, 56), image='Exit.png',
                                   light_image='Exit_light.png')

        # Флаги
        pg.mouse.set_visible(False)

        # Цикл
        while self.running:
            # Фон
            screen.blit(self.fone, (0, 0))

            # Цикл событий:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False

            # Кнопки
            rect_set = self.settings_button.image_btn()
            if rect_set.collidepoint(pg.mouse.get_pos()):
                if event.type == pg.MOUSEBUTTONDOWN:
                    pass
            rect_play = self.play_button.text_btn()
            if rect_play.collidepoint(pg.mouse.get_pos()):
                if event.type == pg.MOUSEBUTTONDOWN:
                    pass
            rect_exit = self.exit_button.image_btn()
            if rect_exit.collidepoint(pg.mouse.get_pos()):
                if event.type == pg.MOUSEBUTTONDOWN:
                    self.running = False

            # Линия
            pg.draw.line(screen, (255, 255, 255), [0, 150], [1240, 150], 2)

            # Уровни
            Levels(screen, self.width - 1220, self.height - 530).window_lvl()
            Levels(screen, self.width - 1220, self.height - 530).buttons_lvl()

            # Курсор
            if pg.mouse.get_focused():
                screen.blit(self.cursor, pg.mouse.get_pos())

            self.clock.tick(self.FPS)
            pg.display.flip()
        pg.quit()


if __name__ == '__main__':
    window = MainWindow()
    window.run()
