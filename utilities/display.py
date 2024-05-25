from tabulate import tabulate
from colorama import Fore, Style, init


init(autoreset=True)


def display_dict(title, data):
    print(f"\n{title}")
    # table = [[key, value] for key, value in data.items()]
    # print(tabulate(table, headers=["Attribute", "Value"], tablefmt="fancy_grid"))
    table = [[color_value(v) for v in data.values()]]
    header = list(data.keys())
    print(tabulate(table, headers=header, tablefmt="fancy_grid"))


def color_value(value):
    if value >= 8:
        return f"{Fore.GREEN}{value}{Style.RESET_ALL}"
    elif value >= 4:
        return f"{Fore.YELLOW}{value}{Style.RESET_ALL}"
    else:
        return f"{Fore.RED}{value}{Style.RESET_ALL}"
