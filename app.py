from fastapi import FastAPI
from fastapi.responses import HTMLResponse, PlainTextResponse
import json

app = FastAPI()


# 辞書読み込み
def load_dictionary():
    try:
        with open("dictionary.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}


# 日本語 → 亜語変換（リスト対応版）
def translate_word(word):
    dictionary = load_dictionary()
    word = word.strip()

    # 日本語がリストに含まれているか探す
    for conlang, jp_list in dictionary.items():
        if word in jp_list:
            return conlang

    return word


# 文変換
def translate_sentence(text):
    dictionary = load_dictionary()
    
    result = []
    i = 0
    text = text.strip()

    # 長い単語を優先してマッチ
    jp_words = []
    for v in dictionary.values():
        jp_words.extend(v)
    jp_words = sorted(jp_words, key=len, reverse=True)

    while i < len(text):
        matched = False

        for word in jp_words:
            if text.startswith(word, i):
                result.append(translate_word(word))
                i += len(word)
                matched = True
                break

        if not matched:
            result.append(text[i])
            i += 1

    return " ".join(result)

# UI
@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>亜語翻訳</title>

        <link href="https://fonts.googleapis.com/css2?family=Noto+Sans&display=swap" rel="stylesheet">

        <style>
            body {
                font-family: 'Noto Sans', sans-serif;
                text-align: center;
                margin-top: 100px;
                background: #f5f5f5;
            }

            input {
                font-size: 20px;
                padding: 10px;
                width: 300px;
            }

            button {
                font-size: 18px;
                padding: 10px 20px;
                margin-left: 10px;
            }

            #result {
                margin-top: 30px;
                font-size: 24px;
            }
        </style>
    </head>
    <body>

        <h1>亜語翻訳機</h1>

        <input id="text" placeholder="文章を入力">
        <button onclick="runTranslate()">翻訳</button>

        <div id="result"></div>

        <script>
            async function runTranslate() {
                const text = document.getElementById("text").value;
                const res = await fetch(`/translate?text=${encodeURIComponent(text)}`);
                const data = await res.text();
                document.getElementById("result").innerText = data;
            }
        </script>

    </body>
    </html>
    """


# API
@app.get("/translate", response_class=PlainTextResponse)
def translate(text: str):
    return translate_sentence(text)