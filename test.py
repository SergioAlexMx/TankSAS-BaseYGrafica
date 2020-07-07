import spritesheet
import pygame

pygame.init()
# Window information
display_w = 1000
display_h = 700
window = pygame.display.set_mode((display_w, display_h))

ss = spritesheet.Spritesheet('array1.png')
image = ss.image_at((0, 0, 90, 90))
images = []
images = ss.images_at((0, 0, 90, 90),(91, 0, 90,90), colorkey=(255, 255, 255))
