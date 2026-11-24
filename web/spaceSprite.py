import pygame, random, math, sys
pygame.init()


class Wallpaper(pygame.sprite.Sprite):
    '''This class creates the moving wall paper. It is infinitely moving
    down. This is achieved when the image gets to a certain position and is
    resetted to the starting position.'''
    def __init__(self,screen):
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        self.__screen = screen
        self.image = pygame.image.load("space.gif")
        self.rect = self.image.get_rect()
        self.rect.bottom = self.__screen.get_height()
    
    def update(self):
        '''This function updates the position of the wallpaper.'''
        self.rect.bottom += 3
        if self.rect.bottom > 4680:
            self.rect.bottom = self.__screen.get_height()
         
class Player(pygame.sprite.Sprite):
    '''This class creates the player. While the player is alive, it will
    have red and green lights blinking. The player can move right, left, down,
    and up. If the player is exploding, it will rapidly load the other images,
    making it animated. There is also shooting detection that avoids
    the player form shooting while they're exploding and the enemy can't shoot
    the player when they're exploding.'''
    def __init__(self):
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        #loads all images that are related to the Player sprite
        self.__playerimage = []
        for imagenumber in range(0,18):
            self.__playerimage.append(pygame.image.load("./Player/boom" + str(imagenumber)+".gif"))
        #setting initial values
        self.__exploding = False
        self.__slow_counter = 0 
        self.__slow_blink = 0
        self.__reset_counter = 0
        self.reset()
        
    def move_vertical(self,y_change):
        '''This accepts the value to change the vertical movement when a key
        is pressed or D-pad moved.'''        
        self.__dy = y_change[1] 
        
    def move_horizontal(self,x_change):
        '''This accepts the value to change the horiztonal movement when a key
        is pressed or D-pad moved.'''
        self.__dx = x_change[1]

    def explode(self):
        '''This makes the player sprite load the explosion images.'''
        self.__exploding = True
        
    def get_explode(self):
        '''This function returns the status of self.__exploding. This is used
        to restrict the enemy's missile ability to deduct a hit if the player
        is hit during explosion.'''
        return self.__exploding   
        
    def get_canshoot(self):
        '''This function returns the status of self.__canshoot. It is used
        to check if the player is able to shoot or not.'''
        return self.__canshoot
       
    def update(self):
        '''This function updates the position of the player. The player can move
        in any direction as long as it is below 400 pixels form the top. It also
        will make the player explode is needed. Or else, the player will be
        altering between two images which makes it look like the lights are
        blinking.'''
        if self.__exploding:
            self.__dy = 0
            self.__dx = 0
            self.__canshoot = False
            #coutner used to slow down animations
            self.__slow_counter += 1
            #updates an image every 2 frames
            if self.__slow_counter == 2:
                if self.__imagenumber < len(self.__playerimage):
                    self.image = self.__playerimage[self.__imagenumber]
                    self.__imagenumber += 1
                else:
                    self.__reset_counter += 1    
                    #resets the player after 60 frames
                    if self.__reset_counter == 60:                        
                        self.reset()
                        self.__reset_counter =0
                self.__slow_counter = 0            
        #While not exploding, it will alter between 2 images (blinking effect)
        else:
            #coutner used to slow down animations
            self.__slow_blink += 1
            #Updates image every 45 frames
            if self.__slow_blink == 45:
                if self.__imagenumber == 0:
                    self.__imagenumber = 1       
                else:
                    self.__imagenumber = 0
                self.image = self.__playerimage[self.__imagenumber]    
                self.__slow_blink = 0
        #updates horizontal position        
        if ((self.rect.left > 20) and (self.__dx > 0)) or\
           ((self.rect.left < 780) and (self.__dx < 0)):
            self.rect.left -= (self.__dx * 7)   
        #updates vertical position     
        if ((self.rect.top > 400) and (self.__dy < 0)) or\
            ((self.rect.top < 720) and (self.__dy > 0)):
            self.rect.top += (self.__dy * 7)  

    def reset(self):
        '''This function reset the position,speed,status and image of the player
        when called.'''
 
        self.__canshoot = True
        self.__imagenumber = 0
        self.image = self.__playerimage[self.__imagenumber]        
        self.rect = self.image.get_rect()
        self.rect.left = 430
        self.rect.top = 700
        self.__dx = 0
        self.__dy = 0 
        self.__exploding = False

class Enemy(pygame.sprite.Sprite):
    '''This class creates the enemies. It accepts values for position, speed, 
    and color decider. The aprite will move down in a straight line at first
    then it a value will be added to speed up the horizotnal movement, giving
    it a curved illusion. Once it moves off the screen, the sprite is killed and
    lost forever. The class will recieve different values as the game 
    progresses and is based on points.'''
    def __init__(self, left, top, x_direction, y_direction, decider):
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        #loads all images that are related to the Enemyr sprite
        self.__enemyimage = []
        for imagenumber in range(1,21):
            self.__enemyimage.append(pygame.image.load("./Enemy/enemy" + str(imagenumber)+".gif"))
        #setting initial values
        #the decider chooses which color enemy to display
        self.__imagenumber = decider
        self.image = self.__enemyimage[self.__imagenumber]
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = top
        self.__dy = y_direction
        self.__dx = x_direction
        self.__slow_counter = 0
        self.__slow_explode = 0
        self.__exploding = False
 
    def explode(self):
        '''This function makes the enemy explode when called.'''
        self.__exploding = True
        
    def get_explode(self):
        '''This function retursn the status of the explosion. If its exploding, 
        the sprite will not deduct a hit from the player when collided.'''
        return self.__exploding
         
    def update(self):
        '''This function updates the position, speed, and images of the the 
        enemy. Once the enemy goes off the screen, it is killed. When the
        enemy is 200 pixels form the top, a value will be added to the
        horizontal speed to make an curved effect.'''
        #coutner used to slow down animations
        self.__slow_counter += 1
        #loads the exploding images and kills the sprite when completed
        if self.__exploding:
            if self.__imagenumber < len(self.__enemyimage):
                self.image = self.__enemyimage[self.__imagenumber]
                self.__imagenumber += 1
            else:
                self.kill()       
            self._slow_explode = 0
        #changes the image so it creates a blinking effect.
        else:    
            if self.__slow_counter == 45:
                if (self.__imagenumber == 0) or (self.__imagenumber == 2):
                    self.__imagenumber += 1
                elif self.__imagenumber == 3:
                    self.__imagenumber = 2
                elif self.__imagenumber == 1:
                    self.__imagenumber = 0
                self.image = self.__enemyimage[self.__imagenumber]
                self.__slow_counter= 0
        #When the enemy approaches the screen, it will then move horizontally    
        if self.rect.top >= -50:
            self.rect.left += self.__dx      
        self.rect.top += self.__dy
        #When it reaches 200 pixels form the top, horiztonal speed increased
        #Increase speed if moving right
        if (self.rect.top > 200) and (self.__dx > 0):
            self.__dx += 0.1
        #Increase speed if moving left
        elif (self.rect.top > 200) and (self.__dx < 0):
            self.__dx += -0.1    
        #If off the screen, kill sprite
        if (self.rect.top > 820) or (self.rect.left < -80) or (self.rect.left > 950):
            self.kill()

        
        
class Missile(pygame.sprite.Sprite):
    '''This class creates the player's missiles. It accepts values for position
    of the player and fires up from there. It will only move in one firection'''
    def __init__(self, screen,  x_position,y_position):
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        #setting values
        self.image = pygame.image.load("./Missiles/missile.gif")
        self.rect = self.image.get_rect()
        self.__dy = 10
        self.rect.centerx = x_position
        self.rect.top = y_position
                
    def update(self):
        '''This updates the position of the missile. If it reaches the top
        of the screen, the missile is killed.'''
        self.rect.top -= self.__dy
        if (self.rect.top < -10):
            self.kill()
            
class EnemyMissile(pygame.sprite.Sprite):
    '''This class creates the enemy's missiles. It accepts values of position
    of enemy and will fire down form there. It will have an exploding effect
    if it collides with an enemy. The sprite is killed when either it collides
    or moves off the screen.'''
    def __init__(self, screen,  x_position,y_position):
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        #loads all the images related the enemy missile sprite
        self.__missileimage = []
        for imagenumber in range(1,18):
            self.__missileimage.append(pygame.image.load("./Missiles/missile" + str(imagenumber)+".gif"))
        #setting initial values
        self.__imagenumber = 0
        self.image = self.__missileimage[self.__imagenumber]
        self.rect = self.image.get_rect()
        self.__dy = -9        
        self.rect.centerx = x_position
        self.rect.top = y_position
        self.__exploding = False
    
    def explode(self):
        '''This makes the enemy missile sprite load the explosion images.'''
        self.__exploding = True
    def get_explode(self):
        '''This function returns if the enemy is exploding or not. If it is, 
        then the sprite would not have an affect on the player if collided.'''
        return self.__exploding                
    def update(self):
        '''This function updates the position of the missile and makes it 
        exploded if needed. Once exploded or off the screen, missile killed.'''
        #makes the missile explode and kills it
        if self.__exploding:
            self.__dy = 0
            if self.__imagenumber < len(self.__missileimage):
                self.image = self.__missileimage[self.__imagenumber]       
                self.__imagenumber += 1
            else:
                self.kill()

        self.rect.top -= self.__dy
        #Checks position and kills it if needed.
        if (self.rect.top < 0):
            self.kill()
        elif (self.rect.top > 900):
            self.kill()
     
class ScoreKeeper(pygame.sprite.Sprite):
    '''This class keeps track,adds,subtracts and displays the score. The score
    is diaplayed at the top center of the screen.'''
    def __init__(self):
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        self.__font = pygame.font.Font("./Fonts/BACKTO1982.ttf",40)
        self.__points = 50
        
    def add_points(self,add):
        '''This function adds the specified amount of points.'''
        self.__points += add
    def subtract_points(self,subtract):
        '''This function subtracts the specified amoutn of points.'''
        self.__points -= subtract
    def get_points(self):
        '''This function returns the amount of points.'''
        return self.__points
    def update(self):
        '''The score is updated and displayed.'''
        message = "%d" % self.__points
        #chanegs the points color to red when above 500 or below 50. Else-blue
        if (self.__points <= 20) or (self.__points >=500):
            self.image = self.__font.render(message,1,(255,0,0))
        else:
            self.image = self.__font.render(message,1,(100,255,255))
        self.rect = self.image.get_rect()
        self.rect.center = (450,30)
        
class LifeKeeper(pygame.sprite.Sprite):
    '''This class keeps tracks f the lifes and hits and displaays them. It can
    add and sbtract lives and subtract hits.Both start wiht a value of 3.
    The life and hits are displayed at the bottom left and right of the 
    screen.'''
    def __init__(self):
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)    
        self.__font = pygame.font.Font("./Fonts/BACKTO1982.ttf",25)
        #set initial values
        self.__lives = 3
        self.__hits = 3
    def subtract_hit(self):
        '''Subtracts a hit form the total.'''
        self.__hits += -1
    def subtract_life(self):
        '''Subtracts a life fmor the total.'''
        self.__lives += -1
    def add_life(self):
        '''Adds a life to the total.'''
        self.__lives += 1
    def reset_hit(self):
        '''Resets the hits to 3. This is called when a life is lost.'''
        self.__hits = 3
    def get_life(self):
        '''returns the number of lives left.'''
        return self.__lives
    def get_hit(self):
        '''returns the number of hits left.'''
        return self.__hits
    def update(self):
        '''Updates the values and displays it to the user.'''
        message = "%d lives                                         \
        %d hits" %(self.__lives ,self.__hits)
        self.image = self.__font.render(message,1,(255,255,255))
        self.rect = self.image.get_rect()
        self.rect.center = (450,755)
        
class Coins(pygame.sprite.Sprite):
    '''This class creates the bonus points coins. Each coin touched by the
    player will result in a gain of 25 points. The coin will appear at 
    random times and travel at random speeds. The animation of the coin is 
    spinning. Only one coin can be on the screen at a time.'''
    def __init__(self):
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        #load the 10 images that creates the coin's spin
        self.__coinimage = []
        for imagenumber in range(1,11):
            self.__coinimage.append(pygame.image.load("./Coins/coin" + str(imagenumber)+".gif"))
        #This counter will slow down the rate of the spin
        self.__slow_counter = 0  
        self.reset()   
    def update(self):
        '''This updates the position of the coin on the y-axis. It also
        rotates the coins but calling different images to be displayed.
        If the coin reaches the bottom of the screen, the sprite is then
        resetted.'''
        self.rect.top += self.__dy
        self.__slow_counter += 1
        #this loop slows down the rate of spin.
        if self.__slow_counter == 4:
            #changes the image while its within the image sequence
            if self.__imagenumber < len(self.__coinimage):
                self.image = self.__coinimage[self.__imagenumber]
                self.__imagenumber += 1
            #checks if image number has reached last image of the sequence
            elif self.__imagenumber == 10:
                self.__imagenumber = 1
            self.__slow_counter = 0

        if self.rect.top >= 800:
            self.reset()
    def reset(self):
        '''This function is called when the coin hits a player or reaches
        the end of the screen. The position,speed,image is then resetted'''
        self.__dy = random.randrange(4,7)
        self.__imagenumber = 1
        self.image = self.__coinimage[self.__imagenumber]
        self.rect = self.image.get_rect()
        self.rect.left = random.randrange(100,800)
        self.rect.top = random.randrange(-10000,-6000)     
            
class LifeBonus(pygame.sprite.Sprite):
    '''This class creates the bonus heart that adds a life. It moves down
    at random times throughout the game. If it reaches the bottom of the screen,
    the position resets.'''
    def __init__(self):
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("./Life/heart.gif")
        self.rect = self.image.get_rect()
        self.reset()
    def update(self):
        '''updates the position of the heart.'''
        self.rect.top += self.__dy
        if self.rect.top >= 800:
            self.reset()  
    def reset(self):
        '''Resets the position and speed of the hear.'''
        self.rect.left = random.randrange(100,800)
        self.rect.top = random.randrange(-20000,-9000)
        self.__dy = random.randrange(4,7)
        
class Astroid(pygame.sprite.Sprite):
    '''This class creates the animated astroid. It moves at a random line and
    appears on the screen at random times (but frequently). 37 images make up
    the animation for the astroid.'''
    def __init__(self):
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self) 
        #Load all the images for the astroid
        self.__rockimage = []
        for imagenumber in range(1,38):
            self.__rockimage.append(pygame.image.load("./Rocks/rock" + str(imagenumber)+".gif"))        
        #This counter will slow down the rate of the spin
        self.__slow_counter = 0  
        self.reset()    
    def update(self):
        '''Updates the position of the astoird as well as the image being 
        displayed. A counter is sused to slow down the roatation.'''
        self.__slow_counter += 1
        self.rect.top += self.__dy
        self.rect.left += self.__dx
        #updates the image every 5 frames
        if self.__slow_counter >= 5:
            if self.__imagenumber < len(self.__rockimage):
                self.image = self.__rockimage[self.__imagenumber]
                self.__imagenumber += 1
            #checks if image number has reached last image of the sequence
            elif self.__imagenumber == 37:
                self.__imagenumber = 1
            self.__slow_counter = 0   
        #When reached the bottom of the screen, sprite resets
        if self.rect.top >= 800:
            self.reset()
      
    def reset(self):
        '''Resets the position and speed of the astroid and changed the image
        number back to 1.'''
        self.__imagenumber = 1
        self.image = self.__rockimage[self.__imagenumber]
        self.rect = self.image.get_rect()        
        self.rect.left = random.randrange(50,800)
        self.rect.top = random.randrange(-1500,-50)
        self.__dy = random.randrange(4,10)
        self.__dx = random.randrange(-1,2)
        
