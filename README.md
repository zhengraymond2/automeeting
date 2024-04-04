# Notes:
- does not work for zoom links.
- if you punt a meeting AFTER the alarm has already opened the meeting, it may be missed

# Installation
1. install xbar
2. modify checkAutomeeting.py's shebang to match your username
3. Then run `./setup.sh` 

The scripts should then run on startup, and play audio alarms if it's running into errors. 

To remove alarms, comment out the appropriates lines in ./checkAutomeeting.1m.py and then rerun setup.sh

# Xbar
As a sanity check, you can install [xbar](https://github.com/matryer/xbar-plugins) to view the status of AutoMeeting on your status bar + play annoying sounds if AutoMeeting isn't running for whatever reason.

To enable this, install xbar, then rerun the setup.sh (or setupAlarm.sh) scripts.

# Authentication requirements
This requires you add a `credentials.json` to the repository root. You can obtain this credentials.json by creating a GCP app:
- https://console.cloud.google.com/apis/
- Create New Project
- OAuth Consent Screen > enable the readonly scopes: <img width="509" alt="image" src="https://github.com/zhengraymond2/automeeting/assets/165727211/52aa37e1-cf00-448a-80b2-ff17d9c49c2d">
- Create OAuth credentials following this short guide: https://developers.google.com/calendar/api/quickstart/python#authorize_credentials_for_a_desktop_application
- Copy those to `./credentials.json`.

If your organization already has this app, then you just need to obtain the credentials.json from someone (the app admin?). Note that the credentials.json is only the authentication for the app -- it doesn't provide access to your google account. The script will prompt you to login to your google account, which will then generate a token.json -- this is your personalized authentication. Do not commit or share either of these secrets (already in .gitignore)!


