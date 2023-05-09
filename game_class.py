import pygame
import pygame_gui
from pygame_gui.core import ObjectID
from spriteclasses import *
from events_states import *
from paragraphs import *
import string 
import random
import math

class GameTextBoxNew:    
    text = None
    totallength = 0
    counterlength = 0
    app = None
    drawlist = []
    color_rect =   (100,100,100)
    color_Past =   (199, 86,221)
    color_Active = (255,255,255)
    color_Future = (59, 185,178) 
    letter_past = []
    letter_active = []
    letter_future = []
    letter_width = []
    letter_location = []
    font = None
    fontsize = 20
    letter_height = None
    box_width = 650
    box_height = 240
    box_width_margin_percent = 0.05 # this means 5 percent
    box_height_margin_percent = 0.05 # this means 5 percent
    box_rect = pygame.Rect((100, 350), (box_width, box_height))
    line_space = 2 #pixels
    word_starting_loc = None    
    
    def __init__(self, app, text): 
        self.totallength = len(text)
        self.counterlength = 0
        self.text = text        
        self.app = app   
        self.font = pygame.font.Font('HBC.ttf', self.fontsize)
        self.initBox()        

    def initBox(self):
        if self.totallength > 0:
            surf = self.font.render("W", True, self.color_Past)
            letter_width, self.letter_height = surf.get_size()             
            where_b_d_spaces = []
            bump_down_distance = []
            word_width = 0
            
            for (index,letter) in zip(range(len(self.text)),self.text):
                self.letter_past.append(self.font.render(letter, True, self.color_Past))
                self.letter_active.append(self.font.render(letter, True, self.color_Active))
                self.letter_future.append(self.font.render(letter, True, self.color_Future))
                letter_width, letter_height = self.letter_past[-1].get_size() 
                bump_down_distance.append(self.letter_height - letter_height) # this is UG-LY
                self.letter_width.append(letter_width)
                word_width += letter_width
                if letter == " ":                    
                    where_b_d_spaces.append((index, word_width)) # where are the word breaks and length of last word
                    word_width = 0   
            where_b_d_spaces.append((-1, 0)) #     
            allowed_width = self.box_width * (1.0 - 2 * self.box_width_margin_percent)
            allowed_row_count = math.floor(self.box_height * (1.0 - 2 * self.box_height_margin_percent) / (self.letter_height + self.line_space))
            tx = self.box_rect.topleft[0]
            ty = self.box_rect.topleft[1]            
            index_of_next_word = 0 
            b_wordstart = True
            cumulative_row_size = 0 
            row_count = 0  
            for index in range(len(self.text)):                                
                if b_wordstart:
                    if cumulative_row_size + where_b_d_spaces[index_of_next_word][1] > allowed_width: #do we have enough space for this word on this line?
                        #this word has to wrap
                        row_count += 1
                        self.letter_location.append((tx + self.box_width * self.box_width_margin_percent, 
                                                ty + self.box_height * self.box_height_margin_percent + bump_down_distance[index] + row_count * (self.letter_height + self.line_space)))
                        cumulative_row_size = self.letter_width[index]                       
                        if row_count > allowed_row_count:
                            print("bounds of box exceeded, too many lines")
                            exit(1)       
                        b_wordstart = False
                    else:
                        if self.text[index] == " ":
                            b_wordstart = True # next letter is start of a word 
                            index_of_next_word += 1
                        else:
                            b_wordstart = False
                        self.letter_location.append((tx + self.box_width * self.box_width_margin_percent + cumulative_row_size, 
                                                ty + self.box_height * self.box_height_margin_percent + bump_down_distance[index] + row_count * (self.letter_height + self.line_space)))  
                        cumulative_row_size += self.letter_width[index]                                      
                    
                else:
                    if self.text[index] == " ":
                        b_wordstart = True # next letter is start of a word 
                        index_of_next_word += 1
                    self.letter_location.append((tx + self.box_width * self.box_width_margin_percent + cumulative_row_size, 
                                               ty + self.box_height * self.box_height_margin_percent + bump_down_distance[index] + row_count * (self.letter_height + self.line_space)))  
                    cumulative_row_size += self.letter_width[index]                  

    def reset(self):
        self.counterlength = 0 # we just rest the progress                

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
        else:
            self.counterlength += 1                    
        
    def drawBox(self):
        pygame.draw.rect(self.app.window_surface, self.color_rect, self.box_rect, 0)
        for index in range(len(self.text)):
            if index == self.counterlength:
                self.app.window_surface.blit(self.letter_active[index], self.letter_location[index])
            elif index < self.counterlength:
                self.app.window_surface.blit(self.letter_past[index], self.letter_location[index])
            else:
                self.app.window_surface.blit(self.letter_future[index], self.letter_location[index])
        


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
        self.gameBoxNew = GameTextBoxNew(self.app, self.para)    
        self.advanceGame = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((760, 560), (40, 40)), container= self.Game_Container,text='>', manager=self.ui_manager)

        self.ship = ShipSpriteClass(self.window_surface,"Ship_1.png","Ship_2.png","Ship_3.png", 20, 100)
        self.countdown = CountdownSpriteClass(self.window_surface,"Countdown_1.png","Countdown_2.png","Countdown_3.png","Countdown_go.png", 250, 60)        
        self.scoreSprite = ScoreSpriteClass(self.window_surface, "Award.png", 250, 60)
        self.winnerSprite = WinnerSpriteClass(self.window_surface, "Award.png", 250, 60)


    def handle_event(self, event):
        if event.type == SWITCH_TO_MENU:
            self.Game_Container.hide()   
        elif event.type == START_COUNTDOWN_TO_GAME:
            self.gameBoxNew.reset()                     
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
            self.gameBoxNew.reset()   
            self.Game_Container.show()
            self.countdown_to_menu = self.app.time_cumulative 
            self.gameendtime = self.app.time_cumulative 
            self.wpm = (len(self.para) / 5.0) / ((self.app.time_cumulative - self.gamestarttime)/60)
            score = self.calculate_score()            
            self.scoreSprite.setup(score, self.wpm, self.wrongcount)
            pygame.time.set_timer(pygame.event.Event(GAME_FINISH), 4000, 1) 
        elif event.type == MULTIPLAYER_SHOW_WIN2:
            self.gameBoxNew.reset()   
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
                self.gameBoxNew.advanceCounter()
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
                    self.gameBoxNew.tryLetter(key)
                    

    def do_state(self):
        if self.app.currentState != GameStates.SHOWING_MENU:  
            self.image_background.draw() 
            self.gameBoxNew.drawBox()
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