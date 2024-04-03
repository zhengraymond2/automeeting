from datetime import datetime, timedelta
import time
import webbrowser
import os.path
import os
import threading

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = [
    "https://www.googleapis.com/auth/calendar.readonly",
    "https://www.googleapis.com/auth/calendar.events.readonly",
]
POLL_RATE = 8 # seconds
JOIN_ADVANCE = 30 # how early to join the meeting
assert POLL_RATE < 300


def alarm(times):
    def play_sound():
        for _ in range(times):
            os.system(f"afplay /System/Library/Sounds/Glass.aiff")
    threading.Thread(target=play_sound).start()

def auth():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return creds

import json
def p(o):
    print(json.dumps(o, indent=4))


# Having a TTL on this means that if meeting changes will be reflected.
# For example, if a meeting is opened, it is entered into cache (so it's not re-opened over and over). However, if that meeting 
#  is then, say, last minute changed, and pushed back, then this script will no longer open the meeting.
from cachetools import TTLCache
CACHE = TTLCache(maxsize=1000, ttl=3600+300)  
def cache(meeting_id):
    if meeting_id in CACHE:
        return False
    CACHE[meeting_id] = 0  # insert into cache
    return True


def poll(service, creds):
    try:
        # Call the Calendar API
        now = datetime.utcnow()
        timeMin = (now - timedelta(minutes=5)).isoformat() + "Z" # inspect 5 minutes in advance so as to not miss any events.
        timeMax = (now + timedelta(seconds=JOIN_ADVANCE)).isoformat() + "Z"  # 'Z' indicates UTC time
        print("Getting events...")
        events_result = (
            service.events()
            .list(
                calendarId="primary",
                timeMin=timeMin,
                timeMax=timeMax,
                maxResults=5,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])

        if not events:
            print("No upcoming events found.")
            return
        else:
            print(f"Found {len(events)} events.")
            for event in events:
                if cache(event["id"]) and "hangoutLink" in event:
                    print("Opening", event["summary"])
                    p(event)
                    webbrowser.open(event["hangoutLink"])
                    alarm(times=15)
                else:
                    print(event["id"], "already opened")
    except HttpError as error:
        alarm(times=1)
        print(f"An error occurred: {error}")


def main():
    while True:
        try:
            creds = auth()
            service = build("calendar", "v3", credentials=creds)
            while True:
                poll(service, creds)
                time.sleep(POLL_RATE)
            return
        except:
            print("Could not start poller, trying again in 30 seconds...")
            alarm(times=1)
            time.sleep(30)

if __name__ == '__main__':
    main()
