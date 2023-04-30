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
    num_players = 0

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
        self.Start_Multi = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((655, 550), (125, 50)), 
                                                    container= self.Menu_Container, 
                                                    text='Start Multi', 
                                                    manager=self.ui_manager)
        self.namePlayer1 = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((20, 10), (150, 40)), 
                                                    container= self.Menu_Container,
                                                    initial_text= "Player 1", 
                                                    manager=self.ui_manager)
        self.ExitGame = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((20, 560), (60, 30)), 
                                                    container= self.Menu_Container,text='Exit', 
                                                    manager=self.ui_manager)
        
        #Materials for Player Select
        self.num_players = 1
        self.Player_Select_Container = pygame_gui.core.UIContainer(relative_rect=pygame.Rect((0,0),(800,600)), manager=self.ui_manager)
        self.playerName1 = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((350, 30), (150, 60)), 
                                                    container= self.Player_Select_Container,
                                                    initial_text= "Player 1", 
                                                    manager=self.ui_manager)
        self.playerName2 = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((350, 130), (150, 60)), 
                                                    container= self.Player_Select_Container,
                                                    initial_text= "Player 2", 
                                                    manager=self.ui_manager)
        self.playerName3 = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((350, 230), (150, 60)), 
                                                    container= self.Player_Select_Container,
                                                    initial_text= "Player 3", 
                                                    manager=self.ui_manager)
        self.playerName4 = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((350, 330), (150, 60)), 
                                                    container= self.Player_Select_Container,
                                                    initial_text= "Player 4", 
                                                    manager=self.ui_manager)
        self.StartMultiplayerGame = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((345, 450), (160, 70)), 
                                                    container= self.Player_Select_Container, 
                                                    text='Start Game', 
                                                    manager=self.ui_manager)
        self.addPlayer = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((600, 250), (60, 60)), 
                                                    container= self.Player_Select_Container, text= "+",manager=self.ui_manager)
        self.deletePlayer = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((200, 250), (60, 60)), 
                                                    container= self.Player_Select_Container, text= "-",manager=self.ui_manager)

    def handle_event(self, event):
        if event.type == SWITCH_TO_MENU:
            self.Player_Select_Container.hide()
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
        elif event.type == MULTIPLAYER_NAME_ENTRY:
            self.Menu_Container.hide()
            self.Player_Select_Container.show()        
            self.update_player_entry(False,True)
        elif event.type == MULTIPLAYER_NEW_PLAYER:
            self.update_player_entry(True,False)
        elif event.type == MULTIPLAYER_LESS_PLAYER:
            self.update_player_entry(False,False)
        elif event.type == pygame_gui.UI_BUTTON_PRESSED:            
            if event.ui_element == self.Start_One:
                pygame.event.post(pygame.event.Event(START_COUNTDOWN_TO_GAME))
            if event.ui_element == self.Start_Multi:
                pygame.event.post(pygame.event.Event(MULTIPLAYER_NAME_ENTRY))
            if event.ui_element == self.addPlayer:
                pygame.event.post(pygame.event.Event(MULTIPLAYER_NEW_PLAYER))
            if event.ui_element == self.deletePlayer:
                pygame.event.post(pygame.event.Event(MULTIPLAYER_LESS_PLAYER))
            if event.ui_element == self.ExitGame:
                pygame.event.post(pygame.event.Event(QUIT_GAME))


    def do_state(self):
        if self.app.currentState == GameStates.SHOWING_MENU:  
            self.image_background.draw() 
            self.ship2.draw(self.app.time_cumulative+ 1.3)  
            self.ship3.draw(self.app.time_cumulative+ 2.7) 
            self.ship4.draw(self.app.time_cumulative+ .7) 
        if self.app.currentState == GameStates.PLAYER_SELECT:
            self.image_background.draw()
    
    def update_player_entry(self, isAdd, resetAll):
        if(isAdd and self.num_players < 4):
            self.num_players += 1
        elif(not(isAdd) and self.num_players > 1):
            self.num_players += -1
        if(resetAll):
            self.num_players = 1
        if(self.num_players == 1):
            self.playerName2.hide()
            self.playerName3.hide()
            self.playerName4.hide()
            self.addPlayer.show()
            self.deletePlayer.hide()
        elif(self.num_players == 2):
            self.playerName2.show()
            self.playerName3.hide()
            self.playerName4.hide()
            self.deletePlayer.show()
        elif(self.num_players == 3):
            self.playerName2.show()
            self.playerName3.show()
            self.playerName4.hide()
            self.addPlayer.show()
        elif(self.num_players == 4):
            self.playerName2.show()
            self.playerName3.show()
            self.playerName4.show()
            self.addPlayer.hide()   
        pygame.display.update()
        