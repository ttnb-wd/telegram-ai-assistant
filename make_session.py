import os
from telethon.sync import TelegramClient
from telethon.sessions import StringSession

API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]

with TelegramClient("my_account", API_ID, API_HASH) as client:
    string_session = StringSession.save(client.session)

print("\n" + "=" * 60)
print("YOUR TELEGRAM SESSION STRING")
print("=" * 60)
print(string_session)
print("=" * 60)
print("\nDO NOT SHARE THIS STRING WITH ANYONE.")