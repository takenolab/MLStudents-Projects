import os.path
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import pickle   
from googleapiclient.errors import HttpError
import os
import pathlib 
 


cr = pathlib.Path(__file__).resolve().parents[0] /"credentials" / "credentials.json"
import os.path

 

 
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
TOKEN_PICKLE_FILE = "token.pickle" 

def get_gmail_service():
    creds = None

    if os.path.exists(TOKEN_PICKLE_FILE):
        with open(TOKEN_PICKLE_FILE, "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
           
            print("No valid credentials available. Please run the OAuth flow manually.")
            return None

        with open(TOKEN_PICKLE_FILE, "wb") as token:
            pickle.dump(creds, token)

    try:
        service = build("gmail", "v1", credentials=creds)
        return service
    except HttpError as error:
        print(f"An error occurred: {error}")
        return None



def check_unread_from_senders(sender_emails: list[str]) -> bool:
 
    if not sender_emails:
        print("Warning: The list of sender emails is empty.")
        return False

    service = get_gmail_service()
    if not service:
        return False

 
    from_query = " OR ".join(sender_emails)
    query = f"is:unread from:({from_query})"
    print(f"Searching with query: {query}")

    try:
         
        response = service.users().messages().list(userId="me", q=query).execute()
        
        if "messages" in response and response["resultSizeEstimate"] > 0:
            print(f"Found {response['resultSizeEstimate']} unread message(s).")
            return True
        else:
            print("No unread messages found from the specified senders.")
            return False

    except HttpError as error:
        print(f"An error occurred during the API call: {error}")
        return False

 
def unread_from(sender_email: str) -> tuple[bool,int]:
 
    if not sender_email:
        print("Error: sender_email cannot be empty.")
        return False
        
    service = get_gmail_service()
    if not service: 
        return False

    query = f"is:unread from:{sender_email}"
    print(f"Searching with query: '{query}'")

    try:
      
        response = service.users().messages().list(userId='me', q=query).execute()
        
     
        if 'messages' in response and len(response['messages']) > 0:
            count = response.get('resultSizeEstimate', 0)
            print(f"✅ Found {count} unread message(s) from {sender_email}.")
            return True,count
        else:
            print(f"❌ No unread messages found from {sender_email}.")
            return False,0

    except HttpError as error:
        print(f"An API error occurred: {error}")
        return False
 