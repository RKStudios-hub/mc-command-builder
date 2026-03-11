from rapidfuzz import process, fuzz
import re


class Resolver:
    def __init__(self, values):
        self.values = values
        self.simple = [v.split(":")[-1] for v in values]
        self.simple_set = set(self.simple)

    def _find_best_match(self, text):
        text_clean = re.sub(r'[^a-z0-9_]', '', text.lower())
        if not text_clean:
            return None
        
        match = process.extractOne(
            text_clean,
            self.simple,
            scorer=fuzz.WRatio
        )
        if match and match[1] > 70:
            return match[0]
        return None

    def resolve(self, text):
        text_lower = text.lower()
        
        words = re.findall(r'[a-zA-Z_][a-zA-Z0-9_]*', text_lower)
        
        combined = "_".join(words)
        if combined in self.simple_set:
            index = self.simple.index(combined)
            return self.values[index]
        
        for i in range(len(words), 0, -1):
            for j in range(len(words) - i + 1):
                combo = "_".join(words[j:j+i])
                if combo in self.simple_set:
                    index = self.simple.index(combo)
                    return self.values[index]
        
        for word in reversed(words):
            if len(word) > 2:
                if word in self.simple_set:
                    index = self.simple.index(word)
                    return self.values[index]
        
        for word in reversed(words):
            if len(word) > 2:
                best = self._find_best_match(word)
                if best:
                    index = self.simple.index(best)
                    return self.values[index]
        
        return None
