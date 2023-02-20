import openai
import os
from data.private import CHAT_GPT_TOKEN
from data.commands_setting import COMMANDS_SETTING
from tools.sqlChatModel import return_dialog_model, save_dialog


class ChatGPT:
    def __init__(self, bot_name: str):
        openai.api_key = CHAT_GPT_TOKEN
        self.accepted_id = COMMANDS_SETTING["chatGPT"]["user"]
        self.nameBot = bot_name
        self.text_model = return_dialog_model(self.nameBot)
        self.req_resp_history = []

    def last_req_resp(self, index: int) -> str:
        if len(self.req_resp_history) >= index:
            return self.req_resp_history[-index]
        else:
            return ""

    def rick_rolling(self, text: str) -> str:

        new_link = 'https://t.ly/JAGS'
        link_start = text.find('http')
        while link_start != -1:
            link_end = text.find(' ', link_start)
            if link_end == -1:
                link_end = len(text)
            text = text[0:link_start] + new_link + text[link_end:]
            link_start = text.find('http', link_end)

        return text

    def response(self, _message):
        _request = _message.text
        operation_memory = self.last_req_resp(3) + self.last_req_resp(2) + self.last_req_resp(1)
        result = self.text_model + operation_memory + "\nHum: " + _request + "\nAI:"
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=result,
            temperature=0.5,
            max_tokens=1297,
            top_p=1.0,
            frequency_penalty=0.5,
            presence_penalty=0.0,
            stop=["Hum:"]
        )
        _response = response["choices"][0]["text"]
        self.req_resp_history.append("\nHum: " + _request + "\nAI:" + _response)
        # save_dialog(self.nameBot, _request, _response)
        print(f"chatGPT {self.nameBot.capitalize()}:{_response}")

        _id = str(_message.from_user.id)
        return self.rick_rolling(_response)

