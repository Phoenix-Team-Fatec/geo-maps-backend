import os, logging, ssl, smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
from fastapi import BackgroundTasks

log = logging.getLogger("mailer")

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


def send_reset_email(to_email: str, code: str, background: BackgroundTasks | None = None) -> None:
    subject = "Seu código para reset de senha"
    body = f"Use este código para redefinir sua senha: {code}\nEle expira em 15 minutos."

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = FROM_ADDRESS
    msg["To"] = to_email
    msg.set_content(body)

    def _send():
        try:
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, context=context) as server:
                if SMTP_USER and SMTP_PASS:
                    server.login(SMTP_USER, SMTP_PASS)
                server.send_message(msg)
            log.info("E-mail de reset enviado para %s", to_email)
        except Exception as e:
            log.exception("Falha ao enviar e-mail para %s: %s", to_email, e)
    
    if background is not None:
        log.debug("Agendando envio em background para %s", to_email)
        background.add_task(_send)
    else:
        _send()
