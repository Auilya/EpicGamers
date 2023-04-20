
# we need to import our libaraies
#if these are not installed we need to insall them
# pip install pygame -U
# pip install pygame_gui -U 
# -U is not needed if you have never installed it will update instead if already there
import pygame
import pygame_gui
from pygame_gui.core import ObjectID
from spriteclasses import *
from enum import Enum


#lets make a bunch of events
SWITCH_TO_MENU          = pygame.event.custom_type()
START_COUNTDOWN_TO_GAME = pygame.event.custom_type()
START_GAME              = pygame.event.custom_type()
END_GAME_PAUSE          = pygame.event.custom_type()
QUIT_GAME               = pygame.event.custom_type() # shut it down
QUIT_PLAY               = pygame.event.custom_type() # give up on play and return to menu

#lets make sone states
class GameStates(Enum):
    SHOWING_MENU        = 1
    COUNTDOWN_TO_GAME   = 2
    PLAYING_GAME        = 3
    SHOW_SCORE          = 4    
    EXIT                = 5

pygame.init()  # pygame library needs to initalize itself
pygame.display.set_caption('Turbo!') # name at the top of the window

#print(pygame.font.get_fonts())
window_surface = pygame.display.set_mode((800, 600)) #window_surface = pygame.display.set_mode((800, 600), pygame.FULLSCREEN)
manager = pygame_gui.UIManager((800, 600), "themes.json") # initalize the gui manager we want to use and HOLD ON to the object it creates

# lets make containers to hold the controls for each 'screen'
Menu_Container = pygame_gui.core.UIContainer(relative_rect=pygame.Rect((0,0),(800,600)), manager=manager)

Start_One = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((550, 550), (100, 50)), container= Menu_Container, text='Start One', manager=manager)
#Start_Two = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((650, 550), (100, 50)), container= Menu_Container,text='Start Duo', manager=manager)
namePlayer1 = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((20, 10), (150, 40)), container= Menu_Container,initial_text= "Player 1", manager=manager)
#namePlayer2 = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((200, 10), (150, 40)), container= Menu_Container,initial_text= "Player 2", manager=manager)
ExitGame = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((20, 560), (60, 30)), container= Menu_Container,text='Exit', manager=manager)

Game_Container = pygame_gui.core.UIContainer(relative_rect=pygame.Rect((0,0),(800,600)), manager=manager)
Score_Field = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((350, 20), (100, 30)), container= Game_Container,text='0000', manager=manager)
BackMenu = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((20, 560), (60, 30)), container= Game_Container,text='Back', manager=manager)


ship = ShipSpriteClass(window_surface,"Ship_1.png","Ship_2.png","Ship_3.png", 200, 200)
ship2 = ShipSpriteClass(window_surface,"Ship_1.png","Ship_2.png","Ship_3.png", 300, 300)
ship3 = ShipSpriteClass(window_surface,"Ship_1.png","Ship_2.png","Ship_3.png", 100, 100)
ship4 = ShipSpriteClass(window_surface,"Ship_1.png","Ship_2.png","Ship_3.png", 300, 100)
coolbackground = BackgroundSpriteClass(window_surface, "background.png")

# create a clock object so we can do thigs with time and things like elapsed time
clock = pygame.time.Clock()
time_cumulative = 0 # we are want to track cummulative time so we start with it as
is_running = True # create a flag for running (and for exiting)

currentState = GameStates.SHOWING_MENU
nextState = GameStates.SHOWING_MENU                     # used as temporary storage when changing states
pygame.event.post(pygame.event.Event(SWITCH_TO_MENU))   # two things happening here, the inner argument creates the event, then we 'post it'

#lets loop until we are told to quit by our is_running flag
countdown_start = 0
while is_running:    
    time_delta = clock.tick(60)/1000.0              #lets get our our time in between 'frames' aka time since new image was displayed
    time_cumulative = time_delta + time_cumulative  # keep track of cumulative time        
    for event in pygame.event.get():                #did 'events' happen (such as button presses or exit hit)

        if event.type == SWITCH_TO_MENU:
            # in here we have to disable UI controls related to anything but the main menu
            # and enable all the controls related to the main menu
            Menu_Container.show()       
            Game_Container.hide()
            nextState = GameStates.SHOWING_MENU   
        elif event.type == START_COUNTDOWN_TO_GAME:
            # clear and restart the game structures (will display during countdown, dont want to see old data)
            Menu_Container.hide()
            Game_Container.show()
            nextState = GameStates.COUNTDOWN_TO_GAME   
            countdown_start = time_cumulative 
            pygame.time.set_timer(pygame.event.Event(START_GAME), 4000) # countdown timer           
        elif event.type == START_GAME:
            Menu_Container.hide()
            Game_Container.show()
            nextState = GameStates.PLAYING_GAME 
        elif event.type == QUIT_PLAY: # give up
            Menu_Container.show()
            Game_Container.hide()
            nextState = GameStates.SHOWING_MENU 
        elif event.type == END_GAME_PAUSE:
            Menu_Container.hide()
            Game_Container.show()
            nextState = GameStates.SHOW_SCORE 
            countdown_start = time_cumulative 
            pygame.time.set_timer(pygame.event.Event(SWITCH_TO_MENU), 4000) # 10 second countdown timer               
        elif event.type == QUIT_GAME:
            Menu_Container.hide()
            Game_Container.show()
            nextState = GameStates.EXIT                        

        # did someone hit quit (x at top left corner)
        if event.type == pygame.QUIT:
            pygame.event.post(pygame.event.Event(QUIT_GAME))  

        #someone hit a button (could have more than one)
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            #which button was hit...was it this one?
            if event.ui_element == Start_One:
                pygame.event.post(pygame.event.Event(START_COUNTDOWN_TO_GAME))
            if event.ui_element == BackMenu:
                pygame.event.post(pygame.event.Event(QUIT_PLAY))
            if event.ui_element == ExitGame:
                pygame.event.post(pygame.event.Event(QUIT_GAME))                
            
        
        #this frame could have more than one event so lets process/get any other that may exist
        manager.process_events(event)
            
    #hand elapsed time to the gui manager, it uses this for things like 'hover over' tool tips and such
    manager.update(time_delta)
    
    # all our drawing is now up in the classes!
    coolbackground.draw()
    ship.draw(time_cumulative)    
    ship2.draw(time_cumulative+ 1.3)  
    ship3.draw(time_cumulative+ 2.7) 
    ship4.draw(time_cumulative+ .7) 
    
    manager.draw_ui(window_surface)
    # swap the background image we have been drawing on to the screen
    pygame.display.update() 
    currentState = nextState # we had a state change, lets set it for next iteration of the look
    if currentState == GameStates.EXIT:
        is_running = False
        
# deactivates the pygame library
pygame.quit()