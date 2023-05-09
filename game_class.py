import pygame
import pygame_gui
from pygame_gui.core import ObjectID
from spriteclasses import *
from events_states import *
from paragraphs import *
import random

class GameTextBox:
    textbox = None
    text = None
    totallength = 0
    counterlength = 0
    manager= None
    container = None
    color_Past =   "'#C756DD'"
    color_Active = "'#FFFFFF'"
    color_Future = "'#3BB9B2'"  

    def __init__(self, text, container, manager): 
        self.totallength = len(text)
        self.counterlength = 0
        self.text = text
        self.manager = manager
        self.container = container        
        self.populateBox()

    def reset(self):
        self.counterlength = 0
        self.populateBox()

    def getProgressPercent(self):
        if self.totallength == 0:
            return 0
        ret = self.counterlength/self.totallength*100.0
        if ret > 100.0: # stuff happens...
            return 100.0
        else:
            return ret

    def tryLetter(self, letter):
        if letter == self.text[self.counterlength:self.counterlength + 1]:
            self.advanceCounter()
            pygame.event.post(pygame.event.Event(CORRECT_CHOICE))
            return True
        else:
            pygame.event.post(pygame.event.Event(WRONG_CHOICE))
            return False

    def advanceCounter(self):
        if self.totallength > 0 and self.counterlength == self.totallength-1:
            pygame.event.post(pygame.event.Event(END_GAME_PAUSE)) # post event that we win    
            self.counterlength += 1
            self.populateBox()            
        else:
            self.counterlength += 1
            self.populateBox()
        
        
    def populateBox(self):
        self.textbox= None
        if self.counterlength == 0: # we are new so we have no portion before the 'cursor'
            newstr = "<font face='HBC.ttf' color=" + self.color_Active + " size=4>" + self.text[:1] + "</font>" \
                "<font face='HBC.ttf' color=" + self.color_Future + " size=4>" + self.text[1:] + "</font>" 
        elif self.counterlength == self.totallength:
            newstr = "<font face='HBC.ttf' color=" + self.color_Past + " size=4>" + self.text[:self.counterlength] + "</font>"+ \
                "<font face='HBC.ttf' color=" + self.color_Active + " size=4>" + self.text[self.counterlength:] + "</font>"
        else:
            newstr = "<font face='HBC.ttf' color=" + self.color_Past + " size=4>" + self.text[:self.counterlength] + "</font>"+ \
                "<font face='HBC.ttf' color=" + self.color_Active + " size=4>" + self.text[self.counterlength:self.counterlength + 1] + "</font>"+ \
                "<font face='HBC.ttf' color=" + self.color_Future + " size=4>" + self.text[self.counterlength + 1:] + "</font>"                    
        self.textbox = pygame_gui.elements.UITextBox(newstr,relative_rect=pygame.Rect((100, 350), (650, 240)), container = self.container, manager = self.manager) 

class GameClass:
    correct_in_a_row = 0
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
    gameBox = None
    gamestarttime = 0    
    wrongcount = 0
    para = paraList[round(random.uniform(0, len(paraList)-1))]
    wpm = 0
    winning_player = None
    winnerSprite = None

    def __init__(self, app): 
        self.app = app
        self.window_surface = self.app.window_surface
        self.ui_manager = self.app.manager
        self.image_background = BackgroundSpriteClass(self.window_surface, "race_background.png")  
        self.Game_Container = pygame_gui.core.UIContainer(relative_rect=pygame.Rect((0,0),(800,600)), manager=self.ui_manager)
        self.Score_Field = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((350, 20), (100, 30)), container= self.Game_Container,text='0000', manager=self.ui_manager)
        self.BackMenu = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((20, 560), (60, 30)), container= self.Game_Container,text='Back', manager=self.ui_manager)
        self.gameBox = GameTextBox(self.para, self.Game_Container, manager=self.ui_manager)        
        self.advanceGame = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((760, 560), (40, 40)), container= self.Game_Container,text='>', manager=self.ui_manager)

        self.ship = ShipSpriteClass(self.window_surface,"Ship_1.png","Ship_2.png","Ship_3.png", 20, 100)
        self.countdown = CountdownSpriteClass(self.window_surface,"Countdown_1.png","Countdown_2.png","Countdown_3.png","Countdown_go.png", 250, 60)        
        self.scoreSprite = ScoreSpriteClass(self.window_surface, "Award.png", 250, 60)
        self.winnerSprite = WinnerSpriteClass(self.window_surface, "Award.png", 250, 60)


    def handle_event(self, event):
        if event.type == SWITCH_TO_MENU:
            self.Game_Container.hide()   
        elif event.type == START_COUNTDOWN_TO_GAME:
            self.gameBox.reset()                     
            self.Game_Container.show()    
            self.countdown_to_game = self.app.time_cumulative  
            pygame.time.set_timer(pygame.event.Event(START_GAME), 4000, 1)         
        elif event.type == START_GAME:
            self.gamestarttime = self.app.time_cumulative             
            self.wrongcount = 0
            self.Game_Container.show()           
        elif event.type == QUIT_PLAY: # give up            
            self.Game_Container.hide()            
        elif event.type == END_GAME_PAUSE:
            self.gameBox.reset()   
            self.Game_Container.show()
            self.countdown_to_menu = self.app.time_cumulative 
            self.gameendtime = self.app.time_cumulative 
            self.wpm = (len(self.para) / 5.0) / ((self.app.time_cumulative - self.gamestarttime)/60)
            score = self.calculate_score()            
            self.scoreSprite.setup(score, self.wpm, self.wrongcount)
            pygame.time.set_timer(pygame.event.Event(GAME_FINISH), 4000, 1) 
        elif event.type == MULTIPLAYER_SHOW_WIN2:
            self.gameBox.reset()   
            self.Game_Container.show()
            self.winnerSprite.update_winner(self.winning_player)
            pygame.time.set_timer(pygame.event.Event(SWITCH_TO_MENU), 4000, 1) 
        elif event.type == QUIT_GAME:            
            self.Game_Container.hide()        
        elif event.type == pygame_gui.UI_BUTTON_PRESSED:            
            if event.ui_element == self.BackMenu:
                pygame.event.post(pygame.event.Event(QUIT_PLAY))
                self.ship.speed = 0
                self.ship.location_x = 0
            if event.ui_element == self.advanceGame:
                self.gameBox.advanceCounter()
        elif event.type == WRONG_CHOICE:
            self.wrongcount += 1
            if self.ship.speed > 0:
                self.ship.speed -= 0.1
        elif event.type == CORRECT_CHOICE and self.ship.speed < 0.9:
            self.ship.speed += 0.3
        elif event.type == pygame.KEYDOWN:               
            if self.app.currentState == GameStates.PLAYING_GAME: # only process keyboard input when game is 'running
                key = event.unicode
                if len(key) and key in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ,.<>1234567890-=+_)(*&^%$#@!~`[]\{}|;':/? ":            
                    self.gameBox.tryLetter(key)
                    

    def do_state(self):
        if self.app.currentState != GameStates.SHOWING_MENU:  
            self.image_background.draw() 
            self.ship.draw(self.app.time_cumulative)
        if self.app.currentState == GameStates.COUNTDOWN_TO_GAME:
            self.countdown.draw(self.app.time_cumulative - self.countdown_to_game)
        elif self.app.currentState == GameStates.SHOW_SCORE:
            self.scoreSprite.draw(self.app.time_cumulative - self.countdown_to_game)
        elif self.app.currentState == GameStates.SHOWING_WINNER:
            self.winnerSprite.draw(self.app.time_cumulative - self.countdown_to_game)

    def calculate_score(self):
        wpm = (len(self.para) / 5.0) / ((self.app.time_cumulative - self.gamestarttime)/60)
        score = wpm * 10 - self.wrongcount * 2
        return score
    
    def update_winner(self, winner):
        self.winning_player = winner