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
        self.collisions = {'up' : False, 'down' : False, 'left' : False, 'right' : False, } #checks if an entity is in contact with a surface in any direction.
        

    def physics_rect(self): #this creates a collision hitbox for entities
        return p.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def update(self, tilemap, movement = (0, 0)): #movement = (x, y)
        perFrame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1]) #how much and in what direction the entity should be moved in this frame
        self.collisions = {'up' : False, 'down' : False, 'left' : False, 'right' : False, } #resets collision detection each frame
        self.velocity[1] += 0.1 #downwards acceleration of gravity
        self.velocity[1] = min(53, self.velocity[1] + 0.1)
        self.interact = False

        self.pos[0] += perFrame_movement[0] # x-axis movement
        entity_rect = self.physics_rect() #This calling the collision hitbox
        for rect in tilemap.physics_rects_around(self.pos): # left/right collision
            if entity_rect.colliderect(rect):
                if perFrame_movement[0] > 0: #If is colliding with something, turn the other way
                    entity_rect.right = rect.left
                    self.collisions['right'] = True #the entity is colliding with a surface to its right
                if perFrame_movement[0] < 0:
                    entity_rect.left = rect.right
                    self.collisions['left'] = True #the entity is colliding with a surface to its left
                self.pos[0] = entity_rect.x
        
        self.pos[1] += perFrame_movement[1] #copied for y-axis movement
        entity_rect = self.physics_rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if perFrame_movement[1] > 0:
                    entity_rect.bottom = rect.top
                    self.collisions['down'] = True
                if perFrame_movement[1] < 0:
                    entity_rect.top = rect.bottom
                    self.collisions['up'] = True
                self.pos[1] = entity_rect.y        

        for rect in tilemap.interact_rects(self.pos):
            if entity_rect.colliderect(rect):
                print('collided')
                self.interact = True


        if self.collisions['down'] or self.collisions['up']: #if set the y-axis velocity to 0 if the entity comes into contact with the top or bottom of any surface.
            self.velocity[1] = 0


    def render(self, surf):
        surf.blit(self.main.assets['player'], self.pos)
