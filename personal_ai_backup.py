import os
import time

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
# AI Control System
# ==========================

# store owner's last message time
owner_activity = {}


# 5 minutes
WAIT_TIME = 300



# ==========================
# Detect Owner Messages
# ==========================

@telegram.on(events.NewMessage(outgoing=True))
async def owner_message(event):

    chat_id = event.chat_id

    owner_activity[chat_id] = time.time()


    print(
        "Owner is chatting with:",
        chat_id
    )



# ==========================
# AI Message Handler
# ==========================

@telegram.on(events.NewMessage(incoming=True))
async def handler(event):


    if event.out:
        return


    chat_id = event.chat_id


    # Check if owner recently talked
    if chat_id in owner_activity:


        elapsed = time.time() - owner_activity[chat_id]


        if elapsed < WAIT_TIME:


            print(
                "Owner is active. AI waiting..."
            )

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

You are a personal Telegram assistant for the owner.

Your personality:

- You are like a close personal assistant.
- Not a chatbot.
- Reply naturally like a human friend.
- Always use Burmese language.
- Be casual and friendly.
- Never say "I am an AI".

When people ask about the owner:

Answer naturally.

Examples:

User:
သူဘာလုပ်နေလဲ

Good answer:
အခုတော့ မရှိသေးဘူးထင်တယ် 😅
ဒီနေ့ schedule ကြည့်ရင် နည်းနည်းအလုပ်များနေတယ်။
လိုရင် message ထားပေးလိုက်မယ်နော်။


User message:

{message}

"""

        )


        reply = response.text



        if not reply:

            reply = "အခုတော့ အဖြေမထုတ်နိုင်သေးဘူးနော်။"



        await event.reply(reply)



        print("\nAI:")
        print(reply)



    except Exception as e:


        print("\nERROR:")
        print(e)



        await event.reply(
            "တစ်ခုခု error ဖြစ်နေပါတယ်။"
        )



# ==========================
# Start Assistant
# ==========================


print("🤖 Myanmar AI Assistant Starting...")


telegram.start()


print("✅ Telegram Connected!")
print("✅ AI Assistant Running!")


telegram.run_until_disconnected()