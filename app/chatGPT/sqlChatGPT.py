import sqlite3
from datetime import datetime
from tools.debuger import debug_log


class SqlChatModel:

    def __init__(self, debug_mode=True):
        self.conn = sqlite3.connect("../../data/chatModel.db" if __name__ == "__main__" else "data/chatModel.db")
        self.cursor = self.conn.cursor()
        self.debug_mode = debug_mode
        self.cursor.execute("CREATE TABLE IF NOT EXISTS bot (name TEXT PRIMARY KEY)")
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS user_bot ("
            "user_id INTEGER PRIMARY KEY, "
            "bot_name TEXT, "
            "FOREIGN KEY (bot_name) REFERENCES bot(name))")

    def add_new_bot(self, bot_name: str):
        """Добавляет бота в таблицу ботов и создает новую таблицу с именем этого бота"""
        self.cursor.execute("SELECT name FROM bot WHERE name=?", (bot_name,))
        exist = self.cursor.fetchone()
        if not exist:
            self.cursor.execute("INSERT INTO bot VALUES (?)", (bot_name,))
            self.conn.commit()
            self.create_bot_table(bot_name=bot_name)

    def get_bot_for_user(self, user_id: int):
        self.cursor.execute("SELECT bot_name FROM user_bot WHERE user_id=?", (user_id,))
        result = self.cursor.fetchone()
        debug_log(self.debug_mode, text=f"id -> bot_name: {user_id} -> {result}", color="blue")
        return result[0] if result is not None else None

    def get_list_bots_for_users(self):
        self.cursor.execute("SELECT * FROM user_bot")
        return self.cursor.fetchall()

    def set_bot_for_user(self, user_id: int, bot_name: str):
        """Устанавливает бота для конкретного юзера"""
        self.add_new_bot(bot_name=bot_name)
        self.cursor.execute("SELECT * FROM user_bot WHERE user_id=?", (user_id,))
        user_id_exist = self.cursor.fetchone()

        if not user_id_exist:
            self.cursor.execute("INSERT INTO user_bot VALUES (?, ?)", (user_id, bot_name,))
        else:
            self.cursor.execute("UPDATE user_bot SET bot_name = ? WHERE user_id = ?", (bot_name, user_id,))
        self.conn.commit()

    def create_bot_table(self, bot_name):

        self.cursor.execute(f'CREATE TABLE IF NOT EXISTS {bot_name}('
                            'id INTEGER, '
                            'request TEXT, '
                            'response TEXT, '
                            'date TEXT,'
                            'priority INEGER)')
        self.conn.commit()

    def add_to_history(self, request: str, response: str, bot_name: str, priority=1):
        self.cursor.execute(f"SELECT MAX(id) FROM {bot_name}")
        max_id = self.cursor.fetchone()[0]
        new_id = 1 if max_id is None else max_id + 1
        date = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        self.cursor.execute(f"INSERT OR IGNORE INTO {bot_name} (id, request, response, date, priority) VALUES (?, ?, ?, ?, ?)",
                            (new_id, request, response, date, priority))
        self.conn.commit()

    def get_priority_history(self, bot_name: str):
        """Загружает все запросы и ответы из истории сообщений SQL"""
        self.cursor.execute(f'SELECT request, response FROM {bot_name} WHERE priority > 1')
        result = self.cursor.fetchall()
        return result

    def get_operation_history(self, bot_name: str, memory_size: int):
        """Загружает все запросы и ответы из истории сообщений SQL"""
        self.cursor.execute(f'DELETE FROM {bot_name} WHERE priority = 1 AND id NOT IN (SELECT id FROM {bot_name} WHERE priority = 1 ORDER BY id DESC LIMIT {memory_size})')
        self.conn.commit()
        self.cursor.execute(f'SELECT request, response FROM {bot_name} WHERE priority == 1 ORDER BY id DESC LIMIT {memory_size}')
        result = self.cursor.fetchall()
        return reversed(result)

    def delete_last(self, bot_name: str):
        self.cursor.execute(f"SELECT MAX(id) FROM {bot_name}")
        max_id = self.cursor.fetchone()[0]

        self.cursor.execute(f"DELETE FROM {bot_name} WHERE id={max_id}")

        # Сохраняем изменения и закрываем соединение
        self.conn.commit()

    def parser(self, data_list):
        """Создает диалоговую систему запроса и ответа и возвращает её в str"""
        dialog_text = ""
        for req_resp in data_list:
            dialog_text += "Hum:" + req_resp[0] + "\n"
            dialog_text += "A:" + req_resp[1] + "\n"

        return dialog_text

    def get_dialog_model(self, bot_name: str):
        """Возвращает модель запроса и ответа в виде диалога"""
        return self.parser(self.get_priority_history(bot_name=bot_name))

    def get_operation_memory(self, bot_name: str, memory_size: int):
        return self.parser(self.get_operation_history(bot_name=bot_name, memory_size=memory_size))


def add_operation_memory(request: str, response: str, bot_name: str):
    _classExemplar = SqlChatModel()
    _classExemplar.add_to_history(request=request, response=response, bot_name=bot_name, priority=1)
    _classExemplar.conn.close()


def get_operation_memory(bot_name: str, memory_size: int):
    _classExemplar = SqlChatModel()
    operation_memory = _classExemplar.get_operation_memory(bot_name=bot_name, memory_size=memory_size)
    _classExemplar.conn.close()
    return operation_memory


def get_dict_bots_for_users():
    _classExemplar = SqlChatModel()
    bots_for_users_list = _classExemplar.get_list_bots_for_users()
    _classExemplar.conn.close()
    return dict(bots_for_users_list)


def get_bot_for_user(user_id: int) -> str:
    _classExemplar = SqlChatModel()
    result = _classExemplar.get_bot_for_user(user_id=user_id)
    _classExemplar.conn.close()
    return result


def get_priority_memory(user_id: int) -> str:
    _classExemplar = SqlChatModel()
    bot_name = _classExemplar.get_bot_for_user(user_id=user_id)
    result = _classExemplar.get_dialog_model(bot_name=bot_name)
    _classExemplar.conn.close()
    return result


def delete_last(user_id: int) -> None:
    _classExemplar = SqlChatModel()
    bot_name = _classExemplar.get_bot_for_user(user_id=user_id)
    _classExemplar.delete_last(bot_name=bot_name)
    _classExemplar.conn.close()


def save_dialog(user_id: int, request: str, response: str, priority=1) -> None:
    _classExemplar = SqlChatModel()
    bot_name = _classExemplar.get_bot_for_user(user_id=user_id)
    _classExemplar.add_to_history(request=request, response=response, bot_name=bot_name, priority=priority)
    _classExemplar.conn.close()


def set_bot_for_user(user_id: int, bot_name: str):
    _classExemplar = SqlChatModel()
    _classExemplar.set_bot_for_user(user_id=user_id, bot_name=bot_name)
    _classExemplar.conn.close()


if __name__ == "__main__":
    _user_id = 1557628538
    _memory_size = 16
    _bot_name = "agny"
    print(get_priority_memory(_user_id) + get_operation_memory(_bot_name, _memory_size))
