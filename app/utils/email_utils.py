import os
import ssl
from email.message import EmailMessage
import smtplib
from dotenv import load_dotenv

load_dotenv()  # carrega .env se existir
SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", 465))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")
FROM_ADDRESS = os.getenv("FROM_ADDRESS", SMTP_USER or "no-reply@example.com")

def send_email_with_attachment(to_email: str, subject: str, body: str, attachment_bytes: bytes, filename: str):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = FROM_ADDRESS
    msg["To"] = to_email
    msg.set_content(body)

    # Anexa o PDF
    msg.add_attachment(attachment_bytes, maintype="application", subtype="pdf", filename=filename)

    # Envio 
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, context=context) as server:
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(msg)
#seguro (SMTP SSL 465). Se usar 587, trocar para starttls.