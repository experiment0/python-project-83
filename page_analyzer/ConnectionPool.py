from psycopg2.pool import SimpleConnectionPool
from psycopg2 import pool
from psycopg2.extensions import connection


class ConnectionPool:
    def __init__(self, DATABASE_URL: str) -> None:
        self.DATABASE_URL = DATABASE_URL
        self.connection_pool = self.__get_connection_pool()
    
    def __get_connection_pool(self) -> SimpleConnectionPool:
        return pool.SimpleConnectionPool(1, 10, self.DATABASE_URL)
    
    def __check_connection_pool(self):
        if self.connection_pool.closed:
            self.connection_pool = self.__get_connection_pool()
    
    def get_conn(self) -> connection:
        self.__check_connection_pool()
        conn = self.connection_pool.getconn()
        return conn
    
    def put_conn(self, conn: connection):
        self.connection_pool.putconn(conn)
