import requests

PROXY_IP = "172.22.89.120"
PROXY_PORT = 4000
TOKEN = "sk-XC8ushILNmfCZObBw_WMlQ"

def ask_ai(text_input):
    url = f"http://{PROXY_IP}:{PROXY_PORT}/v1/chat/completions"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {TOKEN}'
    }
    body = {
        "model": "gpt-4.1-nano",
        "messages": [{"role": "user", "content": text_input}]
    }

    try:
        response = requests.post(url, json=body, headers=headers)
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

# Example usage
if __name__ == "__main__":
    response = ask_ai("Say this is a test")
    if response:
        print(response)
