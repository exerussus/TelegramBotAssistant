
from app.chatGPT.sqlChatGPT import delete_last, save_dialog
from telebot import types
from tools.debuger import debug_log
from tools.sqlSetting import set_user_status, get_user_status
from app.makeCharacterBot.sqlMakeCharacterBot import get_last_request, set_last_request, get_last_response, \
    set_last_response


class AppSample:
    name = "makeCharacterBot"
    activate = ["/edit_bot"]  # Может содержать сколько угодно значений

    def __init__(self, message, bot, debug):
        self.user_id = message.from_user.id
        self.actually_status = get_user_status(self.user_id)
        self.bot = bot
        self.app_name = AppSample.name
        self.debug_mode = debug
        self._request = " "
        self._response = " "
        self.message = message

    def debug_log(self, debug_mode,
                  text: str = "",
                  scenario_start: str = "",
                  condition: str = "",
                  color: str = "grey"):
        """Выводит логи в консоль."""
        debug_log(debug_mode,
                  text=text,
                  scenario_start=scenario_start,
                  scenario_end=self.actually_status["scenario"],
                  condition=condition,
                  color=color,
                  app_name=self.app_name)

    def send_message(self, bot, text: str, user_id=None):
        """Посылает сообщение пользователю. По-умолчанию user_id = self.user_id"""
        if user_id is None:
            bot.send_message(self.user_id, text)
        else:
            bot.send_message(user_id, text)

    def set_status(self, scenario: str, activated_app=None):
        """Меняет активный скрипт и сценарий. По-умолчанию ставит активный скрипт как self.app_name."""
        if activated_app is None:
            set_user_status(user_id=self.user_id, actually_app=self.app_name, scenario=scenario)
        else:
            set_user_status(user_id=self.user_id, actually_app=activated_app, scenario=scenario)

    def reset_status(self):
        set_user_status(user_id=self.user_id, actually_app="", scenario="")

    def run(self):
        """Запускает метод в зависимости от текущего сценария. В начале всегда срабатывает beginning, а затем
        выбранный в beginning последующий сценарий. Сценарии можно переименовывать и расширять."""
        match self.actually_status["scenario"]:

            case "add_human":
                self.add_human()
            case "add_ai":
                self.add_ai()
            case "edit_bot":
                self.edit_bot()
            case "priority":
                self.priority()
            case "":
                self.beginning()

    def add_human(self):
        self._request += self.message.text
        set_last_request(user_id=self.user_id, last_request=self._request)
        self.bot.send_message(self.user_id, "Введите ответ ассистента: ")
        debug_log(self.debug_mode, scenario_start="add_ai", scenario_end="add_human", color="blue")
        set_user_status(user_id=self.user_id, actually_app="makeCharacterBot", scenario="add_ai")

    def add_ai(self):

        self._response += self.message.text
        set_last_response(user_id=self.user_id, last_response=self._response)
        debug_log(self.debug_mode, scenario_start="priority", scenario_end="add_ai", color="blue")
        set_user_status(user_id=self.user_id, actually_app="makeCharacterBot", scenario="priority")
        self.bot.send_message(self.user_id, "Введите приоритет о 1 до 10, где 1 - это оперативная память: ",
                              reply_markup=types.ReplyKeyboardRemove())

    def priority(self):
        try:
            priority_raw = int(self.message.text)
            priority = priority_raw if(10 >= priority_raw >= 1) else 2
        except ValueError:
            priority = 2
        except TypeError:
            priority = 2

        self._request = str(get_last_request(self.user_id))
        self._response = str(get_last_response(self.user_id))
        save_dialog(user_id=self.user_id, request=self._request, response=self._response, priority=priority)
        debug_log(self.debug_mode,
                  scenario_end="priority",
                  color="blue")

        set_user_status(user_id=self.user_id, actually_app="", scenario="")

    def edit_bot(self):
        if "Добавить вопрос-ответ" in self.message.text:
            self.bot.send_message(self.user_id, "Введите ваш вопрос: ",
                             reply_markup=types.ReplyKeyboardRemove())

            debug_log(self.debug_mode, scenario_start="add_human",
                      scenario_end="edit_bot",
                      condition="Добавить вопрос-ответ",
                      color="blue")

            set_user_status(user_id=self.user_id, actually_app="makeCharacterBot", scenario="add_human")
        elif "Удалить последний вопрос-ответ" in self.message.text:
            delete_last(self.user_id)
            self.bot.send_message(self.user_id, "Последний вопрос-ответ удалён.",
                             reply_markup=types.ReplyKeyboardRemove())
            debug_log(self.debug_mode, scenario_end="edit_bot", condition="Удалить последний вопрос-ответ", color="blue")
            set_user_status(user_id=self.user_id, actually_app="", scenario="")
        else:
            debug_log(self.debug_mode, scenario_end="edit_bot", condition="Не нашёл совпадений.", color="blue")
            set_user_status(user_id=self.user_id, actually_app="", scenario="")


    def beginning(self):
        if '/edit_bot' in self.message.text:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            btn1 = types.KeyboardButton("Добавить вопрос-ответ")
            btn2 = types.KeyboardButton("Удалить последний вопрос-ответ")
            markup.add(btn1, btn2)
            self.bot.send_message(self.message.chat.id, text="Выберите действие: ", reply_markup=markup)
            debug_log(self.debug_mode, scenario_start="edit_bot", text="Начало команды", color="blue")
            set_user_status(user_id=self.user_id, actually_app="makeCharacterBot", scenario="edit_bot")

    @staticmethod
    def command_run(message, bot, debug=True):
        """Обязательная функция. Название менять нельзя, так как её вызывает handler."""
        _classExemplar = AppSample(message=message, bot=bot, debug=debug)
        _classExemplar.run()







