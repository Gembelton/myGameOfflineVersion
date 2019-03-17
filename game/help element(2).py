if n == True:
    for wall in all_sprite_list:
        all_sprite_list.remove(wall)
        wall_list.remove(wall)
all_sprite_list.add(player)

for i in range(500):
    wall = Wall(wall_list_of_x[i] + global_x, wall_list_of_y[i] + global_y, 50, 50, bolot)
    wall_list.add(wall)
    all_sprite_list.add(wall)
n = True