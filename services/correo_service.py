import os
import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).parent.parent / ".env"

load_dotenv(env_path)

import pathlib

print("DIRECTORIO ACTUAL:", pathlib.Path().absolute())
print("USUARIO:", os.getenv("OUTLOOK_USUARIO"))
print("PASSWORD:", os.getenv("OUTLOOK_PASSWORD"))

USUARIO = os.getenv(
    "GMAIL_USUARIO"
)

PASSWORD = os.getenv(
    "GMAIL_PASSWORD"
)

print("USUARIO:", USUARIO)
print("PASSWORD:", PASSWORD)

def enviar_correo_prueba(
    destinatario
):

    mensaje = MIMEMultipart()

    mensaje["From"] = USUARIO
    mensaje["To"] = destinatario

    mensaje["Subject"] = (
        "Prueba de Alertas Jurídicas"
    )

    cuerpo = """
Hola.

Este es un correo de prueba del sistema de alertas jurídicas.

Si has recibido este mensaje correctamente,
la configuración de correo funciona.

Saludos.
"""

    mensaje.attach(
        MIMEText(
            cuerpo,
            "plain"
        )
    )

    servidor = smtplib.SMTP(
        "smtp.gmail.com",
        587
    )

    servidor.starttls()

    servidor.login(
        USUARIO,
        PASSWORD
    )

    servidor.send_message(
        mensaje
    )

    servidor.quit()