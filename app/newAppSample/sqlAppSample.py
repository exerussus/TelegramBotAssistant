
import sqlite3


class SqlMakeCharacterBot:

    def __init__(self):
        # Обязательно даем название app_name
        self.app_name = "app_name"
        self.conn = sqlite3.connect("../../data/application.db" if __name__ == "__main__" else "data/application.db")
        self.cursor = self.conn.cursor()
        # Тут можно создать необходимую таблицу
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {self.app_name} (user_id INTEGER PRIMARY KEY, "
                            f"something TEXT, "
                            f"another_something TEXT,)")

    def get_something(self, user_id: int):
        self.cursor.execute(f"SELECT * FROM {self.app_name} WHERE user_id = ?", (user_id,))

    def add_something(self, user_id: int, something: str, another_something: str):
        self.cursor.execute(f"INSERT INTO {self.app_name} VALUES (?, ?, ?)", (user_id, something, another_something))

    def do_something(self, user_id: int):
        pass


def do_somthing(user_id: int):
    _classExemplar = SqlMakeCharacterBot()
    _classExemplar.do_something(user_id=user_id)
