import os
from enum import Enum

from dotenv import load_dotenv
from flask import (
    Flask,
    abort,
    flash,
    get_flashed_messages,
    redirect,
    render_template,
    request,
    url_for,
)
from psycopg2.errors import UniqueViolation
from pydantic_core._pydantic_core import (
    ValidationError as PydanticValidationError,
)

from page_analyzer.ConnectionPool import ConnectionPool
from page_analyzer.models import NewUrlData, UrlsModel

# Загружает переменные окружения из файла .env
load_dotenv()

app = Flask(__name__)

# Ключ для подписи форм
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

# Урл базы данных
DATABASE_URL = os.getenv("DATABASE_URL")

connection_pool = ConnectionPool(DATABASE_URL)
urls_model = UrlsModel(connection_pool)


class MessageCategory(Enum):
    SUCCESS = "success"
    DANGER = "danger"
    INFO = "info"
    

@app.route("/")
def index():
    return render_template("urls/new.html")


@app.route("/urls")
def urls_get():
    urls = urls_model.get_all()
    
    return render_template(
        "urls/index.html",
        urls=urls,
    )


@app.post("/urls")
def urls_post():
    url_data = request.form.to_dict()
    url = url_data["url"]
    
    try:
        new_url_data = NewUrlData(name=url)
        url_id = urls_model.save(new_url_data)
        flash("Страница успешно добавлена", MessageCategory.SUCCESS.value)
        
        return redirect(url_for("urls_show", id=url_id))
    
    except PydanticValidationError:        
        return render_template(
            "urls/new.html",
            messages=[(MessageCategory.DANGER.value, "Некорректный URL")],
            url=url,
        ), 422
    
    except UniqueViolation:
        url_data = urls_model.find_by_url(url)
        
        if url_data is None:
            raise ValueError("url не найден в таблице")
        
        url_id = url_data.id
        flash("Страница уже существует", MessageCategory.INFO.value)
        
        return redirect(url_for("urls_show", id=url_id))
        
    except Exception as error:
        app.logger.error(f"Ошибка при добавлении url '{url}': {error}")
        
        return render_template("error.html"), 422


@app.route("/urls/<id>")
def urls_show(id):
    url_data = urls_model.find_by_id(id)
    
    if url_data is None:
        abort(404)
        
    messages = get_flashed_messages(with_categories=True)
    
    return render_template(
        "urls/show.html",
        url_data=url_data,
        messages=messages,
    )


@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404
