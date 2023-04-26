from scripts.settings import *
from scripts.player import *
vec = pg.math.Vector2







class Platform(pg.sprite.Sprite):
    def __init__(self,game, x, y, w, h,passthrough):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.width = w
        self.height = h
        self.image = self.get_image(platform_image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.transparent = passthrough
        self.addToGroups()

    def addToGroups(self):
        self.game.all_sprites.add(self)
        self.game.platform_group.add(self)

    def get_image(self,img_dir):
        self.img = pg.image.load(img_dir).convert()
        self.img = pg.transform.scale(self.img, (self.width, self.height))
        self.img.set_colorkey(self.game.defaultColor)
        return self.img











