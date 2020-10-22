#!/bin/env python3

from general import class_hitdice
from iterfzf import iterfzf
from rich.console import Console
from roll import roll

import sys

class Class:
    def __init__(self, className = ''):

        self.hd = 0
        self.proficiencies = []
        self.expertise = []
        self.saves = []
        self.armor_proficiencies = []
        self.weapon_proficiencies = []
        self.tool_proficiencies = []
        self.stats = {
                'Strength'    : 0,
                'Dexterity'   : 0,
                'Constitution': 0,
                'Intelligence': 0,
                'Wisdom'      : 0,
                'Charisma'    : 0  }

        # self.hd=class_hitdice[self.className]

        if className == '':
            self.className = iterfzf(class_hitdice)
        else:
            self.className = className

        self.addClassData()

        self.level = ''
        while self.level == '':
            self.level = console.input("[bold yellow]" + self.className + " Level: [/]")
        self.level = int(self.level)

        self.asi = [ 4, 8, 12, 16, 19]
        if self.className == 'Fighter':
            self.asi = [4, 6, 8, 12, 14, 16, 19]

        self.proficiency_bonus = int((self.level - 1)/4) + 2
        self.spells = self.getSpells()

        # HP = HD + CON + (1dHD + CON)*(LEVEL-1)
    def calcHP(self, CON):
        HP = roll(str(self.level-1) + 'd' + str(self.hd) + '+' + str((self.level)*CON + self.hd))
        return HP

    def addClassData(self):
        filename = 'class.info'
        with open(filename, mode='r') as infile:
            for line in infile:
                linearr = line.split(';')
                if (self.className.strip() in linearr[0].strip()):
                    self.hd                   = int(linearr[1])
                    self.proficiencies        = [ x.strip() for x in linearr[2].split(',') if x.strip() not in self.stats.keys() ]
                    self.expertise            = [ x.strip() for x in linearr[2].split(',') if x.strip() not in self.stats.keys() ]
                    self.saves                = [ x.strip() for x in linearr[2].split(',') if x.strip() in self.stats.keys() ]
                    self.armor_proficiencies  = [ x.strip() for x in linearr[3].split(',')]
                    self.weapon_proficiencies = [ x.strip() for x in linearr[4].split(',')]
                    self.tool_proficiencies   = [ x.strip() for x in linearr[5].split(',')]

    def getSpells(self):
        try:
            print("Getting Spells... from file " + 'spells/' + self.className)
            spellfile     = open('spells/' + self.className)
            print("SUCCESS")
            spells        = spellfile.readlines()
            spellfile.close()
            spellsdict = { item.split(',')[0].strip(): item.split(',')[1].strip() for item in spells}
            out           = iterfzf(spellsdict, multi=True) or []
            return out
        except:
            return []

console = Console()
