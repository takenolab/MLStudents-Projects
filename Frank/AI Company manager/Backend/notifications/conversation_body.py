import os.path
import pickle
import base64
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pathlib 
cr = pathlib.Path(__file__).resolve().parents[0] / "credentials" / "credentials.json"

import imaplib

def mark_emails_as_read(username: str, password: str, sender_email: str):
 
    mail = imaplib.IMAP4_SSL("imap.gmail.com")

    try:
    
        mail.login(username, password)

    
        mail.select("inbox")

        
        status, messages = mail.search(None, f'(UNSEEN FROM "{sender_email}")')

        if status == "OK":
            unread_message_ids = messages[0].split()

            if not unread_message_ids:
                print(f"No unread messages found from {sender_email}.")
                return

        
            for msg_id in unread_message_ids:
                mail.store(msg_id, '+FLAGS', '\\Seen')

            print(f"Marked {len(unread_message_ids)} messages from {sender_email} as read.")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        
        mail.logout()




SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.modify"
]
TOKEN_PICKLE_FILE = "token.pickle"

def get_gmail_service():
    """Authenticate and get the Gmail API service."""
    creds = None
    if os.path.exists(TOKEN_PICKLE_FILE):
        with open(TOKEN_PICKLE_FILE, "rb") as token:
            creds = pickle.load(token)
            print("Scopes:", creds.scopes)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)  # Ensure you have the right credentials file
            creds = flow.run_local_server(port=0)
        with open(TOKEN_PICKLE_FILE, "wb") as token:
            pickle.dump(creds, token)
    
    try:
        service = build("gmail", "v1", credentials=creds)
        return service
    except HttpError as error:
        print(f"An error occurred while building the service: {error}")
        return None

def _parse_message_body(parts: list) -> str:
    """Helper function to parse the body of the email and handle multipart messages."""
    if not parts:
        return ""
        
    for part in parts:
        mime_type = part.get("mimeType")
        body = part.get("body")
        data = body.get("data") if body else None
        
        if mime_type == "text/plain" and data:
            text = base64.urlsafe_b64decode(data).decode("utf-8")
            return text
        
        if "parts" in part:
            return _parse_message_body(part.get("parts"))
            
    return ""   


def get_conversation_bodies(sender_email: str, max_threads: int = 5) -> list[dict]:
    """Fetch and process conversations from a specific sender, marking unread ones as read."""
    if not sender_email:
        print("Warning: Sender email is empty.")
        return []

    service = get_gmail_service()
    if not service:
        return []

    from_query = f"from:{sender_email}"
    print(f"Searching for threads with query: {from_query}")

    try:
        thread_response = service.users().threads().list(
            userId="me", q=from_query, maxResults=max_threads
        ).execute()

        threads = thread_response.get("threads", [])
        if not threads:
            print("No conversation threads found from the specified sender.")
            return []

        email_conversations = {}

        for thread in threads:
            thread_id = thread["id"]
            thread_data = service.users().threads().get(userId="me", id=thread_id).execute()
            messages = thread_data.get("messages", [])

            for message in messages:
                message_id = message["id"]
                payload = message.get("payload", {})
                headers = payload.get("headers", [])

                # Check if message is unread
                label_ids = message.get("labelIds", [])
                is_unread = "UNREAD" in label_ids

                # Extract relevant header fields
                sender = next((h["value"] for h in headers if h["name"] == "From"), "N/A")
                date = next((h["value"] for h in headers if h["name"] == "Date"), "N/A")
                subject = next((h["value"] for h in headers if h["name"] == "Subject"), "No Subject")

                # Parse body
                body = ""
                if "parts" in payload:
                    body = _parse_message_body(payload["parts"])
                else:
                    body_data = payload.get("body", {}).get("data")
                    if body_data:
                        body = base64.urlsafe_b64decode(body_data).decode("utf-8")

                if sender not in email_conversations:
                    email_conversations[sender] = []

                email_conversations[sender].append({
                    "date": date,
                    "subject": subject,
                    "body": body,
                    "is_unread": is_unread,
                    "message_id": message_id
                })
                
 
        result = [
            {
                "email": email,
                "conversation": messages
            }
            for email, messages in email_conversations.items()
        ]
        username = "frvnkkwizigira@gmail.com"
        password = "vzaffqodhmjwwssv"  
        sender_email = sender_email

        print(mark_emails_as_read(username, password, sender_email))

        return result

    except HttpError as error:
        print(f"An error occurred during an API call: {error}")
        return []
