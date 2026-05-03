import turtle
import random

# --- Configuration ---
WIDTH, HEIGHT = 1200, 800
RIVER_WIDTH = 500
HORIZON_Y_RIVER = -50
HORIZON_Y_LAND = -50

screen = turtle.Screen()
root = screen._root
root.wm_attributes("-topmost", 1)

screen.setup(WIDTH, HEIGHT)
screen.colormode(255)
screen.tracer(0)

state = {"is_day": True, "game_started": False}
current_stars = []

bg_t = turtle.Turtle()
ui_t = turtle.Turtle()
for t in [bg_t, ui_t]: t.hideturtle()


def draw_pixel_circle(t, xc, yc, r, fill_color):
    t.penup()
    t.color(fill_color)
    x = 0
    y = r
    d = 1 - r

    def draw_lines(xc, yc, x, y):
        t.goto(xc - x, yc + y)
        t.pendown()
        t.goto(xc + x, yc + y)
        t.penup()
        t.goto(xc - x, yc - y)
        t.pendown()
        t.goto(xc + x, yc - y)
        t.penup()
        t.goto(xc - y, yc + x)
        t.pendown()
        t.goto(xc + y, yc + x)
        t.penup()
        t.goto(xc - y, yc - x)
        t.pendown()
        t.goto(xc + y, yc - x)
        t.penup()

    while x <= y:
        draw_lines(xc, yc, x, y)
        if d < 0:
            d = d + 2 * x + 3
        else:
            d = d + 2 * (x - y) + 5
            y -= 1
        x += 1


def draw_sky():
    top_y = HEIGHT // 2
    steps = top_y - HORIZON_Y_LAND

    start = (140, 30, 140) if state["is_day"] else (20, 20, 60)
    end = (255, 60, 120) if state["is_day"] else (60, 20, 100)

    for i in range(steps):
        ratio = i / steps
        r = int(start[0] * (1 - ratio) + end[0] * ratio)
        g = int(start[1] * (1 - ratio) + end[1] * ratio)
        b = int(start[2] * (1 - ratio) + end[2] * ratio)
        bg_t.penup()
        bg_t.goto(-WIDTH // 2, top_y - i)
        bg_t.color(r, g, b)
        bg_t.pendown()
        bg_t.forward(WIDTH)


def draw_single_star(t, x, y, size):
    t.penup()
    t.goto(x, y)
    t.setheading(0)
    t.color("white")
    t.pendown()
    for _ in range(5):
        t.forward(size)
        t.right(144)

    t.penup()


def refresh_stars():
    global current_stars
    current_stars = []
    star_cnt = random.randint(10, 20)
    for _ in range(star_cnt):
        x = random.randint(-580, 580)
        y = random.randint(0, 380)
        size = random.randint(2, 20)
        current_stars.append((x, y, size))


def draw_stars():
    if not state["is_day"]:
        for x, y, size in current_stars:
            if not (x > 380 and y > 180):
                draw_single_star(ui_t, x, y, size)


def draw_midpoint_wave_segment(t, xc, yc, r):
    """Calculates the bottom half of a circle using Midpoint Algorithm."""
    x, y = 0, r
    d = 1 - r
    points = []
    while x <= y:
        # Subtracting from yc ensures the points go DOWN into the river
        points.append((xc + x, yc - y))
        points.append((xc - x, yc - y))
        points.append((xc + y, yc - x))
        points.append((xc - y, yc - x))
        if d < 0:
            d = d + 2 * x + 3
        else:
            d = d + 2 * (x - y) + 5
            y -= 1
        x += 1
    points.sort(key=lambda p: p[0])
    for p in points:
        t.goto(p)



def draw_river():
    # 1. Draw the Gradient FIRST (The Water Body)
    # This ensures the waves can sit ON TOP
    steps = abs(HORIZON_Y_RIVER - (-HEIGHT // 2))
    for i in range(steps):
        ratio = i / steps
        # Using your exact color: (62, 179, 215)
        r = int(72 * (1 - ratio) + 52 * ratio)
        g = int(189 * (1 - ratio) + 169 * ratio)
        b = int(225 * (1 - ratio) + 205 * ratio)

        bg_t.penup()
        bg_t.goto(-RIVER_WIDTH // 2, HORIZON_Y_RIVER - i)
        bg_t.color(r, g, b)
        bg_t.pendown()
        bg_t.forward(RIVER_WIDTH)

    # 1. DRAW THE PINK WAVES (Constrained to RIVER_WIDTH)
    bg_t.penup()
    # Start exactly at the left edge of the river
    bg_t.goto(-RIVER_WIDTH // 2, HORIZON_Y_RIVER)
    if state["is_day"]:
        bg_t.color(255, 60, 120)
    else:
        bg_t.color(60, 20, 100)
    bg_t.begin_fill()

    num_waves = 8
    wave_span = RIVER_WIDTH / num_waves
    radius = wave_span / 2

    # Draw the downward scallops
    for i in range(num_waves):
        xc = (-RIVER_WIDTH // 2) + (i * wave_span) + radius
        yc = HORIZON_Y_RIVER
        draw_midpoint_wave_segment(bg_t, xc, yc, radius)

    # 2. CLOSE THE SHAPE WITHIN RIVER BOUNDARIES
    # Instead of going to screen edges, stay at +/- RIVER_WIDTH // 2
    bg_t.goto(RIVER_WIDTH // 2, HORIZON_Y_RIVER + 50)  # Top Right of wave area
    bg_t.goto(-RIVER_WIDTH // 2, HORIZON_Y_RIVER + 50)  # Top Left of wave area
    bg_t.goto(-RIVER_WIDTH // 2, HORIZON_Y_RIVER)  # Back to start
    bg_t.end_fill()

def draw_land_and_river():

    bg_t.penup()
    draw_river()

    for x_start in [-WIDTH // 2, RIVER_WIDTH // 2]:
        land_w = (WIDTH // 2) - (RIVER_WIDTH // 2)
        steps = abs(HORIZON_Y_LAND - (-HEIGHT // 2))

        for i in range(steps):
            ratio = i / steps
            r = int(105 * (1 - ratio) + 45 * ratio)
            g = int(85 * (1 - ratio) + 95 * ratio)
            b = int(40 * (1 - ratio) + 45 * ratio)

            bg_t.penup()
            bg_t.goto(x_start, HORIZON_Y_LAND - i)
            bg_t.color(r, g, b)
            bg_t.pendown()
            bg_t.forward(land_w)


def draw_play_button():
    bx, by = 0, 150

    if state["is_day"]:
        button_fill = (255, 200, 80)
        button_edge = "black"
        text_color = "black"
    else:
        button_fill = (100, 100, 140)
        button_edge = (200, 200, 255)
        text_color = "white"

    ui_t.penup()
    ui_t.goto(bx - 100, by + 100)
    ui_t.color(button_edge, button_fill)
    ui_t.pensize(4)
    ui_t.begin_fill()
    for _ in range(2):
        ui_t.forward(200);
        ui_t.circle(40, 180)
    ui_t.end_fill()

    ui_t.goto(bx + 5, by + 120)
    ui_t.color(text_color)
    ui_t.write("PLAY", align="center", font=("Arial", 35, "bold"))


def render():
    bg_t.clear()
    ui_t.clear()
    draw_sky()
    draw_land_and_river()
    draw_stars()
    # draw_birds()

    # Celestial Body (Midpoint Circle)
    if state["is_day"]:
        draw_pixel_circle(ui_t, 460, 280, 65, (255, 255, 0))
    else:
        draw_pixel_circle(ui_t, 460, 280, 65, (240, 240, 240))
        # Moon Cutout (match night sky color)
        draw_pixel_circle(ui_t, 485, 295, 65, (40, 20, 80))

    if not state["game_started"]:
        draw_play_button()
    screen.update()


def handle_click(x, y):
    if x > 400 and y > 180:
        state["is_day"] = not state["is_day"]
        if not state["is_day"]:
            refresh_stars()

        render()
    elif -100 < x < 100 and 240 < y < 330:
        state["game_started"] = True
        render()


render()
screen.onclick(handle_click)
screen.mainloop()