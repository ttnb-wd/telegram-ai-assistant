import os
from telethon import TelegramClient, events
from google import genai
from telethon.sessions import StringSession

# ==========================
# Telegram Secrets
# ==========================

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION_STRING = os.getenv("TELEGRAM_SESSION")


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

@telegram.on(events.NewMessage)
async def handler(event):

    # Ignore my own messages
    if event.out:
        return


    message = event.message.message


    if not message:
        return


    print("User:", message)


    try:

        response = client_ai.models.generate_content(
            model="gemini-flash-latest",
            contents=message
        )


        reply = response.text


        if not reply:
            reply = "I cannot generate a response."


        await event.reply(reply)


        print("AI:", reply)


    except Exception as e:

        print("ERROR:", e)


        await event.reply(
            "AI Error: " + str(e)
        )


# ==========================
# Start Bot
# ==========================

print("AI Assistant Started...")


telegram.start()


print("Telegram Connected!")


telegram.run_until_disconnected()