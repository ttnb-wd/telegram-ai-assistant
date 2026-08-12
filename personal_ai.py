import os

from telethon import TelegramClient, events
from telethon.sessions import StringSession

from google import genai


# ==========================
# Telegram Secrets
# ==========================

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
SESSION = os.getenv("TELEGRAM_SESSION")


if not API_ID:
    raise ValueError("Missing API_ID secret")

if not API_HASH:
    raise ValueError("Missing API_HASH secret")

if not SESSION:
    raise ValueError("Missing TELEGRAM_SESSION secret")


API_ID = int(API_ID)


# ==========================
# Gemini AI
# ==========================

GEMINI_KEY = os.getenv("GEMINI_API_KEY")


if not GEMINI_KEY:
    raise ValueError("Missing GEMINI_API_KEY secret")


client_ai = genai.Client(
    api_key=GEMINI_KEY
)


# ==========================
# Telegram Client
# ==========================

telegram = TelegramClient(
    StringSession(SESSION),
    API_ID,
    API_HASH
)


# ==========================
# Message Handler
# ==========================

@telegram.on(events.NewMessage(incoming=True))
async def handler(event):

    # Ignore my own messages
    if event.out:
        return


    message = event.message.message


    if not message:
        return


    print("\nUser:")
    print(message)


    try:

        response = client_ai.models.generate_content(
            model="gemini-flash-latest",
            contents=f"""
You are a personal Telegram assistant for the owner of this account.

Your job:
- Talk like a close personal assistant, not like an AI chatbot.
- Reply naturally like a human friend.
- Always answer in Burmese.
- Do not say "I am an AI".
- Do not explain limitations too much.
- Be casual, friendly and helpful.

You know the owner personally.
If someone asks about the owner:
- Answer naturally.
- If you don't know the exact situation, make a reasonable casual guess.
- You can say things like:
  "အခုတော့ မရှိသေးဘူးထင်တယ်"
  "ဒီနေ့ schedule ကြည့်ရင် နည်းနည်းအလုပ်များနေတယ်"
  "လိုရင် သတိပေးပေးလိုက်မယ်"

Conversation style:
- Like a close friend helping manage the owner's messages.
- Not formal customer support.


User message:
{message}
"""
        )


        reply = response.text


        if not reply:
            reply = "တောင်းပန်ပါတယ်။ အဖြေမထုတ်နိုင်ပါ။"


        await event.reply(reply)


        print("\nAI:")
        print(reply)


    except Exception as e:

        print("\nERROR:")
        print(e)


        await event.reply(
            "AI Error ဖြစ်နေပါတယ်: " + str(e)
        )


# ==========================
# Start Bot
# ==========================

print("🤖 Myanmar AI Assistant Starting...")


telegram.start()


print("✅ Telegram Connected!")
print("✅ AI Assistant is Running...")


telegram.run_until_disconnected()