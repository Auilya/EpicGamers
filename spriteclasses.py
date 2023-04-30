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
        scaled_time = (2 * math.pi * location_time)/ self.period_cycle_time
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

class CountdownSpriteClass:
    surfacego = None
    surface1 = None
    surface2 = None
    surface3 = None
    location_x = 0
    location_y = 0   
    def __init__(self, window_surface, filename1, filename2, filename3, filenamego,  start_x, start_y):
        self.surface1 = pygame.image.load(filename1).convert_alpha()
        self.surface2 = pygame.image.load(filename2).convert_alpha()
        self.surface3 = pygame.image.load(filename3).convert_alpha()
        self.surfacego = pygame.image.load(filenamego).convert_alpha()
        self.location_x = start_x
        self.location_y = start_y
        self.window_surface = window_surface
    def draw(self, delta_time):     
        amplitude_x = 10  # adjust this to change the width of the float
        amplitude_y = 20  # adjust this to change the height of the float
        frequency_x = 1  # adjust this to change the speed in the x direction
        frequency_y = 0.5  # adjust this to change the speed in the y direction
        x = amplitude_x * math.sin(2*math.pi*frequency_x*(delta_time))
        y = amplitude_y * math.cos(2*math.pi*frequency_y*(delta_time))
  
        if delta_time < 1.0:
            self.window_surface.blit(self.surface3, (self.location_x + x, self.location_y + y))
        elif delta_time < 2.0:
            self.window_surface.blit(self.surface2, (self.location_x + x, self.location_y + y))
        elif delta_time < 3.0:
            self.window_surface.blit(self.surface1, (self.location_x + x, self.location_y + y))
        else:
            self.window_surface.blit(self.surfacego, (self.location_x + x, self.location_y + y))  

class ScoreSpriteClass:
    surfacego = None
    surface1 = None
    surface2 = None
    surface3 = None
    location_x = 0
    location_y = 0   
    font1 = None
    textscore = None
    textWPM = None
    textErrors = None
    
    def __init__(self, window_surface, filename1,  start_x, start_y):
        self.surface1 = pygame.image.load(filename1).convert_alpha()
        self.location_x = start_x
        self.location_y = start_y
        self.window_surface = window_surface
        self.font1 = pygame.font.SysFont('HBC.ttf', 30)
        self.textscore = self.font1.render('Score: 0', True, (255, 0, 0))
        self.textWPM = self.font1.render('WPM: 0', True, (255, 0, 0))
        self.textErrors = self.font1.render('Misses: 0', True, (255, 0, 0))

    def setup(self, score, wpm, errors):
        txt = "Score: {:.0f}"
        self.textscore = self.font1.render(txt.format(score), True, (255, 0, 0))
        txt = "WPM: {:.0f}"
        self.textWPM = self.font1.render(txt.format(wpm), True, (255, 0, 0))
        txt = "Errors: {:.0f}"
        self.textErrors = self.font1.render(txt.format(errors), True, (255, 0, 0))        

    def draw(self, delta_time):     
        amplitude_x = 10  # adjust this to change the width of the float
        amplitude_y = 20  # adjust this to change the height of the float
        frequency_x = 1  # adjust this to change the speed in the x direction
        frequency_y = 0.5  # adjust this to change the speed in the y direction
        x = amplitude_x * math.sin(2*math.pi*frequency_x*(delta_time))
        y = amplitude_y * math.cos(2*math.pi*frequency_y*(delta_time))
        #pygame
        t_x = self.location_x + x
        t_y = self.location_y + y
        self.window_surface.blit(self.surface1, (t_x, t_y))
        self.window_surface.blit(self.textscore, (t_x + 90, t_y + 200))
        self.window_surface.blit(self.textWPM, (t_x + 90, t_y + 220))
        self.window_surface.blit(self.textErrors, (t_x + 90, t_y + 240))

class BackgroundSpriteClass:
    surface = None
    window_surface = None
    def __init__(self, window_surface, filename):
        self.window_surface = window_surface
        self.surface = pygame.image.load(filename).convert()

    def draw(self):
        self.window_surface.blit(self.surface, (0, 0))

