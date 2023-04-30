import pygame
import pygame_gui
from pygame_gui.core import ObjectID
from events_states import *


class MultiplayerManager():

    #This class keeps track of who is playing, scores, etc.

    player_scores = []
    player_names = []
    num_players = 1

    def __init__(self):
        player_scores = []
        player_names = []
        num_players = 1

    def handle_events(self,event):
        if event.type == MULTIPLAYER_NEW_PLAYER:
            self.update_players(True)
        elif event.type == MULTIPLAYER_LESS_PLAYER:
            self.update_players(False)
        elif event.type == SWITCH_TO_MENU:
            self.reset_all()

    
    def reset_all(self):
        player_scores = []
        player_names = []
        num_players = 1
    
    def update_players(self,isAdd):
        if(isAdd and self.num_players < 4):
            self.num_players += 1
        elif(not isAdd and self.num_players > 1):
            self.num_players += -1