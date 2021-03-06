#Options
Title="JumPi"
WIDTH=360
HEIGHT=480
FPS=60
FONT_NAME= 'arial'

#Player sett
PLAYER_ACC=0.5
PLAYER_FRICTION=-0.12
PLAYER_GRAV= 1
PLAYER_JUMP=22

#Game Prop
BOOST_POWER=60
POW_SPAWN= 7
MOB_Freq= 8000

#Plataformas formato (x,y,thicknes)
PLATFORM_LIST=[(0, HEIGHT-40),
               (WIDTH/2-50,HEIGHT*3/4),
               (WIDTH-100,200),
               (175,100)]

#colors
WHITE= (255,255,255)
BLACK= (0,0,0)
RED=(255,0,0)
GREEEN=(0,255,0)
BLUE=(0,0,255)
LIGHTBLUE=(0,155,155)
GREY=(157,142,135)
BGCOLOR=LIGHTBLUE
SPRITESHEET="sprite_floor.png"
SPRITESHEETCHAR="sprite_char.png"
SPRITEPOW="power.png"
SPRITEenemies='enemies.png'