import os

from dotenv import load_dotenv
from flask import Flask

# Загружает переменные окружения из файла .env
load_dotenv()

app = Flask(__name__)

# Ключ для подписи форм
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")


@app.route("/")
def run():
    return "Page analyzer"
