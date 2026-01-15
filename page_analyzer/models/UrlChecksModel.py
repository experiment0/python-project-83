from datetime import datetime
from typing import Optional

from psycopg2.extras import RealDictCursor
from pydantic import (
    BaseModel,
    Field,
    computed_field,
    field_validator,
)

from page_analyzer.ConnectionPool import ConnectionPool
from page_analyzer.utils.helpers import crop_text


# Тип для новых данных, которые получаем при парсинге данных урла
class NewUrlCheckData(BaseModel):
    url_id: int = Field(
        description="id записи с данными url, для которого делаем проверку",
    )
    status_code: int = Field(
        description="Статус ответа",
    )
    h1: Optional[str] = Field(
        description="Заголовок h1 на странице", default=None,
    )
    title: Optional[str] = Field(
        description="Содержимое тега title страницы", default=None,
    )
    description: Optional[str] = Field(
        description="Содержимое meta-тега description", default=None,
    )
    
    # Обрежем текст до 255 символов
    @field_validator("h1", "title", "description", mode="before")
    def validate_texts(cls, value):
        return crop_text(value)


# Тип для существующих данных, которые мы получаем из таблицы
class ExistingUrlCheckData(NewUrlCheckData):
    id: int = Field(description="Уникальный идентификатор записи")    
    created_at: datetime = Field(description="Дата и время создания записи")
    
    # Создадим дополнительное поле для отображения даты события в интерфейсе
    @computed_field
    def date(self) -> str:
        return self.created_at.strftime("%Y-%m-%d")
    
    # Во вьюхах будем отображать пустую строку вместо None
    @field_validator("h1", "title", "description", mode="after")
    def validate_texts(cls, value) -> str:
        return "" if value is None else value


class UrlChecksModel:
    def __init__(self, connection_pool: ConnectionPool) -> None:
        self.connection_pool = connection_pool
    
    def get_all_checks_for_url(self, url_id: int) -> list[ExistingUrlCheckData]:
        conn = self.connection_pool.get_conn()
        
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    """SELECT * 
                    FROM url_checks
                    WHERE url_id=%s 
                    ORDER BY created_at DESC""",
                    (url_id,)
                )
                return [
                    ExistingUrlCheckData(**dict(item)) 
                    for item in cursor.fetchall()
                ]
        finally:
            self.connection_pool.put_conn(conn)
    
    def save(self, url_check_data: NewUrlCheckData) -> int:
        conn = self.connection_pool.get_conn()
        is_error = False
        
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """INSERT INTO url_checks
                        (url_id, status_code, h1, title, description) 
                    VALUES 
                        (%s, %s, %s, %s, %s) 
                    RETURNING id""",
                    (
                        url_check_data.url_id,
                        url_check_data.status_code,
                        url_check_data.h1,
                        url_check_data.title,
                        url_check_data.description,
                    )
                )
                url_id = cursor.fetchone()[0]
        except Exception:
            conn.rollback()
            is_error = True
            raise
        finally:
            if not is_error:
                conn.commit()
            self.connection_pool.put_conn(conn)
        
        return url_id