import smtplib
import os
from email.message import EmailMessage

# ⚠️ Reemplaza con tu cuenta real
EMAIL_ADDRESS = "tucorreo@gmail.com"
EMAIL_PASSWORD = "tu_contraseña_de_aplicación"

def enviar_archivos_por_correo(destinatario, archivos, asunto="Archivos desde el bot", cuerpo="Adjunto los archivos solicitados."):
    msg = EmailMessage()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = destinatario
    msg["Subject"] = asunto
    msg.set_content(cuerpo)

    for archivo in archivos:
        with open(archivo, "rb") as f:
            contenido = f.read()
            nombre = os.path.basename(archivo)
            msg.add_attachment(contenido, maintype="application", subtype="zip", filename=nombre)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)
