from memory import *

create_database()


save_message(
    123,
    "user",
    "hello"
)


save_message(
    123,
    "assistant",
    "မင်္ဂလာပါ"
)


print(
    get_history(123)
)