import pygame
import pygame_gui
from pygame_gui.core import ObjectID
from spriteclasses import *
from events_states import *


class GameClass:
    window_surface = None
    ui_manager = None
    image_background = None
    Game_Container = None
    Score_Field = None
    BackMenu = None
    ship = None
    countdown_to_game = 0
    countdown_to_menu = 0
    app = None
    countdown = None

    def __init__(self, app): 
        self.app = app
        self.window_surface = self.app.window_surface
        self.ui_manager = self.app.manager
        self.image_background = BackgroundSpriteClass(self.window_surface, "race_background.png")  
        self.Game_Container = pygame_gui.core.UIContainer(relative_rect=pygame.Rect((0,0),(800,600)), manager=self.ui_manager)
        self.Score_Field = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((350, 20), (100, 30)), container= self.Game_Container,text='0000', manager=self.ui_manager)
        self.BackMenu = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((20, 560), (60, 30)), container= self.Game_Container,text='Back', manager=self.ui_manager)
        self.ship = ShipSpriteClass(self.window_surface,"Ship_1.png","Ship_2.png","Ship_3.png", 20, 150)
        self.countdown = CountdownSpriteClass(self.window_surface,"Countdown_1.png","Countdown_2.png","Countdown_3.png","Countdown_go.png", 250, 100)

        
    def handle_event(self, event):
        if event.type == SWITCH_TO_MENU:
            self.Game_Container.hide()   
        elif event.type == START_COUNTDOWN_TO_GAME:                     
            self.Game_Container.show()    
            self.countdown_to_game = self.app.time_cumulative  
            pygame.time.set_timer(pygame.event.Event(START_GAME), 4000, 1)         
        elif event.type == START_GAME:
            self.Game_Container.show()           
        elif event.type == QUIT_PLAY: # give up
            self.Game_Container.hide()            
        elif event.type == END_GAME_PAUSE:
            self.Game_Container.show()
            self.countdown_to_menu = self.app.time_cumulative 
            pygame.time.set_timer(pygame.event.Event(SWITCH_TO_MENU), 4000, 1) 
        elif event.type == QUIT_GAME:
            self.Game_Container.hide()        
        elif event.type == pygame_gui.UI_BUTTON_PRESSED:            
            if event.ui_element == self.BackMenu:
                pygame.event.post(pygame.event.Event(QUIT_PLAY))

    def do_state(self, state):
        if state != GameStates.SHOWING_MENU:  
            self.image_background.draw() 
            self.ship.draw(self.app.time_cumulative)
        if state == GameStates.COUNTDOWN_TO_GAME:
            self.countdown.draw(self.app.time_cumulative - self.countdown_to_game)