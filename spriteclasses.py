import pygame
import math

class ShipSpriteClass:
    surface1 = None
    surface2 = None
    surface3 = None
    location_x = 0
    location_y = 0    
    movement_y = 40
    period_cycle_time = 5
    framerate_time = 2
    window_surface = None
    def __init__(self, window_surface, filename1, filename2, filename3, start_x, start_y):
        self.surface1 = pygame.image.load(filename1).convert_alpha()
        self.surface2 = pygame.image.load(filename2).convert_alpha()
        self.surface3 = pygame.image.load(filename3).convert_alpha()
        self.location_x = start_x
        self.location_y = start_y
        self.window_surface = window_surface

    def draw(self, cululative_time):
        frametime = cululative_time % self.framerate_time
        location_time = cululative_time % self.period_cycle_time
        # here is some math...sorry
        # we want to move our ship up and down a bit like it is floating...
        # we want to use the sin function from trig which varies from 1 to -1 in a sinusoidal pattern 
        # when given an input from 0 to 2pi ... 
        # so we have three 'variables'
        # ship start location self.location_y
        # time within out 'cycle' which happens every 5 seconds: location_time
        # How far we want out ship to move up and down: self.movement_y
        # ..so.. first we must scale our input location_time to the sin functions range of between 0 ans 2pi
        scaled_time = (math.pi * location_time)/ self.period_cycle_time
        #now lets get our sin value which will range between 1 and -1
        sin_output = math.sin(scaled_time)
        # now lets scale that result to our movement_y range and calculate our ships location
        loc_y = self.location_y + sin_output * self.movement_y

        #every 1/3 of a second we want to change our 'frame' to a different picture
        if frametime < self.framerate_time * .90:
            self.window_surface.blit(self.surface1, (self.location_x, loc_y))
        elif frametime < self.framerate_time * .93:
            self.window_surface.blit(self.surface2, (self.location_x, loc_y))
        elif frametime < self.framerate_time * .96:
            self.window_surface.blit(self.surface3, (self.location_x, loc_y))
        else:
            self.window_surface.blit(self.surface2, (self.location_x, loc_y))            
        
class BackgroundSpriteClass:
    surface = None
    window_surface = None
    def __init__(self, window_surface, filename):
        self.window_surface = window_surface
        self.surface = pygame.image.load(filename).convert()

    def draw(self):
        self.window_surface.blit(self.surface, (0, 0))

