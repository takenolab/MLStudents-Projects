import smtplib
import ssl
from email.message import EmailMessage
import os
import pydantic 
import pathlib 
import dotenv
 

env = pathlib.Path(__file__).resolve().parents[1] / "utilities"/ "secret"/ ".env"
dotenv.load_dotenv(dotenv_path=str(env))

class  SendSingleEmail(pydantic.BaseModel):
    receiver_email: str
    subject: str
    body: str
    
def send_single_email(receiver_email: str, subject: str, body: str) -> bool:
    """
    Send a well-formatted, professional plain-text email.

    Args:
        receiver_email (str): The recipient's email address.
        subject (str): The subject line of the email.
        body (str): The main message content of the email.

    Returns:
        str: A status indicating success or failure.
    """

    sender_email = os.getenv("EMAIL_HOST")
    password = os.getenv("PASS")
    context = ssl.create_default_context()

 
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg.set_content(body)

    print("Attempting to send email...")

    try:
 
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.send_message(msg)
            print("Email sent successfully!")
            return f"Message sent to {receiver_email}"
    except smtplib.SMTPAuthenticationError:
        print("Authentication failed. Please check your email and password.")
        print("For Gmail, you may need to use an 'App Password'.")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return f"I failed send the email due to internal errors"

 
 