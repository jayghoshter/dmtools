#!/usr/bin/env python3

import xmltodict
from rich import print
from addict import Dict
from fuzzywuzzy import process, fuzz
from subprocess import run
import argparse
import pandas as pd
from pyfzf.pyfzf import FzfPrompt
from random import sample

fzf = FzfPrompt()
pd.set_option('display.max_columns', None)

dic = None
with open('/home/jayghoshter/Repositories/dmtools/DnDAppFiles/Compendiums/Full Compendium.xml', 'r', encoding='utf-8') as fd: 
    xml = fd.read()
    dic = Dict(xmltodict.parse(xml))

FZF_FILE_OPTS =  '--cycle -d ":" --prompt="Hi > " '

# df = pd.DataFrame(dic.to_dict()['compendium']['spell'])
# df = df[df['level'].str.contains("8")]
# df = df[df.classes.str.contains("Wizard")]
# print(df.name.tolist())

# selected = fzf.prompt(df['name'], FZF_FILE_OPTS)[0]
# print(df[df.name == selected])

# text = df[df.name == selected].iloc[0]['text']
# text = [ "\n"  if x is None else x  for x in text ]
# print('\n'.join(text))
#
def get_spells_at_level(cclass:str, level:int, k:int=0):
    df = pd.DataFrame(dic.to_dict()['compendium']['spell'])
    df = df[df['level'].str.contains(str(level))]
    df = df[df.classes.str.contains(cclass)]
    outlist = df.name.tolist()
    if k:
        return sample(outlist, k=k)
    else:
        return outlist

print(get_spells_at_level('Wizard', 0, 3))

