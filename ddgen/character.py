#!/bin/env python3

from rich.console import Console
from roll import roll
from classes import Class
from iterfzf import iterfzf
from general import racial_stat_bonus, finesse, ranged, weapons, class_saves, class_hitdice, armors, modsmap, backgrounds
import json

import sys

reroll_threshold = 70

class Character:

    def __init__(self):

        self.name = ''
        while self.name == '':
            self.name = console.input("[bold yellow]Character Name: [/]")

        self.race = iterfzf(racial_stat_bonus)

        self.stats = {
                'Strength'    : 0,
                'Dexterity'   : 0,
                'Constitution': 0,
                'Intelligence': 0,
                'Wisdom'      : 0,
                'Charisma'    : 0  }

        self.stats.update(self.genStats())


        self.classes_list_names = iterfzf(class_hitdice, multi=True)
        self.classes_list = [ Class(name) for name in self.classes_list_names ]

        self.proficiency_bonus = 0
        self.HP = 0
        self.level = 0
        self.proficiencies = []
        self.expertise = []
        self.saves = []
        self.armor_proficiencies = []
        self.weapon_proficiencies = []
        self.tool_proficiencies = []
        self.spells = []
        self.background = ''
        self.DATA={}


        for classitem in self.classes_list:

            for item in classitem.asi:
                if classitem.level >= item:
                    self.asi_update()

            self.level = self.level + classitem.level
            self.proficiencies.extend(classitem.proficiencies)
            self.expertise.extend(classitem.expertise)
            self.saves.extend(classitem.saves)
            self.armor_proficiencies.extend(classitem.armor_proficiencies)
            self.weapon_proficiencies.extend(classitem.weapon_proficiencies)
            self.tool_proficiencies.extend(classitem.tool_proficiencies)
            self.spells.extend(classitem.spells)


        self.proficiency_bonus = int((self.level - 1)/4) + 2

        self.proficiencies        = list(set(self.proficiencies))
        self.expertise            = list(set(self.expertise))
        self.saves                = list(set(self.saves))
        self.armor_proficiencies  = list(set(classitem.armor_proficiencies))
        self.weapon_proficiencies = list(set(classitem.weapon_proficiencies))
        self.tool_proficiencies   = list(set(classitem.tool_proficiencies))
        self.spells               = list(set(classitem.spells))


        self.background = iterfzf(backgrounds)

        ## Select Proficiencies from list of allowable skills
        self.proficiencies = iterfzf(self.proficiencies, multi=True, prompt="Background (" + self.background + "): "  + backgrounds[self.background] + ' ') or []
        self.proficiencies.extend([ x.strip() for x in backgrounds[self.background].split(',') ])
        self.proficiencies = list(set(self.proficiencies))
        print("Proficiencies:", self.proficiencies)

        if any( x in self.classes_list_names for x in  ['Rogue', 'Bard'] ):
            self.expertise = iterfzf(self.expertise, multi=True, prompt='> Select Expertise: ') or []
            print("Expertise:", self.expertise)
        else:
            self.expertise = []


        print("STATS: ", [self.stats[key] for key in self.stats])

        self.mods = {x:modsmap[self.stats[x]] for x in self.stats.keys()}

        print("MODS: ", [self.mods[key] for key in self.mods])
        self.HP = sum([ item.calcHP(self.mods['Constitution']) for item in self.classes_list])

        self.AC = 10
        self.weapons = iterfzf(weapons, multi=True, prompt='> '+', '.join(self.weapon_proficiencies)) or []
        self.armors = iterfzf(armors, prompt='> '+', '.join(self.armor_proficiencies)) or []

        self.skills = {
                'Acrobatics'     : self.mods['Dexterity'],
                'Animal Handling': self.mods['Wisdom'],
                'Arcana'         : self.mods['Intelligence'],
                'Athletics'      : self.mods['Strength'],
                'Deception'      : self.mods['Charisma'],
                'History'        : self.mods['Intelligence'],
                'Insight'        : self.mods['Wisdom'],
                'Intimidation'   : self.mods['Charisma'],
                'Investigation'  : self.mods['Intelligence'],
                'Medicine'       : self.mods['Wisdom'],
                'Nature'         : self.mods['Intelligence'],
                'Perception'     : self.mods['Wisdom'],
                'Performance'    : self.mods['Charisma'],
                'Persuasion'     : self.mods['Charisma'],
                'Religion'       : self.mods['Intelligence'],
                'Sleight of Hand': self.mods['Dexterity'],
                'Stealth'        : self.mods['Dexterity'],
                'Survival'       : self.mods['Wisdom'],
        }

        self.skills.update({x:self.skills[x]+self.proficiency_bonus for x in self.skills.keys() if x in self.proficiencies})
        self.skills.update({x:self.skills[x]+self.proficiency_bonus for x in self.skills.keys() if x in self.expertise})


    def rollStats(self):
        statd = {}
        for key in self.stats:
            rolls = []
            for i in range(4):
                rolls.append(roll('d6'))
            rolls = sorted(rolls, reverse=True)[:-1]
            statd[key] = sum(rolls)
            if key in racial_stat_bonus[self.race]:
                statd[key] = statd[key] + racial_stat_bonus[self.race][key]
        return statd

    def genStats(self):
        total = 0
        while total <= reroll_threshold:
            statd = self.rollStats()
            total = sum([ statd[stat] for stat in statd])
        console.print("[yellow bold]Stats after Racial Bonus: [/]", [statd[key] for key in statd])
        # print("STATS: ", [statd[key] for key in statd])
        console.print("[bold yellow]Total: [/]", total)
        prompt = console.input("[bold red]Change Stats? (y/any)[/]")
        if prompt == 'y':
            for key in statd:
                statd[key] = int(console.input("[bold yellow]" + key + ": [/]"))
        return statd

    def asi_update(self):
        statslist = [ self.stats[x] for x in self.stats.keys()]
        asi_stats = iterfzf(self.stats, multi=True, prompt = str(statslist))
        try:
            if (len(asi_stats)) == 1:
                self.stats[asi_stats[0]] = self.stats[asi_stats[0]] + 2
            elif (len(asi_stats)) == 2:
                self.stats[asi_stats[0]] = self.stats[asi_stats[0]] + 1
                self.stats[asi_stats[1]] = self.stats[asi_stats[1]] + 1
        except:
            pass

    def importChar(self):
        ## From a level up standpoint, for stat upgrades, the core of a character are as follows
        ##      - Stats, Classes/Levels --> Proficiency Bonus, Proficiencies, Expertise, Weapons, Spells
        with open(self.name, 'r') as json_file:
            self.DATA = json.load(json_file)
        print(self.DATA)

    def compile(self):
        self.DATA['name'] = self.name
        self.DATA['race'] = self.race
        ## TODO: Make it class/level = Class N, Class M, ....
        self.DATA['class'] = ', '.join([item.className for item in self.classes_list])
        self.DATA['HP'] = str(self.HP)
        self.DATA['AC'] = str(self.AC)
        self.DATA['armor'] = armors[self.armors]
        self.DATA['initiative'] = '{:+d}'.format(self.mods['Dexterity'])
        self.DATA['proficiencies'] = ', '.join(self.saves + self.proficiencies)
        if any( x in self.classes_list_names for x in  ['Rogue', 'Bard'] ):
            self.DATA['expertise'] = ', '.join(self.expertise)
        self.DATA['proficiency bonus'] = '{:+d}'.format(self.proficiency_bonus)
        self.DATA['stats'] = ' | '.join([str(self.stats[key]) for key in self.stats.keys()])
        for key in self.mods:
            self.DATA[key[:3].upper() + ' modifier'] = '{:+d}'.format(self.mods[key])
        for key in self.skills:
            self.DATA[key] = '{:+d}'.format(self.skills[key])
        for item in self.weapons:
            if item in finesse:
                bonus = max(self.mods['Strength'], self.mods['Dexterity'])
            elif item in ranged:
                bonus = self.mods['Dexterity']
            else:
                bonus = self.mods['Strength']
            self.DATA['- Weapon ' + item] = '{:+d}'.format(bonus + self.proficiency_bonus) + '|' + weapons[item] + '+' + str(bonus)
        for iclass in self.classes_list:
            if iclass.className == 'Rogue':
                self.DATA['Sneak Attack Damage'] = str(int((iclass.level + 1)/2)) + 'd6'
        for item in self.spells:
            self.DATA['- Spell ' + item] = ''
        for item in self.mods.keys():
            if item in self.saves:
                self.DATA[item[:3].upper() + ' save'] = '{:+d}'.format(self.mods[item] + self.proficiency_bonus)
            else:
                self.DATA[item[:3].upper() + ' save'] = '{:+d}'.format(self.mods[item])

    def writenew(self):
        self.compile()
        with open(self.name, 'w') as json_file:
            json.dump(self.DATA, json_file, indent=4)

    # def write(self):
    #     with open(self.name, 'w') as fp:
    #         fp.write('name: ' + self.name + '\n')
    #         fp.write('race: ' + str(self.race) + '\n')
    #         fp.write('class: ' + ', '.join([item.className for item in self.classes_list]) + '\n')
    #         # fp.write('level: ' + str(self.level) + '\n')
    #         fp.write('hit points: ' + str(self.HP) + '\n')
    #         fp.write('armor class: ' + str(self.AC) + '\n')
    #         fp.write('armor: ' + armors[self.armors] + '\n')
    #         fp.write('initiative: ' + '{:+d}\n'.format(self.mods['Dexterity']))
    #         fp.write('proficiencies: ' + ', '.join(self.saves + self.proficiencies) + '\n')
    #         fp.write('expertise: ' + ', '.join(self.expertise) + '\n')
    #         fp.write('proficiency bonus: ' + '{:+d}\n'.format(self.proficiency_bonus))
    #         # for key in self.stats:
    #         #     fp.write(key + ' score' + ': ' + '{:d}\n'.format(self.stats[key]))
    #         fp.write('stats: ' + ' | '.join([str(self.stats[key]) for key in self.stats.keys()]) + '\n')
    #         for key in self.mods:
    #             fp.write(key + ' modifier' + ': ' + '{:+d}\n'.format(self.mods[key]))
    #         for key in self.skills:
    #             fp.write(key + ': ' + '{:+d}\n'.format(self.skills[key]))
    #         for item in self.weapons:
    #             if item in finesse:
    #                 bonus = max(self.mods['Strength'], self.mods['Dexterity'])
    #             elif item in ranged:
    #                 bonus = self.mods['Dexterity']
    #             else:
    #                 bonus = self.mods['Strength']
    #             fp.write('- Weapon ' + item + ': ' + '{:+d}'.format(bonus + self.proficiency_bonus) + '|' + weapons[item] + '+' + str(bonus) + '\n')
    #         # if self.Class == "Rogue":
    #         #     fp.write('Sneak Attack Damage: ' + str(int((self.level + 1)/2)) + 'd6' + '\n')
    #         for iclass in self.classes_list:
    #             if iclass.className == 'Rogue':
    #                 fp.write('Sneak Attack Damage: ' + str(int((iclass.level + 1)/2)) + 'd6' + '\n')
    #         for item in self.spells:
    #             fp.write('- Spell ' + item + ': ' + '\n')
    #         for item in self.mods.keys():
    #             if item in self.saves:
    #                 fp.write(item + ' save: ' +'{:+d}\n'.format(self.mods[item] + self.proficiency_bonus))
    #             else:
    #                 fp.write(item + ' save: ' +'{:+d}\n'.format(self.mods[item]))


console = Console()

