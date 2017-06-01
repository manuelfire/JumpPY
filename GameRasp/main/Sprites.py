'''
Created on May 26, 2017

@author: Manuel
'''
#Sprite classesi
import pygame as pg
from Settings import *
from random import choice, randrange
vec= pg.math.Vector2
class Spritesheet:
    def __init__(self,filename):
        self.spritesheet =pg.image.load(filename).convert()
        
    def get_image(self,x,y,width,height):
        image=pg.Surface((width,height))
        image.blit(self.spritesheet,(0,0),(x,y,width,height))
        image= pg.transform.scale(image,(width*3,height*3))
        return image
    def get_floor(self,x,y,width,height):
        image=pg.Surface((width,height))
        image.blit(self.spritesheet,(0,0),(x,y,width,height))
        image= pg.transform.scale(image,(width*2,height*2))
        return image
    def get_imagepow(self,x,y,width,height):
        image=pg.Surface((width,height))
        image.blit(self.spritesheet,(0,0),(x,y,width,height))
        image= pg.transform.scale(image,(width//5,height//5))
        return image
    def get_imagemob(self,x,y,width,height):
        image=pg.Surface((width,height))
        image.blit(self.spritesheet,(0,0),(x,y,width,height))
        image= pg.transform.scale(image,(width,height))
        return image
    
    
class Player(pg.sprite.Sprite):
    def __init__(self,game):
        self.groups=game.all_sprites
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game=game
        self.walking=False
        self.jumping =False
        self.falling=False
        self.current_frame=0
        self.last_update=0
        self.load_images()
        self.image=self.standing_frames[0]
        self.image.set_colorkey(GREY)
        self.rect=self.image.get_rect()
        self.rect.center= (WIDTH/2, HEIGHT/2)
        self.pos = vec(WIDTH/2,HEIGHT/2)
        self.vel =vec(0,0)
        self.acc =vec(0,0)
    
    def load_images(self):
        self.standing_frames=[self.game.spritesheet.get_image(57,0,12,16),
                              self.game.spritesheet.get_image(0,16,10,15),
                              self.game.spritesheet.get_image(46,48,10,15),
                              self.game.spritesheet.get_image(15,48,10,15)]
        for frame in self.standing_frames:
            frame.set_colorkey(GREY)
            
        self.walk_frames_r=[self.game.spritesheet.get_image(0,48,14,15),
                            self.game.spritesheet.get_image(44,16,12,15),
                            self.game.spritesheet.get_image(36,48,9,15),
                            self.game.spritesheet.get_image(0,32,14,15),
                            self.game.spritesheet.get_image(57,33,12,15),
                            self.game.spritesheet.get_image(44,32,12,15)]
        for frame in self.walk_frames_r:
            frame.set_colorkey(GREY)
        self.walk_frames_l=[]
        for frame in self.walk_frames_r:
            frame.set_colorkey(GREY)
            self.walk_frames_l.append(pg.transform.flip(frame,True,False))
            
        self.fall_frames =[self.game.spritesheet.get_image(27,0,16,30)]
        for frame in self.fall_frames:
            frame.set_colorkey(GREY)                 
                                      
        self.jump_frames=[self.game.spritesheet.get_image(11,16,14,15),
                          self.game.spritesheet.get_image(0,0,11,15),
                          self.game.spritesheet.get_image(57,49,10,14)]
        for frame in self.jump_frames:
            frame.set_colorkey(GREY)
            
            
    
    def jump(self):
         self.rect.y +=2
         hits=pg.sprite.spritecollide(self,self.game.platforms,False)
         self.rect.y -=2
         if hits and not self.jumping:
             self.game.jump_sound.play()
             self.jumping=True
             self.walking=False
             self.vel.y=-PLAYER_JUMP
    
    def jump_cut(self):
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y=-3
    
    def update(self):
        self.animate()
        self.acc =vec(0,PLAYER_GRAV)
        keys=pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x= -PLAYER_ACC
        if keys[pg.K_RIGHT]:
            self.acc.x=PLAYER_ACC
            
        #friccion y acc    
        self.acc.x +=self.vel.x*PLAYER_FRICTION  
        self.vel += self.acc
        if abs(self.vel.x) < 0.1:
            self.vel.x=0
        self.pos += self.vel +0.5 * self.acc
        
        if self.pos.x > WIDTH + self.rect.width/2:
            self.pos.x = 0 - self.rect.width/2
        if self.pos.x < 0 - self.rect.width/2:
            self.pos.x=WIDTH + self.rect.width/2
        
        
        self.rect.midbottom=self.pos
    
    def animate(self):
        now = pg.time.get_ticks()
        if self.vel.x !=0:
            self.walking=True
        else:
            self.walking=False
            
        if self.jumping and not self.walking:
             if now-self.last_update> 400:
                self.last_update=now
                self.current_frame=(self.current_frame+1)% len(self.jump_frames)
                bottom= self.rect.bottom
                self.image=self.jump_frames[self.current_frame]
                self.rect=self.image.get_rect()
                self.rect.bottom=bottom
        if self.walking:
            if now-self.last_update>100:
                self.last_update=now
                self.current_frame=(self.current_frame+1)% len(self.walk_frames_l)
                bottom= self.rect.bottom
                if self.vel.x>0:
                    self.image =self.walk_frames_r[self.current_frame]
                else:
                    self.image=self.walk_frames_l[self.current_frame]
                self.rect=self.image.get_rect()
                self.rect.bottom=bottom
            
        if not self.jumping and not self.walking:
            if now-self.last_update> 900:
                self.last_update=now
                self.current_frame=(self.current_frame+1)% len(self.standing_frames)
                bottom= self.rect.bottom
                self.image=self.standing_frames[self.current_frame]
                self.rect=self.image.get_rect()
                self.rect.bottom=bottom
        
        if self.falling:
            if now-self.last_update> 400:
                self.last_update=now
                self.current_frame=(self.current_frame+1)% len(self.fall_frames)
                bottom= self.rect.bottom
                self.image=self.fall_frames[self.current_frame]
                self.rect=self.image.get_rect()
                self.rect.bottom=bottom
        
                


class Platform(pg.sprite.Sprite):
    def __init__(self,game,x,y,):
        self.groups=game.all_sprites,game.platforms
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game=game
        images = [self.game.spritefloor.get_floor(0,0,62,21),
                  self.game.spritefloor.get_floor(0,22,42,21)]
        self.image =choice(images)
        self.image.set_colorkey(BLACK)
        self.rect= self.image.get_rect()
        self.rect.x=x
        self.rect.y =y
        if self.game.score >100:
            if randrange(100) < POW_SPAWN:
                Powerup(self.game,self)
        
class Powerup(pg.sprite.Sprite):
    def __init__(self,game,plat):
        self.groups =game.all_sprites,game.powerups
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game=game
        self.plat=plat
        self.current_frame=0
        self.last_update=0
        self.load_images()
        self.type=choice(['boost'])
        self.image=self.power_frames[0]
        self.rect=self.image.get_rect()
        self.rect.centerx=self.plat.rect.centerx
        self.rect.bottom=self.plat.rect.top-5
    def update(self):
        
        self.animate()
        self.rect.bottom=self.plat.rect.top-5
        
            
        if not self.game.platforms.has(self.plat):
            self.kill()
      
        
    def animate(self):
        now = pg.time.get_ticks()
        if now-self.last_update> 100:
                self.last_update=now
                self.current_frame=(self.current_frame+1)% len(self.power_frames)
                bottom= self.rect.bottom
                self.image=self.power_frames[self.current_frame]
        
    def load_images(self):
        self.power_frames=[self.game.spritepower.get_imagepow(128,850,144,240),
                            self.game.spritepower.get_imagepow(529,48,144,254),
                            self.game.spritepower.get_imagepow(128,449,144,272),
                            self.game.spritepower.get_imagepow(128,48,144,272),
                            self.game.spritepower.get_imagepow(529,850,144,304),
                            self.game.spritepower.get_imagepow(529,449,144,304)]
             
        for frame in self.power_frames:
            frame.set_colorkey(GREEEN)
        
        
        
        
class Mob(pg.sprite.Sprite):
    def __init__(self,game):
        self.groups =game.all_sprites,game.mobs
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game=game
        self.mobtype=choice(['ghost','spinner'])
        self.mob_frames=[self.game.spritemob.get_imagemob(0,42,70,47),
                          self.game.spritemob.get_imagemob(0,0,88,37),
                          self.game.spritemob.get_imagemob(149,0,51,73),
                          self.game.spritemob.get_imagemob(149,78,51,73),
                          self.game.spritemob.get_imagemob(0,94,63,62),
                          self.game.spritemob.get_imagemob(68,94,61,61)]
        for frames in self.mob_frames:
            frames.set_colorkey(BLACK)
        if self.mobtype == 'ghost':
            self.image_up=self.mob_frames[2]
            self.image_down=self.mob_frames[3]
       
        if self.mobtype == 'spinner':
            self.image_up=self.mob_frames[4]
            self.image_down=self.mob_frames[5]
        self.image=self.image_up
        self.rect=self.image.get_rect()
        
        self.vx= randrange(1,4)
        if self.rect.centerx > WIDTH:
            self.vx *= -1
        
        self.vy=0
        self.dy=0.5
        
        
        
    def update(self,):
        self.rect.x += self.vx
        self.vy += self.dy
        if self.vy > 3 or self.vy <-3:
            self.dy *=-1
        center=self.rect.center
        if self.dy<0:
            self.image=self.image_up
        else:
            self.image=self.image_down
        self.rect=self.image.get_rect()
        self.rect.center=center
        self.rect.y= self.vy
        if self.rect.left > WIDTH+100 or self.rect.right < -100:
            self.kill()
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        