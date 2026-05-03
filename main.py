import turtle

# --- Global Configuration ---
WIDTH = 1200
HEIGHT = 800
RIVER_WIDTH = 300

screen = turtle.Screen()
screen.setup(WIDTH, HEIGHT)
screen.colormode(255)
screen.tracer(0)

# State Management
state = {
    "is_day": True,
    "game_started": False
}

# Turtles
bg_t = turtle.Turtle()
bg_t.hideturtle()
ui_t = turtle.Turtle()
ui_t.hideturtle()


def draw_sky():
    """Draws the purple-to-pink gradient sky."""
    top_y = HEIGHT // 2
    bottom_y = 100  # Sky ends here
    steps = top_y - bottom_y

    # Colors from image_5d0d37.png
    day_start = (140, 30, 140)  # Purple
    day_end = (255, 60, 120)  # Pink
    night_start = (20, 20, 60)  # Deep Blue
    night_end = (60, 20, 100)  # Dark Purple

    start = day_start if state["is_day"] else night_start
    end = day_end if state["is_day"] else night_end

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


def draw_land_gradient(x_start, width):
    """Draws the brown-to-green gradient land from image_51c2f4.png."""
    top_y = 100
    bottom_y = -HEIGHT // 2
    steps = abs(top_y - bottom_y)

    # Brown to Green
    start_col = (105, 85, 40)
    end_col = (45, 95, 45)

    for i in range(steps):
        ratio = i / steps
        r = int(start_col[0] * (1 - ratio) + end_col[0] * ratio)
        g = int(start_col[1] * (1 - ratio) + end_col[1] * ratio)
        b = int(start_col[2] * (1 - ratio) + end_col[2] * ratio)

        bg_t.penup()
        bg_t.goto(x_start, top_y - i)
        bg_t.color(r, g, b)
        bg_t.pendown()
        bg_t.forward(width)


def draw_river():
    bg_t.penup()
    bg_t.goto(-RIVER_WIDTH // 2, 100)
    bg_t.color(70, 130, 180)
    bg_t.begin_fill()
    for _ in range(2):
        bg_t.forward(RIVER_WIDTH)
        bg_t.right(90)
        bg_t.forward(HEIGHT)
        bg_t.right(90)
    bg_t.end_fill()


def draw_sun_moon():
    ui_t.penup()
    ui_t.goto(450, 250)
    if state["is_day"]:
        ui_t.color("yellow")
        ui_t.begin_fill()
        ui_t.circle(50)
        ui_t.end_fill()
    else:
        # Crescent Moon
        ui_t.color("white")
        ui_t.begin_fill()
        ui_t.circle(50)
        ui_t.end_fill()
        ui_t.goto(475, 265)
        # Match sky background color for cutout
        ui_t.color(40, 20, 80)
        ui_t.begin_fill()
        ui_t.circle(50)
        ui_t.end_fill()


def draw_play_button():
    # Button Capsule
    ui_t.penup()
    ui_t.goto(-100, 300)
    ui_t.color("black", (255, 200, 80))  # Gold fill
    ui_t.pensize(5)
    ui_t.begin_fill()
    for _ in range(2):
        ui_t.forward(200)
        ui_t.circle(40, 180)
    ui_t.end_fill()
    ui_t.pendown()
    for _ in range(2):
        ui_t.forward(200)
        ui_t.circle(40, 180)

    # Text
    ui_t.penup()
    ui_t.goto(0, 295)
    ui_t.color("black")
    ui_t.write("PLAY", align="center", font=("Comic Sans MS", 40, "bold"))


def render_scene():
    bg_t.clear()
    ui_t.clear()

    draw_sky()
    draw_river()
    # Left Land: from far left to river start
    draw_land_gradient(-WIDTH // 2, (WIDTH // 2) - (RIVER_WIDTH // 2))
    # Right Land: from river end to far right
    draw_land_gradient(RIVER_WIDTH // 2, (WIDTH // 2) - (RIVER_WIDTH // 2))

    draw_sun_moon()
    if not state["game_started"]:
        draw_play_button()

    screen.update()


def handle_click(x, y):
    # Click Sun/Moon area
    if x > 400 and y > 200:
        state["is_day"] = not state["is_day"]
        render_scene()

    # Click PLAY button
    elif -140 < x < 140 and 260 < y < 380:
        state["game_started"] = True
        render_scene()


# Initialization
render_scene()
screen.onclick(handle_click)
turtle.done()