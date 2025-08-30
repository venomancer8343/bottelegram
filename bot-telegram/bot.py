from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters
)
from telegram import BotCommand

# Importar funciones desde tus módulos
from config import BOT_TOKEN
from handlers.commands import start
from handlers.formats import opciones
from handlers.download import descargar
from handlers.compress import comprimir
from handlers.sendmail import solicitar_correo, recibir_correo, correo_callback

# Crear la aplicación del bot
app = ApplicationBuilder().token(BOT_TOKEN).build()

# Registrar comandos clicables en Telegram
commands = [
    BotCommand("start", "Iniciar el bot"),
    BotCommand("opciones", "Ver formatos disponibles de un video"),
    BotCommand("descargar", "Descargar un formato específico"),
    BotCommand("comprimir", "Comprimir el último archivo descargado"),
    BotCommand("enviar_correo", "Enviar los archivos comprimidos por email")
]
app.bot.set_my_commands(commands)

# Registrar handlers para comandos
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("opciones", opciones))
app.add_handler(CommandHandler("descargar", descargar))
app.add_handler(CommandHandler("comprimir", comprimir))
app.add_handler(CommandHandler("enviar_correo", solicitar_correo))

# Handler para recibir el correo como texto
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, recibir_correo))

# Handler para botones de confirmación de envío
app.add_handler(CallbackQueryHandler(correo_callback, pattern="^correo_"))

# Ejecutar el bot
app.run_polling()
