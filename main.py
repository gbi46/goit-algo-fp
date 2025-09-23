from colorama import Fore, init
from lib.common import print_task_header
from lib.linked_list import LinkedList, merge_sorted_lists

init(autoreset=True)

def main():
    print_task_header(1)
    linked_list = LinkedList()
    
    for value in [3, 1, 4, 1, 5, 9, 2, 6, 5]:
        linked_list.append(value)

    print(Fore.BLUE + "Original Linked List:")
    linked_list.print_list()

    linked_list.reverse()
    print(Fore.BLUE + "Reversed Linked List:")
    linked_list.print_list()

    linked_list.sort()
    print(Fore.BLUE + "Sorted Linked List:")
    linked_list.print_list()

    lst1 = LinkedList()
    for value in [1, 3, 5]:
        lst1.append(value)

    lst2 = LinkedList()
    for value in [2, 4, 6]:
        lst2.append(value)

    merged = merge_sorted_lists(lst1, lst2)
    print(Fore.BLUE + "Merged Linked List:")
    merged.print_list()

if __name__ == "__main__":
    main()
