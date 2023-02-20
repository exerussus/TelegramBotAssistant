
import datetime
import telebot
from data.private import TELEGRAM_TOKEN, NAMES
from data.commands_setting import COMMANDS_SETTING, reset_user_status
from bot.chatGpt import ChatGPT


class TelegramBot:

    def __init__(self):
        self.bot = telebot.TeleBot(TELEGRAM_TOKEN)
        self.name = NAMES
        self.commands_setting = COMMANDS_SETTING
        self.actually_status = self.commands_setting["user_status"]
        self.handler_type = "telegram"

        self.chat_bot_dict = {}
        user_id_bot_name_dict = self.commands_setting["chatGPT"]["bot_name_for_current_user"]
        for user_id_bot_name in user_id_bot_name_dict:
            self.chat_bot_dict[user_id_bot_name] = ChatGPT(user_id_bot_name_dict[user_id_bot_name])

    def logger(self, _message):
        """Shows the message data in the console \n
        Показывает данные сообщения из телеграмма в консоли"""

        print(
            f"{datetime.datetime.now()} "
            f"{_message.from_user.id} "
            f"{self.name.get(str(_message.from_user.id))}: "
            f"{_message.text}"
        )

    def command_check(self, message):
        """Парсит сообщение и ищет в нем команду, возвращает название команды, если нашел"""
        for command_name in self.commands_setting:
            if command_name != "user_status":
                if message.text in self.commands_setting[command_name]["activate"]:
                    return command_name

    def user_check(self, _id: str, _script_name: str):
        """Checks the user's permissions to use the command \n
        Проверяет права юзера на использование команды"""
        if str(_id) in self.commands_setting[_script_name]["user"]:
            return True
        else:
            return False

    def standard_command(self, _message, _script_name: str,):
        """Executes standard commands from the command folder \n
        Выполняет стандартную команду из папки command"""
        user_id = _message.from_user.id
        if self.user_check(user_id, _script_name):
            self.actually_status[str(user_id)], self.commands_setting = self.commands_setting[_script_name]["script"](
                                                                                 _message,
                                                                                 self.bot,
                                                                                 self.actually_status[str(user_id)],
                                                                                 self.commands_setting)

        else:
            self.bot.send_message(_message.from_user.id, "У вас нет прав на использование данной команды.")
            self.actually_status[str(user_id)] = reset_user_status(self.commands_setting, str(user_id))

    def command_handler(self, message):
        """Defines and executes a standard or ChatGPT command \n
        Определяет и выполняет стандартную или ChatGPT команду"""
        user_id = message.from_user.id
        try:
            activated_script = self.actually_status[str(user_id)]["name"]
        except KeyError:
            full_name = message.chat.first_name + " " + message.chat.last_name + " " + message.chat.username
            print("\033[32m" + f"Новый старт. id:{user_id}, name:{full_name}" + "\033[0m")
            reset_user_status(self.commands_setting, str(user_id))
            self.actually_status[str(user_id)] = reset_user_status(self.commands_setting, str(user_id))
            activated_script = self.actually_status[str(user_id)]["name"]
        if activated_script is None:
            command_name = self.command_check(message)
            if command_name is not None:
                self.standard_command(message, command_name)  # Тут скрипт команды
            else:
                if str(user_id) in self.commands_setting["chatGPT"]["user"]:
                    self.bot.send_message(user_id,
                                          self.chat_bot_dict[str(user_id)].response(message),
                                          reply_markup=telebot.types.ReplyKeyboardRemove())  # тут ChatGPT
                else:
                    self.bot.send_message(user_id, "Вы не имеете прав для использования данного бота.",
                                          reply_markup=telebot.types.ReplyKeyboardRemove())
        else:
            self.standard_command(message, self.actually_status[str(user_id)]["name"])

    def run(self):
        """Runs the main logic"""

        @self.bot.message_handler(content_types=['text'])
        def get_text_messages(message):

            self.logger(message)
            self.command_handler(message)

            # bot.send_message(message.from_user.id, f"Ваш ID: {message.from_user.id}")

        self.bot.polling(none_stop=True, interval=0)


def return_exemplar():
    return TelegramBot()


if __name__ == "__main__":
    telegramBot = TelegramBot()
    telegramBot.run()

