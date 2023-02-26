
from tools.debuger import debug_log
from tools.sqlSetting import set_user_status, get_user_status
from app.newAppSample.sqlAppSample import do_somthing


class AppSample:
    name = "app_name"
    activate = ["activate_word", "another_activate_word"]  # Может содержать сколько угодно значений

    def __init__(self, message, bot, debug):
        self.user_id = message.from_user.id
        self.actually_status = get_user_status(self.user_id)
        self.bot = bot
        self.app_name = AppSample.name
        self.debug_mode = debug

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

            case "scenario_1":
                self.scenario_1()
            case "scenario_2":
                self.scenario_2()
            case "scenario_3":
                self.scenario_3()
            case "":
                self.beginning()

    def scenario_1(self):
        pass

    def scenario_2(self):
        pass

    def scenario_3(self):
        pass

    def beginning(self):
        pass

    @staticmethod
    def command_run(message, bot, debug=True):
        """Обязательная функция. Название менять нельзя, так как её вызывает handler."""
        _classExemplar = AppSample(message=message, bot=bot, debug=debug)
        _classExemplar.run()

