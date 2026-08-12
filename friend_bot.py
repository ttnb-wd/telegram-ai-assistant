from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes


TOKEN = "8512582483:AAG6UNO1l3gnPt7GuFgRUBQLSdiP-Bv6Zis"


async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):

    message = update.message.text

    if "ဟေး" in message:
        reply = "ဟေး 😆 ဘာလုပ်နေလဲ"

    elif "နေကောင်းလား" in message:
        reply = "ကောင်းပါတယ်ကွာ 😂 မင်းရော"

    else:
        reply = "အေး နားထောင်နေတယ် 😎 ဆက်ပြော"


    await update.message.reply_text(reply)


app = Application.builder().token(TOKEN).build()


app.add_handler(
    MessageHandler(filters.TEXT, chat)
)


print("Bot is running...")


app.run_polling()