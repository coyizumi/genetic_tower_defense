import pygame
from mob import *
import numpy as np
from time import time

def mobs_in_area(pos, rad, moblist):
    x,y = pos
    results = []
    for m in moblist:
        mx,my = m.x,m.y
        if ((mx - x)**2 + (my - y)**2) < rad**2:
            results.append(m)

    return results



class Tower:
    RED = (255,0,0)
    RAD = 10

    NORMAL = 0
    MAGIC = 1
    FIRE = 2

    def __init__(self, location, color):
        self.x, self.y = location.get_center()
        self.c = color
        self.damage = 10
        self.aoe_damage = 0
        self.aoe_range = 0
        self.radius = 100
        self.damage_type = Tower.NORMAL
        self.delay = 500
        self.last_attacked = 0
        print ("created tower")

    def get_target(self, moblist):
        mobs = self.mobs_in_range (moblist)
        if mobs:
            return max(mobs, key=lambda m: m.distance_traveled)
        else: return None

    def attack(self, moblist):
        if pygame.time.get_ticks() - self.last_attacked < self.delay: return
        target = self.get_target(moblist)
        if target == None: return
        self.last_attacked = pygame.time.get_ticks()
        self.deal_damage(target, moblist)

    def deal_damage(self, target, moblist):
        target.color = (0,0,255)
        splash_mobs = mobs_in_area((target.x,target.y), self.aoe_range, moblist)
        if target in splash_mobs: splash_mobs.remove(target)
        self.deal_aoe_damage (splash_mobs)
        target.get_hurt(self.damage, self.damage_type)

    def deal_aoe_damage(self, mobs):
        for m in mobs:
            m.color = (255,0,255)
            m.get_hurt(self.aoe_damage, self.damage_type)

    def draw(self, screen):
        pygame.draw.circle(screen, Tower.RED,(int(self.x),int(self.y)), self.radius, 1)
        pygame.draw.circle(screen, self.c, (int(self.x), int(self.y)), Tower.RAD)

    def mobs_in_range(self, mob_list):
        return mobs_in_area((self.x,self.y), self.radius, mob_list)

class ArrowTower(Tower):
    def __init__(self, location, color):
        Tower.__init__(self,location, color)
        self.x, self.y = location.get_center()
        self.c = (0,0,0)
        self.damage = 8
        self.aoe_range = 0
        self.radius = 90
        self.damage_type = Tower.NORMAL
        self.delay = 500

class BombTower(Tower):
    def __init__(self, location, color):
        Tower.__init__(self,location, color)
        self.x, self.y = location.get_center()
        self.c = (0,255,255)
        self.damage = 5
        self.aoe_damage = 5
        self.aoe_range = 30
        self.radius = 70
        self.damage_type = Tower.NORMAL
        self.delay = 1000

class FireTower(Tower):
    def __init__(self, location, color):
        Tower.__init__(self,location, color)
        self.x, self.y = location.get_center()
        self.c = (255,0,100)
        self.damage = 8
        self.aoe_damage = 5
        self.aoe_range = 0
        self.radius = 90
        self.damage_type = Tower.FIRE
        self.delay = 500