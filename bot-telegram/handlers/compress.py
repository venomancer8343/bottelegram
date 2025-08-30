import os
import zipfile
from telegram import Update
from telegram.ext import ContextTypes

CHUNK_SIZE_MB = 15
CHUNK_SIZE = CHUNK_SIZE_MB * 1024 * 1024

def dividir_en_partes(file_path):
    partes = []
    with open(file_path, 'rb') as f:
        i = 0
        while True:
            chunk = f.read(CHUNK_SIZE)
            if not chunk:
                break
            parte_path = f"{file_path}.part{i}"
            with open(parte_path, 'wb') as pf:
                pf.write(chunk)
            partes.append(parte_path)
            i += 1
    return partes

def comprimir_partes(partes):
    zip_paths = []
    for parte in partes:
        zip_path = parte + ".zip"
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            zipf.write(parte, arcname=os.path.basename(parte))
        zip_paths.append(zip_path)
    return zip_paths

async def comprimir(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file_path = context.user_data.get("last_file")

    if not file_path or not os.path.exists(file_path):
        await update.message.reply_text("⚠️ No hay archivo reciente para comprimir.")
        return

    file_size = os.path.getsize(file_path)

    if file_size <= CHUNK_SIZE:
        # Archivo pequeño: comprimir directamente
        zip_path = file_path + ".zip"
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            zipf.write(file_path, arcname=os.path.basename(file_path))
        await update.message.reply_document(document=open(zip_path, 'rb'))
    else:
        # Archivo grande: dividir y comprimir por partes
        await update.message.reply_text("📦 Archivo grande detectado. Dividiendo en partes de 15 MB...")
        partes = dividir_en_partes(file_path)
        zip_paths = comprimir_partes(partes)
        for zip_path in zip_paths:
            await update.message.reply_document(document=open(zip_path, 'rb'))
