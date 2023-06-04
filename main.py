import math
import time
import pygame
from basic_functions import resize_image, rotation_about_center, text_align

# Initialize Pygame and related modules
pygame.init()
pygame.font.init()
pygame.mixer.init()

# Load and play the background music
pygame.mixer.music.load('ID1110-Project-main\songs\\background_music.mp3')
pygame.mixer.music.set_volume(0.07)
pygame.mixer.music.play(-1)

# Creating player car and computer car variables
PLAYER_CAR = resize_image(pygame.image.load("ID1110-Project-main/imgs/player_car.png"), 0.35)
COMPUTER_CAR = resize_image(pygame.image.load("ID1110-Project-main/imgs/computer_car.png"), 0.35)

# Setting background variable and track variable and resizing the image used
BACKGROUND = resize_image(pygame.image.load("ID1110-Project-main/imgs/green_grass.jpg"), 2.5)
PATH = resize_image(pygame.image.load("ID1110-Project-main/imgs/race_track.png"), 0.9)

# Defining window width and height equal to the width and height of the track
WID, HT = PATH.get_width(), PATH.get_height()
WINDOW = pygame.display.set_mode((WID, HT))

# Setting the title of the window displayed
pygame.display.set_caption("CAR RACING!!")

# Defining variable for the track and it's mask
RACE_TRACK_BORDER = resize_image(
    pygame.image.load("ID1110-Project-main/imgs/track_outline.png"), 0.9)
RACE_TRACK_BORDER_MASK = pygame.mask.from_surface(RACE_TRACK_BORDER)

# Creating variables for finish line and it's mask
RACE_FINISH = pygame.image.load("ID1110-Project-main/imgs/finish_line.png")
RACE_FINISH_MASK = pygame.mask.from_surface(RACE_FINISH)
RACE_FINISH_POSITION = (130, 250)

# Setting the font of the texts displayed on the window
GAME_FONT = pygame.font.SysFont("Times New Roman", 30, bold=True)

# Setting FPS for a constant frame per second of the window irrespective
# of the processor used
FPS = 120

## Defining path coordinates for the computer car so that it travels in a
# specific path
PATH_COORDINATES = [(155, 163), (160, 103), (134, 72), (87, 92), (66, 224), (60, 350), (62, 409), (58, 456), (79, 500), (109, 535), (285, 707), (315, 727), (347, 726), (409, 550), (423, 500), (550, 494), (596, 560), (604, 674), (654, 725),
                    (714, 718), (733, 602), (733, 478), (714, 390), (656, 362), (461, 357), (401, 315), (434, 251), (604, 238), (701, 220), (722, 109), (598, 69), (404, 74), (325, 75), (273, 137), (284, 247), (273, 370), (190, 388), (170, 260)]

# Creating a class which will contain data about different levels,reset
# and game completion


class GameData:
    GAME_LEVELS = 10

    # Initializing the game
    def __init__(self, lvl=1):
        self.level = lvl
        self.began = False
        self.lvl_begin_time = 0

    # Creating a function which will contain information about the 1st level
    def begin_lvl(self):

        self.began = True
        self.lvl_begin_time = time.time()

    # Defining a function for moving to the next level
    def next_lvl(self):

        # Adding music for playing after a level is finished
        if self.level < self.GAME_LEVELS:
            level_passed_sound = pygame.mixer.Sound('ID1110-Project-main\songs\\next_lvl.mp3')
            pygame.mixer.Sound.play(level_passed_sound)

        self.level += 1
        self.began = False

    # Obtainig the total time since the level has begun
    def obtain_lvl_time(self):
        if not self.began:
            return 0
        return round(time.time() - self.lvl_begin_time)

    # Developing a function for reset of the game
    def reset(self):
        if self.level <= 3:
            self.level = 1
        if 3 < self.level <= 6:
            self.level = 3
        if self.level > 6:
            self.level = self.level
        self.began = False
        self.lvl_begin_time = 0

    # A function for the completion of the game
    def game_completed(self):
        return self.level > self.GAME_LEVELS

class BaseCar:

    # Initialization of the base class
    def __init__(self, max_velocity, rot_velocity):
        self.img = self.IMAGE
        self.max_velocity = max_velocity
        self.velocity = 0
        self.rot_velocity = rot_velocity
        self.angle = 0
        self.x, self.y = self.STARTING_POSITION
        self.accln = 0.1

    # A function which defines forward movement of the cars
    def move_fwd(self):
        self.velocity = min(self.velocity + self.accln, self.max_velocity)
        self.move()

    # A function defining backward movement of the cars
    def move_bwd(self):
        self.velocity = max(self.velocity - self.accln, -self.max_velocity / 2)
        self.move()

    # Defining a function which will define left and right movement i.e.,
    # rotation of the cars
    def rotation(self, left=False, right=False):
        if left:
            self.angle += self.rot_velocity
        elif right:
            self.angle -= self.rot_velocity

    # A function which will actually rotate the cars about the centre
    def draw(self, window):
        rotation_about_center(window, self.img, (self.x, self.y), self.angle)

    # A function to allow the cars to move in the exact forward and backward
    # direction while they're rotated by some angle
    def move(self):
        rad = math.radians(self.angle)
        vertical_velocity = math.cos(rad) * self.velocity
        horizontal_velocity = math.sin(rad) * self.velocity

        self.y -= vertical_velocity
        self.x -= horizontal_velocity

    # Defining collision
    def collision(self, mask, x=0, y=0):
        car_mask = pygame.mask.from_surface(self.img)
        offset = ((self.x - x), (self.y - y))
        poi = mask.overlap(car_mask, offset)
        return poi

    # Defining reset function
    def reset(self):
        self.x, self.y = self.STARTING_POSITION
        self.angle = 0
        self.velocity = 0


# Creating class for player car which inherits the base class
class PlayerCar(BaseCar):

    # Creating variables for player car
    count = 0
    IMAGE = PLAYER_CAR
    STARTING_POSITION = (185, 200)

    # Defining a function which will lead to bouncing back when the car
    # collides
    def bounce_back(self):
        self.velocity = -0.8 * self.velocity
        self.move()

    # A function to reduce the speed of the player car when needed
    def speed_reduction(self):
        self.velocity = max(self.velocity - self.accln / 2, 0)
        self.move()

    # Defining a function for brake application in player car
    def brake(self):
        self.velocity = 0

    # Boost function to boost the speed of the player car once
    def boost(self):
        if self.count <= 1:
            self.velocity = 6
            
# Class for computer car inheriting the base class
class ComputerCar(BaseCar):

    # Creating variables for computer car
    IMAGE = COMPUTER_CAR
    STARTING_POSITION = (150, 200)

    # Initializing computer car's class
    def __init__(self, max_velocity, rot_velocity, path=[]):
        super().__init__(max_velocity, rot_velocity)
        self.path = path
        self.current_point = 0
        self.velocity = max_velocity

    # Defining reset function for computer car
    def resett(self):
        self.x, self.y = self.STARTING_POSITION
        self.angle = 0
        self.velocity = self.max_velocity
        self.current_point = 0

    # A function to create points on the window to get the desired path for
    # the computer car
    def create_points(self, window):
        for point in self.path:
            pygame.draw.circle(window, (255, 0, 0), point, 5)

    # Function to draw created points on the window
    def draw(self, window):
        super().draw(window)
        # self.create_points(window)

    # Calculating angle at which computer car is currently
    def angle_calculator(self):
        x_target, y_target = self.path[self.current_point]
        x_difference = x_target - self.x
        y_difference = y_target - self.y

        if y_difference == 0:
            desired_radian_angle = math.pi / 2
        else:
            desired_radian_angle = math.atan(x_difference / y_difference)

        if y_target > self.y:
            desired_radian_angle += math.pi

        difference_in_angle = self.angle - math.degrees(desired_radian_angle)
        if difference_in_angle >= 180:
            difference_in_angle -= 360

        if difference_in_angle > 0:
            self.angle -= min(self.rot_velocity, abs(difference_in_angle))
        else:
            self.angle += min(self.rot_velocity, abs(difference_in_angle))

    # Updating path points of computer car
    def update_path_point(self):
        target = self.path[self.current_point]
        rect = pygame.Rect(
            self.x, self.y, self.img.get_width(), self.img.get_height())
        if rect.collidepoint(*target):
            self.current_point += 1

    # Defining movement of the computer car
    def move(self):
        if self.current_point >= len(self.path):
            return

        self.angle_calculator()
        self.update_path_point()
        super().move()

    # Defining next level functionality of the computer car
    def next_lvl(self, level):
        self.reset()
        self.velocity = self.max_velocity + (level - 1) * 0.2
        self.current_point = 0

# A function for displaying desired images and texts on the window


def draw(window, images, player_car, computer_car, game_info):
    for img, pos in images:
        window.blit(img, pos)

    level_text = GAME_FONT.render(
        f"Level {game_info.level}", 1, (255, 255, 255))
    window.blit(level_text, (10, HT - level_text.get_height() - 70))

    time_text = GAME_FONT.render(
        f"Time: {game_info.obtain_lvl_time()}s", 1, (255, 255, 255))
    window.blit(time_text, (10, HT - time_text.get_height() - 40))

    vel_text = GAME_FONT.render(
        f"Vel: {round(player_car.velocity, 1)}px/s", 1, (255, 255, 255))
    window.blit(vel_text, (10, HT - vel_text.get_height() - 10))

    player_car.draw(window)
    computer_car.draw(window)
    pygame.display.update()


# Function which lists down some commands and resulting actions for the
# movement of the player car
def move_player(player_car):

    keys = pygame.key.get_pressed()
    moved = False

    if keys[pygame.K_a]:
        player_car.rotation(left=True)
    if keys[pygame.K_d]:
        player_car.rotation(right=True)
    if keys[pygame.K_w]:
        moved = True
        player_car.move_fwd()
    if keys[pygame.K_s]:
        moved = True
        player_car.move_bwd()
    if keys[pygame.K_f]:
        player_car.brake()
    if keys[pygame.K_e]:
        if pygame.KEYUP:
            player_car.count += 1
        player_car.boost()

    if not moved:
        player_car.speed_reduction()
        
# Function for handling the collisions of the cars
def handle_collision(player_car, computer_car, game_info):

    # Collision of the player car with the track
    if player_car.collision(RACE_TRACK_BORDER_MASK) is not None:
        player_car.bounce_back()

    # Computer car crossing finishing line before player car
    computer_finish_poi_collision = computer_car.collision(
        RACE_FINISH_MASK, *RACE_FINISH_POSITION)
    if computer_finish_poi_collision is not None:
        pygame.mixer.Sound.play(pygame.mixer.Sound('ID1110-Project-main\songs\\lost_sound.wav'))
        text_align(WINDOW, GAME_FONT, "You lost!")
        pygame.display.update()
        pygame.time.wait(5000)
        game_info.reset()
        player_car.reset()
        computer_car.resett()

    # Player car crossing finishing line before computer car
    player_finish_poi_collision = player_car.collision(
        RACE_FINISH_MASK, *RACE_FINISH_POSITION)
    if player_finish_poi_collision is not None:
        if player_finish_poi_collision[1] == 0:
            player_car.bounce_back()
        else:
            game_info.next_lvl()
            player_car.reset()
            computer_car.next_lvl(game_info.level)
    
# Variables for main game loop
run = True
clock = pygame.time.Clock()
images = [(BACKGROUND, (0, 0)), (PATH, (0, 0)),
          (RACE_FINISH, RACE_FINISH_POSITION), (RACE_TRACK_BORDER, (0, 0))]
player_car = PlayerCar(4, 4)
computer_car = ComputerCar(1.5, 4, PATH_COORDINATES)
game_info = GameData()

# Main game loop
while run:
    clock.tick(FPS)

    draw(WINDOW, images, player_car, computer_car, game_info)

    # Event handling and game loop updates before a level has begun
    while not game_info.began:
        text_align(
            WINDOW,
            GAME_FONT,
            f"Press any key to start level {game_info.level}!")
        pygame.display.update()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break

            if event.type == pygame.KEYDOWN:
                game_info.begin_lvl()

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break

        # #To get points for path of computer car using mouse

        # if event.type==pygame.MOUSEBUTTONDOWN:
        #     pos=pygame.mouse.get_pos()
        #     computer_car.path.append(pos)

    move_player(player_car)
    computer_car.move()

    handle_collision(player_car, computer_car, game_info)

    # Game updates after completing all level
    if game_info.game_completed():
        pygame.mixer.Sound.play(
            pygame.mixer.Sound('ID1110-Project-main\songs\\game_completed.mp3'))
        text_align(WINDOW, GAME_FONT, "You won the game!")
        pygame.display.update()
        pygame.time.wait(3400)
        pygame.quit()

        # #To be used instead of quit if the game is to be reset after finishing all levels

        # game_info.reset()
        # player_car.reset()
        # computer_car.resett()

# #Printing the computer car path developed using mouse

# print(computer_car.path)

# Quit the game and exit Pygame
pygame.quit()
