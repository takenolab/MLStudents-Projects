import random
import pymongo
import requests
import webbrowser
from email_validator import validate_email, EmailNotValidError



# def username_validation(name):
#   # must include ($#@&*^%?)
#   # must be length > 4
#   # must include(0-9)
#   # must include(a-z)(A-Z)
#    pass
# "https://mail.google.com/mail/?view=cm&fs= 1&to={self.email}

def is_connected(timeout=7):
    """Takes the timeout in seconds"""
    isConnect = False
    try:
      r = requests.get("https://www.google.com" , timeout=timeout)
      return r.status_code == 200

    except requests.RequestException:
      return False


def open_email():

      email = 'frvnkkwizigira@gmial.com'
      gmail_url = f"https://mail.google.com/mail/?view=cm&fs= 1&to={email}"
      webbrowser.open(gmail_url)

def is_legit_email(addr: str) -> bool:
    try:
        info = validate_email(addr, check_deliverability=True)
        print("Normalized:", info.normalized)
        return True
    except EmailNotValidError as e:
        print("Invalid:", e)
        return False 
