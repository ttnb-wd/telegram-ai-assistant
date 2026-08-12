# -*- coding: utf-8 -*-

from google import genai
import os


client = genai.Client(
    api_key=os.environ["GEMINI_API_KEY"]
)


response = client.models.generate_content(
    model="gemini-3.1-flash-lite",
    contents="မြန်မာလို နှုတ်ဆက်စကားတစ်ကြောင်းပြောပါ"
)


print(response.text)