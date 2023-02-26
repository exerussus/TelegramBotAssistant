
import telebot
from tools.sqlSetting import get_user_status, set_user_name, add_access_rights, add_apps
from app.chatGPT.sqlChatGPT import set_bot_for_user
from data.config import TELEGRAM_TOKEN
from settings import EasySettings


bot = telebot.TeleBot(TELEGRAM_TOKEN)


def run():
    print("Напишите что-нибудь чат-боту, и дождитесь ввода имени пользователя и бота.")
    print("После этого, дождитесь завершения работы программы, а")
    print("затем просто запустите telegramBot.")

    @bot.message_handler(content_types=['text'])
    def get_text_messages(message):
        user_id = message.from_user.id
        get_user_status(user_id)
        set_user_name(user_id, input("Введите имя пользователя: "))
        set_bot_for_user(user_id, input("Введите имя бота, который будет привязан к пользователю: "))
        add_apps("chatGPT", "makeCharacterBot")
        add_access_rights(user_id, "makeCharacterBot")
        add_access_rights(user_id, "chatGPT")
        bot.stop_bot()

    bot.polling(none_stop=True, interval=0)


run()
