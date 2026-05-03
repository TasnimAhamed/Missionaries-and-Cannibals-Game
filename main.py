import turtle
import random
import time

# --- Configuration ---
WIDTH, HEIGHT = 1200, 800
RIVER_WIDTH = 500
HORIZON_Y_RIVER = -120
HORIZON_Y_LAND = -120

# --- Position Constants ---
LEFT_BANK_X = -150
RIGHT_BANK_X = 150
CHAR_START_X = -280
CHAR_Y = -30

# Grass Standing Areas (Where characters wait)
LEFT_GRASS_X = -280   # Further left than the boat
RIGHT_GRASS_X = 280   # Further right than the boat

# Vertical Rows
MISSIONARY_Y = -30     # Top row
CANNIBAL_Y = -30      # Bottom row

screen = turtle.Screen()
root = screen._root
root.wm_attributes("-topmost", 1)

screen.setup(WIDTH, HEIGHT)
screen.colormode(255)
screen.tracer(0)

# ----- Characters ----
screen.addshape("missionary.gif")
screen.addshape("cannibal.gif")

state = {
    "is_day": True,
    "game_started": False,
    "boat_position": "left",
    "boat_x": LEFT_BANK_X,
    "target_x": LEFT_BANK_X,
    "boat_speed": 10,
    "birds_data": [],
    "boat_passengers" : [],
    "ui_message": "",
    "missionaries": [
        {
            "x": LEFT_GRASS_X - 10,
            "y": MISSIONARY_Y - 68,
            "home_x": LEFT_GRASS_X - 10,  # Added this
            "home_y": MISSIONARY_Y - 68,  # Added this
            "side": "left"
        },
        {
            "x": LEFT_GRASS_X - 60,
            "y": MISSIONARY_Y - 68,
            "home_x": LEFT_GRASS_X - 60,
            "home_y": MISSIONARY_Y - 68,
            "side": "left"
        },
        {
            "x": LEFT_GRASS_X - 110,
            "y": MISSIONARY_Y - 68,
            "home_x": LEFT_GRASS_X - 110,
            "home_y": MISSIONARY_Y - 68,
            "side": "left"
        }
    ],
    "cannibals": [
        {
            "x": LEFT_GRASS_X - 160,
            "y": CANNIBAL_Y - 68,
            "home_x": LEFT_GRASS_X - 160,
            "home_y": CANNIBAL_Y - 68,
            "side": "left"
        },
        {
            "x": LEFT_GRASS_X - 210,
            "y": CANNIBAL_Y - 68,
            "home_x": LEFT_GRASS_X - 210,
            "home_y": CANNIBAL_Y - 68,
            "side": "left"
        },
        {
            "x": LEFT_GRASS_X - 260,
            "y": CANNIBAL_Y - 68,
            "home_x": LEFT_GRASS_X - 260,
            "home_y": CANNIBAL_Y - 68,
            "side": "left"
        }
    ]
}
current_stars = []

bg_t = turtle.Turtle()
bird_t = turtle.Turtle()
boat_t = turtle.Turtle()
ui_t = turtle.Turtle()
char_t = turtle.Turtle()
msg_t = turtle.Turtle()
test_t = turtle.Turtle()

for t in [bg_t, ui_t, bird_t, boat_t, char_t, msg_t, test_t]: t.hideturtle()


msg_t.hideturtle()
msg_t.penup()
msg_t.color("white")
def show_message(text):
    state["ui_message"] = text
    # The timer still works exactly the same!
    screen.ontimer(hide_message, 2000)

def hide_message():
    state["ui_message"] = ""
    msg_t.clear() # Clear it once when the timer ends


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
    x, y = 0, r
    d = 1 - r
    points = []
    while x <= y:
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

    steps = abs(HORIZON_Y_RIVER - (-HEIGHT // 2))
    for i in range(steps):
        ratio = i / steps

        r = int(72 * (1 - ratio) + 52 * ratio)
        g = int(189 * (1 - ratio) + 169 * ratio)
        b = int(225 * (1 - ratio) + 205 * ratio)

        bg_t.penup()
        bg_t.goto(-RIVER_WIDTH // 2, HORIZON_Y_RIVER - i)
        bg_t.color(r, g, b)
        bg_t.pendown()
        bg_t.forward(RIVER_WIDTH)

    bg_t.penup()
    bg_t.goto(-RIVER_WIDTH // 2, HORIZON_Y_RIVER)

    num_waves = 8
    wave_span = RIVER_WIDTH / num_waves
    radius = wave_span / 2

    for i in range(num_waves):

        start_x = (-RIVER_WIDTH // 2) + (i * wave_span)

        bg_t.penup()
        bg_t.goto(start_x, HORIZON_Y_RIVER)
        bg_t.setheading(-90)
        bg_t.pendown()
        if state["is_day"]:
            bg_t.color(255, 60, 120)
        else:
            bg_t.color(60, 20, 100)

        bg_t.begin_fill()
        bg_t.circle(radius, 180)
        bg_t.goto(start_x, HORIZON_Y_RIVER)

        bg_t.end_fill()

    bg_t.setheading(0)


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


def draw_bird(t, x, y, size, heading_first, heading_second):
    t.penup()
    t.goto(x, y)
    t.color("black")
    t.pensize(2)
    t.setheading(heading_first)
    t.pendown()

    t.circle(size, 90)

    t.setheading(heading_second)
    t.circle(size, 90)
    t.penup()


def initialize_birds(num_birds):
    state["birds_data"] = []
    for _ in range(num_birds):
        bird = {
            "x": random.randint(-800, 600),
            "y": random.randint(150, 400),
            "size": random.randint(10, 15),
            "h1": random.randint(90, 130),
            "h2": random.randint(90, 130)
        }
        state["birds_data"].append(bird)

# 4. Call it once
initialize_birds(10)

def draw_boat(t, x, y, scale=1.5):

    t.penup()
    t.goto(x - (50 * scale), y)
    t.setheading(0)

    if state["is_day"]:
        hull_color = (110, 60, 30)
        sail_color = (255, 255, 245)
        mast_color = (50, 30, 10)
    else:
        hull_color = (100, 100, 140)
        sail_color = (160, 160, 170)
        mast_color = (100, 110, 140)

    # 1. Hull - Made slightly deeper for a "bigger" look
    t.color(hull_color)
    t.begin_fill()
    t.forward(100 * scale)
    t.left(50)
    t.forward(40 * scale)
    t.left(130)
    t.forward(152 * scale)
    t.left(130)
    t.forward(40 * scale)
    t.end_fill()

    # 2. Mast - Positioned on the deck
    t.penup()
    t.goto(x, y + 30 * scale)
    t.setheading(90)
    t.pensize(max(1, int(4 * scale)))
    t.color(mast_color)
    t.pendown()
    t.forward(100 * scale)

    # --- 3. Large 3D Sail
    t.penup()
    t.goto(x, y + 130 * scale)

    # Sail Colors: Using an off-white/cream for a more realistic look
    t.color(sail_color)
    t.begin_fill()
    t.setheading(-140)
    t.forward(100 * scale)
    t.setheading(0)
    t.forward(75 * scale)
    t.goto(x, y + 130 * scale)
    t.end_fill()
    t.penup()


def draw_missionary(t, x, y, size=1.0):
    t.penup()
    t.goto(x, y)
    t.setheading(0)
    if state["is_day"]:
        t.color("blue")
    else:
        t.color((255, 255, 245))
    t.pensize(3 * size)

    # Legs
    t.pendown()
    t.goto(x - (10 * size), y - (20 * size))  # Left leg
    t.penup()
    t.goto(x, y)
    t.pendown()
    t.goto(x + (10 * size), y - (20 * size))  # Right leg

    # Body
    t.penup()
    t.goto(x, y)
    t.pendown()
    t.goto(x, y + (30 * size))

    # Arms
    t.penup()
    t.goto(x - (15 * size), y + (20 * size))
    t.pendown()
    t.goto(x + (15 * size), y + (20 * size))

    # Head
    t.penup()
    t.goto(x, y + (30 * size))
    t.setheading(0)
    t.pendown()
    t.circle(10 * size)
    t.penup()


def draw_cannibal(t, x, y, size=1.0):
    t.penup()
    t.goto(x, y)
    t.setheading(0)
    t.color("#B22222")  # A nice deep red like your image
    t.pensize(3 * size)

    # 1. Legs
    t.pendown()
    t.goto(x - (10 * size), y - (20 * size))
    t.penup()
    t.goto(x, y)
    t.pendown()
    t.goto(x + (10 * size), y - (20 * size))

    # 2. Body
    t.penup()
    t.goto(x, y)
    t.pendown()
    t.goto(x, y + (30 * size))

    # 3. Arms
    t.penup()
    t.goto(x - (15 * size), y + (20 * size))
    t.pendown()
    t.goto(x + (15 * size), y + (20 * size))

    # 4. Head
    t.penup()
    t.goto(x, y + (30 * size))
    t.setheading(0)
    t.pendown()
    t.circle(10 * size)

    # 5. THE HORNS (Added logic)
    # Left Horn
    t.penup()
    t.goto(x - (7 * size), y + (48 * size))  # Start on left top of head
    t.setheading(110)
    t.pendown()
    t.circle(-(15 * size), 60)  # Curved arc for the horn

    # Right Horn
    t.penup()
    t.goto(x + (7 * size), y + (48 * size))  # Start on right top of head
    t.setheading(70)
    t.pendown()
    t.circle((15 * size), 60)

    t.penup()


def toggle_passenger(char_obj):
    # --- NEW GUARD ---
    # If the game hasn't started, exit the function immediately
    if not state["game_started"]:
        show_message("Click PLAY to start!")
        return

        # Determine boat's current side
    boat_side = "left" if state["boat_x"] <= 0 else "right"

    # CASE A: If character is already on boat -> Move back to current bank
    if char_obj in state["boat_passengers"]:
        state["boat_passengers"].remove(char_obj)
        char_obj["side"] = boat_side

        # result = check_game_over()
        # if result:
        #     show_message(result)
        #     state["game_started"] = False

        if boat_side == "left":
            char_obj["x"] = char_obj["home_x"]
        else:
            char_obj["x"] = abs(char_obj["home_x"])

        char_obj["y"] = char_obj["home_y"]

    # CASE B: If character is on bank -> Board the boat
    else:
        # Rules: Boat must have space AND character must be on the same side
        if len(state["boat_passengers"]) < 2 and char_obj["side"] == boat_side:
            state["boat_passengers"].append(char_obj)
            char_obj["side"] = "boat"

            # result = check_game_over()
            # if result:
            #     show_message(result)
            #     state["game_started"] = False

        elif len(state["boat_passengers"]) >= 2:
            show_message("Boat is full!")
        else:
            show_message("Boat is on the other side!")


def check_game_over():
    # Count people on the left
    m_left = sum(1 for m in state["missionaries"] if m["side"] == "left")
    c_left = sum(1 for c in state["cannibals"] if c["side"] == "left")

    # Count people on the right
    m_right = sum(1 for m in state["missionaries"] if m["side"] == "right")
    c_right = sum(1 for c in state["cannibals"] if c["side"] == "right")

    # Check Left Bank: Missionaries die if C > M (and M is not 0)
    if m_left > 0 and c_left > m_left:
        return "Left Bank: The Missionaries were eaten!"

    # Check Right Bank: Missionaries die if C > M (and M is not 0)
    if m_right > 0 and c_right > m_right:
        return "Right Bank: The Missionaries were eaten!"

    return None  # Everyone is safe


def check_win():
    m_right = sum(1 for m in state["missionaries"] if m["side"] == "right")
    c_right = sum(1 for c in state["cannibals"] if c["side"] == "right")

    if m_right == 3 and c_right == 3:
        return True
    return False

def process_arrival():
    # Update side for passengers now that boat has landed
    arrival_side = "left" if state["boat_x"] <= 0 else "right"
    for p in state["boat_passengers"]:
        p["side"] = arrival_side

    # 1. Check if they won!
    if check_win():
        show_message("VICTORY! All crossed safely!")
        state["game_started"] = False
        return

    # 2. Check if Missionaries were eaten
    result = check_game_over()
    if result:
        show_message(result)
        state["game_started"] = False


def render():
    # 1. Clear everything at the start of the frame
    bg_t.clear()
    ui_t.clear()
    boat_t.clear()
    char_t.clear()

    # 2. Draw Background (Sky, Land, Stars)
    draw_sky()
    draw_land_and_river()
    draw_stars()

    # 3. Draw Boat (at current position)
    draw_boat(boat_t, state["boat_x"], HORIZON_Y_RIVER - 35, scale=1.5)

    # 4. Draw Birds from the FIXED list (No more flickering!)
    if state["is_day"]:
        for b in state["birds_data"]:
            # Pass 6 arguments: turtle, x, y, size, h1, h2
            draw_bird(bird_t, b["x"], b["y"], b["size"], b["h1"], b["h2"])

    # 5. Sun / Moon logic
    if state["is_day"]:
        draw_pixel_circle(ui_t, 460, 280, 65, (255, 255, 0))
    else:
        draw_pixel_circle(ui_t, 460, 280, 65, (240, 240, 240))
        draw_pixel_circle(ui_t, 485, 295, 65, (40, 20, 80))

    # Update positions for characters currently on the boat
    for i, p in enumerate(state["boat_passengers"]):
        # Place them side-by-side in the boat
        p["x"] = state["boat_x"] + (-60 if i == 0 else 60)
        p["y"] = HORIZON_Y_RIVER + 32  # Adjust height to sit in the boat

    # Draw all characters
    for m in state["missionaries"]:
        draw_missionary(char_t, m["x"], m["y"], size=1.0)
    for c in state["cannibals"]:
        draw_cannibal(char_t, c["x"], c["y"], size=1.0)

    # 6. Boat Physics (Movement Logic)
    if state["game_started"]:
        # Move Right
        if state["boat_x"] < state["target_x"]:
            state["boat_x"] += state["boat_speed"]
            if state["boat_x"] >= state["target_x"]:
                state["boat_x"] = state["target_x"]
                # --- CHECK LOGIC WHEN BOAT ARRIVES ---
                process_arrival()

        # Move Left
        elif state["boat_x"] > state["target_x"]:
            state["boat_x"] -= state["boat_speed"]
            if state["boat_x"] <= state["target_x"]:
                state["boat_x"] = state["target_x"]
                # --- CHECK LOGIC WHEN BOAT ARRIVES ---
                process_arrival()

    # 7. UI elements
    if not state["game_started"]:
        draw_play_button()

    # --- DRAW UI MESSAGE ---
    if state["ui_message"] != "":
        msg_t.clear()  # Clear previous frame's text
        msg_t.goto(-580, 350)
        msg_t.write(state["ui_message"], font=("Arial", 20, "bold"))
    else:
        msg_t.clear()

    # 8. Final Update and Timer
    screen.update()
    screen.ontimer(render, 16) # This keeps the whole game running at 60FPS

def handle_click(x, y):
    # Day/Night Toggle
    if x > 400 and y > 180:
        state["is_day"] = not state["is_day"]
        if not state["is_day"]:
            refresh_stars()

    # Play Button
    elif -100 < x < 100 and 240 < y < 330:
        state["game_started"] = True

    # --- 2. Character Clicks ---
    # Only allow character movement if the boat is NOT moving
    if state["boat_x"] == state["target_x"]:
        # Check Missionaries
        for m in state["missionaries"]:
            if abs(x - m["x"]) < 30 and abs(y - m["y"]) < 40:
                toggle_passenger(m)
                return  # Exit after one click

        # Check Cannibals
        for c in state["cannibals"]:
            if abs(x - c["x"]) < 30 and abs(y - c["y"]) < 40:
                toggle_passenger(c)
                return

    # --- 3. Boat Movement ---
    # Change: Boat only moves if it has 1 or 2 passengers
    if state["game_started"] and state["boat_x"] == state["target_x"]:
        if abs(x - state["boat_x"]) < 80 and abs(y - (HORIZON_Y_RIVER - 35)) < 60:
            if 1 <= len(state["boat_passengers"]) <= 2:

                result = check_game_over()
                if result:
                    show_message(result)
                    state["game_started"] = False
                else:
                    # Move the boat
                    state["target_x"] = RIGHT_BANK_X if state["target_x"] == LEFT_BANK_X else LEFT_BANK_X

                # if state["target_x"] == LEFT_BANK_X:
                #     state["target_x"] = RIGHT_BANK_X
                # else:
                #     state["target_x"] = LEFT_BANK_X
            else:
                show_message("Boat needs 1 or 2 people to move!")
    else:
        show_message("Click PLAY to start!")

render() # Starts the single, unified game loop
screen.onclick(handle_click)
screen.mainloop()
turtle.done()