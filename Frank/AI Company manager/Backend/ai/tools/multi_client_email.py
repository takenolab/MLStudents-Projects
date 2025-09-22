import smtplib
import ssl
import os
from email.message import EmailMessage
import pathlib 
import dotenv
import pydantic 

env = pathlib.Path(__file__).resolve().parents[1] / "utilities"/ "secret"/ ".env"
dotenv.load_dotenv(dotenv_path=str(env))
class MultiSendEmailShema(pydantic.BaseModel):
    receiver_emails:list[str]
    subject:str
    body:str



import smtplib
import ssl
import os
from email.message import EmailMessage

def multi_send_email(receiver_emails: list[str], subject: str, body: str) -> str:
    """
    Sends a well-formatted, professional, plain-text email to multiple recipients.

    Args:
        receiver_emails (list[str]): A list of recipient email addresses.
        subject (str): The subject line of the email.
        body (str): The main content of the email message.

    Returns:
        str: string showing the status of each email sent,
             or a descriptive error message.
    """

    sender_email = os.getenv("EMAIL_HOST")
    password = os.getenv("PASS")
    context = ssl.create_default_context()

    if not sender_email or not password:
        return "❌ Missing sender email or password environment variables."

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg.set_content(body)

    results = []

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)

            for recipient in receiver_emails:
                msg["To"] = recipient
                try:
                    server.send_message(msg)
                    results.append(f"{recipient} ✅ message sent")
                except Exception as e:
                    results.append(f"{recipient} ❌ failed: {str(e)}")
                del msg["To"]  
                
        return "\n".join(results)

    except smtplib.SMTPAuthenticationError:
        return "❌ Authentication failed. Check your email credentials or use an App Password."

    except Exception as e:
        return f"❌ I faild you sorry , i had some issues"
