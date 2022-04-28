#!/bin/env python3

class_hitdice = {
    'Barbarian': 12,
    'Bard': 8,
    'Cleric': 8,
    'Druid': 8,
    'Fighter': 10,
    'Monk': 8,
    'Paladin': 10,
    'Ranger': 10,
    'Rogue': 8,
    'Sorcerer': 6,
    'Warlock': 8,
    'Wizard': 6
}

class_saves = {
    'Barbarian': ['Strength', 'Constitution'],
    'Bard': ['Dexterity', 'Charisma'],
    'Cleric': ['Wisdom', 'Charisma'],
    'Druid': ['Intelligence', 'Wisdom'],
    'Fighter': ['Strength', 'Constitution'],
    'Monk': ['Strength', 'Dexterity'],
    'Paladin': ['Wisdom', 'Charisma'],
    'Ranger': ['Strength', 'Dexterity'],
    'Rogue': ['Dexterity', 'Intelligence'],
    'Sorcerer': ['Constitution', 'Charisma'],
    'Warlock': ['Wisdom', 'Charisma'],
    'Wizard': ['Intelligence', 'Wisdom']
}

racial_stat_bonus = {
        "human": {
            'Strength'    : 1,
            'Dexterity'   : 1,
            'Constitution': 1,
            'Intelligence': 1,
            'Wisdom'      : 1,
            'Charisma'    : 1
        },
        "hill dwarf": {
            'Constitution': 2,
            'Wisdom': 1
        },
        "mountain dwarf": {
            'Constitution': 2,
            'Strength': 2
        },
        "high elf": {
            'Dexterity': 2,
            'Intelligence': 1
        },
        "wood elf": {
            'Dexterity': 2,
            'Wisdom': 1
        },
        "dark elf": {
            'Dexterity': 2,
            'Charisma': 1
        },
        "lightfoot halfling":{
            'Dexterity': 2,
            'Charisma': 1
        },
        "stout halfling":{
            'Dexterity': 2,
            'Constitution': 1
        },
        "dragonborn": {
            'Strength': 2,
            'Charisma': 1
        },
        "forest gnome": {
            'Intelligence': 2,
            'Dexterity': 1
        },
        "rock gnome": {
            'Intelligence': 2,
            'Constitution': 1
        },
        "half-elf": {
            'Charisma': 2,
            #additional choice increase
        },
        "half-orc": {
            'Strength': 2,
            'Constitution': 1
        },
        "tiefling": {
            'Intelligence': 1,
            'Charisma': 2
        },
        "None": {
        }

}

weapons = {
        'Club'           : '1d4' ,
        'Dagger'         : '1d4' ,
        'Greatclub'      : '1d8' ,
        'Handaxe'        : '1d6' ,
        'Javelin'        : '1d6' ,
        'Light hammer'   : '1d4' ,
        'Mace'           : '1d6' ,
        'Quarterstaff'   : '1d6' ,
        'Sickle'         : '1d4' ,
        'Spear'          : '1d6' ,
        'Crossbow light' : '1d8' ,
        'Dart'           : '1d4' ,
        'Shortbow'       : '1d6' ,
        'Sling'          : '1d4' ,
        'Battleaxe'      : '1d8' ,
        'Flail'          : '1d8' ,
        'Glaive'         : '1d10',
        'Greataxe'       : '1d12',
        'Greatsword'     : '2d6' ,
        'Halberd'        : '1d10',
        'Lance'          : '1d12',
        'Longsword'      : '1d8' ,
        'Maul'           : '2d6' ,
        'Morningstar'    : '1d8' ,
        'Pike'           : '1d10',
        'Rapier'         : '1d8' ,
        'Scimitar'       : '1d6' ,
        'Shortsword'     : '1d6' ,
        'Trident'        : '1d6' ,
        'War pick'       : '1d8' ,
        'Warhammer'      : '1d8' ,
        'Whip'           : '1d4' ,
        'Blowgun'        : '1'   ,
        'Crossbow hand'  : '1d6' ,
        'Crossbow heavy' : '1d10',
        'Longbow'        : '1d8' ,
        'Net'            : '0'
        }

finesse = [ 'Dagger', 'Dart', 'Rapier', 'Scimitar', 'Shortsword', 'Whip']
ranged = ['Shortbow', 'Crossbow light', 'Longbow', 'Crossbow hand', 'Crossbow heavy', 'Dart', 'Sling', 'Blowgun', 'Net']

armors = {
        "Padded"          : "11 + Dex modifier",
        "Leather"         : "11 + Dex modifier",
        "Studded leather" : "12 + Dex modifier",
        "Hide"            : "12 + Dex modifier (max 2)",
        "Chain shirt"     : "13 + Dex modifier (max 2)",
        "Scale mail"      : "14 + Dex modifier (max 2)",
        "Breastplate"     : "14 + Dex modifier (max 2)",
        "Half plate"      : "15 + Dex modifier (max 2)",
        "Ring mail"       : "14",
        "Chain mail"      : "16",
        "Splint"          : "17",
        "Plate"           : "18",
        "None"            : "10 + Dex modifier"
        }

modsmap = {
        1: -5,
        2: -4,
        3: -4,
        4: -3,
        5: -3,
        6: -2,
        7: -2,
        8: -1,
        9: -1,
        10: 0,
        11: 0,
        12: 1,
        13: 1,
        14: 2,
        15: 2,
        16: 3,
        17: 3,
        18: 4,
        19: 4,
        20: 5
}

backgrounds = {

"Acolyte": "Insight, Religion",
"Caravan Specialist": "Animal Handling, Survival",
"Charlatan": "Deception, Sleight of Hand",
"City Watch": "Athletics, Insight",
"Clan Crafter": "History, Insight",
"Cormanthor Refugee": "Nature, Survival",
"Courtier": "Insight, Persuasion",
"Criminal": "Deception, Stealth",
"Earthspur Miner": "Athletics, Survival",
"Entertainer": "Acrobatics, Performance",
"Far Traveler": "Insight, Perception",
"Fisher": "History. Survival",
"Folk Hero": "Animal Handling, Survival",
"Gate Urchin": "Athletics, Survival",
"Guild Artisan": "Insight, Persuasion",
"Harborfolk": "Athletics, Sleight of Hand",
"Hermit": "Medicine, Religion",
"Hillsfar Merchant": "Insight, Persuasion",
"Hillsfar Smuggler": "Perception, Stealth",
"Investigator": "Insight, Investigation",
"Marine": "Athletics, Survival",
"Mercenary Veteran": "Athletics, Persuasion",
"Mulmaster Aristocrat": "Deception, Performance",
"Noble": "History, Persuasion",
"Outlander": "Athletics, Survival",
"Phlan Refugee": "Insight, Athletics",
"Sage": "Arcana, History",
"Sailor": "Athletics, Perception",
"Secret Identity": "Deception, Stealth",
"Shade Fanatic": "Deception, Intimidation",
"Shipwright": "History, Perception",
"Smuggler": "Athletics, Deception",
"Soldier": "Athletics, Intimidation",
"Trade Sherrif": "Investigation, Persuasion",
"Urchin": "Sleight of Hand, Stealth",
"Uthgardt Tribe Member": "Athletics, Survival",
"Waterdhavian Noble": "History, Persuasion"

}

alignments = [
        'Lawful Good',
        'Lawful Neutral',
        'Lawful Evil',
        'Neutral Good',
        'True Neutral',
        'Neutral Evil',
        'Chaotic Good',
        'Chaotic Neutral',
        'Chaotic Evil'
        ]


# class General:
#     def __init__(self):
#         self.skills = {
#                 'acrobatics'     : 0,
#                 'animal handling': 0,
#                 'arcana'         : 0,
#                 'athletics'      : 0,
#                 'deception'      : 0,
#                 'history'        : 0,
#                 'insight'        : 0,
#                 'intimidation'   : 0,
#                 'investigation'  : 0,
#                 'medicine'       : 0,
#                 'nature'         : 0,
#                 'perception'     : 0,
#                 'performance'    : 0,
#                 'persuasion'     : 0,
#                 'religion'       : 0,
#                 'sleight of hand': 0,
#                 'stealth'        : 0,
#                 'survival'       : 0
#                 }
