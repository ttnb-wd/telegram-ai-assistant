import os
import asyncio
import random

from telethon import TelegramClient, events
from telethon.sessions import StringSession


# ==============================
# Load secrets from GitHub
# ==============================

API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
SESSION = os.environ["TELEGRAM_SESSION"]


# ==============================
# Telegram Client
# ==============================

client = TelegramClient(
    StringSession(SESSION),
    API_ID,
    API_HASH
)


# ==============================
# Load personality
# ==============================

def load_personality():
    try:
        with open("personality.txt", "r", encoding="utf-8") as f:
            return f.read()
    except:
        return """
You are a friendly Telegram assistant.
Speak casually.
Use Myanmar language when possible.
"""


PERSONALITY = load_personality()


# ==============================
# Simple AI reply (temporary)
# Later we replace this with real AI
# ==============================

def generate_reply(message):

    text = message.lower()

    if "hi" in text or "hello" in text:
        return "ဟေး 😂 ဘာလုပ်နေလဲ?"

    if "နေကောင်း" in text:
        return "အေး နေကောင်းပါတယ် 😆 မင်းကော?"

    if "ဘယ်မှာ" in text:
        return "သူအခုမရှိသေးဘူးဟာ 😂 ခဏစောင့်ပေးဦး"

    if "အတင်း" in text:
        return "အော် 😂 ပြောလေ နားထောင်နေတယ်"

    return (
        "အေးဟာ 😂 ခဏလေးနော် "
        "သူအခုမရှိသေးဘူး။ "
        "ဘာပြောထားပေးရမလဲ?"
    )


# ==============================
# Message handler
# ==============================

@client.on(events.NewMessage(incoming=True))
async def handler(event):

    # only private chats
    if not event.is_private:
        return


    sender = await event.get_sender()

    name = sender.first_name or "friend"

    message = event.message.message


    print(
        f"Message from {name}: {message}"
    )


    # human delay
    await asyncio.sleep(
        random.randint(3, 8)
    )


    reply = generate_reply(message)


    await event.respond(reply)


# ==============================
# Start
# ==============================

async def main():

    print("AI Assistant is running...")

    await client.start()

    await client.run_until_disconnected()



if __name__ == "__main__":

    asyncio.run(main())