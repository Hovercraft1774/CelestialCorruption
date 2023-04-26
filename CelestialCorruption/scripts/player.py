from scripts.settings import *
vec = pg.math.Vector2


class Player(pg.sprite.Sprite):#must be a sprite inherited otherwise it won't fit in groups

    def __init__(self,game,x,y,img_dir,color_key):
        super(Player,self).__init__()
        self.game = game #adds reference to the game
        self.direction = "right"

        # self.player_img = pg.transform.flip(self.player_img, True, True) #this flips the image along the x,y axis
        # self.image = self.get_image(img_dir)
        # self.image.set_colorkey(color_key)#gets rid of black color and makes it transparent
        # self.image = pg.Surface((30,30)) #gets just a normal rectangle
        self.hitbox = pg.Surface((26, 60))
        self.hitbox.fill(RED)
        self.image = self.hitbox
        self.player_image_l = self.get_image()
        self.image = self.player_image_l
        self.image_rect = self.image.get_rect()

        self.hitbox_rect = self.hitbox.get_rect()
        self.hitbox_rect.center = (x,y)
        self.rect = self.image_rect
        # self.image_rect.center = self.rect.center
        self.pos = vec(self.hitbox_rect.x,self.hitbox_rect.y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.image_rect = self.pos
        self.gliding = False
        self.gravity = GRAV_MOD
        self.ignore_platforms = False



        self.addToGroups()

    def draw(self,screen):

        print("test")
        screen.blit(self.player_image_l, self.rect.center)





    def addToGroups(self):
        self.game.all_sprites.add(self)
        self.game.player_group.add(self)

    def get_image(self):
        self.img = pg.image.load(player_sprite).convert()
        self.img = pg.transform.scale(self.img, (TILE_SIZEX/3.5, TILE_SIZEY+10))
        self.img.set_colorkey(self.game.defaultColor)
        return self.img


    def jump(self):
        self.rect.y += 1
        hits = pg.sprite.spritecollide(self,self.game.platform_group,False)
        self.rect.y += 1
        if hits:
            self.vel.y = -PLAYER_JUMP


    def update(self):
        self.game.check_Events()




        if self.gliding and self.vel.y > 1:
            self.vel.y = 0 #stops previous momentum
            self.gravity = GLIDE_MOD
        else:
            self.gravity = GRAV_MOD

        if self.vel.x < 0:
           self.image = pg.transform.flip(self.player_image_l, False, False)
           self.image_rect = self.image.get_rect()
           self.image_rect.center = self.pos


        else:
            self.image = pg.transform.flip(self.player_image_l,True,False)
            self.image_rect = self.image.get_rect()
            self.image_rect.center = self.pos




        self.acc = vec(0, self.gravity) #gravity


        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.direction = 'left'
            self.acc.x = -PLAYER_ACC


        if keys[pg.K_d]:
            self.direction = 'right'
            self.acc.x = PLAYER_ACC


        if keys[pg.K_s]:
            self.ignore_platforms = True
        else:
            self.ignore_platforms = False

        if keys[pg.K_SPACE]or keys[pg.K_w]:  # do this first so that it doesn't mess with the movement i think
            self.gliding = True
        else:
            self.gliding = False




        # apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        # wrap around the sides of the screen
        if self.pos.x > WIDTH + self.rect.width / 2:
            self.pos.x = 0 - self.rect.width / 2
        if self.pos.x < 0 - self.rect.width / 2:
            self.pos.x = WIDTH + self.rect.width / 2

        self.rect.midbottom = self.pos #set position



class Accesories(pg.sprite.Sprite):
    def __init__(self,game,direction,img_dir, color_key):
        super(Accesories, self).__init__()
        self.game = game
        self.direction = direction
        self.color_key = color_key
        self.image_dir = img_dir
        self.image = self.get_image(img_dir)
        self.rect = self.image.get_rect()
        self.rect.center = self.game.player.rect.center
        self.addToGroups()


    def addToGroups(self):
        self.game.all_sprites.add(self)
        self.game.accesory_group.add(self)

    def get_image(self, img_dir,isflipped=False):
        self.img = pg.image.load(img_dir).convert()
        if isflipped:
            self.img = pg.transform.flip(self.img, True, False)
        self.rect = self.img.get_rect()
        self.img = pg.transform.scale(self.img, (TILE_SIZEX/2, TILE_SIZEY))
        self.img.set_colorkey(self.color_key)
        return self.img

    def update(self):
        if self.game.player.direction == 'left':
            self.image = self.get_image(self.image_dir)
            self.rect.center = self.game.player.rect.topright
            self.rect.x = self.game.player.rect.centerx+10
        else:
            self.image = self.get_image(self.image_dir,True)
            self.rect.center = self.game.player.rect.topleft
            self.rect.x = self.game.player.rect.centerx-53



class Bullet(pg.sprite.Sprite):
    def __init__(self,game,coords,direction,img_dir,color_key):
        super(Bullet,self).__init__()
        self.game = game
        self.direction = direction
        self.image = self.get_image(img_dir)
        self.image.set_colorkey(color_key)#gets rid of black color and makes it transparent
        self.rect = self.image.get_rect()
        self.rect.center = coords
        self.pos = vec(coords)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.addToGroups()

    def addToGroups(self):
        self.game.all_sprites.add(self)
        self.game.bullet_group.add(self)

    def get_image(self, img_dir):
        self.img = pg.image.load(img_dir).convert()
        self.img = pg.transform.scale(self.img, (TILE_SIZEX/2, TILE_SIZEY))
        if self.direction == 'left':
            self.speed = -2
        else:
            self.speed = 2
            self.img = pg.transform.flip(self.img, True, False)
        return self.img

    def update(self):

        self.acc = vec(self.speed, GRAV_MOD//2) #gravity

        # apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rect.midbottom = self.pos #set position

        if self.rect.x > WIDTH+50 or self.rect.x < -50:
            self.kill()

