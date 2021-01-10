#!/usr/bin/env python
#
# PEP8 -E501
#

import os
import sys
import random
import argparse
from shutil import copyfile
from typing import Dict, List, Optional, NewType

RUNNINGDIR:str = os.path.dirname(os.path.realpath(__file__))

SHUFFLE:bool = True
UNSHUFFLE:bool = False

ShuffleSeed = NewType('ShuffleSeed', Dict[int, int])
UnshuffleSeed = NewType('UnshuffleSeed', Dict[int, int])

# Read file
def readFile(filename: str) -> List[str]:
    with open(filename) as f:
        lines = f.readlines()

    return lines


# Write file
def writeFile(filename: str, lines: List[str]) -> None:
    with open(filename, 'w') as f:
        f.writelines(lines)


# Generate Seed list
def generateSeedKeys(nbkeys: int) -> List[int]:
    suffleid = list(range(nbkeys))
    random.shuffle(suffleid)

    return suffleid


# Get Suffle keys
def getSuffleKeys(nbkeys: int) -> ShuffleSeed:
    suffleid = generateSeedKeys(nbkeys)
    keys = ShuffleSeed(dict(zip(range(nbkeys), suffleid)))

    return keys


# Get Suffle vector keys
def getUnsuffleKeys(nbkeys: int) -> UnshuffleSeed:
    suffleid = generateSeedKeys(nbkeys)
    keys = UnshuffleSeed(dict(zip(suffleid, range(size))))

    return keys


def getCreditLines(args: List[str]) -> List[str]:
    # Init credit
    options = list(args)
    indexoption = -1
    if '-p' in options:
        indexoption = options.index('-p')
    elif '--password' in options:
        indexoption = options.index('--password')

    if indexoption >= 0:
        options[indexoption + 1] = "[MASKED]"

    cmd_options = " ".join(options)
    credit_line1 = f"# Shuffle with mandoline {VERSION} => https://github.com/badele/mandoline\n"  # nopep8
    credit_line2 = f"# Command options: {cmd_options}\n"

    return [credit_line1, credit_line2]


# Shufflet/Unshuffle lines
def suffleLines(password: str, items, mode: bool, column: bool = False):
    SEPARATOR: str = " "
    linesshuffled: List[str] = []

    if mode:
        random.seed(f"{password}", version=2)
        shufflekeys: ShuffleSeed = getSuffleKeys(len(items))
        for idx in range(len(items)):
            linesshuffled.append(items[shufflekeys[idx]])

        if column:
            for lineidx, line in enumerate(linesshuffled):
                random.seed(f"{password}-{lineidx}", version=2)
                words = line.replace("\n", "").split(SEPARATOR)
                shufflekeys = getSuffleKeys(len(words))

                wordsshuffle = []
                for wordidx in range(len(words)):
                    wordsshuffle.append(words[shufflekeys[wordidx]])

                linesshuffled[lineidx] = f'{SEPARATOR.join(wordsshuffle)}\n'
    else:
        # Unshuffle
        if column:
            for lineidx, line in enumerate(items):
                random.seed(f"{password}-{lineidx}", version=2)
                words = line.replace("\n", "").split(SEPARATOR)
                unshufflekeys: UnshuffleSeed = getUnsuffleKeys(len(words))

                wordsshuffle = []
                for wordidx in range(len(words)):
                    wordsshuffle.append(words[unshufflekeys[wordidx]])

                items[lineidx] = f'{SEPARATOR.join(wordsshuffle)}\n'

        random.seed(f"{password}", version=2)
        unshufflekeys = getUnsuffleKeys(len(items))

        for idx in range(len(items)):
            linesshuffled.append(items[unshufflekeys[idx]])

    return linesshuffled

if __name__ == "__main__":
    VERSION = readFile(f"{RUNNINGDIR}/VERSION")[0].strip()

    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", type=str, help="file to suffle")
    parser.add_argument("-l", "--list", type=str, help="file list")
    parser.add_argument("-p", "--password", type=str,
                        help="Suffle password", required=True)
    parser.add_argument("-c", "--column", action='store_true',
                        help="Suffle columns")
    args = vars(parser.parse_args())

    if not (args['file'] or args['list']):
        parser.error("Please define --file or --list option")

    # Open file
    filename = args['file']
    lines = readFile(filename)

    CREDIT_LINES = getCreditLines(sys.argv)
    MODE = 'shuffle'
    if CREDIT_LINES[0] in lines:
        MODE = 'unshuffle'

    # Ignore first comments
    shuffleignore = 0
    comment = True
    while lines[shuffleignore].startswith("#"):
        shuffleignore += 1
    texttoshuffle = lines[shuffleignore:]
    size = len(texttoshuffle)

    # Shuffle/Unshuffle
    filenamebk = f"{filename}.{MODE}.bak"
    if MODE == 'shuffle':
        result = suffleLines(args['password'], texttoshuffle, SHUFFLE, args['column'])
        texttosave = lines[0:shuffleignore] + CREDIT_LINES + result
        copyfile(filename, filenamebk)
        writeFile(filename, texttosave)
    elif MODE == 'unshuffle':
        result = suffleLines(args['password'], texttoshuffle, UNSHUFFLE, args['column'])
        texttosave = lines[0:shuffleignore-2] + result
        copyfile(filename, filenamebk)
        writeFile(filename, texttosave)
