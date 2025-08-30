from yt_dlp import YoutubeDL
from telegram import Update
from telegram.ext import ContextTypes

async def opciones(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Proporciona una URL.")
        return

    url = context.args[0]
    context.user_data["url"] = url

    try:
        with YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = info.get("formats", [])
            mensaje = "🎬 *Formatos disponibles:*\n\n"
            for f in formats:
                if f.get("vcodec") != "none":
                    mensaje += f"- ID: `{f['format_id']}` | {f['ext']} | {f['height']}p\n"
            await update.message.reply_text(mensaje, parse_mode="Markdown")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")
