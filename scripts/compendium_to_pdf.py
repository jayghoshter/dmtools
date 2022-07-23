#!/usr/bin/env python3
"""
Currently works for features and traits

./compendium_to_pdf.py --class Rogue --level 3 --cumulative --subclass 'Arcane Trickster'

./compendium_to_pdf.py --race 'high elf'
"""

import xmltodict
from rich import print
from addict import Dict
from fuzzywuzzy import process, fuzz
from subprocess import run
import argparse

dic = None
with open('/home/jayghoshter/Repositories/dmtools/DnDAppFiles/Compendiums/Full Compendium.xml', 'r', encoding='utf-8') as fd: 
    xml = fd.read()
    dic = Dict(xmltodict.parse(xml))


# TODO: write this with YAML/dicts
MDHEADER = "---\ndocumentclass: dndbook\nfontfamily: Alegreya\nclassoption:\n- twocolumn\n---\n"

def get_class_features(classname:str, level:int, cumulative:bool, includeoptional:bool = False, optionalSubstring:str = ''): 
    names =  list(map(lambda x: x.name, dic.compendium['class'])) 

    result_match = process.extractOne(classname, names, scorer=fuzz.token_set_ratio, score_cutoff=70)
    
    result = result_match[0] if result_match else ''

    # print(f"Fuzzy found {result}")
    data = list(filter(lambda x: x.name == result, dic.compendium['class']))[0]

    if cumulative: 
        level_info = list(filter(lambda x: int(x['@level']) <= level, data.autolevel))
    else: 
        level_info = list(filter(lambda x: int(x['@level']) == level, data.autolevel))

## Generic class features
    features = Dict() 

    # print(f"{optionalSubstring = }")

    ## WARNING: MONSTROSITY
    for item in level_info:
        if isinstance(item.feature, list):
            for feature in item.feature:
                if includeoptional: 
                    if feature.name:
                        if feature['@optional'] == 'YES': 
                            if optionalSubstring in feature.name: 
                                features.update({feature.name: feature.text})
                        else: 
                            features.update({feature.name: feature.text})
                elif feature['@optional'] != 'YES': 
                    if feature.name:
                        features.update({feature.name: feature.text})
        else:
            if includeoptional: 
                if item.feature.name:
                    if item.feature['@optional'] == 'YES': 
                        if optionalSubstring in item.feature.name:
                            features.update({item.feature.name: item.feature.text})
                    else: 
                        features.update({item.feature.name: item.feature.text})
            elif item.feature['@optional'] != 'YES':
                if item.feature.name:
                    features.update({item.feature.name: item.feature.text})

    return features


def to_markdown(dct: dict): 
    mdstring = ""
    for  k,v in dct.items(): 
        if isinstance(v, list): 
            v = list(filter(None, v))
            v2 = []
            for item in v: 
                if ':' in item and len(item.split(':')[0])<20: 
                    item = f"**{item.split(':')[0]}**: {item.split(':')[1]}"
                elif '=' in item: 
                    item = f"**{item.split('=')[0]}**= {item.split('=')[1]}"
                elif len(item) < 40 and item[0] != '•': 
                    item = '### ' + item
                v2.append(item)
            v = "\n\n".join(v2)
        mdstring = f"{mdstring}## {k}\n\n{v}\n\n"

    return mdstring

def write_to_markdown(title:str, dct: dict, filename:str): 
    mdcontent = to_markdown(dct)

    with open(f'{filename}.md', 'w') as fd: 
        fd.write(MDHEADER)
        fd.write(f"# {title}\n\n")
        fd.write(mdcontent)

    run(['pandoc', f'{filename}.md', '-o',  f'{filename}.pdf'])

def get_race_features(racename:str): 
    names =  list(map(lambda x: x.name, dic.compendium['race'])) 

    result_match = process.extractOne(racename, names, scorer=fuzz.token_set_ratio, score_cutoff=70)
    
    result = result_match[0] if result_match else ''

    print(f"Fuzzy found {result}")
    data = list(filter(lambda x: x.name == result, dic.compendium['race']))[0]

    features = Dict()
    for item in data.trait: 
        features.update({item['name']: item['text']}) 

    return features

def get_background_features(background:str): 
    names =  list(map(lambda x: x.name, dic.compendium['background'])) 

    result_match = process.extractOne(background, names, scorer=fuzz.token_set_ratio, score_cutoff=70)
    
    result = result_match[0] if result_match else ''

    print(f"Fuzzy found {result}")
    data = list(filter(lambda x: x.name == result, dic.compendium['background']))[0]

    features = Dict()
    for item in data.trait: 
        features.update({item['name']: item['text']}) 

    return features

def get_feats(feat:str): 
    names =  list(map(lambda x: x.name, dic.compendium['feat'])) 

    result_match = process.extractOne(feat, names, scorer=fuzz.token_set_ratio, score_cutoff=70)
    
    result = result_match[0] if result_match else ''

    print(f"Fuzzy found {result}")
    data = list(filter(lambda x: x.name == result, dic.compendium['feat']))[0]

    features = Dict()
    features.update({data['name']: data['text']}) 

    return features

def spells2df():
    names =  list(map(lambda x: x.name, dic.compendium['spell'])) 

if __name__ == "__main__": 
    ap = argparse.ArgumentParser()

    ap.add_argument('--class', help='Select a class to dump features about')
    ap.add_argument('--level', type=int, default=1, help='Class level')
    ap.add_argument('--cumulative', action='store_true', help='dump info upto level')
    ap.add_argument('--subclass', default='', help='Subclass name to filter out')

    ap.add_argument('--race', help='Select a race to dump features about')

    ap.add_argument('--background', help='Select a background to dump features about')

    ap.add_argument('--feat', help='Select a feat to dump features about')

    args = vars(ap.parse_args())

    includeoptional = True if args['subclass'] else False
    
    if args['class']: 
        features = get_class_features(args['class'], level=args['level'], cumulative=args['cumulative'], includeoptional=includeoptional, optionalSubstring=args['subclass'])
        write_to_markdown(args['class'], features, f"{args['class']}_features")
    elif args['race']: 
        features = get_race_features(args['race'])
        write_to_markdown(args['race'], features, f"{args['race']}_features")
    elif args['background']: 
        features = get_background_features(args['background'])
        write_to_markdown(args['background'], features, f"{args['background']}_features")
    elif args['feat']: 
        features = get_feats(args['feat'])
        write_to_markdown(args['feat'], features, f"{args['feat']}_features")
    # elif args['spell']:
    #     get_spells(args['spells'])
