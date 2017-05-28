'''
Created on May 26, 2017

@author: Manuel
'''
#Sprite classesi
import pygame as pg
from Settings import *
from random import choice
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
    
    
class Player(pg.sprite.Sprite):
    def __init__(self,game):
        pg.sprite.Sprite.__init__(self)
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
            
                                      
                                      
        self.jump_frames=[self.game.spritesheet.get_image(11,16,14,15),
                          self.game.spritesheet.get_image(0,0,11,15),
                          self.game.spritesheet.get_image(57,49,10,14)]
        for frame in self.jump_frames:
            frame.set_colorkey(BLACK)
    
    def jump(self):
         self.rect.y +=2
         hits=pg.sprite.spritecollide(self,self.game.platforms,False)
         self.rect.y -=2
         if hits:
             self.vel.y=-PLAYER_JUMP
       
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
            if now-self.last_update> 400:
                self.last_update=now
                self.current_frame=(self.current_frame+1)% len(self.standing_frames)
                bottom= self.rect.bottom
                self.image=self.standing_frames[self.current_frame]
                self.rect=self.image.get_rect()
                self.rect.bottom=bottom
        
                


class Platform(pg.sprite.Sprite):
    def __init__(self,game,x,y,):
        pg.sprite.Sprite.__init__(self)
        self.game=game
        images = [self.game.spritefloor.get_floor(0,0,62,21),
                  self.game.spritefloor.get_floor(0,22,42,21)]
        self.image =choice(images)
        self.image.set_colorkey(BLACK)
        self.rect= self.image.get_rect()
        self.rect.x=x
        self.rect.y =y