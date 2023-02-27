#!C:\Users\sokol\PycharmProjects\nextGenBot\venv\Scripts\python
import datetime
import telebot
from data.config import TELEGRAM_TOKEN
from app.chatGPT.main import ChatGPT
from tools.sqlSetting import get_access_rights, clean_user_status, get_user_status
from app.chatGPT.sqlChatGPT import get_dict_bots_for_users
from tools.apps_getter import get_apps_list
from requests.exceptions import ReadTimeout
from tools.debuger import debug_log


def do_func(function, arg=None):
    try:
        if arg is None:
            function()
        else:
            function(arg)
    except ReadTimeout:
        debug_log(debug_mode=True, text="Нет соединения с интернетом...", color="red")


class TelegramBot:

    def __init__(self):
        self.bot = telebot.TeleBot(TELEGRAM_TOKEN)
        self.name = {}
        self.apps_list = get_apps_list()
        self.chat_bot_dict = {}
        chat_bot_dict = get_dict_bots_for_users()
        for user_id in chat_bot_dict:
            self.chat_bot_dict[user_id] = ChatGPT(user_id)

    def logger(self, _message):
        """Shows the message data in the console \n
        Показывает данные сообщения из телеграмма в консоли"""
        name = self.name.get(_message.from_user.id)
        if name is None:
            name = get_user_status(_message.from_user.id)["user_name"]
            if name is None:
                name = _message.from_user.first_name
        print(
            f"{datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')} "
            f"{_message.from_user.id} "
            f"{name}: "
            f"{_message.text}"
        )

    def is_it_app_check(self, message):
        """Проверяет, является ли текст активатором приложения."""
        _text = message.text
        for app in self.apps_list:
            if _text in app.activate:
                return app

    def user_access_to_app_check(self, user_id: int, app_name: str):
        """Checks the user's permissions to use the app \n
        Проверяет права юзера на использование команды"""
        return get_access_rights(user_id=user_id, app_name=app_name)

    def standard_command(self, message, app):
        """Executes standard commands from the app folder \n
        Выполняет стандартную команду из папки app"""
        user_id = message.from_user.id
        print(f"standard_command: app = {app}")
        if self.user_access_to_app_check(user_id=user_id, app_name=app.name):
            app.command_run(message, self.bot)

        else:
            self.bot.send_message(message.from_user.id, "У вас нет прав на использование данной команды.")
            clean_user_status(user_id=user_id)

    def standard_command_continuation(self, message, app_name):
        """Продолжает работу app"""
        user_id = message.from_user.id
        app = ""
        for _app in self.apps_list:
            if _app.name == app_name:
                app = _app
                break

        if self.user_access_to_app_check(user_id=user_id, app_name=app.name):
            app.command_run(message, self.bot)

        else:
            self.bot.send_message(message.from_user.id, f"id: {user_id}. У вас нет прав на использование данной команды.")
            clean_user_status(user_id=user_id)

    def command_handler(self, message):
        """Defines and executes a standard or ChatGPT app \n
        Определяет и выполняет стандартную или ChatGPT команду"""
        user_id = message.from_user.id
        user_status = get_user_status(user_id=user_id)
        if user_status["activated_app"] == "":
            app = self.is_it_app_check(message)
            if app is not None:
                self.standard_command(message, app)  # Тут скрипт команды
            else:
                if get_access_rights(user_id=user_id, app_name="chatGPT"):
                    self.bot.send_message(user_id,
                                          self.chat_bot_dict[user_id].response(message),
                                          reply_markup=telebot.types.ReplyKeyboardRemove())  # тут ChatGPT
                else:
                    self.bot.send_message(user_id, f"id: {user_id}. Вы не имеете прав для использования ChatGPT.",
                                          reply_markup=telebot.types.ReplyKeyboardRemove())
        else:
            self.standard_command_continuation(message, user_status["activated_app"])

    def run(self):
        """Runs the main logic"""

        @self.bot.message_handler(content_types=['text'])
        def get_text_messages(message):

            do_func(self.logger, message)
            do_func(self.command_handler, message)

        self.bot.polling(none_stop=True, interval=0)


def return_exemplar():
    return TelegramBot()


if __name__ == "__main__":
    telegramBot = TelegramBot()
    telegramBot.run()
