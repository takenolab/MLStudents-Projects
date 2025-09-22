import os
import pathlib 
import pickle
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


cr = pathlib.Path(__file__).resolve().parents[2] / "notifications" / "credentials" / "credentials.json"
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly',
          'https://www.googleapis.com/auth/gmail.modify']

def authenticate_gmail():
 
    creds = None
 
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
     
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                cr, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)
    return service


def get_unread_conversation_from_sender(sender_email):
    service = authenticate_gmail()

    print(f"Searching for unread messages from: {sender_email}")

    query = f"from:{sender_email} is:unread"

    try:
        results = service.users().messages().list(userId='me', q=query, maxResults=1).execute()
        messages = results.get('messages', [])

        if not messages:
            print(f"No unread messages found from {sender_email}.")
            return False, None

        msg = messages[0]
        thread_id = msg['threadId']

        thread = service.users().threads().get(userId='me', id=thread_id).execute()

        return True, thread

    except Exception as error:
        print(f'An error occurred: {error}')
        return False, None


def parse_conversation_to_docstring(thread):
 
    if not thread:
        return ""

    messages = thread['messages']
    conversation_output = []

    for message in messages:
        try:
            headers = {header['name']: header['value'] for header in message['payload']['headers']}
            sender = headers.get('From', 'N/A')
            subject = headers.get('Subject', 'No Subject')
            date = headers.get('Date', 'N/A')

        
            body = ""

     
            body_parts = message['payload'].get('parts', [])
            for part in body_parts:
                if part['mimeType'] == 'text/plain':
                    body = part['body'].get('data', '')
                    break

      
            if not body and message['payload']['body'].get('data'):
                body = message['payload']['body']['data']

      
            import base64
            if body:
                decoded_body = base64.urlsafe_b64decode(body).decode('utf-8')
            else:
                decoded_body = "No readable body found."

            message_str = f"From: {sender}\nDate: {date}\nSubject: {subject}\n\n{decoded_body.strip()}"
            conversation_output.append(message_str)

        except Exception as e:
            conversation_output.append(f"Error processing message: {e}")

    return "\n----\n".join(conversation_output)



import pydantic
class UseenConversationSchema(pydantic.BaseModel):
    sender_email:str


def unseen_conversation(sender_email:str)-> str:
    """
    Handles fetching and parsing unread messages from a specific sender.

    This function connects to the mailbox, searches for unread emails from
    the specified sender, and formats the results into a readable string.

    Args:
        sender_email (str): The sender's email address to check for unread messages.

    Returns:
        str: The parsed conversation if new unread messages are found.
            If there are no new messages, returns a message stating that.

    Raises:
        ConnectionError: If the email server cannot be reached.
        ValueError: If the sender email is invalid or not found.
    """

    has_new_message, conversation_thread = get_unread_conversation_from_sender(sender_email)

    if has_new_message and conversation_thread:
        return str(parse_conversation_to_docstring(conversation_thread))
    else:
        return f"No new messages from {sender_email}."
