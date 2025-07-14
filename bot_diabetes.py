import csv
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = "7914009689:AAHQo8EOuLzolt_kmuIaSQJGj-QuQE23jck"
ARCHIVO = "diario_diabetes.csv"

def inicializar_csv():
    try:
        with open(ARCHIVO, "x", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["FechaHora", "Glucosa", "Comida", "Insulina", "Observaciones"])
    except FileExistsError:
        pass

inicializar_csv()

async def registrar(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    texto = update.message.text.lower()
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    glucosa = ""
    comida = ""
    insulina = ""
    observaciones = ""

    if "glucosa" in texto:
        for palabra in texto.split():
            if palabra.isdigit() and 40 < int(palabra) < 600:
                glucosa = palabra
                break

    if "comí" in texto or "desayuné" in texto or "almorcé" in texto or "cené" in texto:
        comida = texto

    if "unidad" in texto or "u" in texto:
        for palabra in texto.split():
            if palabra.replace("u", "").isdigit():
                insulina = palabra
                break

    if not glucosa and any(c.isdigit() for c in texto):
        observaciones = texto

    with open(ARCHIVO, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([now, glucosa, comida, insulina, observaciones])

    await update.message.reply_text(
        f"📝 Registro guardado:\n"
        f"🕒 {now}\n"
        f"🩸 Glucosa: {glucosa or 'No registrada'}\n"
        f"🍽️ Comida: {comida or 'No registrada'}\n"
        f"💉 Insulina: {insulina or 'No registrada'}\n"
        f"🗒️ Observaciones: {observaciones or 'Ninguna'}"
    )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "¡Hola Miguel! Soy tu bot de diario de diabetes.\n\n"
        "Solo escríbeme tu glucosa, lo que comiste o la insulina que te aplicaste,\n"
        "y lo registraré por ti 📊"
    )

if __name__ == "__main__":
   from telegram.ext import Updater

updater = Updater(TOKEN)
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, registrar))

updater.start_polling()
updater.idle()

