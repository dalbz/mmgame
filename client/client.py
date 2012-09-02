import socket
import json
import pygame 
import sys
import glob
import time
from pygame.locals import * 
from pygame import * 

s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

clock = pygame.time.Clock()

MAX  = 65535
s.connect(("localhost", 43278))
print 'Client socket name is', s.getsockname()
delay = 0.1
while True:
    msg = {'user' : '13', 'event' : 'login'}
    s.send(json.dumps(msg))
    print 'Waiting up to', delay, 'seconds for a reply'
    s.settimeout(delay)
    try:
        data = s.recv(MAX)
    except socket.timeout:
        delay *= 2 # wait even longer for the next request
        if delay > 2.0:
            raise RuntimeError('I think the server is down')
    except:
        raise # a real error so we let the user see it
    else: 
        break

print 'The server says ', repr(data)

class Player:

    def __init__(self): 
        self.x = 0
        self.y = 0
        self.img = []
        self.img.append(pygame.image.load(".\\mmgame\\client\\assets\\hero\\walk\\u\\1.png"))
        self.img.append(pygame.image.load(".\\mmgame\\client\\assets\\hero\\walk\\u\\2.png"))
        self.img.append(pygame.image.load(".\\mmgame\\client\\assets\\hero\\walk\\u\\1.png"))
        self.img.append(pygame.image.load(".\\mmgame\\client\\assets\\hero\\walk\\u\\3.png"))
        self.img.append(pygame.image.load(".\\mmgame\\client\\assets\\hero\\walk\\d\\1.png"))
        self.img.append(pygame.image.load(".\\mmgame\\client\\assets\\hero\\walk\\d\\2.png"))
        self.img.append(pygame.image.load(".\\mmgame\\client\\assets\\hero\\walk\\d\\1.png"))
        self.img.append(pygame.image.load(".\\mmgame\\client\\assets\\hero\\walk\\d\\3.png"))
        self.img.append(pygame.image.load(".\\mmgame\\client\\assets\\hero\\walk\\r\\1.png"))
        self.img.append(pygame.image.load(".\\mmgame\\client\\assets\\hero\\walk\\r\\2.png"))
        self.img.append(pygame.image.load(".\\mmgame\\client\\assets\\hero\\walk\\r\\1.png"))
        self.img.append(pygame.image.load(".\\mmgame\\client\\assets\\hero\\walk\\r\\3.png"))
        self.img.append(pygame.image.load(".\\mmgame\\client\\assets\\hero\\walk\\l\\1.png"))
        self.img.append(pygame.image.load(".\\mmgame\\client\\assets\\hero\\walk\\l\\2.png"))
        self.img.append(pygame.image.load(".\\mmgame\\client\\assets\\hero\\walk\\l\\1.png"))
        self.img.append(pygame.image.load(".\\mmgame\\client\\assets\\hero\\walk\\l\\3.png"))
        self.img_ind = 0
        self.img_dir = 1

    def draw(self, screen):
        screen.blit(self.img[self.img_ind], (self.x, self.y))

screen_mode = (640, 480) 
color_black = 0,0,0

class Game: 
     
    # this gets called first
    def __init__(self, main_player): 
         
        pygame.init() 
        self.screen = pygame.display.set_mode(screen_mode) 
        pygame.display.set_caption("PyGame intro") 
        
        self.main_player = main_player
        self.quit = False
     
    # put game update code here
    def update(self): 
     
        return

    # put drawing code here
    def draw(self): 
        self.screen.fill(color_black) 
        self.main_player.draw(self.screen)
        #self.screen.fill(color_black) 
        pygame.display.flip() 
     
    # the main game loop
    def mainLoop(self): 
     
        while not self.quit: 

            clock.tick(60)
             
            # handle events
            for event in pygame.event.get(): 
                 
                if event.type == KEYDOWN: 
                    if event.key == 273:
                        msg = {'user' : '13', 'event' : 'up'}
                        self.main_player.img_dir = 0

                    if event.key == 274:
                        msg = {'user' : '13', 'event' : 'down'}
                        self.main_player.img_dir = 1

                    if event.key == 275:
                        msg = {'user' : '13', 'event' : 'right'}
                        self.main_player.img_dir = 2

                    if event.key == 276:
                        msg = {'user' : '13', 'event' : 'left'}
                        self.main_player.img_dir = 3
                        
                    if (event.key >= 273 and event.key <= 276):
                        s.send(json.dumps(msg))
                        data = s.recv(MAX)
                        data = json.loads(data)
                        self.main_player.x = data["13"]["pos"][0]
                        self.main_player.y = data["13"]["pos"][1]
                        self.main_player.img_ind = self.main_player.img_dir*4 + (self.main_player.img_ind + 1) % 4


                if event.type == QUIT: 
                    self.quit = True

                   
            self.update() 
            self.draw()             
     
if __name__ == '__main__' : 
     
    player1 = Player() 
    game = Game(player1) 
    game.mainLoop() 