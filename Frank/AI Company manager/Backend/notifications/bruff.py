from kivy.uix.recyclegridlayout import defaultdict
import imaplib
import email
import re
from email.header import decode_header
from pydantic import BaseModel
from typing import Optional


# ---------- Utilities ----------

def clean_subject(subject):
    if not subject:
        return ""
    decoded = decode_header(subject)
    part = decoded[0][0]
    if isinstance(part, bytes):
        return part.decode(decoded[0][1] or "utf-8", errors="ignore")
    return part


def strip_html(html):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', html)


def get_plain_text(msg):
    text = ""
    html = ""

    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            if part.get("Content-Disposition"):
                continue  # skip attachments
            payload = part.get_payload(decode=True)
            if not payload:
                continue
            if content_type == "text/plain":
                text = payload.decode(errors="ignore")
            elif content_type == "text/html" and not text:
                html = payload.decode(errors="ignore")
    else:
        payload = msg.get_payload(decode=True)
        if payload:
            if msg.get_content_type() == "text/plain":
                text = payload.decode(errors="ignore")
            elif msg.get_content_type() == "text/html":
                html = payload.decode(errors="ignore")

    return text or strip_html(html) if html else ""


# ---------- Input Schema ----------

class CheckEmailSchema(BaseModel):
    specific_sender: Optional[str] = None


 

def check_email_replies(specific_sender=None):
    """
    Use this tool to get a reply message or any message from a specific client or anyone.
    
    Inputs:
        specific_sender: Defaults to None if you want any unread reply. If provided, filters by that sender.
        
    Returns:
        The message body of both the sent message and reply message.
    """
    
    FROM = "frvnkkwizigira@gmail.com"
    SECRET = "vzaffqodhmjwwssv"
    IMAP_SERVER = "imap.gmail.com"  # ✅ FIXED — removed trailing comma

    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(FROM, SECRET)

    sent_folder = '"[Gmail]/Sent Mail"' if "gmail" in IMAP_SERVER else "Sent"
    mail.select(sent_folder)

    result, sent_ids_data = mail.search(None, "ALL")
    sent_ids = sent_ids_data[0].split()
    sent_msg_ids = {}

    for sid in sent_ids:
        result, data = mail.fetch(sid, "(BODY.PEEK[HEADER])")
        raw_email = data[0][1]
        msg = email.message_from_bytes(raw_email)
        msg_id = msg.get("Message-ID")
        subject = clean_subject(msg.get("Subject"))
        to = msg.get("To")
        if msg_id:
            sent_msg_ids[msg_id.strip()] = {
                "subject": subject,
                "to": to,
                "id": sid,
            }

    mail.select("inbox")
    search_criteria = f'(UNSEEN FROM "{specific_sender}")' if specific_sender else "(UNSEEN)"
    result, inbox_ids_data = mail.search(None, search_criteria)
    inbox_ids = inbox_ids_data[0].split()

    found = False

    for iid in inbox_ids:
        result, data = mail.fetch(iid, "(BODY.PEEK[HEADER.FIELDS (FROM SUBJECT IN-REPLY-TO)])")
        raw_headers = data[0][1]
        msg = email.message_from_bytes(raw_headers)
        in_reply_to = msg.get("In-Reply-To")
        subject = clean_subject(msg.get("Subject"))
        from_addr = msg.get("From")

        if not in_reply_to or in_reply_to.strip() not in sent_msg_ids:
            continue

        # Fetch full reply message
        result, full_data = mail.fetch(iid, "(RFC822)")
        full_msg = email.message_from_bytes(full_data[0][1])
        reply_body = get_plain_text(full_msg)

        sent_msg_meta = sent_msg_ids[in_reply_to.strip()]
        result, sent_full_data = mail.fetch(sent_msg_meta["id"], "(RFC822)")
        sent_full_msg = email.message_from_bytes(sent_full_data[0][1])
        sent_body = get_plain_text(sent_full_msg).replace(FROM, "you")

        print(f"\n📬 Unseen Reply From: {from_addr}")
        print(f"Subject: {subject}")
        print(f"Reply Body:\n{reply_body[:300]}")
        print(f"\n↪️ In reply to your message to {sent_msg_meta['to']}")

        found = True
        mail.logout()
        print("marked")

    mail.logout()

    if not found:
        print(f"No *unseen* replies found from {specific_sender if specific_sender else 'anyone'}.")
        return None