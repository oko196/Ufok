#!/usr/bin/env python
"""
This simple example is used for the line-by-line tutorial
that comes with pygame. It is based on a 'popular' web banner.
Note there are comments here, but for the full explanation,
follow along in the tutorial.
"""


#Import Modules
import os, pygame,random
from pygame.locals import *
from pygame.compat import geterror
from pygame import gfxdraw as gfx

if not pygame.font: print ('Warning, fonts disabled')
if not pygame.mixer: print ('Warning, sound disabled')

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, 'data')

#functions to create our resources
def load_image(name, colorkey=None):
    fullname = os.path.join(data_dir, name)
    image = pygame.image.load(fullname)
    #try:
        #image = pygame.image.load(fullname)
   # except pygame.error:
    #    print ('Cannot load image:', fullname)
     #   raise SystemExit(str(geterror()))
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

def load_sound(name):
    class NoneSound:
        def play(self): pass
    if not pygame.mixer or not pygame.mixer.get_init():
        return NoneSound()
    fullname = os.path.join(data_dir, name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error:
        print ('Cannot load sound: %s' % fullname)
        raise SystemExit(str(geterror()))
    return sound


#classes for our game objects
class Fist(pygame.sprite.Sprite):
    """moves a clenched fist on the screen, following the mouse"""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        self.image, self.rect = load_image('pistolet1.bmp', -1)
        self.punching = 0

    def update(self):
        "move the fist based on the mouse position"
        pos = pygame.mouse.get_pos()
        self.rect.midtop = pos
        if self.punching:
            self.rect.move_ip(5, 10)

    def punch(self):
        "returns true if the fist collides with the target"
        if not self.punching:
            self.punching = 1
          
        
    def trafione(self, target):
        "returns true if the fist collides with the target"
        if self.punching:
            hitbox = self.rect.inflate(-5, -5)
            return hitbox.colliderect(target.rect)

    def unpunch(self):
        "called to pull the fist back"
        self.punching = 0


class Chimp(pygame.sprite.Sprite):
    """moves a monkey critter across the screen. it can spin the
       monkey when it is punched."""
    def __init__(self,x=10,y=10,dx=9,dy=3,Losowe=False):
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        self.image, self.rect = load_image("alien1.bmp" , -1,)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = x, y 
        self.move = dx
        self.move2= dy
        self.dizzy = 0
        self.Losowe=Losowe
        self.Stan="normalny"
        self.time_0=0

    def update(self):
        "walk or spin, depending on the monkeys state"
        if self.dizzy:
            self._spin()
        else:
            self._walk()
    def  dym(self,screen):
      if self.Stan=="trafiony":
        x0,y0=self.rect.topleft
        x1,y1=self.rect.bottomright
        xs=(x1+x0)/2
        ys=(y1+y0)/2
        r=10
        dx=-5*self.move
        dy=-5*self.move2
##        gfx.filled_circle (screen ,xs+dx,ys+dy,r,pygame.Color("white"))
##        gfx.filled_circle (screen ,xs+3*dx,ys+3*dy,2*r,pygame.Color("white"))
##        gfx.filled_circle (screen ,xs+5*dx,ys+5*dy,3*r,pygame.Color("white"))
##        gfx.filled_circle (screen ,xs+7*dx,ys+8*dy,4*r,pygame.Color("white"))
##        gfx.filled_circle (screen ,xs+12*dx,ys+12*dy,5*r,pygame.Color("white"))
##        gfx.filled_circle (screen ,xs+16*dx,ys+16*dy,6*r,pygame.Color("grey"))
##        gfx.filled_circle (screen ,xs+20*dx,ys+20*dy,7*r,pygame.Color("black"))
        for i in range (7):    
         gfx.filled_circle (screen ,xs+(1+2*i)*dx,ys+(1+2*i)*dy,(i+1)*r,pygame.Color(0xcc,0xcc,0xcc,255-20*i))
    def _walk(self):
        "move the monkey across the screen, and turn at the ends"
        if self.Stan=="lezy":
            if self.mochod.stan== "stop":
         #if pygame.time.get_ticks() - self.time_0 > 3000:
             self.Stan= 'normalny'
             self.move2= -1
             self.move= 1
             newpos = self.rect.move((0, -10))
             self.mochod= None
             self.rect = newpos
        if self.Losowe and self.Stan=="normalny":
         if random.randint (1,20)==20:
            self.move+=1
         if random.randint (1,20)==20:
            self.move-=1
         if random.randint (1,20)==20:
            self.move2+=1
         if random.randint (1,20)==20:
            self.move2-=1
        elif self.Stan=="trafiony":
            self.move= 0
            self.move2= 3
            
        newpos = self.rect.move((self.move, self.move2))
        zmianakierunku= False
        if self.rect.left < self.area.left or \
            self.rect.right > self.area.right:
            self.move = -self.move
            self.image = pygame.transform.flip(self.image, 1, 0)
            zmianakierunku= True
        if self.rect.top < self.area.top or \
              self.rect.bottom > self.area.bottom:
          if  self.Stan=="normalny":
              self.move2= -self.move2
              zmianakierunku= True
          else:
            self.move2= 0
            self.move=0
            if self.Stan != "lezy":
              self.Stan="lezy"
              self.mochod= Mochod(self.rect.centerx,self.area.bottom)
              self.sprites.add(self.mochod)
              #self.time_0=pygame.time.get_ticks()    
        if zmianakierunku:
            #newpos = self.rect.move((self.move, self.move2))
            if self.rect.left < self.area.left:
               self.rect.left = self.area.left+10
            if self.rect.right > self.area.right:
               self.rect.right = self.area.right-10
            if self.rect.top < self.area.top :
               self.rect.top = self.area.top+10
            if self.rect.bottom > self.area.bottom:
               self.rect.bottom = self.area.bottom-10

          

        else:
         self.rect = newpos
 
    def _spin(self):
        "spin the monkey image"
        center = self.rect.center
        self.dizzy = self.dizzy + 12
        if self.dizzy >= 360:
            self.dizzy = 0
            self.image = self.original
        else:
            rotate = pygame.transform.rotate
            self.image = rotate(self.original, self.dizzy)
        self.rect = self.image.get_rect(center=center)

    def punched(self):
        "this will cause the monkey to start spinning"
        if not self.dizzy:
            self.dizzy = 1
            self.original = self.image


class Mochod(pygame.sprite.Sprite):
    def __init__(self,x=100,bottom=100):
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        self.image, self.rect = load_image("mochod.bmp" , -1 ,)
        self.rect.bottom= bottom
        self.startx= x
        self.rect.centerx=x
        self.stan="help"
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        
    def update (self):
        if self.stan== "help": 
          self.rect.move_ip (5,0)
        elif self.stan== "powrot":
          self.rect.move_ip (-5,0)
          if self.rect.centerx < self.startx:
             self.stan="stop"
        elif self.stan== "stop":
             self.kill ()
        if self.rect.left > self.area.right:
          self.stan= "powrot"

class alienlud(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        self.image, self.rect = load_image("alienlud1.bmp" , -1 )
        self.images=[]
        for lud in range(1,5):
            ii,oo=load_image('alienlud'+str (lud)+".bmp",-1)
            self.images.append(ii)
        self.lasttick = pygame.time.get_ticks()
        self.imgnum= 0
    def update(self):
      if pygame.time.get_ticks() - self.lasttick > 100:
         self.lasttick = pygame.time.get_ticks()
         self.imgnum = (self.imgnum + 1) %4
         self.image = self.images[self.imgnum]
def main():
    """this function is called when the program starts.
       it initializes everything it needs, then runs in
       a loop until the function returns."""
#Initialize Everything
    pygame.init()
    screen = pygame.display.set_mode((1000, 500))
    pygame.display.set_caption('Monkey Fever')
    pygame.mouse.set_visible(0)

#Create The Backgound
    background, bgrett = load_image("gory2.bmp")
    #background = pygame.Surface(screen.get_size())
    background = background.convert()
    #background.fill((250, 250, 250))

#Put Text On The Background, Centered
    if pygame.font:
        font = pygame.font.Font(None, 36)
        text = font.render("Wal mnie wal mnie wal mnie", 2, (10, 10, 10))
        textpos = text.get_rect(centerx=background.get_width()/2)
        background.blit(text, textpos)


#Prepare Game Objects
    clock = pygame.time.Clock()
    whiff_sound = load_sound('whiff.wav')
    punch_sound = load_sound('alebul.wav')
    punch_sounds = []
    for ps in ['aua','ale','bul']:
        punch_sounds.append (load_sound(ps+'.wav'))
    chimps = []
    for chimp in range(10):
        chimps.append (Chimp(100,130,3,9,True))
    fist = Fist()
    a=alienlud()
    allsprites = pygame.sprite.RenderPlain([fist,a ]+chimps)
    for chimp in chimps:
        chimp.sprites= allsprites


#Main Loop
    going = True
    while going:
        clock.tick(60)

        #Handle Input Events
        for event in pygame.event.get():
            if event.type == QUIT:
                going = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                going = False
            elif event.type == MOUSEBUTTONDOWN:
                fist.punch()
                malpa_trafiona= False
                for chimp in chimps:
                    if fist.trafione(chimp):
                      chimp.Stan="trafiony"
                      malpa_trafiona= True
                      punch_sounds[random.randint(0,2)].play() #punch
                      chimp.punched()
                if not malpa_trafiona:
                    whiff_sound.play() #miss
            elif event.type == MOUSEBUTTONUP:
                fist.unpunch()

        allsprites.update()
        
        #Draw Everything
        screen.blit(background, (0, 0))

        for maupa in chimps:

          maupa.dym (screen)
        allsprites.draw(screen)
        #gfx.circle (screen,100,100,50,pygame.Color("white")) 
        pygame.display.flip()

    pygame.quit()

#Game Over


#this calls the 'main' function when this script is executed
if __name__ == '__main__':
    main()
