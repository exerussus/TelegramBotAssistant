
from datetime import datetime
from colorama import init, Fore
init(autoreset=True)

def debug_log(debug_mode,
              app_name="",
              text="",
              scenario_start="",
              scenario_end="",
              condition="",
              color="white"):

    if debug_mode:
        text_color = ""
        match color:
            case "white":
                text_color = Fore.WHITE
            case "blue":
                text_color = Fore.BLUE
            case "red":
                text_color = Fore.RED
            case "green":
                text_color = Fore.GREEN
            case _:
                text_color = Fore.RESET

        time = datetime.now()
        time_now = time.strftime("%H:%M:%S")

        pref = "DEBUGGER: "
        app_name = ("Приложение: " + app_name + ". ") if app_name != "" else ""
        scenario_start = ("Начало сценария: " + scenario_start + ". ") if scenario_start != "" else ""
        scenario_end = ("Конец сценария: " + scenario_end + ". ") if scenario_end != "" else ""
        condition = ("Условие: " + condition + ". ") if condition != "" else ""
        text = ("Комментарий: " + text + ". ") if text != "" else ""

        print(text_color + f"{app_name}{pref}{scenario_end}{scenario_start}{condition}{text} || {time_now}")


if __name__ == "__main__":
    debug_log(True, "x = 10")
