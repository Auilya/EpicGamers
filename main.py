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
from paragraphs import *
from multiplayer_manager import *

app = AppClass()
menu = MenuClass(app)
game = GameClass(app)
manager = MultiplayerManager()

nextStates = {SWITCH_TO_MENU: GameStates.SHOWING_MENU, START_COUNTDOWN_TO_GAME: GameStates.COUNTDOWN_TO_GAME,
              START_GAME: GameStates.PLAYING_GAME, QUIT_PLAY: GameStates.SHOWING_MENU, 
              END_GAME_PAUSE: GameStates.SHOW_SCORE, QUIT_GAME: GameStates.EXIT, MULTIPLAYER_NAME_ENTRY: GameStates.PLAYER_SELECT
              }

app.currentState = GameStates.SHOWING_MENU
app.nextState = GameStates.SHOWING_MENU                    
pygame.event.post(pygame.event.Event(SWITCH_TO_MENU))  

while app.is_running:    
    app.updateClock()
    for event in pygame.event.get():                
        menu.handle_event(event)
        game.handle_event(event)
        manager.handle_event(event)

        try: 
            app.nextState = nextStates[event.type]
        except:
            KeyError

        if event.type == MULTIPLAYER_GAME_START: 
            manager.fill_in_names(menu.package_player_information())
        elif event.type == MULTIPLAYER_NEXT_PLAYER:
            if manager.num_players > 1:
                manager.update_scores(game.calculate_score())
            else:
                app.nextState = GameStates.SHOWING_MENU
        elif event.type == MULTIPLAYER_SHOW_WIN:
            game.update_winner(manager.package_winner_information())
            pygame.event.post(pygame.event.Event(MULTIPLAYER_SHOW_WIN2))  
            app.nextState = GameStates.SHOWING_WINNER         
        elif event.type == pygame.QUIT:
            pygame.event.post(pygame.event.Event(QUIT_GAME))  
        app.manager.process_events(event)                

    app.manager.update(app.time_delta)
    menu.do_state()
    game.do_state()        
    app.manager.draw_ui(app.window_surface)
    pygame.display.update() 
    app.currentState = app.nextState # we had a state change, lets set it for next iteration of the look
    if app.currentState == GameStates.EXIT:
        app.is_running = False
pygame.quit()
