import sqlite3
from datetime import datetime


class SqlChatModel:

    def __init__(self, name_bot):
        # Открываем соединение с базой данных
        self.nameBot = name_bot
        self.conn = sqlite3.connect("../data/chatModel.db" if __name__ == "__main__" else "data/chatModel.db")
        self.cursor = self.conn.cursor()

    def create_table(self, bot_name):

        self.cursor.execute('CREATE TABLE IF NOT EXISTS ' + bot_name + '(id INTEGER, request TEXT, response TEXT, date TEXT)')
        self.conn.commit()
        self.conn.close()

    def add_to_history(self, request, response):
        # Получаем максимальный id из таблицы и добавляем 1
        self.cursor.execute(f"SELECT MAX(id) FROM {self.nameBot}")
        max_id = self.cursor.fetchone()[0]
        new_id = 1 if max_id is None else max_id + 1

        # Получаем актуальную дату и время в формате YYYY-MM-DD HH:MM:SS
        date = datetime.now().strftime('%d-%m-%Y %H:%M:%S')

        # Вставляем новую запись в таблицу
        self.cursor.execute(f"INSERT OR IGNORE INTO {self.nameBot} (id, request, response, date) VALUES (?, ?, ?, ?)",
                  (new_id, request, response, date))

        # Сохраняем изменения и закрываем соединение
        self.conn.commit()
        self.conn.close()

    def return_history(self):
        """Загружает все запросы и ответы из истории сообщений SQL"""
        self.cursor.execute(f'SELECT request, response FROM {self.nameBot}')
        result = self.cursor.fetchall()
        return result

    def delete_last(self):
        self.cursor.execute(f"SELECT MAX(id) FROM {self.nameBot}")
        max_id = self.cursor.fetchone()[0]

        self.cursor.execute(f"DELETE FROM {self.nameBot} WHERE id={max_id}")

        # Сохраняем изменения и закрываем соединение
        self.conn.commit()
        self.conn.close()

    def parser(self, data_list):
        """Создает диалоговую систему запроса и ответа и возвращает её в str"""
        dialog_text = ""
        for req_resp in data_list:
            dialog_text += "Hum:" + req_resp[0] + "\n"
            dialog_text += "A:" + req_resp[1] + "\n"

        return dialog_text

    def return_dialog_model(self):
        """Возвращает модель запроса и ответа в виде диалога"""
        return self.parser(self.return_history())


def create_new_table_bot(bot_name: str):
    _classExemplar = SqlChatModel(bot_name)
    _classExemplar.create_table(bot_name)


def return_dialog_model(bot_name: str) -> str:
    _classExemplar = SqlChatModel(bot_name)
    return _classExemplar.return_dialog_model()


def delete_last(bot_name: str) -> None:
    _classExemplar = SqlChatModel(bot_name)
    _classExemplar.delete_last()


def save_dialog(bot_name: str, request: str, response: str) -> None:
    _classExemplar = SqlChatModel(bot_name)
    _classExemplar.add_to_history(request, response)


if __name__ == "__main__":
    new_bot_table_name = input("Введите имя бота: ")
    create_new_table_bot(new_bot_table_name)
