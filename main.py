# we need to import our libaraies
#if these are not installed we need to insall them
# pip install pygame -U
# pip install pygame_gui -U 
# -U is not needed if you have never installed it will update instead if already there
import pygame                           # why is this import
from pygame_gui.core import ObjectID    # different than this import
from spriteclasses import *             # and also different than this one....WTH!
from events_states import *
from app_class import *
from menu_class import *
from game_class import *

app = AppClass()
menu = MenuClass(app)
game = GameClass(app)

currentState = GameStates.SHOWING_MENU
nextState = GameStates.SHOWING_MENU                    
pygame.event.post(pygame.event.Event(SWITCH_TO_MENU))  

while app.is_running:    
    app.updateClock()
    for event in pygame.event.get():                
        menu.handle_event(event)
        game.handle_event(event)
        if event.type == SWITCH_TO_MENU:                            
            nextState = GameStates.SHOWING_MENU   
        elif event.type == START_COUNTDOWN_TO_GAME:                        
            nextState = GameStates.COUNTDOWN_TO_GAME            
        elif event.type == START_GAME:                        
            nextState = GameStates.PLAYING_GAME 
        elif event.type == QUIT_PLAY: # give up                        
            nextState = GameStates.SHOWING_MENU 
        elif event.type == END_GAME_PAUSE:                        
            nextState = GameStates.SHOW_SCORE 
        elif event.type == QUIT_GAME:                        
            nextState = GameStates.EXIT                        
        elif event.type == pygame.QUIT:
            pygame.event.post(pygame.event.Event(QUIT_GAME))  
        app.manager.process_events(event)                

    app.manager.update(app.time_delta)
    menu.do_state(currentState)
    game.do_state(currentState)        
    app.manager.draw_ui(app.window_surface)
    pygame.display.update() 
    currentState = nextState # we had a state change, lets set it for next iteration of the look
    if currentState == GameStates.EXIT:
        app.is_running = False
pygame.quit()