#!/bin/env python3

from general import class_hitdice
from iterfzf import iterfzf
from rich.console import Console
from roll import roll
from pathlib import Path

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

    # def addClassData(self):
    #     # filename = Path(__file__).parent / 'class.info'
    #     # filename = 'class.info'
    #     with open(filename, mode='r') as infile:
    #         for line in infile:
    #             linearr = line.split(';')
    #             if (self.className.strip() in linearr[0].strip()):
    #                 self.hd                   = int(linearr[1])
    #                 self.proficiencies        = [ x.strip() for x in linearr[2].split(',') if x.strip() not in self.stats.keys() ]
    #                 self.expertise            = [ x.strip() for x in linearr[2].split(',') if x.strip() not in self.stats.keys() ]
    #                 self.saves                = [ x.strip() for x in linearr[2].split(',') if x.strip() in self.stats.keys() ]
    #                 self.armor_proficiencies  = [ x.strip() for x in linearr[3].split(',')]
    #                 self.weapon_proficiencies = [ x.strip() for x in linearr[4].split(',')]
    #                 self.tool_proficiencies   = [ x.strip() for x in linearr[5].split(',')]

    def addClassData(self):
        for classItem in classInfo:
            if self.className.strip() in classItem:
                self.hd                   = int(classInfo[classItem][0])
                self.proficiencies        = [ x.strip() for x in classInfo[classItem][1].split(',') if x.strip() not in self.stats.keys() ]
                self.expertise            = [ x.strip() for x in classInfo[classItem][1].split(',') if x.strip() not in self.stats.keys() ]
                self.saves                = [ x.strip() for x in classInfo[classItem][1].split(',') if x.strip() in self.stats.keys() ]
                self.armor_proficiencies  = [ x.strip() for x in classInfo[classItem][2].split(',')]
                self.weapon_proficiencies = [ x.strip() for x in classInfo[classItem][3].split(',')]
                self.tool_proficiencies   = [ x.strip() for x in classInfo[classItem][4].split(',')]



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

classInfo = {
        "Artificer (UA)": [ "8", "Constitution, Intelligence, Arcana, History, Investigation, Medicine, Nature, Perception, Sleight of Hand", "light armor, medium armor, shields", "simple weapons, hand crossbows, heavy crossbows", "Thieves' tools, tinker's tools, one type of artisan's tools of your choice", "5d4x10" ],
        "Barbarian": [ "12", "Strength, Constitution, Animal Handling, Athletics, Intimidation, Nature, Perception, Survival", "light armor, medium armor, shields", "simple weapons, martial weapons", "none", "2d4x10" ],
        "Bard": [ "8", "Dexterity, Charisma", "light armor", "simple weapons, hand crossbows, longswords, rapiers, shortswords", "three musical instruments of your choice", "5d4x10" ],
        "Cleric": [ "8", "Wisdom, Charisma, History, Insight, Medicine, Persuasion, Religion", "light armor, medium armor, shields", "simple weapons", "none", "5d4x10" ],
        "Druid": [ "8", "Intelligence, Wisdom, Arcana, Animal Handling, Insight, Medicine, Nature, Perception, Religion, Survival", "light armor, medium armor, shields (druids will not wear armor or use shields made of metal)", "clubs, daggers, darts, javelins, maces, quarterstaffs, scimitars, sickles, slings, spears", "herbalism kit", "2d4x10" ],
        "Fighter": [ "10", "Strength, Constitution, Acrobatics, Animal Handling, Athletics, History, Insight, Intimidation, Perception, Survival", "light armor, medium armor, heavy armor, shields", "simple weapons, martial weapons", "none", "5d4x10" ],
        "Monk": [ "8", "Strength, Dexterity, Acrobatics, Athletics, History, Insight, Religion, Stealth", "none", "simple weapons, shortswords", "any one type of artisan's tools or any one musical instrument of your choice", "5d4" ],
        "Mystic (UA)": [ "8", "Intelligence, Wisdom, Arcana, History, Insight, Medicine, Nature, Perception, Religion", "light armor", "simple weapons", "none", "5d4x10" ],
        "Paladin": [ "10", "Wisdom, Charisma, Athletics, Insight, Intimidation, Medicine, Persuasion, Religion", "light armor, medium armor, heavy armor, shields", "simple weapons, martial weapons", "none", "5d4x10" ],
        "Ranger (Revised) (UA)": [ "10", "Strength, Dexterity, Animal Handling, Athletics, Insight, Investigation, Nature, Perception, Stealth, Survival", "light armor, medium armor, shields", "simple weapons, martial weapons", "none", "5d10x4" ],
        "Ranger": [ "10", "Strength, Dexterity, Animal Handling, Athletics, Insight, Investigation, Nature, Perception, Stealth, Survival", "light armor, medium armor, shields", "simple weapons, martial weapons", "none", "5d4x10" ],
        "Rogue": [ "8", "Dexterity, Intelligence, Acrobatics, Athletics, Deception, Insight, Intimidation, Investigation, Perception, Performance, Persuasion, Sleight of Hand, Stealth", "light armor", "simple weapons, hand crossbows, longswords, rapiers, shortswords", "thieves' tools", "4d4x10" ],
        "Sorcerer": [ "6", "Constitution, Charisma, Arcana, Deception, Insight, Intimidation, Persuasion, Religion", "none", "daggers, darts, slings, quarterstaffs, light crossbows", "none", "3d4x10" ],
        "Warlock": [ "8", "Wisdom, Charisma, Arcana, Deception, History, Intimidation, Investigation, Nature, Religion", "light armor", "simple weapons", "none", "4d4x10" ],
        "Wizard": [ "6", "Intelligence, Wisdom, Arcana, History, Insight, Investigation, Medicine, Religion", "none", "daggers, darts, slings, quarterstaffs, light crossbows", "none", "4d4x10" ]
        }
