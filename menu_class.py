import pygame
import pygame_gui
from pygame_gui.core import ObjectID
from spriteclasses import *
from events_states import *

class MenuClass:
    window_surface = None
    ui_manager = None
    image_background = None
    Menu_Container = None
    Start_One = None
    namePlayer1 = None
    ExitGame = None
    ship2 = None
    ship3 = None
    ship4 = None
    app = None

    def __init__(self, app):
        self.app = app
        self.window_surface = self.app.window_surface
        self.ui_manager = self.app.manager
        self.image_background = BackgroundSpriteClass(self.window_surface, "background.png")     
        self.ship2 = ShipSpriteClass(self.window_surface,"Ship_1.png","Ship_2.png","Ship_3.png", 200, 200)
        self.ship3 = ShipSpriteClass(self.window_surface,"Ship_1.png","Ship_2.png","Ship_3.png", 100, 100)
        self.ship4 = ShipSpriteClass(self.window_surface,"Ship_1.png","Ship_2.png","Ship_3.png", 300, 100)   
        self.Menu_Container = pygame_gui.core.UIContainer(relative_rect=pygame.Rect((0,0),(800,600)), manager=self.ui_manager)
        self.Start_One = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((550, 550), (100, 50)), 
                                                    container= self.Menu_Container, 
                                                    text='Start One', 
                                                    manager=self.ui_manager)
        self.namePlayer1 = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((20, 10), (150, 40)), 
                                                    container= self.Menu_Container,
                                                    initial_text= "Player 1", 
                                                    manager=self.ui_manager)
        self.ExitGame = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((20, 560), (60, 30)), 
                                                    container= self.Menu_Container,text='Exit', 
                                                    manager=self.ui_manager)

    def handle_event(self, event):
        if event.type == SWITCH_TO_MENU:
            self.Menu_Container.show()   
        elif event.type == START_COUNTDOWN_TO_GAME:            
            self.Menu_Container.hide()            
        elif event.type == START_GAME:
            self.Menu_Container.hide()           
        elif event.type == QUIT_PLAY: # give up
            self.Menu_Container.show()            
        elif event.type == END_GAME_PAUSE:
            self.Menu_Container.hide()
        elif event.type == QUIT_GAME:
            self.Menu_Container.hide()        
        elif event.type == pygame_gui.UI_BUTTON_PRESSED:            
            if event.ui_element == self.Start_One:
                pygame.event.post(pygame.event.Event(START_COUNTDOWN_TO_GAME))
            if event.ui_element == self.ExitGame:
                pygame.event.post(pygame.event.Event(QUIT_GAME))

    def do_state(self, state):
        if state == GameStates.SHOWING_MENU:  
            self.image_background.draw() 
            self.ship2.draw(self.app.time_cumulative+ 1.3)  
            self.ship3.draw(self.app.time_cumulative+ 2.7) 
            self.ship4.draw(self.app.time_cumulative+ .7) 
        