import os
import json
import time

from telethon import TelegramClient, events
from telethon.sessions import StringSession

from google import genai

from memory import (
    create_database,
    save_message,
    get_history
)


# ==========================
# Load JSON Data
# ==========================

with open("owner.json", "r", encoding="utf-8") as f:
    owner = json.load(f)


with open("personality.json", "r", encoding="utf-8") as f:
    personality = json.load(f)



# ==========================
# Telegram Secrets
# ==========================

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
SESSION = os.getenv("TELEGRAM_SESSION")


if not API_ID:
    raise ValueError("Missing API_ID")


if not API_HASH:
    raise ValueError("Missing API_HASH")


if not SESSION:
    raise ValueError("Missing TELEGRAM_SESSION")


API_ID = int(API_ID)



# ==========================
# Gemini
# ==========================

GEMINI_KEY = os.getenv("GEMINI_API_KEY")


if not GEMINI_KEY:
    raise ValueError("Missing GEMINI_API_KEY")


ai = genai.Client(
    api_key=GEMINI_KEY
)



# ==========================
# Database
# ==========================

create_database()



# ==========================
# Telegram Client
# ==========================

telegram = TelegramClient(
    StringSession(SESSION),
    API_ID,
    API_HASH
)



# ==========================
# Owner Activity
# ==========================

owner_activity = {}

WAIT_TIME = 300



# ==========================
# Detect Owner Message
# ==========================

@telegram.on(events.NewMessage(outgoing=True))
async def owner_message(event):

    owner_activity[event.chat_id] = time.time()



# ==========================
# AI Handler
# ==========================

@telegram.on(events.NewMessage(incoming=True))
async def handler(event):


    chat_id = event.chat_id


    # Ignore owner messages
    if event.out:
        return



    # Owner recently chatting
    if chat_id in owner_activity:


        if time.time() - owner_activity[chat_id] < WAIT_TIME:

            print(
                "Owner active. AI sleeping..."
            )

            return



    message = event.message.message


    if not message:
        return



    print("\nUSER:")
    print(message)



    # Save user message

    save_message(
        chat_id,
        "user",
        message
    )



    # Load history

    history = get_history(
        chat_id,
        10
    )


    history_text = ""


    for role, text in history:

        history_text += (
            f"{role}: {text}\n"
        )



    prompt = f"""

You are Metro AI.


Owner:

Name:
{owner["name"]}


Owner personality:

{owner["personality"]}


Owner speaking style:

{owner["speaking_style"]}



Your personality:

{personality["style"]}

Rules:

{personality["rules"]}



Conversation memory:

{history_text}



Instructions:

- Reply in Burmese mixed English naturally.
- Talk like a close friend.
- Do not sound like an AI.
- Do not say you are AI.
- Be casual.
- Use humor sometimes.
- If asked about owner, answer naturally.



User message:

{message}

"""



    try:


        response = ai.models.generate_content(

            model="gemini-flash-latest",

            contents=prompt

        )


        reply = response.text



        if not reply:

            reply = "ခဏနော် 😅"



        await event.reply(reply)



        save_message(
            chat_id,
            "assistant",
            reply
        )



        print("\nAI:")
        print(reply)



    except Exception as e:


        print(
            "ERROR:",
            e
        )



# ==========================
# Start
# ==========================

print(
    "🤖 Metro AI Starting..."
)


telegram.start()


print(
    "✅ Telegram Connected"
)


print(
    "✅ Memory System Active"
)


telegram.run_until_disconnected()