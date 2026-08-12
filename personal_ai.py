import os
from telethon import TelegramClient, events
from google import genai


# Telegram secrets
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION = os.getenv("TELEGRAM_SESSION")


# Gemini
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

client_ai = genai.Client(
    api_key=GEMINI_KEY
)


# Telegram client
telegram = TelegramClient(
    "my_account",
    API_ID,
    API_HASH
)


@telegram.on(events.NewMessage)
async def handler(event):

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


        await event.reply(reply)

        print("AI:", reply)


    except Exception as e:

        print(e)

        await event.reply(
            "Error: " + str(e)
        )



print("AI Assistant Started...")


telegram.start()

telegram.run_until_disconnected()