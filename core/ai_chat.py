import requests

API_KEY = "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"

def chat(message, history):
    messages = [{"role": "system", "content": "You are a helpful Minecraft assistant"}]
    for msg in history:
        messages.append({"role": "user", "content": msg})
    messages.append({"role": "user", "content": message})

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "deepseek/deepseek-chat",
            "messages": messages
        }
    )

    return response.json()["choices"][0]["message"]["content"]
