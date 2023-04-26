from scripts.settings import *
from scripts.player import *
vec = pg.math.Vector2


class Enemy(pg.sprite.Sprite):

    def __init__(self, game, x, y,w,h, img,color_key, behavior):
        super(Enemy,self).__init__()
        self.game = game
        self.width = w
        self.height = h
        self.color_key = color_key
        self.image_l = self.get_image(img)
        self.image_r = pg.transform.flip(self.image_l, True, False)
        self.image = self.get_image(img)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.speed = ENEMY_SPEED
        self.behavior = behavior

        self.ignore_platforms = True
        self.addToGroups()

    def commitCollision(self, pos):
        self.pos.y = pos
        self.vel.y = 0

    def get_image(self,img):
        self.img = pg.image.load(img).convert()
        self.img = pg.transform.scale(self.img, (self.width,self.height))
        self.img.set_colorkey(self.game.defaultColor)
        return self.img

    def addToGroups(self):
        self.game.all_sprites.add(self)
        self.game.enemy_group.add(self)


    def seek(self):
        self.player_pos = self.game.player.pos
        self.acc = (self.player_pos - self.pos).normalize() * self.speed

    def float(self):
        if self.rect.centerx > WIDTH+50:
            self.movement = self.speed*-1.25
        elif self.rect.centerx < -50:
            self.movement = self.speed*1.25
        if self.rect.top > WIDTH+5:
            self.kill()
        self.acc.x = self.movement



    def avoid_others(self):
        for mob in self.game.enemy_group:
            if mob != self:
                dist = self.pos - mob.pos
                if 0 < dist.length() < self.width+10:
                    self.acc -= (mob.pos - self.pos).normalize() * GRAV_MOD/13


    def update(self):
        self.game.check_Events()
        #makes stuff bouncy
        if self.vel.x <0:
            self.image = self.image_l
        else:
            self.image = self.image_r
        self.acc = vec(0, 0.15)
        if self.behavior == 'seek':
            self.seek()
        elif self.behavior == 'float':
            self.float()
        self.avoid_others()


        # apply friction
        self.acc += self.vel * PLAYER_FRICTION
        # equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        # wrap around the sides of the screen



        self.rect.midbottom = self.pos