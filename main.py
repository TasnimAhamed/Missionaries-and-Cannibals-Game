import turtle

# --- Configuration ---
WIDTH, HEIGHT = 1200, 800
RIVER_WIDTH = 300
HORIZON_Y = -50  # Reduced land/river height (Land starts lower now)

screen = turtle.Screen()
root = screen._root
root.wm_attributes("-topmost", 1)

screen.setup(WIDTH, HEIGHT)
screen.colormode(255)
screen.tracer(0)

state = {"is_day": True, "game_started": False}

bg_t = turtle.Turtle()
ui_t = turtle.Turtle()
for t in [bg_t, ui_t]: t.hideturtle()


def draw_pixel_circle(t, xc, yc, r, fill_color):
    """Implementation of Midpoint Circle Algorithm for smooth rendering."""
    t.penup()
    t.color(fill_color)
    # To fill a midpoint circle in Turtle, we draw horizontal lines between points
    x = 0
    y = r
    d = 1 - r

    def draw_lines(xc, yc, x, y):
        # Draws horizontal spans to fill the circle
        t.goto(xc - x, yc + y);
        t.pendown();
        t.goto(xc + x, yc + y);
        t.penup()
        t.goto(xc - x, yc - y);
        t.pendown();
        t.goto(xc + x, yc - y);
        t.penup()
        t.goto(xc - y, yc + x);
        t.pendown();
        t.goto(xc + y, yc + x);
        t.penup()
        t.goto(xc - y, yc - x);
        t.pendown();
        t.goto(xc + y, yc - x);
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
    steps = top_y - HORIZON_Y
    # Purple to Pink Gradient
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


def draw_land_and_river():
    # 1. River (Middle)
    bg_t.penup()
    bg_t.goto(-RIVER_WIDTH // 2, HORIZON_Y)
    bg_t.color(70, 130, 180)
    bg_t.begin_fill()
    for _ in range(2):
        bg_t.forward(RIVER_WIDTH);
        bg_t.right(90)
        bg_t.forward(HEIGHT // 2 + abs(HORIZON_Y));
        bg_t.right(90)
    bg_t.end_fill()

    # 2. Gradient Land
    for x_start in [-WIDTH // 2, RIVER_WIDTH // 2]:
        land_w = (WIDTH // 2) - (RIVER_WIDTH // 2)
        steps = abs(HORIZON_Y - (-HEIGHT // 2))
        for i in range(steps):
            ratio = i / steps
            # Brown to Green
            r = int(105 * (1 - ratio) + 45 * ratio)
            g = int(85 * (1 - ratio) + 95 * ratio)
            b = int(40 * (1 - ratio) + 45 * ratio)
            bg_t.penup()
            bg_t.goto(x_start, HORIZON_Y - i)
            bg_t.color(r, g, b)
            bg_t.pendown()
            bg_t.forward(land_w)


def draw_play_button():
    bx, by = 0, 150  # Centered button position
    ui_t.penup()
    ui_t.goto(bx - 100, by + 100)
    ui_t.color("black", (255, 200, 80))
    ui_t.pensize(4)
    ui_t.begin_fill()
    for _ in range(2):
        ui_t.forward(200);
        ui_t.circle(40, 180)
    ui_t.end_fill()
    # Corrected text position relative to button
    ui_t.goto(bx + 5, by + 120)
    ui_t.write("PLAY", align="center", font=("Arial", 35, "bold"))


def render():
    bg_t.clear()
    ui_t.clear()
    draw_sky()
    draw_land_and_river()

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
    if x > 380 and y > 180:  # Sun/Moon area
        state["is_day"] = not state["is_day"]
        render()
    elif -140 < x < 140 and 130 < y < 250:  # PLAY button area
        state["game_started"] = True
        render()


render()
screen.onclick(handle_click)
screen.mainloop()