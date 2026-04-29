from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import json
from fastapi.responses import PlainTextResponse

app = FastAPI()


def load_dictionary():
    try:
        with open("dictionary.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}


def translate_word(word):
    dictionary = load_dictionary()
    word = word.strip()

    if word in dictionary:
        return dictionary[word]

    w = word.lower()

    if w == "not":
        return "no"

    if w.endswith("ed"):
        base = w[:-2]
        return dictionary.get(base, base) + "-ta"

    if w.endswith("s"):
        base = w[:-1]
        return dictionary.get(base, base) + "-ra"

    return dictionary.get(w, word)


def translate_sentence(text):
    words = text.split()
    return " ".join(translate_word(w) for w in words)


# UIページ
@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>架空言語翻訳</title>

        <!-- フォント -->
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
                color: #333;
            }
        </style>
    </head>
    <body>

        <h1>架空言語翻訳</h1>

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