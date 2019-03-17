import pygame
import random

#---------------------------Цвета----------------------
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
red  = (255, 0, 0)
#свои цвета
ber = (25,170,175)# березовый
lber = ( 9,220,190)# l - светлый березовый
Dpurple = (70,2,90)# D - темный фиолетовый
purple = ( 190,40,175)# фиолетовый
lroze = (255,170,175) # легкий розовый
pygame.init ()


size = (700, 500)
screen = pygame.display.set_mode (size)
pygame.display.set_caption ("My game alpha 0.001")
# Цикл, пока пользователь не нажмет кнопку закрытия.
done = False
#------------------глобальные переменные------------------
rect_x = 50
rect_y = 50
rect_change_x = 5
rect_change_y = 5
snow_list = []
for i in range(50):
    x = random.randrange(0, 700)
    y = random.randrange(0, 400)
    snow_list.append([x, y])
# Скорость, пикселей за кадр
x_speed = 0
y_speed = 0
# Текущая позиция
x_coord = 10
y_coord = 10
star_list = []
#---------------------------------------------------
# Используется для управления скоростью обновления экрана.
clock = pygame.time.Clock ()

#----------------------Функции элементов----------------------

#функция отскока прямоугольника от краев
def Priam():
    global rect_x,rect_y,rect_change_x,rect_change_y
    pygame.draw.rect(screen, purple, [rect_x, rect_y, 50, 50])
    pygame.draw.rect(screen, red, [rect_x + 10, rect_y + 10, 30, 30])
    rect_x += rect_change_x
    rect_y += rect_change_y
    # Заставить прямоугольник отпрыгнуть, если нужно
    if rect_y > 450 or rect_y < 0:
        rect_change_y = rect_change_y * -1
    if rect_x > 650 or rect_x < 0:
        rect_change_x = rect_change_x * -1

#функция снега
def snow_up():

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

#функция заднего фона
def background():
    for y_offset in range(0, 140, 10):
        for x_offset in range(0,140,10):
            pygame.draw.line(screen, ber, [0, 400 + y_offset], [700, 400 + y_offset], 2)
            pygame.draw.line(screen, Dpurple, [0, 405 + y_offset], [700, 405 + y_offset], 8)
# попытка сделать градиент
    global grber
    for y_offset in range(0, 230, 5):
        grber =(255-y_offset ,170,175) #gr - градиент
        pygame.draw.line(screen, grber, [0, 400 - (1.75 *y_offset)],
                         [700, 400 - (1.75*y_offset)],9)

#функция человечка
def draw_stick_figure(screen, x, y):
    # Голова
    pygame.draw.ellipse(screen, black, [1 + x, y, 10, 10], 0)

    # Ноги
    pygame.draw.line(screen, black, [5 + x, 17 + y], [10 + x, 27 + y], 2)
    pygame.draw.line(screen, black, [5 + x, 17 + y], [x, 27 + y], 2)

    # Тело
    pygame.draw.line(screen, red, [5 + x, 17 + y], [5 + x, 7 + y], 2)

    # Руки
    pygame.draw.line(screen, red, [5 + x, 7 + y], [9 + x, 17 + y], 2)
    pygame.draw.line(screen, red, [5 + x, 7 + y], [1 + x, 17 + y], 2)
# Спрятать курсор мыши
pygame.mouse.set_visible(1)
# -------- Основной программный цикл -----------
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

# ------------- Логика игры должна идти здесь--------------
    screen.fill (lber)


# ---------- Код рисования должен идти здесь ----------------
#задний план
    background()
#снег
    snow_up()

#------------------------------------------------------------
    pygame.display.flip ()
    clock.tick (30)
pygame.quit ()
