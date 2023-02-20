from data.private import USER_1, USER_2
from command.makeCharacterBot import command_run as makeCharacterBot_run

COMMANDS_SETTING = {
    "user_status": {USER_1: {"name": None, "scenario": None},
                    USER_2: {"name": None, "scenario": None},
                    },

    "chatGPT": {
        "type": ["telegram"],
        "user": [USER_1, USER_2],
        "script": None,
        "activate": [],
        "bot_name_for_current_user": {USER_1: "name_bot", USER_2: "another_name_bot_if_you_want"}
    },
    "makeCharacterBot": {
        "type": ["telegram"],
        "user": [USER_1, USER_2],
        "script": makeCharacterBot_run,
        "activate": ["/edit_bot"],
        "last_human_request": "",
    },
}


def reset_user_status(settings, user_id):
    settings["user_status"][str(user_id)] = {"name": None, "status": None}
    return settings
