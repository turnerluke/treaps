from __future__ import annotations
import random
import typing
from collections.abc import Iterator
from typing import List, Optional, cast, Set

from py_treaps.comparable import KT, VT

class TreapNode:

    unused_priorities: Optional[List[int]] = None

    # The maximum priority that a node can have.
    # Access this with TreapNode.MAX_PRIORITY
    MAX_PRIORITY = 65535

    """A key-value node for the TreapMap.

    Please do not modify the attributes below, but feel free to add more.
    You do not need to modify this file to complete the project,
     but you are free to modify it if it makes your implementation simpler.
    Again, do not remove or rename any of the 6 attributes below.

    Attributes:
        key (KT): The key of the node.
        value (VT): The value associated with the key of the node.
        priority (int): The priority of the node.
        parent (TreapNode): The parent of the node.
        left_child (TreapNode): The left child of the node.
        right_child (TreapNode): The right child of the node.
    """

    def __init__(
        self, key: KT, value: VT, parent: Optional[TreapNode] = None
    ):
        self.key: KT = key
        self.value: VT = value
        self.priority: int = self.get_priority()

        self.parent: Optional[TreapNode] = parent
        self.left_child: Optional[TreapNode] = None
        self.right_child: Optional[TreapNode] = None

    def get_priority(self):
        """Generate a new priority for a treap node.
    
        Please do not touch this function, and use it on the creation of a standard treap node.
        You do not need to worry about running out of priorities.

        Returns:
            An unused integer priority.
        """

        if TreapNode.unused_priorities is None:
            TreapNode.unused_priorities = list(range(0, TreapNode.MAX_PRIORITY))
            random.shuffle(TreapNode.unused_priorities)
        return TreapNode.unused_priorities.pop()

    def set_priority_to_max(self):
        self.priority = TreapNode.MAX_PRIORITY

    def is_leaf(self):
        return (self.left_child is None) and (self.right_child is None)

    def is_left_child(self):
        if self.parent is not None:
            if self.parent.left_child == self:
                return True
            else:
                return False
        raise ValueError("Node being checked for child type has no parent node.")

    def is_right_child(self):
        return not self.is_left_child()

    def correct_children(self):
        if self.left_child is not None:
            self.left_child.parent = self
        if self.right_child is not None:
            self.right_child.parent = self

    def has_left_child(self):
        return self.left_child is not None

    def has_right_child(self):
        return self.right_child is not None

    def has_children(self):
        return self.has_left_child() or self.has_right_child()