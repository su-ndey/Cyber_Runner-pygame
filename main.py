import random
import pygame
from sys import exit
from random import randint, choice


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        player_walk1 = pygame.image.load(
            "Art/graphics/Player/player_walk_1.png"
        ).convert_alpha()
        player_walk2 = pygame.image.load(
            "Art/graphics/Player/player_walk_2.png"
        ).convert_alpha()

        self.player_walk = [player_walk1, player_walk2]
        self.player_index = 0

        self.player_jump = pygame.image.load(
            "Art/graphics/Player/jump.png"
        ).convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(200, 300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound("Art/audio/jump.mp3")
        self.jump_sound.set_volume(0.4)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump

        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == "fly":
            fly1 = pygame.image.load("Art/graphics/Fly/Fly1.png").convert_alpha()
            fly2 = pygame.image.load("Art/graphics/Fly/Fly2.png").convert_alpha()
            self.frame = [fly1, fly2]
            y_pos = 210
        else:
            snail1 = pygame.image.load("Art/graphics/snail/snail1.png").convert_alpha()
            snail2 = pygame.image.load("Art/graphics/snail/snail2.png").convert_alpha()
            self.frame = [snail1, snail2]
            y_pos = 300

        self.animation_index = 0
        self.image = self.frame[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(random.randint(900, 1100), y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frame):
            self.animation_index = 0
        self.image = self.frame[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()


def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    text_surface = test_font.render(f"{current_time}", False, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(400, 50))
    screen.blit(text_surface, text_rect)

    return current_time


def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5

            if obstacle_rect.bottom == 300:

                screen.blit(snail_surface, obstacle_rect)

            else:
                screen.blit(fly_surface, obstacle_rect)

            obstacle_list = [
                obstacle for obstacle in obstacle_list if obstacle.x > -100
            ]

        return obstacle_list
    else:
        return []


def collisions(player, obstacle):
    if obstacle:
        for obstacle_rect in obstacle:
            if player.colliderect(obstacle_rect):
                return False

    return True


def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else:
        return True


def player_animation():
    global player_surface, player_index

    if player_rect.bottom < 300:
        player_surface = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk):
            player_index = 0
        player_surface = player_walk[int(player_index)]


pygame.init()

screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Runner")
clock = pygame.time.Clock()
test_font = pygame.font.Font("Art/font/Pixeltype.ttf", 50)

bg_sound = pygame.mixer.Sound("Art/audio/music.wav")
bg_sound.set_volume(0.1)
bg_sound.play(loops=-1)


sky_surface = pygame.image.load("Art/graphics/bg.png").convert()
ground_surface = pygame.image.load("Art/graphics/ground.png").convert()


# text_surface = test_font.render("Hello World", False, (64, 64, 64))


snail_frame1 = pygame.image.load("Art/graphics/snail/snail1.png").convert_alpha()
snail_frame2 = pygame.image.load("Art/graphics/snail/snail2.png").convert_alpha()
snail_frame_index = 0
snail_frame = [snail_frame1, snail_frame2]
snail_surface = snail_frame[snail_frame_index]


fly_frame1 = pygame.image.load("Art/graphics/Fly/Fly1.png").convert_alpha()
fly_frame2 = pygame.image.load("Art/graphics/Fly/Fly2.png").convert_alpha()
fly_frame_index = 0
fly_frame = [fly_frame1, fly_frame2]
fly_surface = fly_frame[fly_frame_index]


obstacle_rect_list = []


player_walk1 = pygame.image.load(
    "Art/graphics/Player/player_walk_1.png"
).convert_alpha()
player_walk2 = pygame.image.load(
    "Art/graphics/Player/player_walk_2.png"
).convert_alpha()

player_walk = [player_walk1, player_walk2]
player_index = 0

player_jump = pygame.image.load("Art/graphics/Player/jump.png").convert_alpha()
player_surface = player_walk[player_index]

player_rect = player_surface.get_rect(midbottom=(80, 300))


player_gravity = 0
start_time = 0
game_active = False
score = 0

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()


# homescreen
player_stand = pygame.image.load("Art/graphics/Player/player_stand.png").convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center=(400, 200))

text_surface = test_font.render("Cyber Runner ", False, (64, 64, 64))
text_rect = text_surface.get_rect(center=(400, 50))


# snail_x_pos = 600

# text_rect = text_surface.get_rect(center=(400, 50))


# timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1700)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 200)

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom == 300:
                    player_gravity = -20
            # if event.type == pygame.KEYUP:
            #     print("UP")

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if player_rect.collidepoint((mouse_pos)) and player_rect.bottom == 300:
                    player_gravity = -20
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True

                start_time = int(pygame.time.get_ticks() / 1000)

        if game_active:

            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(["fly", "snail", "snail", "snail"])))

                # if randint(0, 2):
                #     obstacle_rect_list.append(
                #         snail_surface.get_rect(midbottom=(randint(900, 1100), 300))
                #     )
                # else:
                #     obstacle_rect_list.append(
                #         fly_surface.get_rect(midbottom=(randint(900, 1100), 210))
                #     )

            if event.type == snail_animation_timer:
                if snail_frame_index == 0:
                    snail_frame_index = 1
                else:
                    snail_frame_index = 0

                snail_surface = snail_frame[snail_frame_index]

            if event.type == fly_animation_timer:
                if fly_frame_index == 0:
                    fly_frame_index = 1
                else:
                    fly_frame_index = 0
                fly_surface = fly_frame[fly_frame_index]

    if game_active:
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))

        # pygame.draw.rect(screen, "#c0e8ec", text_rect)
        # pygame.draw.rect(screen, "#c0e8ec", text_rect, 10)
        # screen.blit(text_surface, text_rect)
        score = display_score()
        # pygame.draw.line(screen, "Gold", (0, 0), pygame.mouse.get_pos(), 50)

        # snail_x_pos -= 4
        # snail_rect.x -= 4

        # if snail_rect.x < -100:
        #     snail_rect.left = 800
        # screen.blit(snail_surface, snail_rect)

        # player
        # player_gravity += 1
        # player_rect.y += player_gravity

        # obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # if player_rect.bottom >= 300:
        #     player_rect.bottom = 300

        # player_animation()
        # screen.blit(player_surface, player_rect)
        player.draw(screen)
        player.update()
        obstacle_group.draw(screen)
        obstacle_group.update()

        # collisons
        game_active = collision_sprite()

    else:

        screen.fill("#FF8FB1")
        screen.blit(player_stand, player_stand_rect)
        obstacle_rect_list.clear()
        player_rect.midbottom = (80, 300)
        player_gravity = 0

        text_surface1 = test_font.render(
            "PRESS SPACE TO START THE GAME ", False, (64, 64, 64)
        )
        text_rect1 = text_surface1.get_rect(center=(400, 350))

        text_surface2 = test_font.render(f"Your score is {score}", False, (64, 64, 64))
        text_rect2 = text_surface2.get_rect(center=(400, 350))

        screen.blit(text_surface, text_rect)

        if score != 0:
            screen.blit(text_surface2, text_rect2)
        elif score == 0:
            screen.blit(text_surface1, text_rect1)

    # mouse_pos = pygame.mouse.get_pos()
    # if player_rect.collidepoint((mouse_pos)):
    #     print(pygame.mouse.get_pressed())

    pygame.display.update()
    clock.tick(60)
