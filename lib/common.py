from colorama import Fore, init

init(autoreset=True)

def print_task_header(task_number: int):
    print(Fore.GREEN + "==========================")

    for i in range(6):
        if i == 3:
            print(Fore.GREEN + "=" + Fore.YELLOW + " " * 8 + f"Task {task_number}" + Fore.GREEN + " " * 10 + "=")
        else:
            print(Fore.GREEN + "=                        =")
    print(Fore.GREEN + "==========================")
