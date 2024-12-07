import os, key 
import smtplib
import ssl
from email.message import EmailMessage
from connection import email_by_id


def send_email(subject, message, sender):
    email_sender = "jondir.tools.official@gmail.com"
    email_password = os.environ.get("email_key")
    email_receiver = "jondir.tools.official@gmail.com"

    # Set the subject and body of the email
    email_subject = subject
    body = f"Sent by: {sender} \n" + message

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = email_subject
    em.set_content(body)

    # Add SSL (layer of security)
    context = ssl.create_default_context()

    # Log in and send the email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())
    
        
