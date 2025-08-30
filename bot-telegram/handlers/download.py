from yt_dlp import YoutubeDL
from telegram import Update
from telegram.ext import ContextTypes
import os

# Comando: /descargar <ID>
async def descargar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if not args:
        await update.message.reply_text("❗️ Usa: /descargar <ID>\nEjemplo: /descargar 18")
        return

    format_id = args[0]
    url = context.user_data.get("url")

    if not url:
        await update.message.reply_text("⚠️ Primero usa /opciones <URL> para cargar el video.")
        return

    # Configuración de descarga
    ydl_opts = {
        'format': format_id,
        'outtmpl': 'data/downloads/%(title)s.%(ext)s',
        'quiet': True
    }

    try:
        await update.message.reply_text("⏳ Descargando el archivo, espera un momento...")

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)

        # Enviar el archivo al usuario
        await update.message.reply_document(document=open(file_path, 'rb'))

        # Guardar ruta para compresión posterior
        context.user_data["last_file"] = file_path

    except Exception as e:
        await update.message.reply_text(f"❌ Error al descargar: {e}")
