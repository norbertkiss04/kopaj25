import requests

TOKEN = "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"

def ask_ai(text_input, response_format=None):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {TOKEN}'
    }
    body = {
        "model": "x-ai/grok-4-fast",
        "messages": [{"role": "user", "content": text_input}]
    }
    if response_format is not None:
        body["response_format"] = response_format

    try:
        response = requests.post(url, json=body, headers=headers, timeout=30)
        chat_completion = response.json()
        if 'error' in chat_completion:
            print(f"Error from AI service: {chat_completion['error']['message']}")
            return None
        return chat_completion['choices'][0]['message']['content']
    except requests.exceptions.RequestException as e:
        print(f"Error from AI service: {e}")
        return None
    except ValueError as e:
        print(f"Error from AI service: {e}")
        return None
