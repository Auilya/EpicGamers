import pygame                           
import pygame_gui                       # why is this import
from pygame_gui.core import ObjectID    # different than this import
from spriteclasses import *             # and also different than this one....WTH!
from events_states import *
from menu_class import *
from game_class import *

class AppClass():
    is_running = True 
    window_surface = None
    manager = None
    clock = None
    time_delta = 0
    time_cumulative = 0
    currentState = None
    nextState =  None

    def __init__(self):
        pygame.init() 
        pygame.display.set_caption('Turbo!') 
        self.window_surface = pygame.display.set_mode((800, 600)) #window_surface = pygame.display.set_mode((800, 600), pygame.FULLSCREEN)
        self.manager = pygame_gui.UIManager((800, 600), "themes.json") 
        self.clock = pygame.time.Clock()
        self.time_cumulative = 0 
        self.countdown_start = 0

    def updateClock(self):
        self.time_delta = self.clock.tick(60)/1000.0          
        self.time_cumulative = self.time_delta + self.time_cumulative  