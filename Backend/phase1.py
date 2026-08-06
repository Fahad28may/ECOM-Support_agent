from dotenv import load_dotenv
load_dotenv()

import os
from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)

response = client.chat.completions.create(
    model="nvidia/nemotron-3-ultra-550b-a55b:free",
    max_tokens=500,
    messages=[
        {"role": "user", "content": "Do you ship to Lahore and how long does it take?"}
    ],
)

print(response.choices[0].message.content)