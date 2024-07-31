import pygame as p
import random
import sys

class EntityPhysics: #This class will handle the physics calculations for all entities
    def __init__(self, main, entity_type, pos, size):
        self.main = main #This is so that everything inside the 'main.py' file is accessible
        self.type = entity_type #The type of entitie
        self.pos = list(pos) # making this into a list prevents having multiple entities that spawned on the same coordinates all be affected by the movement(change in position) of one of those entities
        self.size = size #the size of the entity
        self.velocity = [0, 0] #the velocity of the entity, [x, y]

    def update(self, movement = (0, 0)): #movement = (x, y)
        perFrame_movement = (movement[0] + self.velocity[0], movement[1], self.velocity[1]) #how much and in what direction the entity should be moved in this frame

        self.pos[0] += perFrame_movement[0]
        self.pos[1] += perFrame_movement[1]

    def render(self, surf):
        surf.blit(self.main.assets['player'], self.pos)