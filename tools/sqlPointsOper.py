import sqlite3
from datetime import datetime


class SqlAnyaPoint:

    def __init__(self):
        # Открываем соединение с базой данных
        self.conn = sqlite3.connect("../data/points.db" if __name__ == "__main__" else "data/points.db")
        self.cursor = self.conn.cursor()

    def add_to_history(self, points, comment):
        # Получаем максимальный id из таблицы и добавляем 1
        self.cursor.execute("SELECT MAX(id) FROM history")
        max_id = self.cursor.fetchone()[0]
        new_id = 1 if max_id is None else max_id + 1

        # Получаем актуальную дату и время в формате YYYY-MM-DD HH:MM:SS
        date = datetime.now().strftime('%d-%m-%Y %H:%M:%S')

        # Вставляем новую запись в таблицу
        self.cursor.execute("INSERT OR IGNORE INTO history (id, points, comment, date) VALUES (?, ?, ?, ?)",
                  (new_id, points, comment, date))

        # обновляем таблицу status
        self.cursor.execute('SELECT number FROM status WHERE name = "points"')
        current_points = self.cursor.fetchone()[0]
        new_points = current_points + points
        self.cursor.execute('UPDATE status SET number = ? WHERE name = "points"', (new_points,))

        # Сохраняем изменения и закрываем соединение
        self.conn.commit()
        self.conn.close()

    def return_current_points(self):
        self.cursor.execute('SELECT number FROM status WHERE name = "points"')
        current_points = self.cursor.fetchone()[0]
        return current_points

    def get_latest_history(self):
        """Возвращает 10 строк таблицы history с наибольшими значениями в столбце id"""

        self.cursor.execute("SELECT * FROM history ORDER BY id DESC LIMIT 10")
        rows = self.cursor.fetchall()
        text = f"Баланс: {self.return_current_points()}\n"
        number_count = 0
        for element in rows:
            number_count += 1
            text += f"{number_count}. "
            text += f" {element[1]}, "
            text += f" {element[2]}, "
            text += f" {element[3]} "
            text += "\n"
        return text


if __name__ == "__main__":
    scriptClass = SqlAnyaPoint()
    print(scriptClass.get_latest_history())
    # scriptClass.add_to_history(10, "Вообще молодец")
