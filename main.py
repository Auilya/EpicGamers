
# we need to import our libaraies
#if these are not installed we need to insall them
# pip install pygame -U
# pip install pygame_gui -U
# -U is not needed if you have never installed it will update instead if already there
import pygame
import pygame_gui
import math

class ShipSpriteClass:
    surface1 = None
    surface2 = None
    surface3 = None
    location_x = 0
    location_y = 0    
    movement_y = 20
    period_cycle_time = 5
    framerate_time = 2
    window_surface = None
    def __init__(self, window_surface, filename1, filename2, filename3, start_x, start_y):
        self.surface1 = pygame.image.load(filename1).convert()
        self.surface1 = pygame.Surface.convert_alpha(self.surface1)
        self.surface2 = pygame.image.load(filename2).convert()
        self.surface2 = pygame.Surface.convert_alpha(self.surface2)
        self.surface3 = pygame.image.load(filename3).convert()
        self.surface3 = pygame.Surface.convert_alpha(self.surface3)
        self.location_x = start_x
        self.location_y = start_y
        self.window_surface = window_surface

    def draw(self, cululative_time):
        frametime = cululative_time % self.framerate_time
        location_time = cululative_time % self.period_cycle_time
        # here is some math...sorry
        # we want to move our ship up and down a bit like it is floating...
        # we want to use the sin function from trig which varies from 1 to -1 in a sinusoidal pattern 
        # when given an input from 0 to 2pi ... 
        # so we have three 'variables'
        # ship start location self.location_y
        # time within out 'cycle' which happens every 5 seconds: location_time
        # How far we want out ship to move up and down: self.movement_y
        # ..so.. first we must scale our input location_time to the sin functions range of between 0 ans 2pi
        print(frametime)
        scaled_time = (math.pi * location_time)/ self.period_cycle_time
        print(scaled_time)
        #now lets get our sin value which will range between 1 and -1
        sin_output = math.sin(scaled_time)
        print(sin_output)
        # now lets scale that result to our movement_y range and calculate our ships location
        loc_y = self.location_y + sin_output * self.movement_y

        #every 1/3 of a second we want to change our 'frame' to a different picture
        if frametime < self.framerate_time * .90:
            self.window_surface.blit(self.surface1, (self.location_x, loc_y))
        elif frametime < self.framerate_time * .93:
            self.window_surface.blit(self.surface2, (self.location_x, loc_y))
        elif frametime < self.framerate_time * .96:
            self.window_surface.blit(self.surface3, (self.location_x, loc_y))
        else:
            self.window_surface.blit(self.surface2, (self.location_x, loc_y))            
        
class BackgroundSpriteClass:
    surface = None
    window_surface = None
    def __init__(self, window_surface, filename):
        self.window_surface = window_surface
        self.surface = pygame.image.load(filename).convert()

    def draw(self):
        self.window_surface.blit(self.surface, (0, 0))

# pygame library needs to initalize itself
pygame.init() 
# name at the top of the window
pygame.display.set_caption('Turbo!') 
window_surface = pygame.display.set_mode((800, 600))

# initalize the gui manager we want to use and HOLD ON to the object it creates
manager = pygame_gui.UIManager((800, 600)) 

# Create a button using our gui library
Start_One = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((550, 550), (100, 50)), text='Start One', manager=manager)
Start_Two = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((650, 550), (100, 50)), text='Start Duo', manager=manager)
namePlayer1 = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((20, 10), (150, 40)), initial_text= "Player 1", manager=manager)
namePlayer2 = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((200, 10), (150, 40)), initial_text= "Player 2", manager=manager)

# load and scale an image stored in the same directory as this .py file
#ship1 = pygame.image.load("ship_1.png").convert()
#ship1 = pygame.Surface.convert_alpha(ship1)
ship = ShipSpriteClass(window_surface,"Ship_1.png","Ship_2.png","Ship_3.png", 200, 200)

coolbackground = BackgroundSpriteClass(window_surface, "background.png")
#coolbackground = pygame.image.load("background.png").convert()
# create a clock object so we can do thigs with time and things like elapsed time
clock = pygame.time.Clock()
# we are want to track cummulative time so we start with it as
time_cumulative = 0
# create a flag for running (and for exiting)
is_running = True
#lets make our image location into variables so we can change them while running
image_location_x = 0
image_location_y = 0
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
                #print some stuff anf move our image
                print('Start Pressed!!')
                print(time_delta) # time since last frame update
                print(time_cumulative) # time since  game started                
                image_location_x += 10
        #this frame could have more than one event so lets process/get any other that may exist
        manager.process_events(event)
            
    #hand elapsed time to the gui manager, it uses this for things like 'hover over' tool tips and such
    manager.update(time_delta)
    
    # all our drawing is now up in the classes!
    coolbackground.draw()
    ship.draw(time_cumulative)    
    
    manager.draw_ui(window_surface)
    # swap the background image we have been drawing on to the screen
    pygame.display.update() 

# deactivates the pygame library
pygame.quit()