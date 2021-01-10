#!/usr/bin/env bash

# Vars
declare -A VERSION_TYPES=( ["major"]=0 ["minor"]=1 ["fix"]=2)
GIT_ROOT=$(git rev-parse --show-toplevel)
GIT_COUNT_STATE=$(git status -uno --porcelain=v1 | wc -l)
TAGS_COUNT=$(git tag | wc -l)
SHORT_TAG=$(git describe --tags  --match "[0-9]*\.[0-9]*\.[0-9]*" --abbrev=0 2>/dev/null)
CURRENT_TAG=$(git tag --contains HEAD 2>/dev/null)
VERSION_TYPE=$1

# Check parameters
if [ -z "$VERSION_TYPE" ]; then
    echo "Usage: release.sh [major|minor|fix]"
    exit 1
fi

# Check git state
if [ $GIT_COUNT_STATE -gt 0 ]; then
    echo "Please commit your changes"
    exit 1
fi

# Check if the last commit allready tagged
if [ -n "$CURRENT_TAG" ]; then
    echo "This commit is allready released with $CURRENT_TAG"
    exit 1
fi

# Check version
VERSION_INDEX=${VERSION_TYPES[$VERSION_TYPE]}
if [ -z $VERSION_INDEX ]; then
    echo "Usage: release.sh [major|minor|fix]"
    exit 1
fi

# https://stackoverflow.com/a/64390598/2015612
increment_version() {
  local delimiter=.
  local array=($(echo "$1" | tr $delimiter '\n'))
  array[$2]=$((array[$2]+1))
  if [ $2 -lt 2 ]; then array[2]=0; fi
  if [ $2 -lt 1 ]; then array[1]=0; fi
  echo $(local IFS=$delimiter ; echo "${array[*]}")
}

if [ $TAGS_COUNT -eq 0 ]; then
    NEXTVERSION="0.1.0"
else
    NEXTVERSION=$(increment_version "$SHORT_TAG" $VERSION_INDEX)
fi

MESS="Release $NEXTVERSION version"
echo $NEXTVERSION > ${GIT_ROOT}/VERSION

cp README.md README_SHUFFLED_SAMPLE.md
cp README.md README_SHUFFLED_COLUMN_SAMPLE.md
python ${GIT_ROOT}/mandoline.py -p "password" -f README_SHUFFLED_SAMPLE.md
python ${GIT_ROOT}/mandoline.py -p "password" -c -f README_SHUFFLED_COLUMN_SAMPLE.md

git add ${GIT_ROOT}/VERSION ${GIT_ROOT}/README_SHUFFLED_SAMPLE.md ${GIT_ROOT}/README_SHUFFLED_COLUMN_SAMPLE.md
git commit -m "$MESS"
git tag -a "$NEXTVERSION" -m "$MESS"
