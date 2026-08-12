import os
import zipfile
from datetime import datetime

from telethon import TelegramClient
from telethon.sessions import StringSession


# ==========================
# Telegram Secrets
# ==========================

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION = os.getenv("TELEGRAM_SESSION")


# ==========================
# Backup File
# ==========================

DATABASE = "memory.db"


def create_backup():

    filename = (
        f"memory_backup_"
        f"{datetime.now().strftime('%Y-%m-%d_%H-%M')}.zip"
    )


    with zipfile.ZipFile(
        filename,
        "w"
    ) as zipf:

        zipf.write(
            DATABASE
        )


    return filename



async def main():

    backup_file = create_backup()


    telegram = TelegramClient(
        StringSession(SESSION),
        API_ID,
        API_HASH
    )


    await telegram.start()


    me = await telegram.get_me()


    print(
        "Connected:",
        me.first_name
    )


    await telegram.send_file(
        "me",
        backup_file,
        caption=
        "🤖 Metro AI Memory Backup\n"
        +
        datetime.now().strftime(
            "%Y-%m-%d %H:%M"
        )
    )


    print(
        "Backup sent successfully"
    )


    await telegram.disconnect()



with telegram:
    telegram.loop.run_until_complete(main())