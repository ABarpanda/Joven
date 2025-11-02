import os
from google import genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client()

with open("jobDetail.txt", "r", encoding="utf-8") as file:
    contents = file.read()

prompt = "For the given data, create a json data of format : \n\n" + contents

try:
    response = client.models.generate_content(
        model="gemini-2.5-flash", 
        contents="Explain how AI works in a few words"
    )
    print(response)
finally:
    client.close()