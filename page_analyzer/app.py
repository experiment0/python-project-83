import os

from dotenv import load_dotenv
from flask import Flask, render_template

# Загружает переменные окружения из файла .env
load_dotenv()

app = Flask(__name__)

# Ключ для подписи форм
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")


@app.route("/")
def home():
    return render_template("home.html")
