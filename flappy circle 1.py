import turtle
import time
import random

# ---------------- SCREEN ----------------
screen = turtle.Screen()
screen.title("Flappy Bird with Clouds")
screen.bgcolor("skyblue")
screen.setup(width=600, height=600)
screen.tracer(0)

# ---------------- CLOUDS ----------------
clouds = []

def create_cloud(x, y):
    c = turtle.Turtle()
    c.hideturtle()
    c.penup()
    c.color("white")
    c.shape("circle")
    c.shapesize(1.5, 2.5)
    c.goto(x, y)
    c.showturtle()
    clouds.append(c)

def move_clouds():
    for c in clouds:
        c.setx(c.xcor() - 0.4)
        if c.xcor() < -350:
            c.setx(350)
            c.sety(random.randint(120, 260))

create_cloud(-100, 220)
create_cloud(80, 260)
create_cloud(200, 180)

# ---------------- BIRD (BODY + BEAK + WING) ----------------
bird = turtle.Turtle()
bird.shape("circle")
bird.color("yellow")
bird.penup()
bird.goto(-200, 0)
bird.dy = 0

# Beak (triangle)
beak = turtle.Turtle()
beak.shape("triangle")
beak.color("orange")
beak.penup()
beak.setheading(0)

# Wing (ellipse-like)
wing = turtle.Turtle()
wing.shape("circle")
wing.color("gold")
wing.shapesize(0.6, 1.2)
wing.penup()

def update_bird_parts():
    # Beak in front of bird
    beak.goto(bird.xcor() + 14, bird.ycor())
    beak.setheading(0)

    # Wing slightly behind and down
    wing.goto(bird.xcor() - 6, bird.ycor() - 2)

# ---------------- GROUND ----------------
ground = turtle.Turtle()
ground.hideturtle()
ground.penup()
ground.color("green")
ground.goto(-300, -250)
ground.begin_fill()
for _ in range(2):
    ground.forward(600)
    ground.left(90)
    ground.forward(50)
    ground.left(90)
ground.end_fill()

# ---------------- PIPES ----------------
pipe_top = turtle.Turtle()
pipe_top.shape("square")
pipe_top.color("green")
pipe_top.shapesize(stretch_wid=8, stretch_len=2)
pipe_top.penup()

pipe_bottom = turtle.Turtle()
pipe_bottom.shape("square")
pipe_bottom.color("green")
pipe_bottom.shapesize(stretch_wid=8, stretch_len=2)
pipe_bottom.penup()

PIPE_GAP = 100

def reset_pipe():
    x = 300
    y = random.randint(-80, 120)
    pipe_top.goto(x, y + PIPE_GAP + 140)
    pipe_bottom.goto(x, y - PIPE_GAP - 140)

# ---------------- SCORE ----------------
score_writer = turtle.Turtle()
score_writer.hideturtle()
score_writer.penup()

# ---------------- GAME STATE ----------------
gravity = 0.5
pipe_speed = 3
game_over = False
score = 0

def reset_game():
    global game_over, score
    game_over = False
    score = 0

    bird.goto(-200, 0)
    bird.dy = 0

    reset_pipe()

    score_writer.clear()
    score_writer.goto(0, 260)
    score_writer.write("Score: 0", align="center",
                       font=("Arial", 18, "bold"))

    beak.showturtle()
    wing.showturtle()

reset_game()

# ---------------- CONTROLS ----------------
def flap():
    if not game_over:
        bird.dy = 8

def restart():
    reset_game()

screen.listen()
screen.onkey(flap, "space")
screen.onkey(restart, "r")

# ---------------- GAME LOOP ----------------
while True:
    screen.update()
    time.sleep(0.02)

    move_clouds()

    if not game_over:
        # Bird physics (UNCHANGED)
        bird.dy -= gravity
        bird.sety(bird.ycor() + bird.dy)

        update_bird_parts()   # 🔴 visual update only

        # Pipes move
        pipe_top.setx(pipe_top.xcor() - pipe_speed)
        pipe_bottom.setx(pipe_bottom.xcor() - pipe_speed)

        # Reset pipes & score
        if pipe_top.xcor() < -320:
            reset_pipe()
            score += 1
            score_writer.clear()
            score_writer.write(f"Score: {score}", align="center",
                               font=("Arial", 18, "bold"))

        # Collision with pipes
        if abs(bird.xcor() - pipe_top.xcor()) < 30:
            if bird.ycor() > pipe_top.ycor() - 120 or \
               bird.ycor() < pipe_bottom.ycor() + 120:
                game_over = True

        # Ground or sky collision
        if bird.ycor() < -200 or bird.ycor() > 280:
            game_over = True

    else:
        beak.hideturtle()
        wing.hideturtle()
        score_writer.goto(0, 0)
        score_writer.write("GAME OVER\nPress R to Restart",
                           align="center",
                           font=("Arial", 24, "bold"))
