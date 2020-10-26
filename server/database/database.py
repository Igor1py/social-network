import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2.errors import UniqueViolation, ProgrammingError

class Database:
    
    def __init__(self, **kwargs):
        self._connection = psycopg2.connect(**kwargs)
        self._cursor = self._connection.cursor(
            cursor_factory=RealDictCursor
        )

    def rollback(self):
        self._connection.rollback()
    
    def execute(self, query, params={}):
        try:
            self._cursor.execute(query, params)
        except UniqueViolation:
            self.rollback()

    def execute_and_commit(self, query, params={}):
        self.execute(query, params)
        self._connection.commit()
    
    def fetch_one(self, query, params={}):
        self.execute(query, params)
        try:
            return self._cursor.fetchone()
        except ProgrammingError:
            return {}
    
    def fetch_all(self, query, params={}):
        self.execute(query, params)
        return self._cursor.fetchall()
    
    def execute_with_returning(self, query, params={}):
        value = self.fetch_one(query, params)
        self._connection.commit()
        return value
