from datetime import datetime
from typing import Optional

from psycopg2.extras import RealDictCursor
from pydantic import (
    BaseModel,
    Field,
    computed_field,
)

from page_analyzer.ConnectionPool import ConnectionPool


class LastUrlCheck(BaseModel):
    url_id: int = Field(description="Идентификатор url")
    name: str = Field(description="url главной страницы сайта")
    status_code: Optional[int] = Field(
        description="Статус последней проверки", default=None,
    )
    created_at: Optional[datetime] = Field(
        description="Дата и время последней проверки", default=None,
    )
    
    # Создадим дополнительное поле для отображения даты события в интерфейсе
    @computed_field
    def date(self) -> str:
        return "" if self.created_at is None \
            else self.created_at.strftime("%Y-%m-%d")
    
    # Для пустого статуса ответа будем отображать пустую строку вместо None
    @computed_field
    def status(self) -> str:
        return "" if self.status_code is None else str(self.status_code)
    

class MixedModel:
    def __init__(self, connection_pool: ConnectionPool) -> None:
        self.connection_pool = connection_pool
    
    def get_last_url_checks(self) -> list[LastUrlCheck]:
        conn = self.connection_pool.get_conn()
        
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                # В данном запросе нужно расположить новые записи выше.
                # Поскольку id записи в общем случае не должен соответствовать 
                # порядку записей, то сортируем их по времени добавления.
                cursor.execute(
                    """SELECT url_id, name, status_code, created_at FROM (
                            SELECT 
                                urls.id as url_id,
                                urls.name ,
                                url_checks.status_code,		
                                url_checks.created_at,
                                ROW_NUMBER() OVER(
                                    PARTITION BY urls.id 
                                    ORDER BY url_checks.created_at DESC
                                ) AS url_check_order
                            FROM urls
                                LEFT JOIN url_checks 
                                ON urls.id = url_checks.url_id
                            ORDER BY
                                urls.created_at DESC, 
                                url_checks.created_at DESC
                        ) AS all_url_checks
                        WHERE url_check_order = 1;"""
                )
                return [
                    LastUrlCheck(**dict(item)) for item in cursor.fetchall()
                ]
        finally:
            self.connection_pool.put_conn(conn)
