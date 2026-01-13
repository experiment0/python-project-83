from datetime import datetime
from typing import Optional

from psycopg2.extensions import connection
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

from page_analyzer.utils.helpers import get_root_url

URLS_TABLE_NAME = "urls"

UrlType = Annotated[
    AnyUrl, 
    UrlConstraints(
        max_length=255,
        allowed_schemes=["http", "https"],
        host_required=True,
        preserve_empty_path=True,
    )
]


class NewUrlData(BaseModel):
    name: UrlType = Field(description="url корня сайта")
    
    @field_validator("name", mode="before")
    def validate_name(cls, value):
        return get_root_url(value)


class ExistingUrlData(NewUrlData):
    id: int = Field(description="Уникальный идентификатор записи")    
    created_at: datetime = Field(description="Дата и время создания записи")
    
    @computed_field
    def date(self) -> str:
        return self.created_at.strftime("%Y-%m-%d")


class UrlsModel:
    def __init__(self, conn: connection) -> None:
        self.conn = conn
    
    def get_all(self) -> list[ExistingUrlData]:
        with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                f"SELECT * FROM {URLS_TABLE_NAME} ORDER BY created_at DESC"
            )

            return [ExistingUrlData(**dict(item)) for item in cursor.fetchall()]
    
    def save(self, url_data: NewUrlData) -> int:
        url_name = url_data.name.encoded_string()
        
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(
                    f"""INSERT INTO {URLS_TABLE_NAME} (name) 
                    VALUES (%s) 
                    RETURNING id""",
                    (url_name,)
                )
                url_id = cursor.fetchone()[0]
        except Exception:
            self.conn.rollback()
            raise
            
        self.conn.commit()
        
        return url_id
    
    def find_by_id(self, id: int) -> Optional[ExistingUrlData]:
        with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                f"SELECT * FROM {URLS_TABLE_NAME} WHERE id = %s", 
                (id,)
            )
            url_data = cursor.fetchone()

            if url_data is None:
                return None
            
            return ExistingUrlData(**dict(url_data))
    
    def find_by_url(self, url_name: str) -> Optional[ExistingUrlData]:
        with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                f"SELECT * FROM {URLS_TABLE_NAME} WHERE name = %s",
                (url_name,)
            )
            url_data = cursor.fetchone()

            if url_data is None:
                return None
            
            return ExistingUrlData(**dict(url_data))