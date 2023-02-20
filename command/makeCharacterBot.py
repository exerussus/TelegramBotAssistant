
from tools.sqlChatModel import delete_last, save_dialog
from telebot import types
from tools.debuger import debug_log


def command_run(message, bot, actually_status, settings, debug=True):
    user_id = str(message.from_user.id)
    bot_name = settings["chatGPT"]["bot_name_for_current_user"][user_id]
    _reset = {"name": None, "scenario": None}
    print(message.text)
    _request = " "
    _response = " "

    match actually_status["scenario"]:

        case "add_human":
            _request += message.text
            settings["makeCharacterBot"]["last_human_request"] = _request
            bot.send_message(message.from_user.id, "Введите ответ ассистента: ")
            debug_log(debug, scenario_start="add_ai", scenario_end="add_human", color="blue")
            return {"name": "makeCharacterBot", "scenario": "add_ai"}, settings
        case "add_ai":
            _request = settings["makeCharacterBot"]["last_human_request"]
            _response += message.text
            save_dialog(bot_name, _request, _response)
            debug_log(debug, scenario_end="add_ai", color="blue")
            return _reset, settings

        case "edit_bot":
            if "Добавить вопрос-ответ" in message.text:
                bot.send_message(message.from_user.id, "Введите ваш вопрос: ",
                                          reply_markup=types.ReplyKeyboardRemove())

                debug_log(debug, scenario_start="add_human",
                                   scenario_end="edit_bot",
                                      condition="Добавить вопрос-ответ",
                                          color="blue")

                return {"name": "makeCharacterBot", "scenario": "add_human"}, settings
            elif "Удалить последний вопрос-ответ" in message.text:
                delete_last(bot_name)
                bot.send_message(message.from_user.id, "Последний вопрос-ответ удалён.",
                                          reply_markup=types.ReplyKeyboardRemove())
                debug_log(debug, scenario_end="edit_bot", condition="Удалить последний вопрос-ответ", color="blue")
                return _reset, settings
            else:
                debug_log(debug, scenario_end="edit_bot", condition="Не нашёл совпадений.", color="blue")
                return _reset, settings

        case None:
            if '/edit_bot' in message.text:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
                btn1 = types.KeyboardButton("Добавить вопрос-ответ")
                btn2 = types.KeyboardButton("Удалить последний вопрос-ответ")
                markup.add(btn1, btn2)
                bot.send_message(message.chat.id, text="Выберите действие: ", reply_markup=markup)
                debug_log(debug, scenario_start="edit_bot", text="Начало команды", color="blue")
                return {"name": "makeCharacterBot", "scenario": "edit_bot"}, settings




