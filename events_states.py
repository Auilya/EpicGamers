import pygame
from enum import Enum

#lets make a bunch of events
SWITCH_TO_MENU          = pygame.event.custom_type()
START_COUNTDOWN_TO_GAME = pygame.event.custom_type()
START_GAME              = pygame.event.custom_type()
END_GAME_PAUSE          = pygame.event.custom_type()
QUIT_GAME               = pygame.event.custom_type() # shut it down
QUIT_PLAY               = pygame.event.custom_type() # give up on play and return to menu
CORRECT_CHOICE          = pygame.event.custom_type()
WRONG_CHOICE            = pygame.event.custom_type()
GAME_FINISH             = pygame.event.custom_type()

MULTIPLAYER_NAME_ENTRY  = pygame.event.custom_type() # Multiplayer-related events
MULTIPLAYER_NEW_PLAYER  = pygame.event.custom_type()
MULTIPLAYER_LESS_PLAYER = pygame.event.custom_type()
MULTIPLAYER_GAME_START  = pygame.event.custom_type()
MULTIPLAYER_NEXT_PLAYER = pygame.event.custom_type()
MULTIPLAYER_SHOW_WIN    = pygame.event.custom_type()
MULTIPLAYER_SHOW_WIN2   = pygame.event.custom_type()

#lets make sone states
class GameStates(Enum):
    SHOWING_MENU        = 1
    COUNTDOWN_TO_GAME   = 2
    PLAYING_GAME        = 3
    SHOW_SCORE          = 4    
    EXIT                = 5
    PLAYER_SELECT       = 6
    SHOWING_WINNER      = 7