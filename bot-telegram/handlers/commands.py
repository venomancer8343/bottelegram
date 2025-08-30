from telegram import Update
from telegram.ext import ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Bienvenido al bot multimedia.\n\n"
        "Comandos disponibles:\n"
        "/opciones <URL> – Ver formatos de video\n"
        "/descargar <ID> – Descargar formato específico\n"
        "/comprimir – Comprimir el último archivo"
    )
