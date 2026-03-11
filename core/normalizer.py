def normalize(text):
    text = text.lower()
    replacements = {
        "teleport": "tp",
        "blocks": "block",
        "diamonds": "diamond",
        "me": "@s"
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text
