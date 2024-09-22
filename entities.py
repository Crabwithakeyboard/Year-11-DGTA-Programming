import pygame as p
import random
import sys
import math


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
                # print('collided')
                self.interact = True


        if self.collisions['down'] or self.collisions['up']: #if set the y-axis velocity to 0 if the entity comes into contact with the top or bottom of any surface.
            self.velocity[1] = 0


    def render(self, surf, camera_scroll = (0,0)):
        surf.blit(self.main.assets['player'], (self.pos[0] - camera_scroll[0], self.pos[1] - camera_scroll[1]))
        # p.draw.circle(surf, p.Color(255, 255, 0), (self.pos[0] - camera_scroll[0], self.pos[1] - camera_scroll[1]), 10)        

class Arrow:
    def __init__(self, main, entity_type, pos, size):
        self.main = main #This is so that everything inside the 'main.py' file is accessible
        self.type = entity_type #The type of entity
        self.pos = list(pos) # making this into a list prevents having multiple entities that spawned on the same coordinates all be affected by the movement(change in position) of one of those entities
        self.charge = False
        self.arrow_charge = 0
        self.size = size #the size of the entity
        self.velocity = [0, 0] #the velocity of the entity, [x, y]
        self.collisions = {'up' : False, 'down' : False, 'left' : False, 'right' : False, } #checks if an entity is in contact with a surface in any direction.     
        self.mpos = list(p.mouse.get_pos())

        #DO NOT TOUCH!!!!
        #WE DON'T KNOW WHY THIS FIXES EVERYTHING, SO DO NOT TOUCH!!!
        self.mpos = (self.mpos[0] / 2, self.mpos[1] / 2) 
        #                 MVP of the above fix:
        ######XXXxxx======= print(self.mpos) =======xxxXXX######
        # Usage: 15+

        self.temp = self.mpos
        
        # self.mpos = (304, 382)
        self.dir = (self.mpos[0] - self.pos[0], self.mpos[1] - self.pos[1])
        # print(self.dir)
        length = math.hypot(*self.dir)
        if length == 0.0:
            self.dir = (0, -1)  # Default to up if no direction
        else:
            self.dir = (self.dir[0] / length, self.dir[1] / length)  # Normalize direction
        self.angle = math.degrees(math.atan2(-self.dir[1], self.dir[0]))

        self.arrow = p.image.load('Data/images/Entity_sprites/Arrow/arrow.png').convert_alpha() 

        self.arrow = p.transform.rotate(self.arrow, self.angle)
        self.speed = 0
        self.arrow_charge = 0

        # print(f"mouse_pos: {self.mpos}, player_pos: {self.pos}, direction: {self.dir}")
        
    def physics_rect(self): #this creates a collision hitbox for entities
        return p.Rect(self.pos[0] , self.pos[1], self.size[0], self.size[1]-27)

    def update(self, tilemap, movement = [0,0], player_pos = None):  
        
        perFrame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])  #how much and in what direction the entity should be moved in this frame
        self.collisions = {'up' : False, 'down' : False, 'left' : False, 'right' : False, } #resets collision detection each frame  
        self.velocity[1] = min(53, self.velocity[1] + 0.02)
        self.interact = False
          
            
        # Update position based on direction and velocity

        entity_rect = self.physics_rect() #This calling the collision hitbox
        for rect in tilemap.physics_rects_around(self.pos): #collision
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
                # print('collided')
                self.interact = True

        if not self.collisions['down'] and not self.collisions['up']: #if set the y-axis velocity to 0 if the entity comes into contact with the top or bottom of any surface.
            self.velocity[1] += 0.5 #downwards acceleration of gravity
        if self.collisions['down'] or self.collisions['up']: #if set the y-axis velocity to 0 if the entity comes into contact with the top or bottom of any surface.
            self.speed = 0 #downwards acceleration of gravity
            
        if self.charge:  # While charging, follow the player's position
            if player_pos:  # player_pos is passed while charging
                self.pos = [player_pos[0] + 10, player_pos[1] + 10]
            self.arrow_charge += 1  # Increase arrow charge continuously while space is held down
            self.velocity = [0, 0]  # Reset velocity during charge
        else:
            # Move arrow based on its direction and velocity after release
            self.pos = [self.pos[0] + self.dir[0] * self.speed, 
                        self.pos[1] + self.dir[1] * self.speed]
            self.speed += self.arrow_charge * 0.1  # Apply accumulated charge to speed
        # print(f"L_collide: {self.collisions['left']}, R_collide: {self.collisions['right']}, U_collide: {self.collisions['up']}, D_collide: {self.collisions['down']}")
        
        self.pos = [self.pos[0] + movement[0] + self.dir[0]*self.speed, 
                    self.pos[1] + movement[1] + self.dir[1]*self.speed] 

    def draw(self, surf, camera_scroll = (0, 0)):
        arrow_rect = self.physics_rect()
        surf.blit(self.arrow, (self.pos[0] - camera_scroll[0], self.pos[1] - camera_scroll[1]))

        # p.draw.line(surf, p.Color(0, 0, 255), self.pos, (self.pos[0] + self.dir[0] * 30, self.pos[1] + self.dir[1] * 30))
        # p.draw.circle(surf, p.Color(123,12,1), self.temp, 10)
        # p.draw.circle(surf, p.Color(225,225,0), self.dir, 10)
        # p.draw.line(surf, p.Color(0, 0, 255), self.pos, (self.pos[0] - self.velocity[0], self.pos[1] + self.velocity[1]))

class Bow:
    def __init__(self, main, entity_type, pos, size):
        self.main = main
        self.type = entity_type
        self.pos = list(pos)
        self.size = size
        self.velocity = [0, 0]
        self.bow_image = self.main.assets['bow']  # Load the bow image once

    def update(self):
        # Update the bow's position to the player's position
        self.pos = [self.main.player.pos[0], self.main.player.pos[1]]

        # Get and adjust the mouse position
        self.mpos = list(p.mouse.get_pos())
        #DO NOT TOUCH!!!!
        #WE DON'T KNOW WHY THIS FIXES EVERYTHING, SO DO NOT TOUCH!!!
        self.mpos = (self.mpos[0] / 2, self.mpos[1] / 2) 
        #                 MVP of the above fix:
        ######XXXxxx======= print(self.mpos) =======xxxXXX######
        # Usage: 15+
        # Calculate direction and angle
        self.dir = (self.mpos[0] - self.pos[0], self.mpos[1] - self.pos[1])
        length = math.hypot(*self.dir)
        if length == 0.0:
            self.dir = (0, -1)  # Default direction if length is zero
        else:
            self.dir = (self.dir[0] / length, self.dir[1] / length)
        self.angle = math.degrees(math.atan2(-self.dir[1], self.dir[0]))

        # Rotate the bow image
        self.rotated_bow_image = p.transform.rotate(self.bow_image, self.angle)

    def render(self, surf, camera_scroll=(0, 0)):
        # Draw the rotated bow image at the bow's position adjusted for camera scroll
        surf.blit(self.rotated_bow_image, (self.pos[0] - camera_scroll[0], self.pos[1] - camera_scroll[1]))
