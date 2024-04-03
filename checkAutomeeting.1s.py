#!/bin/bash

# ANSI escape codes for colors and font weight
GREEN='\033[32m'
RED='\033[1;31m'
RESET='\033[0m'

# Check if the script is running
if pgrep -f "run.sh --alarm" > /dev/null
then
    echo "${GREEN}Automeeting running${RESET}"
else
    echo "${RED}AUTOMEETING ERROR${RESET}"
    afplay /System/Library/Sounds/Glass.aiff
fi
