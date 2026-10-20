x = 0
y = 0

direction = ["North", "East", "South", "West"]
c_direction = direction[0]

def turn_left():
    global direction
    global c_direction

    if c_direction == direction[0]:
        c_direction = direction[3]
    elif c_direction == direction[1]:
        c_direction = direction[0]
    elif c_direction == direction[2]:
        c_direction = direction[1]
    elif c_direction == direction[3]:
        c_direction = direction[2]
        
    return c_direction

def turn_right():
    global direction
    global c_direction

    if c_direction == direction[0]:
        c_direction = direction[1]
    elif c_direction == direction[1]:
        c_direction = direction[2]
    elif c_direction == direction[2]:
        c_direction = direction[3]
    elif c_direction == direction[3]:
        c_direction = direction[0]
        
    return c_direction


current_step = 0


if_exists = {
    (0, 0): False
}

x, y = 0, 0


def go():
    global c_direction
    global direction
    global x
    global y

    if c_direction == direction[0]:
        x += 1
    elif c_direction == direction[1]:
        y += 1
    elif c_direction == direction[2]:
        x -= 1
    elif c_direction == direction[3]:
        y -= 1



def play():
    global current_step
    current_location = (x, y)
    is_light = if_exists.get(current_location, False)
    if_exists[current_location] = not is_light

    if is_light:
        turn_left()
    else:
        turn_right()

    go()

    current_step += 1
    if current_step % 100 == 0:
        print(f"Step {current_step}: ant at ({x}, {y})")


import pygame as pg

pg.init()

CELL_SIZE = 10
WIDTH, HEIGHT = 1000, 1000
BACKGROUND = (18, 18, 24)
GRID_COLOR = (45, 45, 58)
NEON_CELL = (57, 255, 20)
ANT_COLOR = (255, 70, 180)

screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("ant pattern")
clock = pg.time.Clock()

screen_direction = {
    "North": (0, -1),
    "East": (1, 0),
    "South": (0, 1),
    "West": (-1, 0),
}

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    play()

    screen.fill(BACKGROUND)

    grid_offset = CELL_SIZE // 2
    for grid_x in range(grid_offset, WIDTH, CELL_SIZE):
        pg.draw.line(screen, GRID_COLOR, (grid_x, 0), (grid_x, HEIGHT))
    for grid_y in range(grid_offset, HEIGHT, CELL_SIZE):
        pg.draw.line(screen, GRID_COLOR, (0, grid_y), (WIDTH, grid_y))

    for (grid_x, grid_y), state in if_exists.items():
        if not state:
            continue
        left = WIDTH // 2 + grid_y * CELL_SIZE - CELL_SIZE // 2
        top = HEIGHT // 2 - grid_x * CELL_SIZE - CELL_SIZE // 2
        rect = (left + 1, top + 1, CELL_SIZE - 2, CELL_SIZE - 2)
        pg.draw.rect(screen, NEON_CELL, rect)

    ant_center = (
        WIDTH // 2 + y * CELL_SIZE,
        HEIGHT // 2 - x * CELL_SIZE,
    )
    dx, dy = screen_direction[c_direction]
    perpendicular = (-dy, dx)
    ant_tip_size = CELL_SIZE * 2 // 5
    ant_rear_size = CELL_SIZE // 4
    ant_tip = (
        ant_center[0] + dx * ant_tip_size,
        ant_center[1] + dy * ant_tip_size,
    )
    ant_rear_left = (
        ant_center[0] - dx * ant_rear_size + perpendicular[0] * ant_rear_size,
        ant_center[1] - dy * ant_rear_size + perpendicular[1] * ant_rear_size,
    )
    ant_rear_right = (
        ant_center[0] - dx * ant_rear_size - perpendicular[0] * ant_rear_size,
        ant_center[1] - dy * ant_rear_size - perpendicular[1] * ant_rear_size,
    )
    pg.draw.polygon(screen, ANT_COLOR, (ant_tip, ant_rear_left, ant_rear_right))
    pg.draw.circle(screen, (255, 255, 255), ant_center, max(1, CELL_SIZE // 10))

    pg.display.flip()
    clock.tick(5000)

pg.quit()


