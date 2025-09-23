class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        last = self.head
        while last.next:
            last = last.next
        last.next = new_node

    def print_list(self):
        current = self.head
        elements = []
        while current:
            elements.append(current.data)
            current = current.next
        print(" -> ".join(map(str, elements)))

    def reverse(self):
        prev = None
        current = self.head
        while current:
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node
        self.head = prev

    def _merge_sort(self, head):
        if not head or not head.next:
            return head

        # Find middle using slow/fast pointer
        slow, fast = head, head.next

        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next

        # If odd length, slow is middle element
        mid = slow.next
        slow.next = None
        left = self._merge_sort(head)
        right = self._merge_sort(mid)

        return self._merge(left, right)

    def _merge(self, l1, l2):
        dummy = Node(0)
        curr = dummy

        while l1 and l2:
            if l1.data < l2.data:
                curr.next = l1
                l1 = l1.next
            else:
                curr.next = l2
                l2 = l2.next
            curr = curr.next

        curr.next = l1 if l1 else l2
        return dummy.next
    
    def sort(self):
        self.head = self._merge_sort(self.head)

def merge_sorted_lists(l1, l2):
    dummy = Node(0)
    curr = dummy

    h1, h2 = l1.head, l2.head

    while h1 and h2:
        if h1.data < h2.data:
            curr.next = h1
            h1 = h1.next
        else:
            curr.next = h2
            h2 = h2.next
        curr = curr.next

    curr.next = h1 if h1 else h2

    merged = LinkedList()
    merged.head = dummy.next
    return merged
