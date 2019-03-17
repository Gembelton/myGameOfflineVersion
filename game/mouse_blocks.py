
import pygame
import random

# Define some colors
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)

class Block(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()

        self.image = pygame.Surface([width+50, height]) # область которая затронется
        self.image.fill(RED) # цвет области с которой взаимодействуется
        self.image.set_colorkey(WHITE) # какой цвет сделать прозрачным
        pygame.draw.ellipse(self.image, color, [0, 0, width, height])# что нарисовать
        self.rect = self.image.get_rect()

    def update(self):
        # Подвинуть блок на один пиксель вниз
        self.rect.y += 1
        # если зашел за кэран
        if self.rect.y > screen_height:
            self.rect.y = random.randrange(-100, -10)
            self.rect.x = random.randrange(0, screen_width)


pygame.init()

screen_width = 700
screen_height = 400
screen = pygame.display.set_mode([screen_width, screen_height])

block_list = pygame.sprite.Group()

all_sprites_list = pygame.sprite.Group()

for i in range(50):
    block = Block(BLACK, 20, 15)

    # задают координату где появится обьект
    block.rect.x = random.randrange(screen_width)
    block.rect.y = random.randrange(screen_height)

    # добавляет обьект в список
    block_list.add(block)
    all_sprites_list.add(block)

# создает блок игрока
player = Block(RED, 20, 15)
all_sprites_list.add(player)

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

score = 0

# -------- Main Program Loop -----------
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # Clear the screen
    screen.fill(WHITE)
    block_list.update()
    #в эту переменную заносятся координаты х,у мыши
    pos = pygame.mouse.get_pos()

    # Двигает блок игрока, в зависимости от координат мыши
    player.rect.x = pos[0]
    player.rect.y = pos[1]

    # если наш квадрат столкнулся с каким блоком, убирает блок
    blocks_hit_list = pygame.sprite.spritecollide(player, block_list, True)

    # цикл нахождения, если блок еще есть в списке убитых, то добавляет +1.
    for block in blocks_hit_list:
        score += 1
        print(score)

    # рисует все эти спрайты
    all_sprites_list.draw(screen)

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # Limit to 60 frames per second
    clock.tick(60)

pygame.quit()