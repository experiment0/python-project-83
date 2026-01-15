from datetime import datetime
from typing import Optional

from psycopg2.extras import RealDictCursor
from pydantic import (
    AnyUrl,
    BaseModel,
    Field,
    UrlConstraints,
    computed_field,
    field_validator,
)
from typing_extensions import Annotated

from page_analyzer.ConnectionPool import ConnectionPool
from page_analyzer.utils.helpers import get_root_url

# Правила, которым должен соответствовать url, добавляемый в модель
UrlType = Annotated[
    AnyUrl, 
    UrlConstraints(
        max_length=255,
        allowed_schemes=["http", "https"],
        host_required=True,
        preserve_empty_path=True,
    )
]


# Тип для новых данных, которые мы добавляем из формы
class NewUrlData(BaseModel):
    name: UrlType = Field(description="url корня сайта")
    
    # Перед добавлением в модель оставим от url только путь до корня сайта
    @field_validator("name", mode="before")
    def validate_name(cls, value):
        return get_root_url(value)
    
    @computed_field
    def name_str(self) -> str:
        return self.name.encoded_string()


# Тип для существующих данных, которые мы получаем из таблицы
class ExistingUrlData(NewUrlData):
    id: int = Field(description="Уникальный идентификатор записи")    
    created_at: datetime = Field(description="Дата и время создания записи")
    
    # Создадим дополнительное поле для отображения даты события в интерфейсе
    @computed_field
    def date(self) -> str:
        return self.created_at.strftime("%Y-%m-%d")


class UrlsModel:
    def __init__(self, connection_pool: ConnectionPool) -> None:
        self.connection_pool = connection_pool
    
    def save(self, url_data: NewUrlData) -> int:
        conn = self.connection_pool.get_conn()
        is_error = False
        
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO urls (name) VALUES (%s) RETURNING id",
                    (url_data.name_str,)
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
    
    def find_by_id(self, id: int) -> Optional[ExistingUrlData]:
        conn = self.connection_pool.get_conn()
        
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    "SELECT * FROM urls WHERE id = %s", 
                    (id,)
                )
                url_data = cursor.fetchone()

                if url_data is None:
                    return None
                
                return ExistingUrlData(**dict(url_data))
        finally:
            self.connection_pool.put_conn(conn)
    
    def find_by_url(self, url_name: str) -> Optional[ExistingUrlData]:
        conn = self.connection_pool.get_conn()
        
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    "SELECT * FROM urls WHERE name = %s",
                    (url_name,)
                )
                url_data = cursor.fetchone()

                if url_data is None:
                    return None
                
                return ExistingUrlData(**dict(url_data))
        finally:
            self.connection_pool.put_conn(conn)
