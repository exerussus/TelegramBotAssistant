import sqlite3


class SettingsSql:

    def __init__(self):
        self.conn = sqlite3.connect("../data/settings.db" if __name__ == "__main__" else "data/settings.db")
        self.cur = self.conn.cursor()

        self.cur.execute("CREATE TABLE IF NOT EXISTS user (id INTEGER PRIMARY KEY, "
                         "name TEXT, "
                         "actually_app TEXT, "
                         "scenario TEXT)")

        self.cur.execute("CREATE TABLE IF NOT EXISTS user_access (user_id INTEGER, "
                         "app_name TEXT, "
                         "FOREIGN KEY (user_id) REFERENCES user(id),"
                         "FOREIGN KEY (app_name) REFERENCES app(name))")

        self.cur.execute("CREATE TABLE IF NOT EXISTS app (name TEXT PRIMARY KEY)")

    def get_apps_names_list(self):
        self.cur.execute("SELECT * FROM app")
        return self.cur.fetchall()

    def execute(self, user_id):
        self.cur.execute("SELECT * FROM user WHERE id = ?", (user_id,))
        return self.cur.fetchone()

    def set_user_name(self, user_id: int, user_name: str):
        result = user_name, user_id
        self.cur.execute("UPDATE user SET name = ? WHERE id = ?", result)
        self.conn.commit()

    def get_user_status(self, user_id: int):
        result = self.execute(user_id)
        if self.execute(user_id) is None:
            result = (user_id, '', '', '')
            self.cur.execute("INSERT INTO user VALUES (?, ?, ?, ?)", result)
            self.conn.commit()
        return result

    def set_user_status(self, user_id: int, actually_app: str, scenario: str):
        result = actually_app, scenario, user_id,
        self.cur.execute("UPDATE user SET actually_app = ?, scenario = ? WHERE id = ?", result)
        self.conn.commit()

    def delete_access_rights(self, user_id: int, app_name: str):
        result = user_id, app_name
        self.cur.execute("DELETE FROM user_access WHERE user_id = ? AND app_name = ?", result)
        self.conn.commit()

    def add_access_rights(self, user_id: int, app_name: str):
        result = user_id, app_name
        self.cur.execute("INSERT INTO user_access VALUES (?, ?)", result)
        self.conn.commit()

    def get_access_rights(self, user_id: int, app_name: str):
        result = (user_id, app_name)
        self.cur.execute("SELECT * FROM user_access WHERE user_id = ? AND app_name = ?", result)
        rights = self.cur.fetchone()
        return True if rights is not None else False

    def add_app(self, app_name: str):
        self.cur.execute("INSERT INTO app VALUES (?)", (app_name,))
        self.conn.commit()

    def app_exist_check(self, app_name: str):
        self.cur.execute("SELECT * FROM app WHERE name = ? ", (app_name,))
        result = self.cur.fetchone()
        return True if result is not None else False

    def get_all_user_access_rights(self, user_id: int):

        self.cur.execute("SELECT app_name FROM user_access WHERE user_id = ?", (user_id,))
        app_names = self.cur.fetchall()
        return app_names


def get_access_apps_names_list_for_user(user_id: int):
    _classExemplar = SettingsSql()
    app_names = _classExemplar.get_all_user_access_rights(user_id=user_id)
    _classExemplar.conn.close()
    return app_names


def get_apps_names_list():
    _classExemplar = SettingsSql()
    apps_names_list = _classExemplar.get_apps_names_list()
    _classExemplar.conn.close()
    return apps_names_list


def get_user_status(user_id: int):
    """Возвращает словарь с ключами: id, user_name, activated_app, scenario."""
    _classExemplar = SettingsSql()
    result = _classExemplar.get_user_status(user_id=user_id)
    dict_result = {"id": result[0], 'user_name': result[1], "activated_app": result[2], "scenario": result[3]}
    _classExemplar.conn.close()
    return dict_result


def set_user_status(user_id: int, actually_app: str, scenario: str):
    _classExemplar = SettingsSql()
    _classExemplar.set_user_status(user_id=user_id, actually_app=actually_app, scenario=scenario)
    _classExemplar.conn.close()


def add_access_rights(user_id: int, app_name: str):
    _classExemplar = SettingsSql()
    _classExemplar.add_access_rights(user_id=user_id, app_name=app_name)
    _classExemplar.conn.close()


def delete_access_rights(user_id: int, app_name: str):
    _classExemplar = SettingsSql()
    _classExemplar.delete_access_rights(user_id=user_id, app_name=app_name)
    _classExemplar.conn.close()


def get_access_rights(user_id: int, app_name: str):
    _classExemplar = SettingsSql()
    result = _classExemplar.get_access_rights(user_id=user_id, app_name=app_name)
    _classExemplar.conn.close()
    return result


def set_user_name(user_id: int, user_name: str):
    _classExemplar = SettingsSql()
    _classExemplar.set_user_name(user_id=user_id, user_name=user_name)
    _classExemplar.conn.close()


def clean_user_status(user_id: int):
    actually_app = scenario = ""
    set_user_status(user_id=user_id, actually_app=actually_app, scenario=scenario)


def add_apps(*apps_names: str):
    _classExemplar = SettingsSql()
    for app_name in apps_names:
        if not _classExemplar.app_exist_check(app_name=app_name):
            _classExemplar.add_app(app_name=app_name)
    _classExemplar.conn.close()


