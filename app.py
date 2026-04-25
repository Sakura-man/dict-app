from fastapi import FastAPI
import json

app = FastAPI()

# 辞書読み込み
with open("dictionary.json", "r", encoding="utf-8") as f:
    dictionary = json.load(f)

def translate_word(word):
    word = word.lower()

    # 否定
    if word == "not":
        return "no"

    # 過去形（例: liked → like-ta）
    if word.endswith("ed"):
        base = word[:-2]
        return dictionary.get(base, base) + "-ta"

    # 複数形（例: apples → apple-ra）
    if word.endswith("s"):
        base = word[:-1]
        return dictionary.get(base, base) + "-ra"

    # 通常変換
    return dictionary.get(word, word)

def translate_sentence(text):
    words = text.lower().split()

    # SVOそのまま変換
    result = " ".join(translate_word(w) for w in words)

    return result

@app.get("/translate")
def translate(text: str):
    return translate_sentence(text)