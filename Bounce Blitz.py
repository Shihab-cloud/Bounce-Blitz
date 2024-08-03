from tkinter import Tk, Canvas

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600
BALL_DIAMETER = 15
INITIAL_VELOCITY = 5
PADDLE_HEIGHT = 100
PADDLE_WIDTH = 10
START_X = 0
START_Y = 0
DELAY = 10
GAME_OVER_DELAY = 3000

def main():
    root = Tk()
    root.geometry(f"{CANVAS_WIDTH}x{CANVAS_HEIGHT}")

    global canvas, paddle, score, game_over, ball_x, ball_y, x_velocity, y_velocity
    canvas = Canvas(root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
    canvas.pack()

    paddle_x = CANVAS_WIDTH - PADDLE_WIDTH
    paddle_y = (CANVAS_HEIGHT - PADDLE_HEIGHT) / 2
    paddle = canvas.create_rectangle(paddle_x, paddle_y, paddle_x + PADDLE_WIDTH, paddle_y + PADDLE_HEIGHT, fill='black')
    canvas.bind('<Motion>', draw_rectangle)

    lost_message = canvas.create_text(CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2, text="", font=('Helvetica', 54, 'bold italic'), fill='gray')

    x_velocity = INITIAL_VELOCITY
    y_velocity = INITIAL_VELOCITY
    ball_x = START_X
    ball_y = START_Y
    ball_end_x = ball_x + BALL_DIAMETER
    ball_end_y = ball_y + BALL_DIAMETER

    ball = canvas.create_oval(ball_x, ball_y, ball_end_x, ball_end_y, fill='black')

    score = 0
    game_over = False

    #ball position update
    def update_ball():
        global ball_x, ball_y, x_velocity, y_velocity, score, game_over

        if game_over:
            return

        # Check if the ball hits the left wall
        if ball_x < 0:
            x_velocity = -x_velocity

        # Check if the ball hits the top or bottom wall
        if ball_y < 0 or ball_y + BALL_DIAMETER >= CANVAS_HEIGHT:
            y_velocity = -y_velocity

        # Check if the ball hits the paddle
        paddle_coords = canvas.coords(paddle)
        if (ball_x + BALL_DIAMETER >= paddle_coords[0]) and (ball_y + BALL_DIAMETER >= paddle_coords[1]) and (ball_y <= paddle_coords[3]):
            if x_velocity > 0:
                x_velocity = -x_velocity
                score += 6  #score increasing whenever the ball hits the paddle

        # Check if the ball goes beyond the right side without hitting the paddle
        if ball_x >= CANVAS_WIDTH:
            canvas.itemconfig(lost_message, text=f"Game Over! \nScore: {score}")
            game_over = True
            root.after(GAME_OVER_DELAY, root.destroy)#automatically close the game after game over
            return

        ball_x += x_velocity
        ball_y += y_velocity
        canvas.move(ball, x_velocity, y_velocity)

        root.after(DELAY, update_ball)

    update_ball()

    root.mainloop()

def draw_rectangle(event):
    x = event.x
    y = event.y

    if x < 0:
        x = 0
    elif x + PADDLE_WIDTH > CANVAS_WIDTH:
        x = CANVAS_WIDTH - PADDLE_WIDTH

    if y < 0:
        y = 0
    elif y + PADDLE_HEIGHT > CANVAS_HEIGHT:
        y = CANVAS_HEIGHT - PADDLE_HEIGHT

    canvas.coords(paddle, x, y, x + PADDLE_WIDTH, y + PADDLE_HEIGHT)

if __name__ == '__main__':
    main()
