import openai
from data.config import CHAT_GPT_TOKEN
from app.chatGPT.sqlChatGPT import get_priority_memory, get_bot_for_user, add_operation_memory, get_operation_memory


class AppSample:
    name = "chatGPT"
    activate = []  # Может содержать сколько угодно значений
    pass


class ChatGPT:
    def __init__(self, user_id: int):
        openai.api_key = CHAT_GPT_TOKEN
        self.user_id = user_id
        self.req_resp_history = []
        self.nameBot = get_bot_for_user(self.user_id)

    def last_req_resp(self, index: int) -> str:
        if len(self.req_resp_history) >= index+1:
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

    def load_operation_memory(self, memory_size):  # openai.error.InvalidRequestError:
        operation_memory = ""
        for i in reversed(range(memory_size)):
            operation_memory += self.last_req_resp(i)
        return operation_memory

    def try_gpt_response(self, memory_size, _request):
        priority_memory = get_priority_memory(self.user_id)
        try:
            operation_memory = get_operation_memory(bot_name=self.nameBot, memory_size=memory_size)
            result = priority_memory + operation_memory + "\nHum: " + _request + "\nAI:"
            response = self.gpt_response(result)
            return response
        except openai.error.InvalidRequestError:
            self.try_gpt_response(memory_size - 1, _request)
        except openai.error.RateLimitError:
            return "Прости, болит голова. Давай поговорим чуть позже..."

    def gpt_response(self, result):
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=result,
            temperature=0.5,
            max_tokens=500,
            top_p=1.0,
            frequency_penalty=0.5,
            presence_penalty=0.0,
            stop=["Hum:"]
        )
        return response["choices"][0]["text"]

    def response(self, _message):
        memory_size = 3
        _request = _message.text
        _response = self.try_gpt_response(memory_size=memory_size, _request=_request)
        add_operation_memory(_request, _response, self.nameBot)
        print(f"chatGPT {self.nameBot.capitalize()}:{_response}")
        return self.rick_rolling(_response)
