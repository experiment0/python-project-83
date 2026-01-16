from psycopg2 import pool
from psycopg2.extensions import connection
from psycopg2.pool import SimpleConnectionPool


class ConnectionPool:
    def __init__(self, database_url: str) -> None:
        self.database_url = database_url
        self.connection_pool = self.__get_connection_pool()
    
    def __get_connection_pool(self) -> SimpleConnectionPool:
        return pool.SimpleConnectionPool(1, 10, self.database_url)
    
    def __check_connection_pool(self):
        # На платформе render.com, где деплоится данный проект,
        # в бесплатном варианте очень неустойчивое соединение с БД,
        # которое закрывается после каждого запроса.
        # Поэтому здесь добавлено пересоздание пула соединений в случае,
        # если оно закрыто.
        if self.connection_pool.closed:
            self.connection_pool = self.__get_connection_pool()
    
    def get_conn(self) -> connection:
        self.__check_connection_pool()
        conn = self.connection_pool.getconn()
        return conn
    
    def put_conn(self, conn: connection):
        self.connection_pool.putconn(conn)
