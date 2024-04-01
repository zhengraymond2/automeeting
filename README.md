# Installation
`./run.sh`

# Authentication requirements
This requires you add a `credentials.json` to the repository root. You can obtain this credentials.json by creating a GCP app:
- https://console.cloud.google.com/apis/
- Create New Project
- OAuth Consent Screen > enable the readonly scopes: <img width="509" alt="image" src="https://github.com/zhengraymond2/automeeting/assets/165727211/52aa37e1-cf00-448a-80b2-ff17d9c49c2d">
- Create OAuth credentials following this short guide: https://developers.google.com/calendar/api/quickstart/python#authorize_credentials_for_a_desktop_application
- Copy those to `./credentials.json`.

If your organization already has this app, then you just need to obtain the credentials.json from someone (the app admin?). Note that the credentials.json is only the authentication for the app -- it doesn't provide access to your google account. The script will prompt you to login to your google account, which will then generate a token.json -- this is your personalized authentication. Do not commit or share either of these secrets (already in .gitignore)!


