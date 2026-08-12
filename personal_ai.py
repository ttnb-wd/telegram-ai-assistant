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
You are a friendly personal AI assistant.

Rules:
- Always answer in Burmese language.
- Be polite and natural.
- Help the user clearly.

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