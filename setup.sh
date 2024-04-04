#!/bin/bash

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

# XBAR:
if [ -d "$HOME/Library/Application Support/xbar/plugins/" ]; then
    xbar_dir="$HOME/Library/Application Support/xbar/plugins/"
    echo "enabling xbar plugin"
    cp checkAutomeeting.py "$xbar_dir/checkAutomeeting.1m.py"
    mkdir -p "$xbar_dir/resources"
    cp credentials.json "$xbar_dir/resources/credentials.json"
    touch "$xbar_dir/resources/CACHE"
fi

