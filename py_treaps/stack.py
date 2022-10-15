class LinkedListNode:

    def __init__(self, val=None, next=None):
        self.val = val
        self.next = next


class Stack:

    def __init__(self):
        self.head = LinkedListNode()

    def __bool__(self):
        return not self.is_empty()

    def is_empty(self):
        if self.head.next is not None:
            return False
        return True

    def push(self, val):
        node = LinkedListNode(val)
        node.next = self.head.next
        self.head.next = node

    def pop(self):
        if self.is_empty():
            raise Exception("Pop from empty stack.")

        ret = self.head.next.val
        self.head.next = self.head.next.next
        return ret