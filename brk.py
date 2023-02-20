import pygame
import random
import flask
import threading
import math
import numpy as np

from os import path


imagedir = path.join(path.dirname(__file__), "sprites")
width = 480
height: int = 640
fps = 60

white = (255, 255, 255)
black = (0, 0, 0)

pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Zaidimas")
clock = pygame.time.Clock()
fontname = pygame.font.match_font("Arial")


class Background(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(path.join(imagedir, 'Background.jpg')).convert()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()


class Meteorite(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(path.join(imagedir, 'Meteorite.png')).convert()
        self.image = pygame.transform.scale(self.image, (width//5, height//5))
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randint(0, width)
        self.rect.bottom = random.randint(0, height)
        self.xspeed = 1
        self.yspeed = 1

    def update(self):
        if self.rect.centerx > width:
            self.rect.centerx = 0
        if self.rect.centerx < 0:
            self.rect.centerx = width
        if self.rect.bottom > height:
            self.rect.bottom = 0
        if self.rect.bottom < 0:
            self.rect.bottom = height
        self.rect.centerx -= self.xspeed
        self.rect.bottom -= self.yspeed


class Raketa(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_original = pygame.image.load(path.join(imagedir, 'Rocket.png')).convert()
        self.image_original = pygame.transform.scale(self.image_original, (width//10, height//10))
        self.image_original.set_colorkey(black)
        self.rect = self.image_original.get_rect()
        self.rect.centerx = width//2
        self.rect.bottom = height//2
        self.xspeed = 0
        self.yspeed = 0
        self.degrees = 0

    def kampas(self):
        if self.xspeed == 0 and self.yspeed == 0:                       # skaiciuoja kampa
            return
        vector_1 = [0, 50]
        vector_2 = [self.xspeed, self.yspeed]
        unit_vector_1 = vector_1 / np.linalg.norm(vector_1)
        unit_vector_2 = vector_2 / np.linalg.norm(vector_2)
        dot_product = np.dot(unit_vector_1, unit_vector_2)
        angle = np.arccos(dot_product)
        self.degrees = angle * 180 / math.pi
        if self.xspeed < 0:
            self.degrees = self.degrees * -1
        return self.degrees

    def update(self):
        if self.rect.centerx > width:
            self.rect.centerx = width
        if self.rect.centerx < 0:
            self.rect.centerx = 0
        if self.rect.bottom > height:
            self.rect.bottom = height
        if self.rect.bottom < 0:
            self.rect.bottom = 0
        self.rect.centerx -= self.xspeed
        self.rect.bottom -= self.yspeed
        self.kampas()
        self.image = pygame.transform.rotate(self.image_original, self.degrees)

    def up(self):
        self.yspeed = 10

    def left(self):
        self.xspeed = 10

    def down(self):
        self.yspeed = -10

    def right(self):
        self.xspeed = -10

    def stopvertical(self):
        self.yspeed = 0
        return self.yspeed == 0

    def stophorizontal(self):
        self.xspeed = 0
        return self.xspeed == 0

    def is_collided_with(self, image):
        pass


class Raketa2(Raketa, pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_original = pygame.image.load(path.join(imagedir, 'Rocket.png')).convert()
        self.image_original = pygame.transform.scale(self.image_original, (width//10, height//10))
        self.image_original.set_colorkey(black)
        self.rect = self.image_original\
            .get_rect()
        self.rect.centerx = width//2
        self.rect.bottom = height//2
        self.xspeed = 0
        self.yspeed = 0
        self.degrees = 0
        self.connection()

    def connection(self):
        app = flask.Flask(__name__)
        app.debug = False
        app.use_reloader = False

        @app.route('/', methods=['GET'])
        def home():
            # response = requests.get("http://api.open-notify.org/this-api-doesnt-exist")
            query_parameters = flask.request.args
            komanda = query_parameters.get('command')
            if komanda == "left":
                self.kampas()
            if komanda == "right":
                self.kampas()
            if komanda == "up":
                self.kampas()
            if komanda == "down":
                self.kampas()
            if komanda == "stopx":
                self.stophorizontal()
            if komanda == "stopy":
                self.stopvertical()

            return "Pavyko." + komanda

        threading.Thread(target=app.run).start()

    def update(self):
        if self.rect.centerx > width:
            self.rect.centerx = 0
        if self.rect.centerx < 0:
            self.rect.centerx = width
        if self.rect.bottom > height:
            self.rect.bottom = 0
        if self.rect.bottom < 0:
            self.rect.bottom = height
        self.rect.centerx -= self.xspeed
        self.rect.bottom -= self.yspeed
        self.kampas()
        self.image = pygame.transform.rotate(self.image_original, self.degrees)


class Bullet(Raketa, pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(path.join(imagedir, 'Bullet.png')).convert()
        self.image = pygame.transform.scale(self.image, (width//20, height//20))
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.xspeed = int(math.sin(raketa.degrees)*10)
        self.yspeed = int(math.cos(raketa.degrees)*10)
        self.angle = 0
        self.image = pygame.transform.rotate(self.image, raketa.degrees)

    def update(self):
        if self.rect.centerx > width:
            self.rect.centerx = 0
        if self.rect.centerx < 0:
            self.rect.centerx = width
        if self.rect.bottom > height:
            self.rect.bottom = 0
        if self.rect.bottom < 0:
            self.rect.bottom = height
        self.rect.centerx -= self.xspeed
        self.rect.bottom -= self.yspeed

    def up(self):
        self.yspeed = 15

    def left(self):
        self.xspeed = 15

    def right(self):
        self.xspeed = -15

    def down(self):
        self.yspeed = -15


class Bullet2(Bullet, pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(path.join(imagedir, 'Bullet.png')).convert()
        self.image = pygame.transform.scale(self.image, (width//20, height//20))
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.xspeed = 0
        self.yspeed = 15
        self.angle = 0
        self.image = pygame.transform.rotate(self.image, raketa2.degrees)

    def update(self):
        if self.rect.centerx > width:
            self.rect.centerx = 0
        if self.rect.centerx < 0:
            self.rect.centerx = width
        if self.rect.bottom > height:
            self.rect.bottom = 0
        if self.rect.bottom < 0:
            self.rect.bottom = height
        self.rect.centerx -= self.xspeed
        self.rect.bottom -= self.yspeed


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(fontname, size)
    text_surface = font.render(text, True, white)
    text_rectangle = text_surface.get_rect()
    text_rectangle.midtop = (x, y)
    surf.blit(text_surface, text_rectangle)


def pagrindinis_meniu():
    global screen

    while True:
        myevent = pygame.event.poll()
        if myevent.type == pygame.KEYDOWN:
            if myevent.key == pygame.K_RETURN:
                break
        elif myevent.type == pygame.QUIT:
            pygame.quit()
            quit()
        else:
            draw_text(screen, "Press Enter to start", 30, width//2, height//2)
            pygame.display.update()
    screen.fill(black)
    draw_text(screen, "Pasiruosimas", 30, width//2, height//2)
    pygame.display.update()


running = True
menuDisplay = True
a = 0
z = 0
start = 0
start2 = 0
lifeCount = 5
print("Rocket 2 lives left = " + str(lifeCount))
lifeCount2 = 5
print("Rocket 2 lives left = " + str(lifeCount2))
while running:
    if menuDisplay:
        pagrindinis_meniu()
        pygame.time.wait(1000)
        menuDisplay = False
        allsprites = pygame.sprite.Group()
        background = Background()
        allsprites.add(background)
        raketa = Raketa()
        allsprites.add(raketa)
        raketa2 = Raketa2()
        allsprites.add(raketa2)
        meteoritas = Meteorite()
        allsprites.add(meteoritas)
        bullet = Bullet(raketa.rect.centerx, raketa.rect.bottom)
        bullet2 = Bullet(raketa2.rect.centerx, raketa2.rect.bottom)
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
                pygame.quit()
                quit()
            if event.key == pygame.K_SPACE:
                while pygame.time.get_ticks() - start > 1000:
                    bullet = Bullet(raketa.rect.centerx, raketa.rect.bottom)
                    allsprites.add(bullet)
                    start = pygame.time.get_ticks()
                    break

            if event.key == pygame.K_x:
                while pygame.time.get_ticks() - start2 > 1000:
                    bullet2 = Bullet2(raketa2.rect.centerx, raketa2.rect.bottom)
                    allsprites.add(bullet2)
                    start2 = pygame.time.get_ticks()
                    break

            if event.key == pygame.K_LEFT:
                z = 1
                raketa.left()
            if event.key == pygame.K_RIGHT:
                z = 2
                raketa.right()
            if event.key == pygame.K_DOWN:
                z = 3
                raketa.down()
            if event.key == pygame.K_UP:
                z = 4
                raketa.up()

            if event.key == pygame.K_a:
                a = 1
                raketa2.left()
            if event.key == pygame.K_d:
                a = 2
                raketa2.right()
            if event.key == pygame.K_s:
                a = 3
                raketa2.down()
            if event.key == pygame.K_w:
                a = 4
                raketa2.up()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                raketa.stophorizontal()
            if event.key == pygame.K_RIGHT:
                raketa.stophorizontal()
            if event.key == pygame.K_DOWN:
                raketa.stopvertical()
            if event.key == pygame.K_UP:
                raketa.stopvertical()

            if event.key == pygame.K_a:
                raketa2.stophorizontal()
            if event.key == pygame.K_d:
                raketa2.stophorizontal()
            if event.key == pygame.K_s:
                raketa2.stopvertical()
            if event.key == pygame.K_w:
                raketa2.stopvertical()

        while z:
            if z == 1:
                bullet.stopvertical()
                bullet.left()
            if z == 2:
                bullet.stopvertical()
                bullet.right()
            if z == 3:
                bullet.stophorizontal()
                bullet.down()
            if z == 4:
                bullet.stophorizontal()
                bullet.up()
            break

        while a:
            if a == 1:
                bullet2.stopvertical()
                bullet2.left()
            if a == 2:
                bullet2.stopvertical()
                bullet2.right()
            if a == 3:
                bullet2.stophorizontal()
                bullet2.down()
            if a == 4:
                bullet2.stophorizontal()
                bullet2.up()
            break

    if pygame.sprite.collide_rect(bullet, meteoritas):
        bullet.kill()
        meteoritas.kill()
        meteoritas = Meteorite()
        allsprites.add(meteoritas)

    if pygame.sprite.collide_rect(bullet2, meteoritas):
        bullet2.kill()
        meteoritas.kill()
        meteoritas = Meteorite()
        allsprites.add(meteoritas)

    if pygame.sprite.collide_rect(raketa, meteoritas):
        meteoritas.kill()
        raketa.kill()
        lifeCount -= 1
        print("Rocket 1 lives left = " + str(lifeCount))
        raketa = Raketa()
        allsprites.add(raketa)
        meteoritas = Meteorite()
        allsprites.add(meteoritas)

    if pygame.sprite.collide_rect(raketa2, meteoritas):
        meteoritas.kill()
        raketa2.kill()
        lifeCount2 -= 1
        print("Rocket 2 lives left = " + str(lifeCount2))
        raketa2 = Raketa()
        allsprites.add(raketa2)
        meteoritas = Meteorite()
        allsprites.add(meteoritas)

    if lifeCount == 0:
        screen.fill(black)
        draw_text(screen, "Zaidimas baigtas, laimejo Raketa 2", 30, width // 2, height // 2)
        pygame.display.update()
        pygame.time.wait(3000)
        running = False
        pygame.quit()
        quit()
    if lifeCount2 == 0:
        screen.fill(black)
        draw_text(screen, "Zaidimas baigtas, laimejo Raketa 1", 30, width // 2, height // 2)
        pygame.display.update()
        pygame.time.wait(3000)
        running = False
        pygame.quit()
        quit()

    allsprites.update()
    for sprite in allsprites:
        if isinstance(sprite, Bullet):
            if sprite.rect.centerx > width or sprite.rect.centerx < 0 or sprite.rect.bottom > height or sprite.rect.bottom < 0:
                allsprites.remove(sprite)
                sprite = None

    screen.fill(black)
    allsprites.draw(screen)
    pygame.display.flip()
