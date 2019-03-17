import pygame
import random
import math

# --------------------------------------------------------
# ----------------Глобальные переменные-------------------
# --------------------------------------------------------
done = False
# пропускает 1-ну итерацию удаления блоков,так-как нечего удалять, еще не создало
acess_to_clearing = False
# переменная отвечающая за всё на экране относителньо статического игрока
global_x = 0
global_y = 0
# для рандома координат блоков
wall_list_of_x = []
wall_list_of_y = []
# для рандома координат леких врагов
enemy_list_of_x = []
enemy_list_of_y = []
# Цвета
black = (0, 0, 0)
white = (255, 255, 255)
blue = (50, 50, 255)
red = (255, 0, 0)
bolot = (60, 200, 85)
dpurple = (70, 2, 90)  # темно-фиолетовый
ber = (25, 170, 175)  # березовый
lber = (9, 220, 190)  # светлый березовый
lroze = (255, 170, 175)  # легкий розовый
# разрешение экрана
screen_width = 1200
screen_height = 600
# список снежинок
snow_list = []
# переменная заработанных очков
score = 0


# ------------------------------------------------------------------------
# --------------------------------КЛАССЫ----------------------------------
# ------------------------------------------------------------------------

# класс персонажа
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # задаем размер спрайту - высота,ширина
        self.image = pygame.Surface([15, 15])
        self.image.fill(white)
        # начальные координаты предмета
        self.rect = self.image.get_rect()
        self.rect.x = 600
        self.rect.y = 300
        # Скорость по осям.
        self.change_x = 0
        self.change_y = 0

    def changespeed(self, x, y):
        """ Скорость предмета.Оно нужно чтобы оно скользило, а не рывками """
        self.change_x += x
        self.change_y += y

    def block_hit_l(self):
        """ Липкий блок"""
        # Если игрок дотронется до блока,True-False - исчезнуть блоку, или нет
        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        for block in block_hit_list:
            if self.change_x > 0 or self.change_y > 0:
                self.rect.right = block.rect.left
                self.change_x = 0
                self.rect.bottom = block.rect.top
                self.change_y = 0
            if self.change_x < 0 or self.change_y < 0:
                self.rect.left = block.rect.right
                self.change_x = 0
                self.rect.top = block.rect.bottom
                self.change_y = 0

    def hit_enemyes(self):
        """Противники"""
        # если дотронется до противников
        enemy_hit_list = pygame.sprite.spritecollide(self, self.enemyes, False)
        for enemy in enemy_hit_list:
            if self.change_x > 0 or self.change_y > 0:
                self.rect.right = enemy.rect.left
                self.change_x = 0
                self.rect.bottom = enemy.rect.top
                self.change_y = 0
                print("Looooooooser!")
            if self.change_x < 0 or self.change_y < 0:
                self.rect.left = enemy.rect.right
                self.change_x = 0
                self.rect.top = enemy.rect.bottom
                self.change_y = 0

    def focus_camera(self):
        self.rect.x = 600
        self.rect.y = 300

    def moving_all_without_player(self):
        """эти две нелюбимые переменные везде используются,
         для движения всего относительно стоячего игрока"""
        global global_x
        global global_y
        if player.rect.x > 0:
            global_x -= player.change_x
        elif player.rect.x < 0:
            global_x += player.change_x
        # ---------------------------
        if player.rect.y > 0:
            global_y -= player.change_y
        elif player.rect.y < 0:
            global_y += player.change_y


# Класс препятствий
class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        super().__init__()

        # создаем болотистую стену с размером по высоте и ширине
        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        # Задаем местоположение на экране
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


# Класс противников(легких)
class Easy_enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        super().__init__()
        # задаем размер спрайту - высота,ширина
        self.image = pygame.Surface([width, height])
        self.image.fill(lroze)
        # начальные координаты предмета
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def enemy_folowing(self, start_x, end_x, start_y, end_y, speed_x_y):
        # по оси Х:
        self.rect.x = start_x
        self.rect.y = start_y
        # Из-за формул, возможно появление точки,позже эту переменную позже изменим на целочисленную
        self.floating_point_x = start_x
        self.floating_point_y = start_y
        x_diff = end_x - start_x
        y_diff = end_y - start_y
        angle = math.atan2(y_diff, x_diff)
        self.speed_x_y = speed_x_y
        self.change_x = math.cos(angle) * self.speed_x_y
        self.change_y = math.sin(angle) * self.speed_x_y

        global global_x, global_y

        # обновление координаты пули, после всех высчитываний
        self.floating_point_y += self.change_y
        self.floating_point_x += self.change_x
        # Преображение в целочисленный тип
        self.rect.y = int(self.floating_point_y) + global_y
        self.rect.x = int(self.floating_point_x) + global_x


# Класс оружия
class Bullet(pygame.sprite.Sprite):
    def __init__(self, start_x, start_y, end_x, end_y, speed_x_y):
        super().__init__()

        # Задает ширину ,высоту,цвет пуле
        self.image = pygame.Surface([5, 5])
        self.image.fill(white)

        # Начальные координаты появления
        self.rect = self.image.get_rect()
        self.rect.x = start_x
        self.rect.y = start_y
        # Из-за формул, возможно появление точки,позже эту переменную позже изменим на целочисленную
        self.floating_point_x = start_x
        self.floating_point_y = start_y

        # создание угла между начальной координатой и конечной
        x_diff = end_x - start_x
        y_diff = end_y - start_y
        angle = math.atan2(y_diff, x_diff)

        # изменение по осям, с высчитыванием угла, а также скорость самой пули
        self.speed_x_y = speed_x_y
        self.change_x = math.cos(angle) * self.speed_x_y
        self.change_y = math.sin(angle) * self.speed_x_y

    def update(self):
        global global_x, global_y

        # обновление координаты пули, после всех высчитываний
        self.floating_point_y += self.change_y
        self.floating_point_x += self.change_x
        # Преображение в целочисленный тип
        self.rect.y = int(self.floating_point_y) + global_y
        self.rect.x = int(self.floating_point_x) + global_x

        # Если пуля зашла за экран
        if self.rect.x < 0 or self.rect.x > screen_width or self.rect.y < 0 or self.rect.y > screen_height:
            self.kill()


# ------------------------------------------------------------------------
# --------------------------------ФУНКЦИИ---------------------------------
# ------------------------------------------------------------------------

for i in range(50):
    x = random.randrange(0, 1200)
    y = random.randrange(0, 600)
    snow_list.append([x, y])


# функция снега
def snow_up():
    global global_x
    global global_y
    for i in range(len(snow_list)):
        # рисует круг, по координате, а потом по координате -1, и так двигает
        pygame.draw.circle(screen, lroze, snow_list[i], 2)
        # меняет местоположение снежинки(скорость),направление
        snow_list[i][1] -= 1
        # если снег зашел за экран ( вверх)
        if snow_list[i][1] == 0:
            # новая позиция игрика
            y = random.randrange(401, 402)
            snow_list[i][1] = y


# функция заднего фона
def background():
    # градиент
    for y_offset in range(0, 250, 1):
        grber = (255 - y_offset, 170, 175)  # gr - градиент
        pygame.draw.line(screen, grber, [0, 600 - (2.35 * y_offset)],
                         [1200, 600 - (2.35 * y_offset)], 40)


# функция вывода очков
def fonts(score):
    # Шрифт,размер,полужирный,курсив
    font = pygame.font.SysFont('Calibri', 25, True, False)
    # Сам текст,сглаженность,цвет
    text = font.render("Score: " + str(score), True, white)
    # Л-В-яя координата
    screen.blit(text, [1100, 15])


pygame.init()
screen = pygame.display.set_mode([screen_width, screen_height])
pygame.display.set_caption('\n My game alpha 0.11b')
# ---------------------------------------------------------
# создание списков спрайтов
# ---------------------------------------------------------
all_sprite_list = pygame.sprite.Group()
wall_list = pygame.sprite.Group()
enemy_list = pygame.sprite.Group()
bullet_list = pygame.sprite.Group()
# ---------------------------------------------------------
# создание главного персонажа
# ---------------------------------------------------------
player = Player()
player.walls = wall_list
player.enemyes = enemy_list
# ---------------------------------------------------------
# создание рандомных координат липких блоков
# ---------------------------------------------------------
for i in range(500):
    if i <= 220:
        wall_list_of_x.append(random.randrange(700, 2500, 50))
        wall_list_of_y.append(random.randrange(-2500, 2500, 50))
    if i > 220 and i <= 440:
        wall_list_of_x.append(random.randrange(-2500, 500, 50))
        wall_list_of_y.append(random.randrange(-2500, 2500, 50))
    if i > 440 and i <= 470:
        wall_list_of_x.append(random.randrange(500, 700, 50))
        wall_list_of_y.append(random.randrange(-2500, -400, 50))
    if i > 470:
        wall_list_of_x.append(random.randrange(500, 700, 50))
        wall_list_of_y.append(random.randrange(400, 2500, 50))
# --------------------------------------------------------
# создание врагов (в любом количестве)
# -----------------------------------------------------------------------------
for i in range(2):
    # рандомное создание места врага как по X, так и по Y
    enemy_list_of_x.append(random.randint(-500, 1500))
    enemy_list_of_y.append(random.randint(-500, 1500))
    easy_enemy = Easy_enemy(enemy_list_of_x[i], enemy_list_of_y[i], 20, 20, blue)
    enemy_list.add(easy_enemy)
    all_sprite_list.add(easy_enemy)
# ------------------------------------------------------------------------------
clock = pygame.time.Clock()

# ------------------------------------------------------------------------------
# --------------------------------ГЛАВНЫЙ ЦИКЛ----------------------------------
# ------------------------------------------------------------------------------
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                player.changespeed(-3, 0)
            elif event.key == pygame.K_f:
                player.changespeed(3, 0)
            elif event.key == pygame.K_e:
                player.changespeed(0, -3)
            elif event.key == pygame.K_d:
                player.changespeed(0, 3)
            elif event.key == pygame.K_SPACE:
                if player.change_x > 0:
                    player.change_x = 2
                elif player.change_x < 0:
                    player.change_x = -2
                if player.change_y > 0:
                    player.change_y = 2
                elif player.change_y < 0:
                    player.change_y = -2
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_s:
                pass
            elif event.key == pygame.K_f:
                pass
            elif event.key == pygame.K_e:
                pass
            elif event.key == pygame.K_d:
                pass
            elif event.key == pygame.K_SPACE:
                pass
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # выстреливает пулю при нажатии кнопки мышки
            # получаем координаты самой мыши
            pos = pygame.mouse.get_pos()
            mouse_x = pos[0]
            mouse_y = pos[1]

            # создает нашу пулю.Параметры:началльная позиция по Х и У, конечная по Х и У, скорость
            bullet = Bullet(player.rect.x - global_x, player.rect.y - global_y, mouse_x - global_x, mouse_y - global_y,
                            12)

            # добавляет ее в список
            all_sprite_list.add(bullet)
            bullet_list.add(bullet)
    """Сделал по секретному, рисует блоки,относительно "типо" измененной
    скорости игрока, меняет их,будто он перемещается, для этого сделал блоки,
    которые рисуются и стираются, меняя свою координату относительно скорости,
    крайне сложно и маразматично, но как-будто мир больше чем окно приложения"""

    screen.fill(black)
    # background()
    snow_up()
    all_sprite_list.add(player)
    all_sprite_list.update()
    # ------------------------------------
    # доступ к очистке блоков
    # ------------------------------------
    if acess_to_clearing == True:
        for wall in wall_list:
            all_sprite_list.remove(wall)
            wall_list.remove(wall)

    # --------------------------------------------------------
    # Движение врагов за игроком(параметры: скорость врага.)
    # ---------------------------------------------------------
    for easy_enemy in enemy_list:
        easy_enemy.enemy_folowing(player.rect.x - global_x, player.rect.y - global_y, 600 - global_x, 300 - global_y,
                                  12)
    # -----------------------------------------------------------------------------------------
    # создать стену,х,у,ширина,высота,цвет
    # ----------------------------------------------------------------------------------------
    for i in range(500):
        wall = Wall(wall_list_of_x[i] + global_x, wall_list_of_y[i] + global_y, 50, 50, lber)
        wall_list.add(wall)
        all_sprite_list.add(wall)

    acess_to_clearing = True
    # -----------------------------------------------------------------------------------------
    # создание пуль убивающих врагов
    # -----------------------------------------------------------------------------------------
    for bullet in bullet_list:
        """Контакт с врагами"""
        # Для контакта пули и блока, True - чтобы его убрало
        enemy_hit_list = pygame.sprite.spritecollide(bullet, enemy_list, True)

        # Для каждого врага в списке врагов
        for enemy in enemy_hit_list:
            bullet_list.remove(bullet)
            all_sprite_list.remove(bullet)
            score += 1

        # Убирает пулю ,если она зашла за экран
        if bullet.rect.y < 0 or bullet.rect.y > screen_height or bullet.rect.x < 0 or bullet.rect.x > screen_width:
            bullet_list.remove(bullet)
            all_sprites_list.remove(bullet)

        """Контакт с блоками"""
        wall_hit_list = pygame.sprite.spritecollide(bullet, wall_list, False)
        # Если дотронется до стены, убирает пулю
        for wall in wall_hit_list:
            bullet_list.remove(bullet)
            all_sprite_list.remove(bullet)
    # -----------------------------------------------------------------
    # движение всех частиц , независимо от игрока, но относительно него.
    # -----------------------------------------------------------------
    player.moving_all_without_player()
    # ----------------------------------

    player.block_hit_l()
    player.hit_enemyes()
    player.focus_camera()

    all_sprite_list.draw(screen)
    fonts(score)
    print(global_y, global_x)
    pygame.display.flip()
    clock.tick(30)
pygame.quit()
# ----------------------------------БАГИ------------------------------
# баг с стоячим игроков в которого вьезжает противник , и нихуя...((
# Враг может войти во врага на экране,исправить это
# Пуля летит не относительно скорости игрока, она просто идет по экрану, как будто он не движется #yes!
# может заспавнить в блоке и во враге
# ----------------------------------ПЛАН------------------------------
# зарандомить этих врагов по карте АВТОМАТИЧЕСКИ!!! а не в ручную...)#yes!
# Дать игроку оружие (пистолет,нож(еще думаю)) #yes!
# Сделать пулю(удар) в сторону мышки #yes!
# Сделать исчезновение противника от удара(будет тяжко)#yes!
# получение очков от убийства врага#yes!
# Очки,куда без них,думаю относительно кол-ва очков, улучшать оружие, придется еще класс создавать)
# Вывод плачевной таблички при смерте,(победа невозможна, враги бесконечны)
# чтоб оно всё работало,оптимизировать
# РАСТОВАЯ ГРАФИКА))))))))) бля, дожить бы...)
# Если приспичит, добавить звуки, и сделать .exe файл, для моментального запуска
