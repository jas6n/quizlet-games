import pygame
import os
import random
      

terms = ["Lansing", "Albany", "Springfield", "Indianapolis", "Columbus", "Sacramento"]

definitions = ["Capital of Michigan", "Capital of New York", "Capital of Illinois", "Capital of Indiana", "Capital of Ohio", "Capital of California"]

pygame.init()

BIRD_IMGS = [pygame.image.load(os.path.join("imgs", "bird1.png")),
               pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))),
               pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))]



class Player:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.IMGS = BIRD_IMGS
        self.img = self.IMGS[0]

    def move(self, space_pressed, min, max): # make it so players move with a b c d or 1 2 3 4 or move up to a certain area so you dont have to spam space bar

        if space_pressed:
            self.y -= 4
        else:
            self.y += 3

        if self.y < min:
            self.y = min
        elif self.y > max:
            self.y = max


    def draw(self, screen):
        screen.blit(self.img, (self.x, self.y))

class Obstacle:

    def __init__(self, text, x=0, y=0, color=(0, 0, 0), text_color=(255, 255, 255)):
        self.x = x
        self.y = y
        self.color = color
        self.text_color = text_color
        self.text = text
        self.text_font = pygame.font.Font(None, 30)

    def move(self, speed):
        
        self.x -= speed

    def change_pos(self, x, y):
        self.x = x
        self.y = y

    def change_white(self):
        self.color = (255, 255, 255)
        self.text_color = (0, 0 , 0)
        
    def change_black(self):
        self.text_color = (255, 255, 255)
        self.color = (0, 0 , 0)

    def draw_text(self, text, font, color, x, y, screen):
        img = font.render(text, True, color)
        screen.blit(img, (x, y))

    def draw(self, screen, width, height):
        
        pygame.draw.rect(screen, self.color, [self.x, self.y, width, height])
        self.draw_text(self.text, self.text_font, self.text_color, self.x, self.y, screen)









class Game:

    def __init__(self, width, height):
        self.player = Player(250, 50)
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.lines = [0, self.width / 4, 2 * self.width / 4, 3 * self.width / 4]
        self.game_speed = 2
        self.fps = 60
        self.text_font = pygame.font.Font(None, 30)
        self.timer = pygame.time.Clock()
        self.terms = []
        self.definitions = []
        self.indices = []
        self.a = 0
        self.b = 0
        self.c = 0
        self.d = 0
        self.reviewed_all = False
        self.current = []
        self.cutoff = 0
        self.learn_freq = 3
        self.i = 0
        self.wave = True
        self.mode = True # true means terms are being showed as the answer choices


    def learn(self):

        if not self.reviewed_all:
            if (len(self.current) == 0): # if current block is empty
                for i in range(self.learn_freq):
                    if i + self.cutoff < len(self.terms):
                        self.current.append(i + self.cutoff) # add the current working indices
                    else:
                        break

                self.cutoff += self.learn_freq

                if self.cutoff >= len(self.terms):
                    self.reviewed_all = True
                    self.current = self.indices
                    self.i = 0

            temp = self.i
            self.i += 1 
            self.i = self.i % self.learn_freq

            return self.current[temp] # return the current problem
        else:

            temp = self.i
            self.i += 1 


            return self.current[temp] # return the reviewed problem



    def draw_screen(self): # background of screen
        self.screen.fill((0,0,0)) # background color

        top = pygame.draw.rect(self.screen, (180, 180, 180), [0, 0, self.width, 50])
        bot = pygame.draw.rect(self.screen, (180, 180, 180), [0, self.height - 50, self.width, 50])

        for i in range(len(self.lines)):
            pygame.draw.line(self.screen, (0, 0, 0), (self.lines[i], 0), (self.lines[i], 50), 3) # draws the line separating the cobblestone on top
            pygame.draw.line(self.screen, (0, 0, 0), (self.lines[i], self.height - 50), (self.lines[i], self.height), 3) # on bottom
            self.lines[i] -= self.game_speed
            if self.lines[i] < 0:
                self.lines[i] = self.width

    def terms_and_defs(self):

        for i in range(len(terms)): # initialize terms and defs arrays in game class
            self.terms.append(Obstacle(terms[i]))
            self.definitions.append(Obstacle(definitions[i]))
            self.indices.append(i)

        random.shuffle(self.indices) # shuffle the cards

    def randomize_choices(self, a=False, b=False, c=False, d=False):

        sample = random.sample(range(0, len(terms)), 4)


        if not a:
            self.a = sample[0]
        if not b:
            self.b = sample[1]
        if not c:
            self.c = sample[2]
        if not d:
            self.d = sample[3]



    def move_obstacles(self):


        if self.wave:

            self.randomize_choices()
            self.terms[self.a].change_black()
            self.terms[self.a].change_pos(self.width, 50)

            self.terms[self.b].change_white()
            self.terms[self.b].change_pos(self.width, (self.height - 100) / 4 + 50)

            self.terms[self.c].change_black()
            self.terms[self.c].change_pos(self.width, 2* (self.height - 100) / 4 + 50)

            self.terms[self.d].change_white()
            self.terms[self.d].change_pos(self.width, 3 * (self.height - 100) / 4 + 50)
            self.wave = False

        self.terms[self.a].move(2)
        self.terms[self.a].draw(self.screen, self.width / 5, (self.height - 100) / 4)
        self.terms[self.b].move(2)
        self.terms[self.b].draw(self.screen, self.width / 5, (self.height - 100) / 4)
        self.terms[self.c].move(2)
        self.terms[self.c].draw(self.screen, self.width / 5, (self.height - 100) / 4)
        self.terms[self.d].move(2)
        self.terms[self.d].draw(self.screen, self.width / 5, (self.height - 100) / 4)

        if self.terms[self.a].x < -250:
            self.wave = True



    def run(self):

    
        run = True

        self.terms_and_defs() # create obstacle classes

        while run:

            self.timer.tick(self.fps)

            self.draw_screen()
            

            self.move_obstacles()
            self.player.draw(self.screen)

            key = pygame.key.get_pressed()

            space_pressed = key[pygame.K_SPACE] or key[pygame.K_w]

            self.player.move(space_pressed, 50, self.height - 100)


            for event in pygame.event.get():
                if event.type == pygame.QUIT: # if x was pressed then quit the game
                    run = False

            pygame.display.flip() # updates the screen 

        pygame.quit() # quits the game


game = Game(1000, 600)
game.run()
