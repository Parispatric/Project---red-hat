import pygame
import sys
from random import randint
from settings import Settings

pygame.init()  # инициализация для качественной работы

setting = Settings()

screen = pygame.display.set_mode((setting.screen_widht, setting.screen_height))  # создание игровой поверхности
pygame.display.set_caption("Red Hat")  # Название окна
pygame.display.set_icon(pygame.image.load('images/icon.png'))  # Иконка игры

background = pygame.image.load("images/background.png")  # Задний фон игры
first_game = True

def instruction():
    global first_game
    if first_game:
        instruction = pygame.image.load('images/instruction.png')
        screen.blit(instruction, instruction.get_rect())
        pygame.display.update()
        pygame.time.delay(8000)
        first_game = False


def start_game():
    """Начальное меню"""
    play_image = pygame.image.load('images/buttom_play.png')  # Кнопка для начала игры
    play_image_rect = play_image.get_rect(topleft=(450, 100))

    level_image = pygame.image.load('images/buttom_level.png')  # Кнопка для выбора сложности
    level_image_rect = level_image.get_rect(topleft=(450, 300))

    quit_image = pygame.image.load('images/buttom_quit.png')  # Кнопка для выхода из игры
    quit_image_rect = quit_image.get_rect(topleft=(450, 500))

    setting.move_r = False
    setting.move_l = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if play_image_rect.collidepoint(pygame.mouse.get_pos()):
                        instruction()
                        game()
                    elif level_image_rect.collidepoint(pygame.mouse.get_pos()):
                        level()
                    elif quit_image_rect.collidepoint(pygame.mouse.get_pos()):
                        sys.exit()
        screen.blit(background, screen.get_rect())
        screen.blit(play_image, play_image_rect)
        screen.blit(level_image, level_image_rect)
        screen.blit(quit_image, quit_image_rect)
        pygame.display.update()


def game():

    pygame.time.set_timer(pygame.USEREVENT, setting.time)  # Установление таймера для появления пирожков
    clock = pygame.time.Clock()  # для воспроизведения кадров в секунду


    pie_with_wolf = pygame.image.load('images/pie_with_wolf.png').convert_alpha()  # подгрузка изображения с пирожком 1
    pie_with_wolf.set_colorkey((255, 255, 255))

    pie_default = pygame.image.load('images/pie.png').convert_alpha()  # подгрузка изображения с пирожком 2
    pie_default.set_colorkey((255, 255, 255))

    TYPE_PIE = [pie_default, pie_with_wolf]  # типы пирожков

    count_life = 5  # Счетчик жизней
    count_point = 0  # Счетчик пойманых

    def text_create(count_life, count_point):
        f1 = pygame.font.SysFont('bahnschrift', 36)
        t1 = f"Количество жизней: {count_life}"
        text_life = f1.render(t1, True, (0, 0, 0))

        f2 = pygame.font.SysFont('bahnschrift', 36)
        t2 = f"Количество очков: {count_point}"
        text_point = f2.render(t2, True, (0, 0, 0))
        return text_life, text_point

    class Red_hat(pygame.sprite.Sprite):
        """Главный герой"""

        def __init__(self, im):
            super().__init__()
            self.image = im
            self.image.set_colorkey((255, 255, 255))  # Удаление белого цвета с главного персонажа
            self.f = self.image
            self.f.set_colorkey((255, 255, 255))
            self.rect = self.image.get_rect(center=(600, 736))  # Создание Rect г.г. и размещение его

        def move(self):
            """Движение игрока"""
            if setting.move_r and self.rect.right < 1200:
                self.image = self.f
                self.image.set_colorkey((255, 255, 255))  # Удаление белого цвета с главного персонажа
                self.rect.x += setting.red_hat_speed
            if setting.move_l and self.rect.x > 0:
                self.image = pygame.transform.flip(self.f, True, False)
                self.image.set_colorkey((255, 255, 255))
                self.rect.x -= setting.red_hat_speed

    class Pie(pygame.sprite.Sprite):
        """Класс для пирожков"""

        def __init__(self, x, type, group):
            super().__init__()
            self.image = type
            self.rect = self.image.get_rect(center=(x, 0))
            self.add(group)

        def update(self):
            if self.rect.y < 800:
                self.rect.y += setting.speed_pie
            else:
                self.kill()

    first_fase = pygame.image.load('images/red_hat.png')
    first_fase.set_colorkey((255, 255, 255))
    second_fase = pygame.image.load('images/red_hat1.png')
    second_fase.set_colorkey((255, 255, 255))

    IMAGES_RED_HAT = [first_fase, second_fase]
    red_hat = Red_hat(IMAGES_RED_HAT[1])  # главный герой 1
    red_hat_two = Red_hat(IMAGES_RED_HAT[0])  # главный герой 2

    pies = pygame.sprite.Group()  # группа для пирожков
    Pie(randint(50, 1150), TYPE_PIE[randint(0, 1)], pies)  # добавление первого пирожка

    def foot():
        red_hat.move()  # Передвижение главного героя
        red_hat_two.move()  # Передвижение главного героя
        if setting.fase >= 10 and (setting.move_l or setting.move_r):
            setting.fase += 1
            screen.blit(red_hat.image, red_hat.rect)  # Отрисовка на главном экране персонажа
            if setting.fase == 20:
                setting.fase = 0
        elif setting.fase < 10 and (setting.move_l or setting.move_r):
            setting.fase += 1
            screen.blit(red_hat_two.image, red_hat_two.rect)  # Отрисовка на главном экране персонажа
        else:
            if setting.fase >= 10:
                screen.blit(red_hat.image, red_hat.rect)  # Отрисовка на главном экране персонажа
            else:
                screen.blit(red_hat_two.image, red_hat_two.rect)  # Отрисовка на главном экране персонажа

    def lose():
        """Для проигрыша"""
        lose = pygame.image.load('images/lose.png')  # Загрузка изображения проигрыша
        flag_lose = False
        play_again = pygame.image.load('images/again.png')  # Зарузка изображения кнопки
        rect_play_again = play_again.get_rect(center=(600, 500))  # Прямоугольник кнопки
        screen.blit(lose, lose.get_rect())  # Отображение изображения проигрыша
        screen.blit(play_again, rect_play_again)  # Отображение кнопки
        pygame.display.update()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if rect_play_again.collidepoint(pygame.mouse.get_pos()):
                            flag_lose = True
                            break
            if flag_lose:
                break
        start_game()  # Запуск заново

    while True:
        """Игровой процесс"""
        for event in pygame.event.get():  # получение событий
            if event.type == pygame.QUIT:
                sys.exit()  # Завершение игры
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    setting.move_l = True
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    setting.move_r = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    setting.move_l = False
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    setting.move_r = False
            if event.type == pygame.USEREVENT:
                Pie(randint(0, 1200), TYPE_PIE[randint(0, 1)], pies)

        screen.blit(background, background.get_rect())  # Отрисовка на главном экране отрисовка фона
        pies.draw(screen)  # отрисовка каждого пирожка
        pies.update()  # обновление каждого пирожка
        if pygame.sprite.spritecollideany(red_hat, pies):
            list_collideany = pygame.sprite.spritecollide(red_hat, pies, False)
            for sprite in list_collideany:
                if sprite.image == pie_with_wolf:
                    count_life -= 1
                else:
                    count_point += 1
                sprite.kill()
        if count_life == 0:
            lose()
        text_life, text_point = text_create(count_life, count_point)
        screen.blit(text_life, (0, 50))
        screen.blit(text_point, (0, 150))
        clock.tick(setting.FPS)  # установление кадров в секунду
        foot()
        pygame.display.update()  # Обновление экрана


def level():
    """Выбор уровня"""
    one_image = pygame.image.load('images/first_level.png')  # Кнопка 1 сложности
    one_image_rect = one_image.get_rect(topleft=(450, 100))

    two_image = pygame.image.load('images/two_level.png')  # Кнопка 2 сложности
    two_image_rect = two_image.get_rect(topleft=(450, 300))

    three_image = pygame.image.load('images/three_level.png')  # Кнопка 3 сложности
    three_image_rect = three_image.get_rect(topleft=(450, 500))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if pygame.mouse.get_focused():
                        if one_image_rect.collidepoint(pygame.mouse.get_pos()):
                            setting.speed_pie = 4
                            start_game()
                        elif two_image_rect.collidepoint(pygame.mouse.get_pos()):
                            setting.speed_pie = 4
                            setting.time = 500
                            start_game()
                        elif three_image_rect.collidepoint(pygame.mouse.get_pos()):
                            setting.speed_pie = 6
                            setting.time = 300
                            start_game()
        screen.blit(background, screen.get_rect())
        screen.blit(one_image, one_image_rect)
        screen.blit(two_image, two_image_rect)
        screen.blit(three_image, three_image_rect)
        pygame.display.update()




while True:
    start_game()
    screen.blit(background, screen.get_rect())
    pygame.display.update()
