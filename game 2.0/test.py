from constants import *
import pygame, math, random, time, datetime

start_ticks = pygame.time.get_ticks()


# ------------------------------------------------------------------------
# --------------------------------КЛАССЫ----------------------------------
# ------------------------------------------------------------------------

# класс персонажа
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.hp = 100
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
            player.hp -= 0.2
            if self.change_x > 0 or self.change_y > 0:
                self.rect.right = enemy.rect.left
                self.change_x = 0
                self.rect.bottom = enemy.rect.top
                self.change_y = 0
                self.hp -= 5
            if self.change_x < 0 or self.change_y < 0:
                self.rect.left = enemy.rect.right
                self.change_x = 0
                self.rect.top = enemy.rect.bottom
                self.change_y = 0
                self.hp -= 5

    def hit_hp(self):
        """Противники"""
        # если дотронется до противников
        healing_hit_list = pygame.sprite.spritecollide(self, self.hp_es, True)
        for hp in healing_hit_list:
            player.hp += 5

    def hit_boss(self):
        """Противники"""
        # если дотронется до босса
        boss_hit_list = pygame.sprite.spritecollide(self, self.bosses, False)
        for boss in boss_hit_list:
            player.hp -= 0.5
            if self.change_x > 0 or self.change_y > 0:
                self.rect.right = boss.rect.left
                self.change_x = 0
                self.rect.bottom = boss.rect.top
                self.change_y = 0
            if self.change_x < 0 or self.change_y < 0:
                self.rect.left = boss.rect.right
                self.change_x = 0
                self.rect.top = boss.rect.bottom
                self.change_y = 0

    def focus_camera(self):
        """Фиксирует камеру на игроке"""
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
        # кол-во здоровья легких противников
        self.hp = 2
        super().__init__()

        # задаем размер спрайту - высота,ширина
        self.image = pygame.Surface([width, height])
        self.image.fill(lroze)

        # начальные координаты предмета
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def enemy_folowing(self, speed_x_y):
        # следование за игроком
        # по оси Х:
        if self.rect.x > player.rect.x:
            self.rect.x -= speed_x_y + player.change_x
        if self.rect.x < player.rect.x:
            self.rect.x += speed_x_y - player.change_x
        if self.rect.x == player.rect.x:
            if player.rect.x > 0:
                self.rect.x += speed_x_y
            elif player.rect.x < 0:
                self.rect.x -= speed_x_y
        # -----------------------------------------------
        # по оси Y:

        if self.rect.y > player.rect.y:
            self.rect.y -= speed_x_y + player.change_y
        if self.rect.y < player.rect.y:
            self.rect.y += speed_x_y - player.change_y
        if self.rect.y == player.rect.y:
            if player.rect.y > 0:
                self.rect.y += speed_x_y
            elif player.rect.y < 0:
                self.rect.y -= speed_x_y

        # -----------------------------------------------


# Класс босса
class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        self.hp = 35
        super().__init__()
        # задаем размер спрайту - высота,ширина
        self.image = pygame.Surface([width, height])
        self.image.fill(dpurple)
        # начальные координаты предмета
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def enemy_folowing(self, speed_x_y):
        # по оси Х:

        if self.rect.x > player.rect.x:
            self.rect.x -= speed_x_y + player.change_x
        if self.rect.x < player.rect.x:
            self.rect.x += speed_x_y - player.change_x
        if self.rect.x == player.rect.x:
            if player.rect.x > 0:
                self.rect.x += speed_x_y
            elif player.rect.x < 0:
                self.rect.x -= speed_x_y
        # -----------------------------------------------
        # по оси Y:

        if self.rect.y > player.rect.y:
            self.rect.y -= speed_x_y + player.change_y
        if self.rect.y < player.rect.y:
            self.rect.y += speed_x_y - player.change_y
        if self.rect.y == player.rect.y:
            if player.rect.y > 0:
                self.rect.y += speed_x_y
            elif player.rect.y < 0:
                self.rect.y -= speed_x_y

        # -----------------------------------------------


# Класс пули
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


# Класс подбираемого оружия
class Weapon_sprite(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        super().__init__()

        # создаем спрайт с размером по высоте и ширине
        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        # Задаем местоположение на экране
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


# Класс подбираемого здоровья
class Healing_box(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        super().__init__()

        # создаем спрайт с размером по высоте и ширине
        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        # Задаем местоположение на экране
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


# Класс интерфейсной части
class Interface():
    # функция вывода очков
    def fonts_score(self, score):
        # Шрифт,размер,полужирный,курсив
        font = pygame.font.SysFont('Calibri', 25, True, False)
        # Сам текст,сглаженность,цвет
        text = font.render("Score: " + str(score), True, white)
        # Л-В-яя координата
        screen.blit(text, [1100, 15])

    # функция ввода кол-ва патронов
    def fonts_ammo(self, ammo):
        # Шрифт,размер,полужирный,курсив
        font = pygame.font.SysFont('Calibri', 25, True, False)
        # Сам текст,сглаженность,цвет
        text = font.render("Ammo: " + str(ammo), True, white)
        # Л-В-яя координата
        screen.blit(text, [10, 65])

    def fonts_weapon(self, weapon):
        # Шрифт,размер,полужирный,курсив
        font = pygame.font.SysFont('Calibri', 25, True, False)
        # Сам текст,сглаженность,цвет
        text = font.render("Weapon: " + str(weapon), True, white)
        # Л-В-яя координата
        screen.blit(text, [10, 35])

    def fonts_health(self, hp):
        # Шрифт,размер,полужирный,курсив
        font = pygame.font.SysFont('Calibri', 25, True, False)
        # Сам текст,сглаженность,цвет
        text = font.render("Health: " + str(int(hp)), True, white)
        # Л-В-яя координата
        screen.blit(text, [10, 5])

    def fonts_loose(self):
        # Шрифт,размер,полужирный,курсив
        font = pygame.font.SysFont('Calibri', 160, True, False)
        # Сам текст,сглаженность,цвет
        text = font.render("You loose ", True, white)
        # Л-В-яя координата
        screen.blit(text, [300, 200])

    def fonts_win(self):
        # Шрифт,размер,полужирный,курсив
        font = pygame.font.SysFont('Calibri', 160, True, False)
        # Сам текст,сглаженность,цвет
        text = font.render("You Win ", True, white)
        # Л-В-яя координата
        screen.blit(text, [280, 200])


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


pygame.init()
screen = pygame.display.set_mode([screen_width, screen_height])
pygame.display.set_caption('\n My game alpha 0.11b')
# ---------------------------------------------------------
# создание списков спрайтов
# ---------------------------------------------------------
all_sprite_list = pygame.sprite.Group()
wall_list = pygame.sprite.Group()
enemy_list = pygame.sprite.Group()
boss_list = pygame.sprite.Group()
bullet_list = pygame.sprite.Group()
weapons_list = pygame.sprite.Group()
healing_list = pygame.sprite.Group()
# ---------------------------------------------------------
# создание главного персонажа
# ---------------------------------------------------------
player = Player()
player.walls = wall_list
player.enemyes = enemy_list
player.bosses = boss_list
player.hp_es = healing_list
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
for i in range(10):
    healing_list_of_x.append(random.randrange(-2500, 2500, 5))
    healing_list_of_y.append(random.randrange(-2500, 2500, 5))


# ----------------------------------------------------------------------------
# создание врагов (в любом количестве)
# -----------------------------------------------------------------------------
a = random.randint(-1000,1000)
def rand(a):
    for i in range(a):
        # рандомное создание места врага как по X, так и по Y
        global enemy_list_of_x
        global enemy_list_of_y
        enemy_list_of_x.append(random.randint(-3500, 3500))
        enemy_list_of_y.append(random.randint(-3500, 3500))
        easy_enemy = Easy_enemy(enemy_list_of_x[i], enemy_list_of_y[i], 20, 20, blue)
        enemy_list.add(easy_enemy)
        all_sprite_list.add(easy_enemy)


def rand_boss(a):
    for i in range(a):
        global boss_list_of_x
        global boss_list_of_y
        boss_list_of_x.append(random.randint(-3500, 3500))
        boss_list_of_y.append(random.randint(-3500, 3500))
        boss = Boss(boss_list_of_x[i], boss_list_of_y[i], 50, 50, dpurple)
        boss_list.add(boss)
        all_sprite_list.add(boss)


# ------------------------------------------------------------------------------
clock = pygame.time.Clock()

# ------------------------------------------------------------------------------
# --------------------------------ГЛАВНЫЙ ЦИКЛ----------------------------------
# ------------------------------------------------------------------------------
while not done:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                player.changespeed(-2, 0)
            elif event.key == pygame.K_f:
                player.changespeed(2, 0)
            elif event.key == pygame.K_e:
                player.changespeed(0, -2)
            elif event.key == pygame.K_d:
                player.changespeed(0, 2)
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
            if ammo != 0:
                if weapon_choise == 'pistol':
                    timer_stop = datetime.datetime.utcnow() + datetime.timedelta(seconds=5)
                    # выстреливает пулю при нажатии кнопки мышки
                    # получаем координаты самой мыши
                    pos = pygame.mouse.get_pos()
                    mouse_x = pos[0]
                    mouse_y = pos[1]

                    # создает нашу пулю.Параметры:началльная позиция по Х и У, конечная по Х и У, скорость
                    bullet = Bullet(player.rect.x - global_x, player.rect.y - global_y,
                                    mouse_x - global_x + (random.randint(-15, 15)),
                                    mouse_y - global_y + (random.randint(-15, 15)), 12)
                    # добавляет ее в список
                    all_sprite_list.add(bullet)
                    bullet_list.add(bullet)
                    ammo -= 1
                if weapon_choise == 'shortgun':
                    timer_stop = datetime.datetime.utcnow() + datetime.timedelta(seconds=3)
                    # выстреливает пулю при нажатии кнопки мышки
                    # получаем координаты самой мыши
                    pos = pygame.mouse.get_pos()
                    mouse_x = pos[0]
                    mouse_y = pos[1]

                    # создает нашу пулю.Параметры:началльная позиция по Х и У, конечная по Х и У, скорость
                    for i in range(5):
                        bullet = Bullet(player.rect.x - global_x, player.rect.y - global_y,
                                        mouse_x - global_x + (random.randint(-25, 25)),
                                        mouse_y - global_y + (random.randint(-25, 25)), 20)
                        # добавляет ее в список
                        all_sprite_list.add(bullet)
                        bullet_list.add(bullet)
                    ammo -= 1

    """Сделал по секретному, рисует блоки,относительно "типо" измененной
    скорости игрока, меняет их,будто он перемещается, для этого сделал блоки,
    которые рисуются и стираются, меняя свою координату относительно скорости,
    крайне сложно и маразматично, но как-будто мир больше чем окно приложения"""

    screen.fill(black)
    background()
    snow_up()
    if screen_off == False:
        all_sprite_list.add(player)
    all_sprite_list.update()
    # ------------------------------------
    # доступ к очистке блоков
    # ------------------------------------
    if acess_to_clearing:
        for wall in wall_list:
            all_sprite_list.remove(wall)
            wall_list.remove(wall)
        for weapon in weapons_list:
            all_sprite_list.remove(weapon)
            weapons_list.remove(weapon)
        for h_box in healing_list:
            all_sprite_list.remove(h_box)
            healing_list.remove(h_box)
    # --------------------------------------------------------
    # Движение врагов за игроком(параметры: скорость врага.)
    # ---------------------------------------------------------
    seconds = (pygame.time.get_ticks() - start_ticks) / 1000  # смотрит сколько всего секунд
    if player.hp < 0 and screen_off == False:
        timer = datetime.datetime.utcnow() + datetime.timedelta(seconds=5)
        screen_off = True
    # Первая волна зомби
    # ---------------------------------------------------------
    if seconds > 2 and enemy_add == False and score != 10:
        rand(10)
        enemy_add = True
    for easy_enemy in enemy_list:
        easy_enemy.enemy_folowing((random.randrange(3000, 5000, 2) / 1000))

    # Вторая волна зомби
    # ---------------------------------------------------------
    if score == 10 and enemy_add == True:
        rand(20)
        enemy_add = False
    # Босс
    # ---------------------------------------------------------
    if boss_add == False and score > 35:
        rand_boss(2)
        boss_add = True
    for boss in boss_list:
        boss.enemy_folowing((random.randrange(5000, 8000, 2) / 1000))
    # -----------------------------------------------------------------------------------------
    # создать стену,х,у,ширина,высота,цвет
    # ----------------------------------------------------------------------------------------
    for i in range(500):
        wall = Wall(wall_list_of_x[i] + global_x,
                    wall_list_of_y[i] + global_y,
                    50, 50, lber)
        wall_list.add(wall)
        all_sprite_list.add(wall)
    for i in range(10):
        h_box = Healing_box(healing_list_of_x[i] + global_x,
                            healing_list_of_y[i] + global_y,
                            20, 20, bolot)
        healing_list.add(h_box)
        all_sprite_list.add(h_box)
    if weapon_invis == True:
        weapon = Weapon_sprite(a + global_x,a + global_y, 15, 15, red)
        weapons_list.add(weapon)
        all_sprite_list.add(weapon)

    acess_to_clearing = True
    # -----------------------------------------------------------------------------------------
    # создание пуль убивающих врагов
    # -----------------------------------------------------------------------------------------
    for bullet in bullet_list:
        """Контакт с врагами"""
        # Для контакта пули и блока, True - чтобы его убрало
        enemy_hit_list = pygame.sprite.spritecollide(bullet, enemy_list, False)
        boss_hit_list = pygame.sprite.spritecollide(bullet, boss_list, False)
        for enemy in enemy_hit_list:
            enemy.hp -= 1
            timer = datetime.datetime.utcnow() + datetime.timedelta(seconds=3)
            bullet_list.remove(bullet)
            all_sprite_list.remove(bullet)
            if enemy.hp == 0:
                # Для каждого врага в списке врагов
                for enemy in enemy_hit_list:
                    enemy_hit_list = pygame.sprite.spritecollide(bullet, enemy_list, True)
                    score += 1
                    timer = datetime.datetime.utcnow() + datetime.timedelta(seconds=5)

        for boss in boss_hit_list:
            boss.hp -= 1
            bullet_list.remove(bullet)
            all_sprite_list.remove(bullet)
            if boss.hp == 0:
                # Для каждого врага в списке врагов
                for boss in boss_hit_list:
                    boss_hit_list = pygame.sprite.spritecollide(bullet, boss_list, True)
                    score += 10
                    timer = datetime.datetime.utcnow() + datetime.timedelta(seconds=5)
        # Убирает пулю ,если она зашла за экран
        if bullet.rect.y < 0 or bullet.rect.y > screen_height or bullet.rect.x < 0 or bullet.rect.x > screen_width:
            bullet_list.remove(bullet)
            all_sprite_list.remove(bullet)

        """Контакт с блоками"""
        wall_hit_list = pygame.sprite.spritecollide(bullet, wall_list, False)
        # Если дотронется до стены, убирает пулю
        for wall in wall_hit_list:
            bullet_list.remove(bullet)
            all_sprite_list.remove(bullet)

    for hp in healing_list:
        healing_hit_list = pygame.sprite.spritecollide(player, healing_list, True)
        for hp in healing_hit_list:
            if player.hp < 100:
                player.hp += 0.1
            all_sprite_list.remove(hp)
            healing_list.remove(hp)

        ####
    for weapon in weapons_list:
        # Для контакта пули и блока, True - чтобы его убрало
        weapons_hit_list = pygame.sprite.spritecollide(player, weapons_list, True)
        for weapon in weapons_hit_list:
            weapon_invis = False
            weapon_choise = 'shortgun'
            ammo = 4
            weapons_list.remove(weapon)
            all_sprite_list.remove(weapon)

    # -----------------------------------------------------------------
    # движение всех частиц , независимо от игрока, но относительно него.
    # -----------------------------------------------------------------
    player.moving_all_without_player()
    # ----------------------------------

    player.block_hit_l()
    player.hit_enemyes()
    player.hit_hp()
    player.hit_boss()
    player.focus_camera()
    all_sprite_list.draw(screen)
    if player.hp >= 0:
        hud = Interface()
        hud.fonts_score(score)
        hud.fonts_ammo(ammo)
        hud.fonts_health(player.hp)
        hud.fonts_weapon(weapon_choise)
    # ------------------------------------------------------
    # -----------------------Боезапас-----------------------
    # -----------------------------------------------------
    # Если патронов стало 0
    if ammo == 0 and weapon_choise == 'pistol':
        # берем время перезярядки и ждем когда пройдет
        if datetime.datetime.utcnow() > timer_stop:
            # послечего заполняем обойму патронами
            ammo = 12
        # Если патронов стало 0
    if ammo == 0 and weapon_choise == 'shortgun':
        # берем время перезярядки и ждем когда пройдет
        if datetime.datetime.utcnow() > timer_stop:
            # послечего заполняем обойму патронами
            ammo = 4

    if screen_off == True and player.hp < 5:
        hud.fonts_loose()
        all_sprite_list.remove(player)
        if datetime.datetime.utcnow() > timer:
            break
    if score == 60:
        hud.fonts_win()
        if datetime.datetime.utcnow() > timer:
            break

    pygame.display.flip()
    clock.tick(30)
pygame.quit()
# ----------------------------------БАГИ------------------------------

# ----------------------------------ПЛАН------------------------------
# РАСТОВАЯ ГРАФИКА))))))))) бля, дожить бы...)
# Если приспичит, добавить звуки, и сделать .exe файл, для моментального запуска
