# Notes:
- does not work for zoom links.
- if you punt a meeting AFTER the alarm has already opened the meeting, it may be missed

# Installation
`./run.sh` This will create a system service plist file, then launch it. 

If you want to remove the audio alarms, update `server.py`'s alarm() method to do nothing, then relaunch the plist:
```
launchctl unload ~/Library/LaunchAgents/automeeting.plist
launchctl load ~/Library/LaunchAgents/automeeting.plist
```

The automeeting script should then always be running. It will make ringing noises if it's encountering errors (such as network issues). 

You can also add a status checker as a sanity check to make sure automeeting is actually running without error. Download and install xbar (https://github.com/matryer/xbar-plugins), then copy the checkAutomeeting.1s.py into "~/Library/Application Support/xbar/plugins/checkAutomeeting.1s.py":
```
cp checkAutomeeting.1s.py ~/Library/Application\ Support/xbar/plugins/checkAutomeeting.1s.py
```

# Authentication requirements
This requires you add a `credentials.json` to the repository root. You can obtain this credentials.json by creating a GCP app:
- https://console.cloud.google.com/apis/
- Create New Project
- OAuth Consent Screen > enable the readonly scopes: <img width="509" alt="image" src="https://github.com/zhengraymond2/automeeting/assets/165727211/52aa37e1-cf00-448a-80b2-ff17d9c49c2d">
- Create OAuth credentials following this short guide: https://developers.google.com/calendar/api/quickstart/python#authorize_credentials_for_a_desktop_application
- Copy those to `./credentials.json`.

If your organization already has this app, then you just need to obtain the credentials.json from someone (the app admin?). Note that the credentials.json is only the authentication for the app -- it doesn't provide access to your google account. The script will prompt you to login to your google account, which will then generate a token.json -- this is your personalized authentication. Do not commit or share either of these secrets (already in .gitignore)!


