from lib.common import print_task_header
from lib.linked_list import LinkedList

def main():
    print_task_header(1)
    linked_list = LinkedList()
    
    for value in [3, 1, 4, 1, 5, 9, 2, 6, 5]:
        linked_list.append(value)

    print("Original Linked List:")
    linked_list.print_list()

    linked_list.reverse()
    print("Reversed Linked List:")
    linked_list.print_list()

    linked_list.sort()
    print("Sorted Linked List:")
    linked_list.print_list()

if __name__ == "__main__":
    main()
