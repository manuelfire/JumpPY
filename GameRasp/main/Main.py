import pygame as pg
import random
from Settings import *
from Sprites import *
from os import path

class Game:
    def __init__(self):
        #gmae windows
        pg.init()
        pg.mixer.init()
        self.screen=pg.display.set_mode((WIDTH,HEIGHT))
        pg.display.set_caption(Title)
        self.clock=pg.time.Clock()
        self.running=True
        self.font_name =pg.font.match_font(FONT_NAME)
        self.load_data()
        pass
    def new(self):
        #new game
        self.score=0
        self.all_sprites= pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.powerups=pg.sprite.Group()
        self.mobs =pg.sprite.Group()
        self.player= Player(self)
        
        for plat in PLATFORM_LIST:
           Platform(self,*plat)
        self.mob_timer =0
        pg.mixer.music.load(path.join(self.snd_dir,"BG1.ogg"))
        self.run()
        pass
    def load_data(self):
        self.dir =path.dirname(__file__)
        img_dir=path.join(self.dir, 'Img')
        
        self.spritesheet=Spritesheet(path.join(img_dir,SPRITESHEETCHAR))
        self.spritefloor=Spritesheet(path.join(img_dir,SPRITESHEET))
        self.spritepower=Spritesheet(path.join(img_dir,SPRITEPOW))
        self.spritemob=Spritesheet(path.join(img_dir,SPRITEenemies))
        
        #load sound
        self.snd_dir=path.join(self.dir,'Sound')
        self.jump_sound =pg.mixer.Sound(path.join(self.snd_dir,'Jump.wav'))
    def run(self):
        #gameloop
        pg.mixer.music.play(loops=-1)
        self.playing=True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        pg.mixer.music.fadeout(1000)
            
        pass
    def update(self):
        self.all_sprites.update()
        #spawn mobs
        now=pg.time.get_ticks()
        if now -self.mob_timer > MOB_Freq +random.choice([-1000,1000,-500,0,2000,-2000]):
            self.mob_timer=now
            Mob(self)
         # hit mobs?
        mob_hits = pg.sprite.spritecollide(self.player, self.mobs, False)
        if mob_hits:
            self.playing = False
        
        if self.player.vel.y > 0:
            hits= pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                lowest= hits[0]
                for hit in hits:
                    if hit.rect.bottom > lowest.rect.centery:
                        lowest=hit
                if self.player.pos.x <lowest.rect.right -10 and self.player.pos.x >lowest.rect.left-10:
                    if self.player.pos.y <lowest.rect.centery:
                        self.player.pos.y= lowest.rect.top +1
                        self.player.vel.y=0
                        self.player.jumping=False
        
        #if player reaches near edge move camera
        if self.player.rect.top <= HEIGHT /4:
            self.player.pos.y +=max(abs(self.player.vel.y),2)
            for mob in self.mobs:
                mob.rect.y +=max(abs(self.player.vel.y),2)
            for plat in self.platforms:
                plat.rect.y +=max(abs(self.player.vel.y),2)
                if plat.rect.top >=HEIGHT:
                    plat.kill()
                    self.score +=5
        #player+powerup
        pow_hits=pg.sprite.spritecollide(self.player, self.powerups, True)
        for pow in pow_hits:
            if pow.type=='boost':
                self.player.vel.y = -BOOST_POWER
                self.player.jumping=False
        #Death
        if self.player.rect.bottom >HEIGHT:
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y, 10)
                if sprite.rect.bottom <0:
                    sprite.kill()
        if len(self.platforms)==0:
            self.playing=False
        
        #nuevas plataformas
        while len(self.platforms) < 5:
            width= random.randrange(50,100)
            Platform(self,random.randrange(0,WIDTH-width), random.randrange(-55,-PLAYER_JUMP))
            
            
        pass
    def events(self):
        for event in pg.event.get():
            if event.type== pg.QUIT:
                if self.playing:
                    self.playing=False
                self.running=False
            if event.type== pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    
                    self.player.jump()
                    
            if event.type== pg.KEYUP:
                if event.key == pg.K_SPACE:
                    self.player.jump_cut()
            if self.player.vel.y > 1:
                self.player.falling=True
            else:
                self.player.falling=False
        pass
    def draw(self):
        self.screen.fill(BGCOLOR)
        self.all_sprites.draw(self.screen)
        self.screen.blit(self.player.image,self.player.rect)
        self.draw_text(str(self.score), 22, WHITE, WIDTH/2, 15)
        pg.display.flip()
       
        pass
    def show_start_screen(self):
        self.screen.fill(BGCOLOR)
        self.draw_text(Title, 48, WHITE, WIDTH/2, HEIGHT/4)
        self.draw_text("Presione una tecla para comenzar", 22, WHITE,WIDTH/2, HEIGHT*3/4)
        pg.display.flip()
        self.wait_for_key()
        pass
    def show_go_screen(self):
        if not self.running:
            return
        self.screen.fill(BGCOLOR)
        self.draw_text("GAME OVER",48, WHITE, WIDTH/2, HEIGHT/4)
        self.draw_text("Score:"+str(self.score), 22, WHITE,WIDTH/2, HEIGHT/2)
        self.draw_text("Presione una tecla para jugar otra vez", 22, WHITE,WIDTH/2, HEIGHT*3/4)
        pg.display.flip()
        self.wait_for_key()
        pass
    def wait_for_key(self):
        waiting=True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                
                if event.type==pg.QUIT:
                    waiting=False
                    self.running=False
                if event.type ==pg.KEYUP:
                    waiting=False
        pass

    def draw_text(self,text,size,color,x,y):
        font=pg.font.Font(self.font_name,size)
        text_surface=font.render(text,True,color)
        text_rect =text_surface.get_rect()
        text_rect.midtop=(x,y)
        self.screen.blit(text_surface,text_rect)
        
        pass

g=Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()
pg.quit()
