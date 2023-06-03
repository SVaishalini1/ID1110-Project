import pygame
from pygame.locals import *

# Initialize Pygame and related modules
pygame.init()
pygame.font.init()

# Defining rotation of the cars about their centre for turning


def rotation_about_center(window, img, top_left, angle):
    rotated_image = pygame.transform.rotate(img, angle)
    new_rect = rotated_image.get_rect(
        center=img.get_rect(topleft=top_left).center)
    window.blit(rotated_image, new_rect.topleft)

# A function to resize an image by a given factor


def resize_image(image, fact):
    size = round(image.get_width() * fact), round(image.get_height() * fact)
    return pygame.transform.scale(image, size)

# Function for displaying the text at an aligned position


def text_align(window, font, text):
    render = font.render(text, True, (255, 140, 0))
    window.blit(
        render,
        (window.get_width() /
         2 -
         render.get_width() /
         2,
         (window.get_height() /
         2 -
         render.get_height() /
         2) - 20))
