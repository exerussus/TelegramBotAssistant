# TelegramBotAssistant
Это рабочий чат-бот с возможностью использовать заскриптованные команды, а так же вести беседу и помогать в решении самых разных задач, задействуя chatGPT.
Пока что работает только Windows, тестируется на Linux.

## Технологии
- [Python](https://www.python.org/)
- [Telebot](https://pypi.org/project/telebot/)
- [OpenAI](https://openai.com/)
- [Colorama](https://pypi.org/project/colorama/)

## Использование
Чтобы включить ассистента, запустите telegramBot, но
перед началом использования данной программы, Вам необходимо будет получить TOKEN телеграма, TOKEN chatGPT и провести небольшую инициализацию в easy_start.py.

### Установка пакетов
Установите необходимые пакеты в requirements.txt:
```sh
pip install -r requirements.txt
```

### Добавление токенов
Откройте data/config.py и вставьте и заполните TELEGRAM_TOKEN и CHAT_GPT_TOKEN.

### Старт с easy_start
Запустите easy_start.py, напишите телеграм-боту произвольное сообщение и дождитесь ввода Вашего имени, затем введите имя 
бота.

### Команды \ Приложения \ Скрипты
В папке app находятся стандартные приложения для взаимодействия с chatGPT, а так же шаблон для подключения новых приложений.
Чтобы подключить новое приложение, создайте папку с точным названием вашего приложения, создайте в нем main.py,  
скопируйте и вставьте в него код из app/newAppSample/main.py. 

### Активация, активный скрипт и сценарий
Каждый класс AppSample должен иметь name и activate для определения скрипта и его стартовой команды. Обратите внимание, 
что name и название папки должны совпадать. Если вы хотите установить одну, или несколько команд для активации приложения - 
добавьте в лист activate. Каждый пользователь обладает "активным приложением" и "сценарием". Изначально, пользователь 
не имеет никакого активированного приложения и сценария.
Если никакая команда не активировалась - сообщение пользователя автоматически идёт в запрос к chatGPT. 
Когда срабатывает активация приложения - он попадает в метод: 
```python
def beginning(self):
    pass
```
Именно сюда вы можете подключить исполнение любой желаемой программы. После отработки скрипта, пользователь попадает в изначальное 
состояние, но если вы хотите, чтобы программа отработала в несколько этапов, то воспользуйтесь set_status() методом, в котором 
Вы можете назначить другой сценарий своей программы, например:
```python
self.set_status(scenario="scenario_1") 
```
Следующее 
сообщение пользователя автоматически попадает в ту же программу в сценарий "scenario_1" и в соответствующий ему метод.
```python
match self.actually_status["scenario"]:

    case "scenario_1":  # Здесь идёт проверка на сценарий
        self.scenario_1()
    case "":
        self.beginning()


def scenario_1(self):
    pass  # Здесь будет активировано следующее действие
```
После того как ваша программа отработала - обязательно пропишите в последнем сценарии:
```python
self.reset_status()
```
Тогда состояние пользователя вернётся к изначальному.
Когда вы закончите своё приложение - обязательно добавьте ваше приложение через settings.py. Просто запустите файл, и там 
будет меню со всем необходимым, рекомендую ознакомиться.

### Концепция памяти ChatGPT
Чтобы бот мог помнить как Вас и его зовут, помнить какие-то важные для Вас детали и держать в голове последние 
события в чате - я создал систему памяти, которая делится на:

- архивная память 
- оперативная память


#### Архивная память
Архивная память - это постоянная память, которую бот должен помнить всегда. Например, как Вас зовут, как зовут бота, 
кем он является - из него можно слепить практически что угодно. С помощью приложения makeCharacterBot вы можете 
задавать боту вопрос и сами же за него отвечать. Таким образом, он будет поддерживать якобы собственный предыдущий ответ, пример: 
``` 
HUMAN: Как тебя зовут?
AI: Меня зовут Евгений, я ваш личный ассистент.
```
И всё, у Вас есть ассистент Евгений. Стоит сказать, что порой нужно задать один и тот же вопрос, только немного по-разному. 
Бот будет копировать не только то, что он "написал" ранее, но и стиль поведения написанного. Например, таким образом, вы можете создать себе 
дружелюбного собеседника: 
```
HUMAN: Как тебя зовут?
AI: Меня зовут Аня, я твоя лучшая подруга. :)
```
#### Оперативная память
Оперативная память - это память, которая динамически сохраняется и очищается по мере необходимости. Изначально, бот может 
удерживать до 16 вопросов-ответов, но когда "перегружается" - подчищает последние до тех пор, пока не разгрузится.




## Автор

- [Илья Соловьев](https://github.com/exerussus) — backend-developer
