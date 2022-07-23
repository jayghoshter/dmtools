#!/usr/bin/env python3

from random import seed, randint
from rich import print as rprint
from rich.text import Text
import argparse
from functools import partial
import enum

## TODO: Make multiroll return a list instead of printing

class Mode(enum.Enum):
    DISADVANTAGE = -1
    NORMAL = 0
    ADVANTAGE = 1

    @classmethod
    def from_string(cls, string: str) -> 'Mode':
        """Get an enum value from a string, defaulting to NORMAL."""
        encode = {
            'normal': cls.NORMAL,
            'advantage': cls.ADVANTAGE,
            'disadvantage': cls.DISADVANTAGE,
            'adv': cls.ADVANTAGE,
            'dis': cls.DISADVANTAGE,
            'disadv': cls.DISADVANTAGE,
        }
        return encode.get(string.lower(), cls.NORMAL)

def multiroll(string:str, silent:bool=False, mode:Mode=Mode.NORMAL):
    """
    Accepts advanced multiple rolls separated by '|'
        - ad20 | +5 | 1d3
    """

    string = string.split(';')[0]
    results = []
    for index,item in enumerate(string.split('|')):
        text = Text()
        rollstr = item.strip()
        if index == 0:
            if mode == Mode.ADVANTAGE:
                rollstr = 'a' + rollstr
            elif mode == Mode.DISADVANTAGE: 
                rollstr = 'z' + rollstr
        rollval = roll(str(rollstr), silent=silent)
        text.append(rollstr + ": ", style="bold white")
        text.append(str(rollval), style="bold cyan")
        if not silent:
            rprint(text)
        # else:
        #     print(rollval)
        results.append(rollval)
    return results


def roll(string:str, **kwargs):
    """
    Accepts advanced single rolls:
        - 1d5 + 10
        - ad20
        - 10d50/3
        - +5 (Rolls d20+5)
    """
    _silent = kwargs.get('silent', False)
    roller = partial(roll, silent=_silent)
    roller_nds = partial(roll_nds, silent=_silent)

    if(string[0] == 'a'):
        if not _silent:
            rprint(Text("Rolling with Advantage!", style="bold blue"))
        r1 = roller(string[1:])
        r2 = roller(string[1:])
        return [max(r1, r2), (r1,r2)]
    elif(string[0] == 'z'):
        if not _silent:
            rprint(Text("Rolling with Disadvantage!", style="bold blue"))
        r1 = roller(string[1:])
        r2 = roller(string[1:])
        # return min(r1, r2)
        return [min(r1, r2), (r1,r2)]
    elif ';' in string:
        # Everything after ; is a comment.
        splitstring=string.split(';')
        return roller(splitstring[0])
    elif string.strip() == '':
        return 0
    elif string.strip()[0] == '+':
        return roller('1d20' + string.strip())
    elif string.strip()[0] == '-':
        return roller('1d20' + string.strip())
    elif '+' in string:
        rollsum = 0
        splitstring = string.split('+')
        for item in splitstring:
            rollsum = rollsum + roller(item.strip())
        return rollsum
    elif '/' in string:
        splitstring = string.split('/')
        return roller(splitstring[0])/roller(splitstring[1])
    elif '*' in string:
        splitstring = string.split('*')
        return roller(splitstring[0])*roller(splitstring[1])
    elif '-' in string:
        splitstring = string.split('-')
        return roller(splitstring[0]) - roller(splitstring[1])
    else:
        return roller_nds(string)

def roll_nds(string:str, **kwargs):
    """
    Accepts single simple rollstring:
        - 10d20
        - 1d10
        - (num)d(sides)
    """
    seed(a=None, version=2)
    if 'd' in string:
        try:
            n = int(string.split('d')[0])
        except:
            n = 1
        s = int(string.split('d')[1])
        rolls = [ randint(1,s) for _ in range(n)]
        maxrolls = [s for _ in range(n)]

        # NOTE: Only applies on multiple dice when EVERY hit is critical.
        # But since advantage and disadvantage are rolled as two separate dice
        # we can see crits and fumbles on ad20 and zd20, just not on 5d20
        # TODO: Make this work per individual roll?
        if not kwargs.get('silent', False):
            if (maxrolls == rolls):
                rprint(Text("CRITICAL ROLL!", style="bold yellow"))
            elif (rolls == [1]*n):
                rprint(Text("FUMBLED ROLL!", style="bold red"))

        return (sum(rolls))
    else:
        try:
            return int(string)
        except:
            return 0

if __name__ == "__main__":

    ap = argparse.ArgumentParser()
    ap.add_argument("-s", "--silent", action='store_true', default=False, help="Only print output.")
    ap.add_argument("-d", "--debug", action='store_true', default=False, help="Print args for debug")
    ap.add_argument("input", nargs='*', help="input data")
    args = vars(ap.parse_args())

    if args['debug']:
        print(args)

    multiroll(''.join(args['input']), silent=args['silent'])
