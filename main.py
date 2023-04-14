
# we need to import our libaraies
#if these are not installed we need to insall them
# pip install pygame -U
# pip install pygame_gui -U 
# -U is not needed if you have never installed it will update instead if already there
import pygame
import pygame_gui
from spriteclasses import *

# pygame library needs to initalize itself
pygame.init() 
# name at the top of the window
pygame.display.set_caption('Turbo!') 
#window_surface = pygame.display.set_mode((800, 600), pygame.FULLSCREEN)
window_surface = pygame.display.set_mode((800, 600))

# initalize the gui manager we want to use and HOLD ON to the object it creates
manager = pygame_gui.UIManager((800, 600)) 

# Create a button using our gui library
Start_One = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((550, 550), (100, 50)), text='Start One', manager=manager)
Start_Two = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((650, 550), (100, 50)), text='Start Duo', manager=manager)
namePlayer1 = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((20, 10), (150, 40)), initial_text= "Player 1", manager=manager)
namePlayer2 = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((200, 10), (150, 40)), initial_text= "Player 2", manager=manager)

ship = ShipSpriteClass(window_surface,"Ship_1.png","Ship_2.png","Ship_3.png", 200, 200)
ship2 = ShipSpriteClass(window_surface,"Ship_1.png","Ship_2.png","Ship_3.png", 300, 300)
ship3 = ShipSpriteClass(window_surface,"Ship_1.png","Ship_2.png","Ship_3.png", 100, 100)
coolbackground = BackgroundSpriteClass(window_surface, "background.png")
# create a clock object so we can do thigs with time and things like elapsed time
clock = pygame.time.Clock()
# we are want to track cummulative time so we start with it as
time_cumulative = 0
# create a flag for running (and for exiting)
is_running = True
#lets loop until we are told to quit by our is_running flag
while is_running:
    #lets get our our time in between 'frames' aka time since new image was displayed
    time_delta = clock.tick(60)/1000.0
    # keep track of cumulative time
    time_cumulative = time_delta + time_cumulative
    #did 'events' happen (such as button presses or exit hit)
    for event in pygame.event.get():
        # did someone hit quit (x at top left corner)
        if event.type == pygame.QUIT:
            #inform and set the flag to not running so we quit next loop through
            print('Lets quit.')
            is_running = False

        #someone hit a button (could have more than one)
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            #which button was hit...was it this one?
            if event.ui_element == Start_One:
                is_running = False
        
        #this frame could have more than one event so lets process/get any other that may exist
        manager.process_events(event)
            
    #hand elapsed time to the gui manager, it uses this for things like 'hover over' tool tips and such
    manager.update(time_delta)
    
    # all our drawing is now up in the classes!
    coolbackground.draw()
    ship.draw(time_cumulative)    
    ship2.draw(time_cumulative+ 1.3)  
    ship3.draw(time_cumulative+ 2.7) 
    
    manager.draw_ui(window_surface)
    # swap the background image we have been drawing on to the screen
    pygame.display.update() 

# deactivates the pygame library
pygame.quit()