#!/usr/bin/env bash

# Vars
GIT_ROOT=$(git rev-parse --show-toplevel)

# Generate samples
cp ${GIT_ROOT}/README.md ${GIT_ROOT}/README_SHUFFLED_SAMPLE.md
cp ${GIT_ROOT}/README.md ${GIT_ROOT}/README_SHUFFLED_COLUMN_SAMPLE.md
python ${GIT_ROOT}/mandoline.py -p "password" -f ${GIT_ROOT}/README_SHUFFLED_SAMPLE.md
python ${GIT_ROOT}/mandoline.py -p "password" -c -f ${GIT_ROOT}/README_SHUFFLED_COLUMN_SAMPLE.md
