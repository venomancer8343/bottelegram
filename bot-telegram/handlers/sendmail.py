import os
from telegram import Update
from telegram.ext import ContextTypes
from handlers.emailer import enviar_archivos_por_correo

# Paso 1: comando /enviar_correo
async def solicitar_correo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file_path = context.user_data.get("last_file")
    if not file_path or not os.path.exists(file_path):
        await update.message.reply_text("⚠️ No hay archivo reciente para enviar.")
        return

    context.user_data["esperando_correo"] = True
    await update.message.reply_text("✉️ Por favor, escribe la dirección de correo a la que deseas enviar los archivos.")
