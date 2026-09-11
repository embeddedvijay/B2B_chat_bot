class LanguageService:
    def detect(self, text: str) -> str:
        if any("\u0900" <= char <= "\u097f" for char in text):
            return "hi"
        common_hinglish = {"hai", "nahi", "mera", "kaise", "kya", "karna", "issue"}
        words = set(text.lower().split())
        return "hinglish" if words.intersection(common_hinglish) else "en"
