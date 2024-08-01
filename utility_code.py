import os
import pygame as p

BASE_IMAGE_PATH = 'Data/images/' #this will be the default folder that python will try to pull images out of 

def load_image(path):
    img = p.image.load(BASE_IMAGE_PATH + path).convert_alpha() #the '.convert_alpha()' keeps the transparency of all transparent pixels
    return img

def load_images(path):
    images = [] #List of all loaded images
    for img_name in os.listdir(BASE_IMAGE_PATH + path): # operating_system.list_directory
        images.append(load_image(path + '/' + img_name)) # appends the load_image's loaded image onto the list that contains all loaded images
        return images