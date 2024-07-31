import pygame as p

BASE_IMAGE_PATH = 'Data/images/' #this will be the default folder that python will try to pull images out of 

def load_image(path):
    img = p.image.load(BASE_IMAGE_PATH + path).convert_alpha() #the '.convert_alpha()' keeps the transparency of all transparent pixels
    return img