import requests
import smtplib
from email.message import EmailMessage

def fetch_req(url):
    r = requests.get(
        url=url,
        params={"limit": 20, "offset": 0},
        timeout=30,
    )
    r.raise_for_status()
    data = r.json()

    return data

def send_mail(sender, receiver, message, app_password):
    msg = EmailMessage()
    msg["Subject"] = "(API) New Job Notification"
    msg["From"] = sender
    msg["To"] = receiver
    msg.set_content(message)

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender, app_password)
    
    server.send_message(msg)
    
    server.close()