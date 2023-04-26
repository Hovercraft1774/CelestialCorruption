from scripts.settings import *
from scripts.player import *
from scripts.enemy import *
from scripts.terrain import  *


class Game(object):

    def __init__(self):
        self.playing = True
        pg.init()
        pg.mixer.init() #if using online editor, take this out
        # creates a screen for the game
        self.screen = pg.display.set_mode((WIDTH,HEIGHT))
        pg.display.set_caption(TITLE) #Title of the screen window
        # creates time
        self.clock = pg.time.Clock()
        self.defaultColor = DEFAULT_COLOR
        self.font_name = pg.font.match_font("comic_sans")
        self.load_snd()
        self.load_data()


    def new(self):
        # create Sprite Groups
        self.all_sprites = pg.sprite.Group()
        self.enemy_group = pg.sprite.Group()
        self.player_group = pg.sprite.Group()
        self.bullet_group = pg.sprite.Group()
        self.platform_group = pg.sprite.Group()
        self.accesory_group = pg.sprite.Group()
        self.score = 0
        self.canShoot = True
        self.last_update = pg.time.get_ticks()

        # creates terrain objects
        self.p1 = Platform(self, -5, HEIGHT - 40, WIDTH, 40, False)  # base ground
        for plat in PLATFORM_CONFIG_1:
            p = Platform(self, *plat)

        #create player player objects
        self.player = Player(self,WIDTH / 2 - 140, HEIGHT * 3 / 4 - 10,BLUE,self.defaultColor)
        self.wings = Accesories(self,self.player.direction,player_wings,self.defaultColor)

        #create enemy objects
        self.maxEnemies = 2
        self.spawnScore = 500
        self.behavior = ['float','float','float','float']
        self.spawnEnemies()
        self.load_music(MAIN_THEME)


        # self.p2 = Platform(self,
        # self.p3 = Platform(self,)
        # self.p4 = Platform(self,)
        # self.p5 = Platform(self,)
        # self.p6 = Platform(self,)
        # self.p7 = Platform(self,)



    def load_data(self):
        with open(HS_FILE, 'r') as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0
        self.bg_img = pg.image.load(alt_background_image).convert()
        self.bg_img = pg.transform.scale(self.bg_img, (WIDTH * 1.15, HEIGHT * 1.15))

    def gameLoop(self):
        pg.mixer.music.play(loops=-1)
        while self.playing:
            #tick clock
            self.clock.tick(fps)

            #check events
            self.check_Events()

            #update all
            self.update()

            #draw
            self.draw()
        pg.mixer.music.fadeout(500)  # makes the music fade instead of cutting off

    def spawnEnemies(self):
        for i in range(self.maxEnemies-len(self.enemy_group)):
            w =random.randint(60,120)
            movement = random.choice(self.behavior)
            x = [-150,WIDTH+150]
            self.enemy = Enemy(self,random.choice(x),random.randint(-50,HEIGHT-300),w,w,enemy_cloud,self.defaultColor, movement)

    def checkCanShoot(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 300:
            self.canShoot = True
            self.last_update = now


    def check_Events(self):
        self.checkCanShoot()
        self.left_click = pg.mouse.get_pressed()[0]
        if self.canShoot and self.left_click:
            self.canShoot = False
            self.bullet_snd.play()
            self.bullet = Bullet(self, self.player.rect.midleft, self.player.direction, bullet_sprite,
                                 self.defaultColor)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE or event.key == pg.K_w:
                    self.player.jump()


        if self.score >= self.spawnScore:
            self.maxEnemies += 1
            self.behavior.append('seek')
            self.spawnScore = self.spawnScore*len(self.enemy_group)
            for enemy in self.enemy_group:
                enemy.speed += 0.1
        if len(self.enemy_group) < self.maxEnemies:
            self.spawnEnemies()




        #if group hit group, kill group1 or 2
        if self.player.vel.y >0:
            hits = pg.sprite.spritecollide(self.player, self.platform_group, False)
            for hit in hits:
                if hit.transparent and not self.player.ignore_platforms:
                    if self.player.pos.y-15 < hit.rect.centery:
                        self.player.pos.y = hit.rect.top
                        self.player.vel.y = 0
                if not hit.transparent:
                    self.player.pos.y = hit.rect.top
                    self.player.vel.y = 0


        hits = pg.sprite.groupcollide(self.bullet_group,self.enemy_group,True,True)
        if hits:
            self.enemy_death_snd.play()
            self.score += 50

        hits = pg.sprite.groupcollide(self.player_group, self.enemy_group, False, False)
        if hits:
            self.player_death_snd.play()
            self.playing = False

        # for enemy in self.enemy_group:
        #     hits = pg.sprite.spritecollide(enemy,self.platform_group, False)
        #     for hit in hits:
        #         if not hit.transparent:
        #             enemy.pos.y = hit.rect.top
        #             enemy.vel.y = 0
        #     old_pos = enemy.pos



        # for hit in hits:
        #     if hit.transparent and not self.player.ignore_platforms:
        #         self.player.pos.y = hits[0].rect.top-15
        #         self.player.vel.y = 0
        #     if not hit.transparent:
        #         self.player.pos.y = hits[0].rect.top - 15
        #         self.player.vel.y = 0




    def load_snd(self):
        self.player_death_snd = pg.mixer.Sound(player_death_sound)
        self.enemy_death_snd = pg.mixer.Sound(enemy_death_sound)
        self.bullet_snd = pg.mixer.Sound(bullet_sound)
        self.confirm_snd = pg.mixer.Sound(CONFIRM_SOUND)
        self.enemy_death_snd.set_volume(0.3)
        self.player_death_snd.set_volume(0.5)
        self.bullet_snd.set_volume(0.2)
        self.confirm_snd.set_volume(3)



    def update(self):
        self.all_sprites.update()


    def load_music(self,music):
        self.track1 = pg.mixer.music.load(music)
        pg.mixer.music.set_volume(0.5)



    def draw(self):
        self.screen.fill(self.defaultColor)
        self.screen.blit(self.bg_img, self.bg_img.get_rect())
        self.all_sprites.draw(self.screen)
        self.draw_Text(str(self.score), 50, WIDTH / 2, 10, WHITE)




        # think whiteboard, must be last line
        pg.display.flip()

    def wait_for_key(self,boolien=False):
        waiting = True

        while waiting:
            self.clock.tick(fps)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                    pg.quit()
                if boolien:
                    if event.type == pg.KEYUP:
                        if event.key == pg.K_y:
                            self.confirm_snd.play()
                            return True
                        elif event.key == pg.K_n:
                            self.confirm_snd.play()
                            return False
                else:
                    if event.type == pg.KEYUP:
                        self.confirm_snd.play()
                        waiting = False


    def draw_Text(self, text, size, x, y, color):
        font = pg.font.Font(self.font_name, size)
        text_sprite = font.render(text, True, color)
        text_rect = text_sprite.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_sprite, text_rect)

    def start_Screen(self):
        self.load_music(TITLE_THEME)
        pg.mixer.music.play(loops=-1)
        self.screen.fill(self.defaultColor)
        self.draw_Text(TITLE, 120, WIDTH / 2, HEIGHT / 4, LIGHT_PURPLE)
        self.draw_Text("WASD to move, Space or W to jump", 22, WIDTH / 2, HEIGHT*3/4-100, LIGHT_PURPLE)
        self.draw_Text("Press a key to play", 22, WIDTH / 2, HEIGHT * 3 / 4, LIGHT_PURPLE)
        self.draw_Text("High Score: " + str(self.highscore), 22, WIDTH / 2, 15, ORANGE)
        pg.display.flip()
        self.wait_for_key()
        pg.mixer.music.fadeout(500)#makes the music fade instead of cutting off

    def end_Screen(self):
        self.screen.fill(self.defaultColor)
        self.draw_Text("GAME OVER", 48, WIDTH / 2, HEIGHT / 4, RED)
        self.draw_Text("Score: " + str(self.score), 22, WIDTH / 2, HEIGHT / 2, ORANGE)
        self.draw_Text("Press Y to play again", 22, WIDTH / 2, HEIGHT * 3 / 4, WHITE)
        self.draw_Text("or press N to quit", 22, WIDTH / 2, HEIGHT * 3 / 4+22, WHITE)
        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_Text("NEW HIGH SCORE!", 22, WIDTH / 2, HEIGHT / 2 + 40, YELLOW)
            with open(HS_FILE, 'w') as f:
                f.write(str(self.score))
        else:
            self.draw_Text("High Score: " + str(self.highscore), 22, WIDTH / 2, HEIGHT / 2 + 40, ORANGE)
        pg.display.flip()
        playAgain = self.wait_for_key(True)
        if playAgain:
            self.playing = True
            pg.mixer.music.fadeout(500)
            return True
        else:
            pg.mixer.music.fadeout(500)
            quit()



