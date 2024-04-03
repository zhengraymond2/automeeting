#!/bin/bash

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

# Get the current directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# Create the plist content
PLIST="<?xml version=\"1.0\" encoding=\"UTF-8\"?>
<!DOCTYPE plist PUBLIC \"-//Apple//DTD PLIST 1.0//EN\" \"http://www.apple.com/DTDs/PropertyList-1.0.dtd\">
<plist version=\"1.0\">
<dict>
<key>Label</key>
<string>automeetingScript</string>
<key>ProgramArguments</key>
<array>
    <string>${DIR}/run.sh</string>
    <string>--alarm</string>
</array>
<key>RunAtLoad</key>
<true/>
<key>KeepAlive</key>
<true/>
</dict>
</plist>"

# Write the plist content to the plist file
echo "$PLIST" > ~/Library/LaunchAgents/automeeting.plist

# launch the plist
launchctl unload ~/Library/LaunchAgents/automeeting.plist
launchctl load ~/Library/LaunchAgents/automeeting.plist

