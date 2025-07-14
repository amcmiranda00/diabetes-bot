import csv
from datetime import datetime
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

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

def registrar(update, context):
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

    context.bot.send_message(chat_id=update.effective_chat.id,
        text=(
            f"📝 Registro guardado:\n"
            f"🕒 {now}\n"
            f"🩸 Glucosa: {glucosa or 'No registrada'}\n"
            f"🍽️ Comida: {comida or 'No registrada'}\n"
            f"💉 Insulina: {insulina or 'No registrada'}\n"
            f"🗒️ Observaciones: {observaciones or 'Ninguna'}"
        )
    )

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
        text="¡Hola Miguel! Soy tu bot de diario de diabetes.\n\nSolo escríbeme tu glucosa, lo que comiste o la insulina que te aplicaste, y lo registraré por ti 📊"
    )

if __name__ == "__main__":
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, registrar))

    updater.start_polling()
    updater.idle()
