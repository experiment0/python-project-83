import os
from enum import Enum

import requests
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
from page_analyzer.models import (
    MixedModel,
    NewUrlCheckData,
    NewUrlData,
    UrlChecksModel,
    UrlsModel,
)
from page_analyzer.utils.helpers import get_page_seo_info

# Загружает переменные окружения из файла .env
load_dotenv()

app = Flask(__name__)

# Ключ для подписи форм
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
# Урл базы данных
DATABASE_URL = os.getenv("DATABASE_URL")

# Объект для организации пула соединений с БД
connection_pool = ConnectionPool(DATABASE_URL)
# Объект для взаимодействия с таблицей urls
urls_model = UrlsModel(connection_pool)
# Объект для взаимодействия с таблицей url_checks
url_checks_model = UrlChecksModel(connection_pool)
# Объект для получения результатов запросов, которые объединяют обе таблицы
mixed_model = MixedModel(connection_pool)


# Категории flash-сообщений. 
# Тип соответствует имени класса сообщения в bootstrap
class MessageCategory(Enum):
    SUCCESS = "success"
    DANGER = "danger"
    INFO = "info"


ERROR_TEMPLATE = "error.html"


@app.route("/")
def index():
    return render_template("urls/new.html")


@app.route("/urls")
def urls_get():
    last_url_checks = mixed_model.get_last_url_checks()
    
    return render_template(
        "urls/index.html",
        last_url_checks=last_url_checks,
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
        url_data = urls_model.find_by_url(new_url_data.name_str)
        
        if url_data is None:
            raise ValueError("url не найден в таблице")
        
        url_id = url_data.id
        flash("Страница уже существует", MessageCategory.INFO.value)
        
        return redirect(url_for("urls_show", id=url_id))
        
    except Exception as error:
        app.logger.error(f"Ошибка при добавлении url '{url}': {error}")
        
        return render_template(ERROR_TEMPLATE), 422


@app.route("/urls/<id>")
def urls_show(id):
    url_data = urls_model.find_by_id(id)
    
    if url_data is None:
        abort(404)
    
    url_checks_data = url_checks_model.get_all_checks_for_url(url_data.id)
        
    messages = get_flashed_messages(with_categories=True)
    
    return render_template(
        "urls/show.html",
        url_data=url_data,
        url_checks_data=url_checks_data,
        messages=messages,
    )


@app.post("/urls/<id>/checks")
def urls_checks_post(id):
    url_data = urls_model.find_by_id(id)
    
    if url_data is None:
        return render_template(ERROR_TEMPLATE), 422
    
    try:
        response = requests.get(url_data.name_str)
        response.raise_for_status()
        
        page_seo_info = get_page_seo_info(response.text)        
        url_check_data = NewUrlCheckData(
            url_id=id,
            status_code=response.status_code,
            h1=page_seo_info.h1,
            title=page_seo_info.title,
            description=page_seo_info.description,
        )
        url_checks_model.save(url_check_data)        
        flash("Страница успешно проверена", MessageCategory.SUCCESS.value)
        
        return redirect(url_for("urls_show", id=id))

    except requests.exceptions.RequestException as error:
        error_first_word = str(error).split()[0]
        response_status = \
            error_first_word if error_first_word.isdigit() else None
        
        return render_template(
            ERROR_TEMPLATE,
            response_status=response_status,
        )
    
    except Exception:
        flash("Произошла ошибка при проверке", MessageCategory.DANGER.value)
        
        return redirect(url_for("urls_show", id=id))


@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run()
