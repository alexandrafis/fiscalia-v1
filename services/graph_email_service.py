import smtplib

from email.mime.text import MIMEText

from config.email_config import (
    SMTP_SERVER,
    SMTP_PORT,
    CORREO_REMITENTE,
    CLAVE_CORREO
)


def enviar_correo(
    destinatario,
    asunto,
    mensaje
):

    print("INICIO ENVIO")

    try:

        print("SERVIDOR:", SMTP_SERVER)
        print("PUERTO:", SMTP_PORT)
        print("REMITENTE:", CORREO_REMITENTE)

        correo = MIMEText(
            mensaje,
            "plain",
            "utf-8"
        )

        correo["Subject"] = asunto
        correo["From"] = CORREO_REMITENTE
        correo["To"] = destinatario

        print("CONECTANDO SMTP")

        servidor = smtplib.SMTP(
            SMTP_SERVER,
            SMTP_PORT
        )

        print("STARTTLS")

        servidor.starttls()

        print("LOGIN")

        servidor.login(
            CORREO_REMITENTE,
            CLAVE_CORREO
        )

        print("ENVIANDO")

        servidor.sendmail(
            CORREO_REMITENTE,
            destinatario,
            correo.as_string()
        )

        servidor.quit()

        print("EMAIL ENVIADO")

        return True

    except Exception as e:

        print("ERROR SMTP:")
        print(str(e))

        return False