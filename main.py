# Jump man

import pygame as pg
import random
import os
from settings import *
from sprites import *


class Game:

    def __init__(self):
        # initialize game window, etc
        # pass = do nothing
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)

    def new(self):
        # start a new game
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.plat_start = pg.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)
        p1 = Platform(0, SCREEN_HEIGHT-20, SCREEN_WIDTH, 120)
        self.all_sprites.add(p1)
        self.plat_start.add(p1)
        p2 = Platform(SCREEN_WIDTH / 2 - 50, SCREEN_HEIGHT / 2, 100, 100)
        self.all_sprites.add(p2)
        self.platforms.add(p2)
        p3 = Platform(SCREEN_WIDTH / 2 + 250, SCREEN_HEIGHT / 3, 100, 200)
        self.all_sprites.add(p3)
        self.platforms.add(p3)
        self.run()

    def run(self):
        # Game loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        # Game loop - Update
        self.all_sprites.update()
        # add collision to all side of the ascending platform
        hits_other_plat = pg.sprite.spritecollide(self.player, self.platforms, False)
        if hits_other_plat:
            # all if statements are checking all sides of the platforms
            # Checking collision on the top of the platforms
            if self.player.rect.top < hits_other_plat[0].rect.top:
                self.player.pos.y = hits_other_plat[0].rect.top + 1
                self.player.vel.y = 0
                # removes stuttering of player on platforms
                self.player.vx = 0
            # Checking collision on the bottom of the platforms
            elif self.player.rect.bottom > hits_other_plat[0].rect.bottom:
                self.player.vel.y *= COLLISION_CONST
            # Checking collision on the left of the platforms
            elif self.player.rect.right > hits_other_plat[0].rect.left:
                self.player.vx *= -1
                self.player.vel.y *= 1
            # Checking collision on the right of the platforms
            elif self.player.rect.left < hits_other_plat[0].rect.right:
                self.player.vx *= -1
                self.player.vel.y *= 1
        # add collision to the top of the starting platform
        hits_start_plat = pg.sprite.spritecollide(self.player, self.plat_start, False)
        if hits_start_plat:
            self.player.pos.y = hits_start_plat[0].rect.top + 1
            self.player.vel.y = 0
            self.player.vx = 0
        # if player is high enough, scroll screen
        if self.player.rect.top <= SCREEN_HEIGHT / 4:
            self.player.pos.y += abs(self.player.vel.y)
            for plat in self.platforms:
                plat.rect.y += abs(self.player.vel.y)
            for plat1 in self.plat_start:
                plat1.rect.y += abs(self.player.vel.y)
        # if player is low enough, scroll screen
        if self.player.rect.top >= SCREEN_HEIGHT - (SCREEN_HEIGHT / 5):
            self.player.pos.y -= abs(self.player.vel.y)
            for plat in self.platforms:
                plat.rect.y -= abs(self.player.vel.y)
            for plat in self.plat_start:
                plat.rect.y -= abs(self.player.vel.y)

    def events(self):
        # Game loop - events
        for event in pg.event.get():
            # check for closing of window
            keys = pg.key.get_pressed()
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                    self.running = False
            if keys[pg.K_ESCAPE]:
                if self.playing:
                    self.playing = False
                    self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    # print("space is pressed")
                    self.player.jump_charge_right()
            if event.type == pg.KEYUP:
                if event.key == pg.K_SPACE:
                    # print("space is released")
                    self.player.jump_release_right()

            # if event.type == pg.KEYDOWN:
            #     if event.key == pg.K_SPACE:
            #         pass
            #     if event.key == pg.K_RIGHT and PLAYER_CHARGE_RIGHT_X <= 15:
            #         self.vx += 1
            #     if event.key == pg.K_LEFT and PLAYER_CHARGE_LEFT_X <= -15:
            #         PLAYER_VEL_LEFT_X == 0
            #         PLAYER_VEL_RIGHT_X == 0
            #         PLAYER_CHARGE_LEFT_X -= 3

    def draw(self):
        # Game loop - draw
        self.screen.fill(BGCOLOR)
        self.all_sprites.draw(self.screen)
        # *after* drawing everything, flip the display
        pg.display.flip()

    def show_start_screen(self):
        # start menu / splash screen
        self.screen.fill(BGCOLOR)
        self.draw_text(TITLE, 48, WHITE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4)
        self.draw_text("Space to jump, Arrows to move", 22,
                       WHITE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.draw_text("Press a key to play", 22, WHITE, SCREEN_WIDTH / 2, SCREEN_HEIGHT * 3 / 4)
        pg.display.flip()
        self.wait_for_key()

    def show_go_screen(self):
        # game over/continue
        if not self.running:
            return
        self.screen.fill(BGCOLOR)
        self.draw_text("GAME OVER", 48, WHITE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4)
        self.draw_text("Press a key to play", 22, WHITE, SCREEN_WIDTH / 2, SCREEN_HEIGHT * 3 / 4)
        pg.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False

    def draw_text(self, text, size, color, x, y):
        pg.init()
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)


g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()
