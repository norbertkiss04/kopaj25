import os
from openai import OpenAI

api_key = "your-default-api-key-here"
base_url = "https://api.openai.com/v1"

client = OpenAI(
    api_key=api_key,
    base_url=base_url
)

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Say this is a test"}
    ]
)

print(response.choices[0].message.content)

# Example using requests library instead of OpenAI client
import requests
import json

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

data = {
    "model": "gpt-3.5-turbo",
    "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Say this is a test"}
    ]
}

response_raw = requests.post(
    f"{base_url}/chat/completions",
    headers=headers,
    json=data
)

if response_raw.status_code == 200:
    content = response_raw.json()["choices"][0]["message"]["content"]
    print(content)
else:
    print(f"Error: {response_raw.status_code} - {response_raw.text}")
