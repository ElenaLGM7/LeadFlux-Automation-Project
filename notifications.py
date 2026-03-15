import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import APP_NAME

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "tucorreo@gmail.com"
SMTP_PASS = "tu_password_app"

ADMIN_EMAIL = "cliente@empresa.com"


def send_email(subject: str, body: str, to_email: str = ADMIN_EMAIL):
    msg = MIMEMultipart()
    msg["From"] = SMTP_USER
    msg["To"] = to_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.sendmail(SMTP_USER, to_email, msg.as_string())
        server.quit()
        print("Email enviado")
    except Exception as e:
        print("Error enviando email:", e)


def notify_lead(lead):
    subject = f"[{APP_NAME}] Nuevo lead {lead.status.upper()}"

    body = f"""
Nuevo lead recibido

Nombre: {lead.name}
Email: {lead.email}
Empresa: {lead.company}
Mensaje: {lead.message}

Score: {lead.score}
Estado: {lead.status}
"""

    send_email(subject, body)
