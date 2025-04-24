import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

USERNAME = os.getenv("EMAIL_USERNAME")
PASSWORD = os.getenv("EMAIL_PASSWORD")
SMTP_SERVER = os.getenv("EMAIL_SMTP_SERVER")
SMTP_PORT = int(os.getenv("EMAIL_SMTP_PORT", "587"))
IMAP_SERVER = os.getenv("EMAIL_IMAP_SERVER")
IMAP_PORT = int(os.getenv("EMAIL_IMAP_PORT", "993"))

import smtplib
import ssl
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr, formatdate

TEMPLATES_DIR = "./email_templates"

def send_welcome_email(email, name):
    # Load the HTML template
    with open(f"{TEMPLATES_DIR}/welcome_email.html", "r") as f:
        html = f.read()
        html = html.replace("[name]", name)

    # Send the email
    send_email(email, "Welcome to WhoWhyWhen", html)

def send_new_user_notification_email(email, name):
    to = os.getenv("ADMIN_EMAIL", "admin@example.com")
    # Create HTML content
    html = f"""
    New user registered: {name} ({email})
    """
    # Send the email
    send_email(to, "WhoWhyWhen | New User Registered", html)

def send_password_reset_email(email):
    # Load the HTML template
    with open(f"{TEMPLATES_DIR}/password_reset_email.html", "r") as f:
        html = f.read()

    # Send the email
    send_email(email, "Reset Your Password", html)

def send_password_reset_email(email, temp_password):
    # Load the HTML template
    with open(f"{TEMPLATES_DIR}/password_reset_email.html", "r") as f:
        html = f.read()
        html = html.replace("[temp_password]", temp_password)

    # Send the email
    send_email(email, "Reset Your Password", html)


def send_email(to, subject, html):
    # Create a secure SSL context for the SMTP connection
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    # Create the SMTP connection
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls(context=context)
    server.login(USERNAME, PASSWORD)

    # Create the email message
    msg = MIMEMultipart()
    msg["From"] = formataddr((str(Header("WhoWhyWhen Support", "utf-8")), USERNAME))
    msg["To"] = to
    msg["Subject"] = subject
    msg["Date"] = formatdate(localtime=True)

    # Create the HTML part of the message
    part1 = MIMEText(html, "html", "utf-8")

    # Attach the HTML part to the message
    msg.attach(part1)

    # Send the email via the server
    server.sendmail(msg["From"], msg["To"], msg.as_string())
    server.quit()
