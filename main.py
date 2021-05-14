# --------------------------------------- imports
import pygame, random, time

base_addition = 1
bird_motion = 0.0001
collision = True
score = 0
high_score = 0


# --------------------------------------- main game function
def play():
    global base_addition, collision, score, high_score  # global variable

    pygame.init()  # initialise pygame

    game_font = pygame.font.Font("assets/Minecraft.ttf", 35)

    # ---------------- Game Window
    window = pygame.display.set_mode((500, 650))  # initialise screen
    pygame.display.update()  # update screen

    # ---------------- images
    bg_image = pygame.image.load('assets/background-image.png').convert()  # load background image
    bg_image = pygame.transform.smoothscale(bg_image, (500, 650))

    bird_image = pygame.image.load('assets/bluebird-midflap.png').convert()  # load base image
    bird_rect = bird_image.get_rect(center = (100, 250))

    pipe_image = pygame.image.load('assets/pipe-green.png').convert()  # load base image
    pipelist = []
    pipe_time = pygame.USEREVENT
    pygame.time.set_timer(pipe_time, 1500)
    """pipe_rect = bird_image.get_rect(midbottom=(200, 254))"""

    base_image = pygame.image.load('assets/base.png').convert()  # load base image
    base_image = pygame.transform.smoothscale(base_image, (500, 100))

    # ---------------- variables
    running = True
    clock = pygame.time.Clock()

    # ---------------- functions
    def base():
        global base_addition  # global variable

        base_addition -= 3

        if base_addition <= -500:
            base_addition = 0

    def score_display():
        if collision == False:
            score_surface = game_font.render(f"Score: {int(score)}", True, (255, 255, 255))
            score_rect = score_surface.get_rect(center = (250, 50))
            window.blit(score_surface, score_rect)
        elif collision == True:
            score_surface = game_font.render(f"Score: {int(score)}", True, (255, 255, 255))
            score_rect = score_surface.get_rect(center=(250, 50))
            window.blit(score_surface, score_rect)

            high_score_surface = game_font.render(f" High Score: {int(high_score)}", True, (255, 255, 255))
            high_score_rect = high_score_surface.get_rect(center=(250, 100))
            window.blit(high_score_surface, high_score_rect)

            message_surface = game_font.render("Press Arrow key to start", True, (255, 255, 255))
            message_rect = high_score_surface.get_rect(midtop=(160, 135))
            window.blit(message_surface, message_rect)

    def bird_gravity():
        global bird_motion

        bird_motion += 0.1
        bird_rect.centery += bird_motion

    def bird_jump():
        global bird_motion

        bird_motion = 0
        bird_motion -= 4.5

    def create_pipe():
        random_pos = random.randint(255 , 450)

        bottom_pipe = pipe_image.get_rect(midtop = (600, random_pos))
        top_pipe = pipe_image.get_rect(midbottom = (600, random_pos - 150))

        return top_pipe, bottom_pipe

    def move_pipes(pipe):
        for x in pipe:
            x.centerx -= 3

        return pipe

    def draw_pipes(pipe):
        global score

        score += 0.007
        for x in pipe:
            if x.bottom >= 550:
                window.blit(pipe_image, x)
            else:
                flip_pipe = pygame.transform.flip(pipe_image, False, True)
                window.blit(flip_pipe, x)

    def draw_bird():
        window.blit(bird_image, bird_rect)  # draw bird image on the screen

    def game_over():
        if collision == True:
            window.blit(bird_image, (100, 250))

    def check_collision(pipe):
        global collision

        for x in pipe:
            if bird_rect.colliderect(x):
                collision = True

                convert_high_score()
            if bird_rect.bottom >= 570  or bird_rect.top <= -10:
                collision = True

                convert_high_score()

    def convert_high_score():
        global high_score, score

        if high_score < score:
            high_score = score

    # ---------------- main while loop
    while running:
        for event in pygame.event.get():
            # ---------- Quit Window
            if event.type == pygame.QUIT:  # Quit window if close button pressed
                running = False
            if event.type == pipe_time:  # check pipe_time event
                pipelist.extend(create_pipe())
            # ---------- Track Buttons
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Escape Button Quit Window
                    running = False
                if event.key == pygame.K_SPACE and collision == False:  # jump bird when space bar
                    bird_jump()
                if event.key == pygame.K_UP and collision == True:  # jump bird when space bar
                    pipelist.clear()
                    bird_rect.center = (100, 252)
                    collision = False
                    score = 0
                    bird_motion = 0
                if event.key == pygame.K_UP:  # jump bird when up key
                    bird_jump()

        window.blit(bg_image, (0, 0))  # draw bg image on the screen

        if collision == False:


            draw_bird()
            bird_gravity()  # called gravity function

            """
            window.blit(pipe_image, pipe_rect)  # draw bird image on the screen """
            pipe_list = move_pipes(pipelist)
            draw_pipes(pipelist)

        window.blit(base_image, (base_addition, 550))  # draw base image on the screen
        window.blit(base_image, (base_addition + 500, 550))  # draw base image on the screen
        base()  # called base function

        game_over()
        score_display()

        check_collision(pipelist)

        pygame.display.update()  # update screen

        clock.tick(120)  # fps


# --------------------------------------- needed if statement
if __name__ == "__main__":
    play()  # called play function
