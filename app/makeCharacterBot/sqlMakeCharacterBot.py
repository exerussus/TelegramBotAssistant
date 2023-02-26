import sqlite3
from datetime import datetime


class SqlMakeCharacterBot:

    def __init__(self):
        # Открываем соединение с базой данных
        self.conn = sqlite3.connect("../../data/application.db" if __name__ == "__main__" else "data/application.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS makeCharacterBot (user_id INTEGER PRIMARY KEY, "
                            "last_request TEXT,"
                            "last_response TEXT)")

    def is_user_exist(self, user_id: int):
        self.cursor.execute("SELECT * FROM makeCharacterBot WHERE user_id = ?", (user_id,))
        return True if self.cursor.fetchone() is not None else False

    def add_user_to_table_if_not_exist(self, user_id: int):
        if not self.is_user_exist(user_id=user_id):
            self.cursor.execute(f"INSERT OR IGNORE INTO makeCharacterBot (user_id, last_request, last_response) VALUES "
                                f"(?, ?, ?)", (user_id, "None", "None"))

    def set_last_response(self, user_id: int, last_response: str):
        self.add_user_to_table_if_not_exist(user_id=user_id)
        result = (last_response, user_id)
        self.cursor.execute("UPDATE makeCharacterBot SET last_response = ? WHERE user_id = ?", result)
        self.conn.commit()

    def get_last_response(self, user_id: int):
        self.cursor.execute("SELECT last_response FROM makeCharacterBot WHERE user_id = ?", (user_id,))
        last_response = self.cursor.fetchone()[0]
        return last_response

    def set_last_request(self, user_id: int, last_request: str):
        self.add_user_to_table_if_not_exist(user_id=user_id)
        result = (last_request, user_id)
        self.cursor.execute("UPDATE makeCharacterBot SET last_request = ? WHERE user_id = ?", result)
        self.conn.commit()

    def get_last_request(self, user_id: int):
        self.cursor.execute("SELECT last_request FROM makeCharacterBot WHERE user_id = ?", (user_id,))
        last_request = self.cursor.fetchone()[0]
        return last_request


def set_last_response(user_id: int, last_response: str):
    _classExemplar = SqlMakeCharacterBot()
    _classExemplar.set_last_response(user_id=user_id, last_response=last_response)
    _classExemplar.conn.close()


def get_last_response(user_id: int):
    _classExemplar = SqlMakeCharacterBot()
    last_response = _classExemplar.get_last_response(user_id=user_id)
    _classExemplar.conn.close()
    return last_response


def set_last_request(user_id: int, last_request: str):
    _classExemplar = SqlMakeCharacterBot()
    _classExemplar.set_last_request(user_id=user_id, last_request=last_request)
    _classExemplar.conn.close()


def get_last_request(user_id: int):
    _classExemplar = SqlMakeCharacterBot()
    last_request = _classExemplar.get_last_request(user_id=user_id)
    _classExemplar.conn.close()
    return last_request
