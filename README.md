# DMTools repository

Contains data and tools I use in my dnd sessions as both, a DM and player. Do not expect perfect, production-ready scripts. 

- The submodule DnDAppFiles contains compendiums in XML format created by someone else. The scripts in this repo can be used to access the data in them quickly using fzf.
- roland is another useful tool, the full potential of which is not yet utilized in my scripts. 
- the 'lists' folder contains lists taken from r/d100, and some other websites and is used by roland to generate random names, encounters, items etc.

# Requirements

- [fzf](https://github.com/junegunn/fzf)
- [xq](https://github.com/jeffbr13/xq)
    - xq might also be part of [yq](https://github.com/kislyuk/yq)
    - [jq](https://github.com/stedolan/jq)
- roland (submodule)
    - perl

# Scripts
- denc: dnd encounter manager
    - supply input in csv format: characters,HP
    - denc asks for initiative values
    - and starts combat
- fdfil: apply xq filters on compendiums.
    - for example, list all monsters of .cr == "7" or .size == "G"
- fdnd: generic fuzzy finder applied to the compendium 
    - fdnd <monster | spell | class | race | background | feat>
- fplay: fuzzy searchable character sheet
    - Just uses fzf to find lines in text files
    - ctrl-e edits said lines
    - (It's not perfect, sed command in script doesn't escape special characters)
- froland: fzf + roland
    - generate random things while DMing
- gtrack: gold tracker
    - doesn't support electrum
    - built for 10x multiplier between cp,sp,gp,pp (gold standard)
    - can work for silver standard as well, but rebalancing won't work (yet).
- roll: dice
    - roll <n>d<m> dice; where n = number of dice, m = number of sides
    - doesn't support addition () yet
    - the perl module Games::Dice necessary for roland does support addition, but provides final sum only.
