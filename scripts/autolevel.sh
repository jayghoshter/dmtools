#!/bin/bash

## TODO: Remove nulls from arrays
## TODO: Even more readable output
## TODO: argparse printlevel or printupto
## TODO: Separate Traits and Features

# xq -r --arg l "$level" '.compendium.class[] | select(.name == "Rogue") |.autolevel[] | select(."@level" == $l) |[.feature | if type=="array" then . else [.] end | .[].name]  ' Full\ Compendium.xml

scriptDir=$(dirname -- "$(readlink -f -- "$BASH_SOURCE")")
file="../DnDAppFiles/Compendiums/Full Compendium.xml"
LIST="$scriptDir/$file"

printLevel()
{
    class="$1"
    level="$2"
    LEVELDATA=$(xq -r --arg l "$level" --arg c "$class" '.compendium.class[] | select(.name == $c) |.autolevel[] | select(."@level" == $l) ' "$LIST")
    LEVELNUM=$(echo "$LEVELDATA" | jq -r '."@level"')
    LEVELFEATNAMES=$(echo "$LEVELDATA" | jq -r '.feature | if type=="array" then . else [.] end | .[].name')
    LEVELFEATTEXT=$(echo "$LEVELDATA" | jq -r '.feature | if type=="array" then . else [.] end | .[] | [.name, (.text | if type=="array" then . else [.] end | join("//"))]' | tr '//' '\n')

    echo 
    echo "---------------------"
    echo "====== $level ======="
    echo "---------------------"
    echo "$LEVELFEATTEXT"

}

printUptoLevel()
{
    START=1
    END=$2
    for (( c=$START; c<=$END; c++ ))
    do
        printLevel "$1" $c
    done
}

# printLevel "$1" "$2"
# printUptoLevel "$1" "$2"

MODE="SINGLE"

POSITIONAL=()
while [[ $# -gt 0 ]]
do
    key="$1"

    case $key in
        -u|--upto)
            MODE="UPTO"
            shift # past value
            ;;
        *)    # unknown option
            POSITIONAL+=("$1") # save it in an array for later
            shift # past argument
            ;;
    esac
done
set -- "${POSITIONAL[@]}" # restore positional parameters

[ $MODE == "UPTO" ] && printUptoLevel "$1" "$2" || printLevel "$1" "$2"
