import pygame
import pygame_gui
from pygame_gui.core import ObjectID
from events_states import *


class MultiplayerManager():

    #This class keeps track of who is playing, scores, etc.

    player_scores = []
    player_names = []
    num_players = 1
    current_player = 0

    def __init__(self):
        player_scores = []
        player_names = []
        num_players = 1
        current_player = 0

    def handle_event(self,event):
        if event.type == MULTIPLAYER_NEW_PLAYER:
            self.update_players(True)
        elif event.type == MULTIPLAYER_LESS_PLAYER:
            self.update_players(False)
        elif event.type == SWITCH_TO_MENU:
            self.reset_all()
        elif event.type == MULTIPLAYER_GAME_START:
            pygame.event.post(pygame.event.Event(MULTIPLAYER_NEXT_PLAYER))
        elif event.type == MULTIPLAYER_NEXT_PLAYER:
            self.next_player_start()
            pygame.event.post(pygame.event.Event(START_COUNTDOWN_TO_GAME))
        elif event.type == GAME_FINISH:
            if(self.current_player+1 > self.num_players):
                pygame.event.post(pygame.event.Event(MULTIPLAYER_SHOW_WIN))
            else:
                pygame.event.post(pygame.event.Event(MULTIPLAYER_NEXT_PLAYER))
            

    
    def reset_all(self):
        player_scores = []
        player_names = []
        num_players = 1
        pygame.display.set_caption("Turbo!")
    
    def update_players(self,isAdd):
        if(isAdd and self.num_players < 4):
            self.num_players += 1
        elif(not isAdd and self.num_players > 1):
            self.num_players += -1
    
    def update_scores(self,score):
        self.player_scores.append(score)
    
    def fill_in_names(self, name_list):
        self.player_names = name_list

    def next_player_start(self):
        try: 
            pygame.display.set_caption(self.player_names[self.current_player]+", your turn!")
            self.current_player += 1
        except:
            IndexError
    
    def package_winner_information(self):
        index = 0
        for item in range(0,self.num_players):
            #Let's ignore ties for now.
            if(self.player_scores[item] > self.player_scores[index]):
                index = item
        return self.player_names[index]