#--------------------------------------------------------
#----------------Глобальные переменные-------------------
#--------------------------------------------------------
done = True
#пропускает 1-ну итерацию удаления блоков,так-как нечего удалять, еще не создало
acess_to_clearing = False
enemy_add = False
boss_add = False
screen_off = False
#переменная отвечающая за всё на экране относителньо статического игрока
global_x = 0
global_y = 0
player_fire = 'none'
#для рандома координат блоков
wall_list_of_x = []
wall_list_of_y = []

healing_list_of_x = []
healing_list_of_y = []
#для рандома координат леких врагов
enemy_list_of_x = []
enemy_list_of_y = []

boss_list_of_x = []
boss_list_of_y = []
#для рандома спрайта с лежачим оружием
weapons_list = []
# разрешение экрана
screen_width = 1200
screen_height = 600
#список снежинок
snow_list = []
#переменная заработанных очков
score = 0
# Цвета
black = (0, 0, 0)
white = (255, 255, 255)
blue = (50, 50, 255)
red = (255, 0, 0)
bolot = (60,200,85)
dpurple = (70,2,90) #темно-фиолетовый
ber = (25,170,175) #березовый
lber = ( 9,220,190) #светлый березовый
lroze = (255,170,175) # легкий розовый

weapon_invis = True
weapon_choise = 'pistol'
ammo_shortgun = True
ammo = 12
