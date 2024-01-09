import pygame
pygame.init()
pygame.font.init()

SCORE_FONT = pygame.font.SysFont("comicsans", 30)

WIDTH, HEIGHT = 1100, 800
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_RADIUS = 7
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WINNING_SCORE = 15


class Paddle:
    VELOCITY = 4

    def __init__(self, x, y, width, height, color):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.width = width
        self.height = height
        self.color = color

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))

    def move(self, up=True):
        if up:
            self.y -= self.VELOCITY
        else:
            self.y += self.VELOCITY
        self.y = max(min(self.y, HEIGHT - self.height), 0)

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y

    def ai_move(self, ball):
        if self.y + self.height / 2 < ball.y:
            self.move(up=False)
        elif self.y + self.height / 2 > ball.y:
            self.move(up=True)


class Ball:
    MAX_VELOCITY = 5
    COLOR = WHITE

    def __init__(self, x, y, radius):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.x_velocity = self.MAX_VELOCITY
        self.y_velocity = 0

    def draw(self, win):
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.x_velocity
        self.y += self.y_velocity

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.y_velocity = 0
        self.x_velocity *= -1


def draw_scores(win, left_score, right_score):
    left_score_rendered = SCORE_FONT.render(f"{left_score}", 1, WHITE)
    right_score_rendered = SCORE_FONT.render(f"{right_score}", 1, WHITE)
    win.blit(left_score_rendered, (WIDTH // 4 - left_score_rendered.get_width() // 2, 20))
    win.blit(right_score_rendered, (WIDTH * 3 // 4 - right_score_rendered.get_width() // 2, 20))


def draw_center_divider(win):
    for i in range(10, HEIGHT, HEIGHT // 20):
        pygame.draw.rect(win, WHITE, (WIDTH // 2 - 2, i, 4, HEIGHT // 40))


def draw(win, paddles, ball, left_score, right_score):
    win.fill(BLACK)

    draw_scores(win, left_score, right_score)

    for paddle in paddles:
        paddle.draw(win)

    draw_center_divider(win)

    ball.draw(win)

    pygame.display.update()


def collision(ball, left_paddle, right_paddle):
    if ball.y + ball.radius >= HEIGHT or ball.y - ball.radius <= 0:
        ball.y_velocity *= -1

    if ball.x_velocity < 0:
        if left_paddle.y <= ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                ball.x_velocity *= -1

                middle1 = left_paddle.y + left_paddle.height / 2
                diff_y = middle1 - ball.y
                reduction = (left_paddle.height / 2) / ball.MAX_VELOCITY
                y_velocity = diff_y / reduction
                ball.y_velocity = -1 * y_velocity
    else:
        if right_paddle.y <= ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_velocity *= -1

                middle1 = right_paddle.y + right_paddle.height / 2
                diff_y = middle1 - ball.y
                reduction = (right_paddle.height / 2) / ball.MAX_VELOCITY
                y_velocity = diff_y / reduction
                ball.y_velocity = -1 * y_velocity


def paddles_move(keys, left_paddle, right_paddle, ball):
    if keys[pygame.K_w] and left_paddle.y - left_paddle.VELOCITY >= 0:
        left_paddle.move(up=True)
    if keys[pygame.K_s] and left_paddle.y + left_paddle.VELOCITY + left_paddle.height <= HEIGHT:
        left_paddle.move(up=False)
    right_paddle.ai_move(ball)


def main():
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pong")

    game_run = True
    clock = pygame.time.Clock()

    left_paddle = Paddle(10, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT, RED)
    right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT,
                          BLUE)
    ball = Ball(WIDTH // 2, HEIGHT // 2, BALL_RADIUS)

    left_score = 0
    right_score = 0

    while game_run:
        clock.tick(FPS)
        draw(window, [left_paddle, right_paddle], ball, left_score, right_score)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_run = False
                break

        keys = pygame.key.get_pressed()
        paddles_move(keys, left_paddle, right_paddle, ball)  # Pass ball as a parameter

        ball.move()
        collision(ball, left_paddle, right_paddle)

        if ball.x < 0:
            right_score += 1
            ball.reset()
        elif ball.x > WIDTH:
            left_score += 1
            ball.reset()

        won = False
        if left_score >= WINNING_SCORE:
            won = True
            win_text = "Left Player Won!"
        elif right_score >= WINNING_SCORE:
            won = True
            win_text = "Right Player Won!"

        if won:
            text = SCORE_FONT.render(win_text, 1, WHITE)
            window.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
            pygame.display.update()
            pygame.time.delay(5000)
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
            left_score = 0
            right_score = 0

    pygame.quit()

if __name__ == '__main__':
    main()
