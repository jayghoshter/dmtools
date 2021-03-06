#!/bin/env python3

# DONE: Add prof to skills
# DONE: Expertise
# DONE: iterfzf proficiencies
# DONE: iterfzf weapons
# DONE: iterfzf armors
# DONE: auto update saves
# DONE: iterfzf multi character selection?
# DONE: MODS for <10
# DONE: Handle expertise in multiclassing.
# DONE: Fix expertise output
# DONE: Show ability score stats during updates (move to character.py)
# DONE: Implement Backgrounds & Proficiencies
# TODO: Fully incorporate fdnd compendium data?
# TODO: Allow escaping from iterfzf prompts without crashing
# TODO: Allow other forms of stat generation
# TODO: Allow read-input of char sheet and level ups

## TODO: true randomness -> os.systemrandom or os.urandom

## TODO: personality, ideals, bonds, flaws, in vipe
## https://stackoverflow.com/questions/12164280/is-pythons-random-randint-statistically-random

from character import Character

def main():
    char = Character()
    char.writenew()

if __name__ == "__main__":
    main()
