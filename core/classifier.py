import joblib


class IntentClassifier:
    def __init__(self):
        self.model = joblib.load("models/intent_model.pkl")
        self.vectorizer = joblib.load("models/vectorizer.pkl")
        self.chat_keywords = {"what", "how", "why", "who", "tell", "joke", "hello", "hi", "hey", "thanks", "good", "help", "can you", "your name", "where", "recipe", "how to", "what is", "what's", "where am", "where's"}
        self.command_keywords = {"give", "tp", "teleport", "kick", "ban", "op", "deop", "locate", "setblock", "summon", "warp", "find", "search", "nearest", "nearby", "all"}

    def classify(self, text):
        text_lower = text.lower()
        
        if "where am i" in text_lower or "where's" in text_lower:
            return "chat"
        
        if any(kw in text_lower for kw in self.chat_keywords):
            if not any(cmd in text_lower for cmd in ["give", "tp", "teleport", "kick", "ban", "op", "deop", "locate", "setblock", "summon", "warp", "find", "search", "kill"]):
                return "chat"
        
        if any(kw in text_lower for kw in self.command_keywords):
            return "command"
        
        return self.model.predict(self.vectorizer.transform([text]))[0]
