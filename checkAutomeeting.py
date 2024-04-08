#!/Users/rzheng/automeeting/venv/bin/python

from datetime import datetime, timedelta
import time
import webbrowser
import os.path
import os
import sys
import threading
import pytz

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

new_dir = os.path.join(os.environ['HOME'], 'Library/Application Support/xbar/plugins/')
os.chdir(new_dir)

# If modifying these scopes, delete the file token.json.
SCOPES = [
    "https://www.googleapis.com/auth/calendar.readonly",
    "https://www.googleapis.com/auth/calendar.events.readonly",
]
POLL_RATE = 8 # seconds
JOIN_ADVANCE = 30 # how early to join the meeting
assert POLL_RATE < 300
MSG_LIMIT = 30

LOG_FILE = "resources/automeeting.log"
def log(message):
    with open(LOG_FILE, "a") as log_file:
        log_file.write(f"{datetime.now()}: {message}\n")
    # print(message)

def alarm(msg, times=1):
    def play_sound():
        for _ in range(times):
            os.system(f"say \"{msg}\"")
    threading.Thread(target=play_sound).start()

TOKEN_FILE="resources/token.json"
CREDENTIALS_FILE="resources/credentials.json"
def auth():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())
    return creds

import json
def p(o, log_only = False):
    if log_only:
        log(json.dumps(o, indent=4))
    else:
        print(json.dumps(o, indent=4))


def already_opened(meeting_id):
    filename = 'resources/CACHE'
    result = False
    with open(filename, "r") as f:
        ids = f.read()
        if meeting_id in ids:
            return True

    with open(filename, "w") as f:
        f.write(ids[-500:] + meeting_id)

    return result

def is_personal_block(event):
    attendees = event.get("attendees", [])
    return (
        len(attendees) == 0 or
        (
            len(attendees) == 1 and 
            attendees[0].get("self", False) and 
            event.get("organizer", {}).get("self", False)
        )
    )


def parse_time(event):
    start = datetime.fromisoformat(event["start"].get("dateTime", event["start"].get("date")))
    now = datetime.utcnow().replace(tzinfo=pytz.UTC).astimezone(pytz.timezone('US/Pacific'))
    diff = start - now
    if now.date() == start.date():
        # If they are the same day, display the difference in hours and minutes
        hours = diff.seconds // 3600
        minutes = (diff.seconds % 3600) // 60
        if hours == 0:
            return f"{minutes}m"
        else:
            return f"{hours}:{minutes:02d}"
    else:
        # If they are different days, display the difference in days
        days = (start.date() - now.date()).days
        if days == 1:
            return f"_Tmr@{start.strftime('%H:%M')}"
        else:
            return f"{days}d"

def get_next_event(service):
    now_ts = datetime.utcnow().replace(tzinfo=pytz.UTC).astimezone(pytz.timezone('US/Pacific'))
    now = now_ts.isoformat().rsplit("-", 1)[0] + "Z"  # 'Z' indicates UTC time
    events_result = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=now,
            maxResults=10,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = events_result.get("items", [])
    if not events:
        return "ERROR | could not find events"
    else:
        for event in events:
            if is_personal_block(event):
                continue
            start = datetime.fromisoformat(event["start"].get("dateTime", event["start"].get("date")))
            if now_ts > start + timedelta(minutes=6):
                continue
            break
        
        summary = event['summary']
        if len(summary) > MSG_LIMIT:
             summary = summary[:MSG_LIMIT] + ".."
        return f"{summary}{parse_time(event)}"

def open_meetings(service):
    # Call the Calendar API
    now = datetime.utcnow()
    timeMin = (now - timedelta(minutes=5)).isoformat() + "Z" # inspect 5 minutes in advance so as to not miss any events.
    timeMax = (now + timedelta(seconds=JOIN_ADVANCE)).isoformat() + "Z"  # 'Z' indicates UTC time
    log("Getting events...")
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
        log("No upcoming events found.")
        return
    else:
        log(f"Found {len(events)} events.")
        for event in events:
            summary = event.get("summary", "NO_TITLE")
            if "hangoutLink" not in event:
                log(f"{summary} isn't a hangout")
                continue
            if already_opened(event["id"]):
                log(f"{summary} already opened, skipping")
                continue
            log(f"Opening {summary}")
            p(event, log_only=True)
            webbrowser.open(event["hangoutLink"])
            alarm("Meeting about to begin", times=10)

def poll():
    try:
        creds = auth()
        service = build("calendar", "v3", credentials=creds)

        open_meetings(service)
        print(get_next_event(service))  # prints out to xbar
    except Exception as e:
        alarm("Automeeting Error")
        raise e

poll()
