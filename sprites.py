# sprite classes for "jump man"

import pygame as pg
from settings import *


class Player(pg.sprite.Sprite):
    def __init__(self, game):
        self.game = game
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((30, 40))
        self.image.fill(BROWN)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.pos = pg.math.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.vx = 0
        self.acc = pg.math.Vector2(0, 0)
        self.vel = pg.math.Vector2(0, 0)

    # def jump_charge(self):
    #     # jump only if standing on a platform
    #     hits = pg.sprite.spritecollide(self.player, self.game.platforms, False)
    #     if hits:
    #         pass
    #
    # def jump_charge_left(self):
    #     # jump only if standing on a platform
    #     hits = pg.sprite.spritecollide(self.player, self.game.platforms, False)
    #     if hits:
    #         pass

    def jump_charge_right(self):
        # jump only if standing on a platform
        hits_other_plat = pg.sprite.spritecollide(self, self.game.platforms, False)
        if hits_other_plat:
            self.vel.y = 0
            self.vx = 0
        hits_start_plat = pg.sprite.spritecollide(self, self.game.plat_start, False)
        if hits_start_plat:
            self.vel.y = 0
            self.vx = 0

    # def jump_release(self):
    #     # jump only if standing on a platform
    #     hits = pg.sprite.spritecollide(self.player, self.game.platforms, False)
    #     if hits:
    #         pass
    #
    # def jump_release_left(self):
    #     # jump only if standing on a platform
    #     hits = pg.sprite.spritecollide(self.player, self.game.platforms, False)
    #     if hits:
    #         pass

    def jump_release_right(self):
        # jump only if standing on a platform
        hits_other_plat = pg.sprite.spritecollide(self, self.game.platforms, False)
        if hits_other_plat:
            if self.pos.y == hits_other_plat[0].rect.top + 1:
                self.vel.y = PLAYER_VEL_UP_Y
                self.vx = PLAYER_VEL_RIGHT_X
        hits_start_plat = pg.sprite.spritecollide(self, self.game.plat_start, False)
        if hits_start_plat:
            self.vel.y = PLAYER_VEL_UP_Y
            self.vx = PLAYER_VEL_RIGHT_X

    def get_keys(self):
        hits_other_plat = pg.sprite.spritecollide(self, self.game.platforms, False)
        if hits_other_plat:
            if self.pos.y == hits_other_plat[0].rect.top + 1:
                # self.vx = 0
                keys = pg.key.get_pressed()
                if keys[pg.K_LEFT]:
                    self.vx = PLAYER_VEL_LEFT_X
                if keys[pg.K_RIGHT]:
                    self.vx = PLAYER_VEL_RIGHT_X
        hits_start_plat = pg.sprite.spritecollide(self, self.game.plat_start, False)
        if hits_start_plat:
            # self.vx = 0
            keys = pg.key.get_pressed()
            if keys[pg.K_LEFT]:
                self.vx = PLAYER_VEL_LEFT_X
            if keys[pg.K_RIGHT]:
                self.vx = PLAYER_VEL_RIGHT_X

    def update(self):
        self.get_keys()
        # combined make the gravity
        self.acc = pg.math.Vector2(0, PLAYER_GRAV)
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        # wrap around the screen
        if self.pos.x > SCREEN_WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = SCREEN_WIDTH
        # Makes it so the player rect moves with button press
        self.pos.x += self.vx
        self.rect.midbottom = self.pos


class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, width_plat, height_plat):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((width_plat, height_plat))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.rect.x = x
        self.rect.y = y
