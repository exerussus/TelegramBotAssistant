
from datetime import datetime


def debug_log(debug_mode,
              app_name="",
              text="",
              scenario_start="",
              scenario_end="",
              condition="",
              color="grey"):

    if debug_mode:
        text_color = ""
        match color:
            case "grey":
                text_color = "0m"
            case "blue":
                text_color = "34m"
            case "red":
                text_color = "31m"
            case "green":
                text_color = "32m"
            case _:
                text_color = "0m"

        time = datetime.now()
        time_now = time.strftime("%H:%M:%S")

        pref = "DEBUGGER: "
        app_name = ("Приложение: " + app_name + ". ") if app_name != "" else ""
        scenario_start = ("Начало сценария: " + scenario_start + ". ") if scenario_start != "" else ""
        scenario_end = ("Конец сценария: " + scenario_end + ". ") if scenario_end != "" else ""
        condition = ("Условие: " + condition + ". ") if condition != "" else ""
        text = ("Комментарий: " + text + ". ") if text != "" else ""

        print("\033[" + text_color + f"{app_name}{pref}{scenario_end}{scenario_start}{condition}{text} |"
                                     f"| {time_now}\033[0m")


if __name__ == "__main__":
    debug_log(True, "x = 10")
