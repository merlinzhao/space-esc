'''
Author: Merlin Zhao
Made in Toronto, ON.
Description:
        ***REQUIRED: Python 2.7, pygame 1.9.1 for python 2.7***
        Space Escape is inspired by the class aracde game - Galaga. The 
        objective of the game is to achieve 1000 points. At 1000 points, you 
        escape the enemy infected area of space and win! If you lost all your
        lives or reach 0 points, you lose! The player starts with 50 points
        and each misile costs 2 points. Getting hit by enemies, missiels, and
        astroid will also result in the deduction of points. Each enemy killed
        will gain 10 points and there will be life and points bonuses 
        throughout the game. As the points increase, so will the difficutly.
        It will first spawn slowly and in small groups, then get fsater and 
        larger. After winning or loosing, the appropriate msuic and image will
        be playerd and displayed. The player has the option to quit at anytime 
        with the ESC key and if at a result menu (win/lost), the player has
        the option to play again or quit. Space Escape is a great, simple game
        that is nolstagic of the good-o aracde games you find in laundromats. 
        HAVE FUN AND ESCAPE THE ENEMEIES!
             
'''


#INITIALIZE
import pygame, random, spaceSprite
pygame.init()
pygame.mixer.init()    
screen = pygame.display.set_mode((900, 780))

#List of Joystick objects.
joysticks = []
for joystick_no in range(pygame.joystick.get_count()):
    stick = pygame.joystick.Joystick(joystick_no)
    stick.init()
    joysticks.append(stick)
    
def menu():
    '''This loops displays the menu with the introduction and intructions. This
    is where you may return after you win or loose the game and when it first
    starts. Spcebar or any button on the koystick will start the main game
    loop.'''
    #DISPLAY
    pygame.display.set_caption("Space Escape")       

    #ENTITIES
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))    
    #background music
    pygame.mixer.music.load("./Sounds/Background1.wav")
    pygame.mixer.music.set_volume(0.6)
    pygame.mixer.music.play(-1)  
    start_sound = pygame.mixer.Sound("./Sounds/explosion.wav")
    start_sound.set_volume(0.8)
    
    #everything sprite!!!
    wallpaper = spaceSprite.Wallpaper(screen)
    lifekeeper = spaceSprite.LifeKeeper()    
    player = spaceSprite.Player()
    astroid = spaceSprite.Astroid()
    intro_image = pygame.image.load("./Intro/intro.gif")
    introSprites = pygame.sprite.OrderedUpdates(wallpaper, player,lifekeeper\
                                                , astroid)
    #intro imagae
    intro_image = pygame.image.load("./Intro/intro.gif")
    
    #ASSIGN
    introGoing = True
    clock = pygame.time.Clock()
    #Menu game loop
    while introGoing:
        #TIME
        clock.tick(60)
        #ENTITIES
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                introGoing = False 
            elif event.type == pygame.JOYBUTTONDOWN:
                start_sound.play()
                main()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    start_sound.play()
                    main()
                elif event.key == pygame.K_ESCAPE:
                    introGoing = False             
        #REFRESH
        introSprites.clear(screen,background)
        introSprites.update()
        introSprites.draw(screen)  
        screen.blit(intro_image,(0,0)) 
        pygame.display.flip() 
    pygame.quit()
    
def end_game(game_decider):
    '''This function is called when a player lose or wins. It plays the 
    music accordingly and displays the text accordingly. Pressing space or a
    button on the joystick will return it to the menu. A decider is passed in
    that chooses which image and msuic to choose.'''
    #DISPLAY
    pygame.display.set_caption("Space Escape")   
    #ENTITIES
    #1 is for the winner, else loser
    if game_decider == 1:
        end_image = pygame.image.load("./Intro/winner.gif")
    else:
        end_image = pygame.image.load("./Intro/loser.gif")
    screen.blit(end_image,(0,0))
    #background music
    if game_decider == 1:
        pygame.mixer.music.load("./Sounds/winner.mp3")
    else: 
        pygame.mixer.music.load("./Sounds/SpaceInvaders.wav")
        pygame.mixer.music.set_volume(0.6)        
    pygame.mixer.music.play(-1)
    #ASSIGN
    endGoing = True
    clock = pygame.time.Clock()    
    #Winner game loop
    while endGoing:
        #TIME
        clock.tick(60)
        #ENTITIES
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                endGoing = False 
            elif event.type == pygame.JOYBUTTONDOWN:
                menu()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    menu()
                elif event.key == pygame.K_ESCAPE:
                    endGoing = False           
        #REFRESH
        pygame.display.flip()
    pygame.quit()
    
def main():
    '''This function defines the 'mainline logic' for the game. This is wear 
    the actualy game happens, full of sprites and movements.'''
    #DISPLAY
    pygame.display.set_caption("Space Escape")    
    
    #ENTITIES 
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))
    #everything sprites
    scorekeeper = spaceSprite.ScoreKeeper()
    lifekeeper = spaceSprite.LifeKeeper()
    coinbonus = spaceSprite.Coins()
    lifebonus = spaceSprite.LifeBonus()
    astroid = spaceSprite.Astroid()
    player = spaceSprite.Player()
    wallpaper = spaceSprite.Wallpaper(screen)
    enemies = pygame.sprite.Group() 
    missiles = pygame.sprite.Group()
    enemy_missiles = pygame.sprite.Group()
    #groups the sprites
    allSprites = pygame.sprite.OrderedUpdates(wallpaper, player, scorekeeper,\
    lifekeeper, astroid,missiles,enemy_missiles,enemies, coinbonus,lifebonus)

    #Sounds effects
    shoot_sound = pygame.mixer.Sound("./Sounds/shoot.wav")
    shoot_sound.set_volume(0.2)
    enemy_die_sound = pygame.mixer.Sound("./Sounds/invaderkilled.wav")
    enemy_die_sound.set_volume(0.1)
    player_die_sound = pygame.mixer.Sound("./Sounds/explosion.wav")
    player_shot = pygame.mixer.Sound("./Sounds/explosion.wav")
    player_shot.set_volume(0.2)
    bonus_sound = pygame.mixer.Sound("./Sounds/Apple Pay.wav")
    fail_sound = pygame.mixer.Sound("./Sounds/fail.wav")
    fail_sound.set_volume(0.6)
    
    #Background sound
    pygame.mixer.music.load("./Sounds/SpaceInvaders.wav")
    pygame.mixer.music.set_volume(0.6)
    pygame.mixer.music.play(-1)    
        
    #ACTION
    #ASSIGN
    clock = pygame.time.Clock()
    keepGoing = True
    spawn_counter = 0
    
    #MAIN GAME LOOP
    while keepGoing:
        #TIME
        clock = pygame.time.Clock()
        clock.tick(60)   
        
        #Making the game more difficault as it progresses. Code from here...
        #...to Event-handling spawns all the enemies.
        #beginning difficulty. BABY STUFF
        if scorekeeper.get_points() <= 125:
            determine_spawn = 180
            spawn_count = 3
            yrandom1 = 4
            yrandom2 = 6
            xrandom1 = 1
            xrandom2 = 3
            #determines the rate the enemies fire missiles
            if scorekeeper.get_points() <= 100:
                missile_frequency = 260
            else:
                missile_frequency = 240
        #difficulty after 125 points. MEDIUM-EASY        
        elif scorekeeper.get_points() <= 500:
            determine_spawn = 200
            if scorekeeper.get_points() >= 350:
                spawn_count = 5
            else:
                spawn_count = 4
            yrandom1 = 4
            yrandom2 = 8
            xrandom1 = 1
            xrandom2 = 3
            #determines the rate the enemies fire missiles
            if scorekeeper.get_points() <= 250:
                missile_frequency = 220
            else:
                missile_frequency = 200   
        #difficulty after 500 points. HARD        
        elif scorekeeper.get_points() <= 1000:
            if scorekeeper.get_points() >= 750:
                spawn_count = 8
                determine_spawn = 160
            else:
                spawn_count =7
                determine_spawn = 180
            yrandom1 = 7
            yrandom2 = 13
            xrandom1 = 1
            xrandom2 = 3
            #determines the rate the enemies fire missiles
            if scorekeeper.get_points() <= 750:
                missile_frequency = 150
            elif scorekeeper.get_points() <= 850:
                missile_frequency = 125     
            else:
                missile_frequency = 100
        spawn_counter += 1
        #When counter reached, it will spawn enemies with the given values
        if spawn_counter >= determine_spawn:
            top = -700
            left = random.randrange(50,400)
            y_direction = random.randrange(yrandom1,yrandom2)            
            decider = random.randrange(1,3)
            if left > 200:
                x_direction = random.randrange(xrandom1,xrandom2)
            else:
                x_direction = random.randrange(-(xrandom2-1),-(xrandom1-1))
            if left > 200:
                top_decider = random.randrange(45,90)
            else: 
                top_decider = random.randrange(-90,-45)    
            left_decider = random.randrange(45,90)
                                              
            #creating the enemies    
            for times in range(spawn_count):
                top += top_decider
                left += left_decider
                enemies.add(spaceSprite.Enemy(left,top,x_direction,\
                                              y_direction,decider))
            spawn_counter = 0
        allSprites = pygame.sprite.OrderedUpdates(wallpaper, player,\
        scorekeeper,lifekeeper, astroid,missiles,enemy_missiles,enemies,\
        coinbonus,lifebonus)
          
        #EVENTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False 
            #Joystick events    
            elif event.type == pygame.JOYHATMOTION:
                if event.joy == 0:
                    if event.value == (-1,0):
                        player.move_horizontal((0,1))
                    elif event.value == (1,0):
                        player.move_horizontal((0,-1))                        
                    elif event.value == (0,1):
                        player.move_vertical((0,-1))
                    elif event.value == (0,-1):
                        player.move_vertical((0,0.6)) 
                    elif event.value == (0,0):
                        player.move_horizontal((0,0))
                        player.move_vertical((0,0))
            elif event.type == pygame.JOYBUTTONDOWN:
                if player.get_canshoot() == True:
                    shoot_sound.play()
                    missile = spaceSprite.Missile(screen, player.rect.centerx, \
                                                  player.rect.top - 25)
                    missiles.add(missile)
                    allSprites = pygame.sprite.OrderedUpdates(wallpaper, player\
                    , scorekeeper,lifekeeper, astroid,missiles,enemy_missiles,\
                    enemies, coinbonus,lifebonus)
                    scorekeeper.subtract_points(2)                              
            #keyboard events  
            #keys pressed down
            elif event.type == pygame.KEYDOWN:                     
                if event.key == pygame.K_ESCAPE:
                    keepGoing = False  
                elif event.key == pygame.K_LEFT:
                    player.move_horizontal((0, 1))
                elif event.key == pygame.K_RIGHT:
                    player.move_horizontal((0, -1))
                elif event.key == pygame.K_UP:
                    player.move_vertical((0, -1))
                elif event.key == pygame.K_DOWN:
                    player.move_vertical((0, 0.6))   
                elif event.key == pygame.K_SPACE:
                    if player.get_canshoot() == True:
                        shoot_sound.play()
                        missile = spaceSprite.Missile(screen,\
                            player.rect.centerx, player.rect.top - 25)
                        missiles.add(missile)
                        allSprites = pygame.sprite.OrderedUpdates(wallpaper, \
                            player, scorekeeper,lifekeeper, astroid,missiles,\
                            enemy_missiles,enemies, coinbonus,lifebonus)
                        scorekeeper.subtract_points(2)
            #keys released
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    player.move_horizontal((0, 0))
                elif event.key == pygame.K_RIGHT:
                    player.move_horizontal((0, 0))
                elif event.key == pygame.K_UP:
                    player.move_vertical((0, 0))
                elif event.key == pygame.K_DOWN:
                    player.move_vertical((0, 0))                
      
        #checks if a player missile hits and enemy        
        for missile in missiles:
            hit_enemy = pygame.sprite.spritecollide(missile,enemies,False)
            if hit_enemy:
                for enemy in hit_enemy:
                    enemy_die_sound.play()
                    #Checks if enemy exploding already. If not, then add points
                    if enemy.get_explode() == False:
                        scorekeeper.add_points(10)
                    missile.kill()
                    enemy.explode()      
            #if missile hits an astroid, it is killed
            if astroid.rect.colliderect(missile.rect):
                missile.kill() 
        #enemies shooting back at the player
        for enemy in enemies:
            if (random.randrange(missile_frequency) == 25):
                enemy_missile = spaceSprite.EnemyMissile(screen, \
                    enemy.rect.centerx, (enemy.rect.top))
                enemy_missiles.add(enemy_missile)
                allSprites = pygame.sprite.OrderedUpdates(wallpaper, player,\
                    scorekeeper,lifekeeper, astroid,missiles,enemy_missiles,\
                    enemies, coinbonus,lifebonus)        
        #checks if enemy missile hits the playaer
        for missile in enemy_missiles:
            if player.rect.colliderect(missile.rect):
                if (missile.get_explode() == False) and \
                (player.get_explode() == False):
                    player_shot.play()
                    scorekeeper.subtract_points(5)
                    lifekeeper.subtract_hit()
                    missile.explode()
        #checks if the player collides with the enemy            
        enemy_hit_player =  pygame.sprite.spritecollide(player, enemies,False)
        if enemy_hit_player:
            for enemy in enemy_hit_player:
                if(enemy.get_explode() == False) and (player.get_explode() == False): 
                    player_shot.play()
                    scorekeeper.subtract_points(25)
                    lifekeeper.subtract_hit()                    
                    enemy.explode()
        #checks if player gets a bonus coin      
        if player.rect.colliderect(coinbonus.rect):
            bonus_sound.play()
            scorekeeper.add_points(25)
            coinbonus.reset()
        #checks if player gets a bonus life   
        if player.rect.colliderect(lifebonus.rect):
            bonus_sound.play()
            lifekeeper.add_life()
            lifebonus.reset()        
        #checks if a player colliodes with an astroid    
        if player.rect.colliderect(astroid.rect):
            if (player.get_explode() == False):
                player_die_sound.play()
                player.explode()
                lifekeeper.subtract_life()
                astroid.reset()
        #checks if the hits reaches 0. If so, life will be lost, player explode    
        if lifekeeper.get_hit() <= 0:
            player_die_sound.play()
            player.explode()
            lifekeeper.subtract_life()
            lifekeeper.reset_hit()
        #checks if theres a winner!
        if scorekeeper.get_points() >= 1000:
            end_game(1)
        #checks for loser...
        if (scorekeeper.get_points() <= 0) or (lifekeeper.get_life() == 0):
            fail_sound.play()
            end_game(0)
        #REFRESH
        allSprites.clear(screen,background)
        allSprites.update()
        allSprites.draw(screen)              
        pygame.display.flip()
    pygame.quit()
        
menu()