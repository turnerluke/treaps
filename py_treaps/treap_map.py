from __future__ import annotations
import random
import typing
from collections.abc import Iterator
from typing import List, Optional, cast
import math

from py_treaps.stack import Stack
from py_treaps.treap import KT, VT, Treap
from py_treaps.treap_node import TreapNode


# Example usage found in test_treaps.py
class TreapMap(Treap[KT, VT]):
    # Add an __init__ if you want. Make the parameters optional, though.
    def __init__(self, root: TreapNode = None):
        """
        Initializes the TreapMap. If a root is passed, that root's parent will be cleaved.
        """
        self.root = root
        self.num_nodes = 0
        if self.root is not None:
            self.root.parent = None
            self.num_nodes += 1

    def get_root_node(self) -> Optional[TreapNode]:
        return self.root

    def get_num_elements(self) -> int:
        return self.num_nodes

    def lookup(self, key: KT) -> Optional[VT]:
        """
        Returns the value for the given key.

        Helper is utilized to ensure the inputs are the same as provided for testing.
        """

        def helper(node: TreapNode) -> Optional[VT]:
            if node is None:
                return None
            if node.key == key:
                return node.value
            if key > node.key:
                return helper(node.right_child)
            if key < node.key:
                return helper(node.left_child)

        return helper(self.root)

    def find_parent(self, key: KT) -> TreapNode:
        """
        Finds the parent where the next node with key, `key`, should be inserted.
        If key is in the Treap, returns the corresponding node.
        """
        x = self.root
        # Perform the BST insertion
        while True:
            if x.key > key:
                if x.left_child is None:
                    return x
                x = x.left_child
            elif x.key < key:
                if x.right_child is None:
                    return x
                x = x.right_child
            elif x.key == key:
                return x

    def insert(self, key: KT, value: VT) -> None:
        self.num_nodes += 1
        if self.root is None:
            self.root = TreapNode(key, value)
        else:
            parent = self.find_parent(key)

            if parent.key > key:
                new = TreapNode(key, value, parent)
                parent.make_left_child(new)
            elif parent.key < key:
                new = TreapNode(key, value, parent)
                parent.make_right_child(new)
            elif parent.key == key:
                parent.value = value
                return

            # Rebalance maxheap
            if new.priority > parent.priority:  # The heap is imbalanced
                self.rebalance_heap(new)

    def left_rotate(self, node: TreapNode) -> None:
        """
        Helper for re-balancing. Performs a left rotation around node.
        """
        # Get relational nodes
        child = node.right_child
        grandparent = node.parent
        if grandparent is not None:
            node_child_type = 'L' if node.is_left_child() else 'R'

        node.right_child = child.left_child
        node.correct_children()
        child.left_child = node
        node.parent = child

        if grandparent is not None:
            if node_child_type == 'L':
                grandparent.left_child = child
            elif node_child_type == 'R':
                grandparent.right_child = child
            child.parent = grandparent

        elif grandparent is None:  # The child was rotated to the root
            self.root = child
            child.parent = None

    def right_rotate(self, node: TreapNode) -> None:
        """
        Helper for re-balancing. Performs a right rotation around node.
        """
        # Get relational nodes
        child = node.left_child
        grandparent = node.parent
        if grandparent is not None:
            node_child_type = 'L' if node.is_left_child() else 'R'

        node.left_child = child.right_child
        node.correct_children()
        child.right_child = node
        node.parent = child

        if grandparent is not None:
            if node_child_type == 'L':
                grandparent.left_child = child
            elif node_child_type == 'R':
                grandparent.right_child = child
            child.parent = grandparent

        elif grandparent is None:
            self.root = child
            child.parent = None

    def rebalance_heap(self, child: TreapNode) -> None:
        grandparent = child.parent.parent
        if child.is_left_child():
            self.right_rotate(child.parent)
        elif child.is_right_child():
            self.left_rotate(child.parent)

        # Check for new imbalances (first child had too large priority, check if this is still the case
        # btw child & it's new parent
        if grandparent is not None:
            if child.priority > grandparent.priority:
                self.rebalance_heap(child)

    def remove(self, key: KT) -> Optional[VT]:
        """
        Removes the node with this key from the tree. Returns the value for that node. Returns None if not present.
        """
        if self.get_root_node() is None:
            return None

        victim = self.find_parent(key)  # Note, if key is in Treap `find_parent` returns that node
        if victim.key != key:  # The key is not in the Treap
            return None
        val = victim.value

        # victim is now the node to be removed
        # The child taking its place should have the largest priority
        # We rotate the highest priority child to the victims spot

        while victim.has_children():
            if not victim.has_right_child() and victim.has_left_child():
                self.right_rotate(victim)
            elif not victim.has_left_child() and victim.has_right_child():
                self.left_rotate(victim)

            elif victim.left_child.priority > victim.right_child.priority:
                self.right_rotate(victim)
            elif victim.right_child.priority > victim.left_child.priority:
                self.left_rotate(victim)

        # Victim is now a leaf
        victim.remove()

        return val

    def insert(self, key: KT, value: VT) -> None:
        self.num_nodes += 1
        if self.root is None:
            self.root = TreapNode(key, value)
        else:
            parent = self.find_parent(key)

            if parent.key > key:
                new = TreapNode(key, value, parent)
                parent.make_left_child(new)
            elif parent.key < key:
                new = TreapNode(key, value, parent)
                parent.make_right_child(new)
            elif parent.key == key:
                parent.value = value
                return

            # Rebalance maxheap
            if new.priority > parent.priority:  # The heap is imbalanced
                self.rebalance_heap(new)

    def insert_with_max_priority(self, key: KT) -> None:
        """
        Helper for `split`. Same function as insert, however sets the priority
        of the new node to the max priority.
        """
        value = None
        if self.root is None:
            self.root = TreapNode(key, value)
        else:
            parent = self.find_parent(key)

            if parent.key >= key:
                new = TreapNode(key, value, parent)
                parent.make_left_child(new)
            elif parent.key < key:
                new = TreapNode(key, value, parent)
                parent.make_right_child(new)

            new.set_priority_to_max()
            self.rebalance_heap(new)

    def split(self, threshold: KT) -> List[Treap[KT, VT]]:
        """
        Splits the Treap into 2, one with keys less than, the other with keys greater than or equal to the threshold.
        Performed by inserting a new node with key threshold and priority MAXPRIORITY.
        The left subtree is the lesser keys, the right subtree is the greater/equal to keys.

        """
        # 1) Insert new entry x with key threshold, and priority = MAXPRIORITY
        self.insert_with_max_priority(threshold)
        # 2) T1 is the left subtree, T2 is the right
        T1 = TreapMap(self.root.left_child)
        T2 = TreapMap(self.root.right_child)
        return [T1, T2]

    def join(self, _other: Treap[KT, VT]) -> None:
        """
        Joins another Treap to this Treap.
        Note it's assumed that all keys in T1 are smaller than keys in T2.

        """
        if _other.root is None:
            return
        if self.root is None:
            self.root = _other.root
            return
        # Create new TreapMap with arbitrary root, x
        T = TreapMap(TreapNode(0, None))
        # Make T1 & T2 the subtreaps
        T1, T2 = (self, _other) if self.root.key < _other.root.key else (_other, self)
        T.root.left_child = T1.root
        T.root.right_child = T2.root
        T.root.correct_children()
        self.root = T.root
        # Delete x
        self.remove(0)

    def meld(self, other: Treap[KT, VT]) -> None:
        """
        Merges two Treaps. Does not assume any relationship between keys.

        Must run in O(m log(n/m)). n, m are the Treap sizes. (m<n)
        """

        if len(other) > len(self):
            self, other = other, self

        subtrees = [other.root]

        while subtrees:
            subtree = subtrees.pop()
            # Start at the root
            k = subtree.key
            # Try to insert like a node
            parent = self.find_parent(k)

            if parent.key < k:
                # We are moving right
                # If you move right, check down the left child to see if also larger
                y = subtree.left_child
                while y is not None:
                    if y.key < parent.key:
                        y.split()
                        subtrees.append(y)
                        break
                    else:
                        y = y.left_child

                if parent.parent is not None:
                    z = subtree.right_child
                    while z is not None:
                        if z.key > parent.parent.key:
                            z.split()
                            subtrees.append(z)
                            break
                        else:
                            z = z.right_child

                parent.make_right_child(subtree)

            elif parent.key > k:
                # We are moving left
                # If you move left, check down the right child to see if also larger
                y = subtree.right_child
                while y is not None:
                    if y.key > parent.key:
                        y.split()
                        subtrees.append(y)
                        break
                    else:
                        y = y.right_child

                if parent.parent is not None:
                    z = subtree.left_child
                    while z is not None:
                        if z.key < parent.parent.key:
                            z.split()
                            subtrees.append(z)
                            break
                        else:
                            z = z.right_child

                parent.make_left_child(subtree)

            # Rebalance, BUT each time a section of the subtree is moved, check that subtree for imbalances
            if subtree.priority > parent.priority:
                self.rebalance_heap_rebalance_transplants(subtree)

    def left_rotate_rebalance_transplants(self, node: TreapNode) -> None:
        """
        Helper for re-balancing for meld. Performs a left rotation around node.
        Checks each transplanted section of tree for imbalances.
        """
        # Get relational nodes
        child = node.right_child
        grandparent = node.parent
        if grandparent is not None:
            node_child_type = 'L' if node.is_left_child() else 'R'

        node.right_child = child.left_child
        node.correct_children()
        child.left_child = node
        node.parent = child

        if grandparent is not None:
            if node_child_type == 'L':
                grandparent.left_child = child
            elif node_child_type == 'R':
                grandparent.right_child = child
            child.parent = grandparent

        elif grandparent is None:  # The child was rotated to the root
            self.root = child
            child.parent = None

        # node.right_child may have a priority imbalance
        if node.right_child is not None:
            if node.right_child.priority > node.priority:
                self.rebalance_heap_rebalance_transplants(node.right_child)

    def right_rotate_rebalance_transplants(self, node: TreapNode) -> None:
        """
        Helper for re-balancing for meld. Performs a right rotation around node.
        Checks each transplanted section of tree for imbalances.
        """
        # Get relational nodes
        child = node.left_child
        grandparent = node.parent
        if grandparent is not None:
            node_child_type = 'L' if node.is_left_child() else 'R'

        node.left_child = child.right_child
        node.correct_children()
        child.right_child = node
        node.parent = child

        if grandparent is not None:
            if node_child_type == 'L':
                grandparent.left_child = child
            elif node_child_type == 'R':
                grandparent.right_child = child
            child.parent = grandparent

        elif grandparent is None:
            self.root = child
            child.parent = None

        # node.left_child may have a priority imbalance
        if node.left_child is not None:
            if node.left_child.priority > node.priority:
                self.rebalance_heap_rebalance_transplants(node.left_child)

    def rebalance_heap_rebalance_transplants(self, child: TreapNode) -> None:
        """
        Rebalance function for the meld method. Works same as `rebalance_heap` except checks transplanted sections of
        the new subtree for imbalances.
        """
        grandparent = child.parent.parent
        if child.is_left_child():
            self.right_rotate_rebalance_transplants(child.parent)
        elif child.is_right_child():
            self.left_rotate_rebalance_transplants(child.parent)

        # Check for new imbalances (first child had too large priority, check if this is still the case
        # btw child & it's new parent
        if grandparent is not None:
            if child.priority > grandparent.priority:
                self.rebalance_heap_rebalance_transplants(child)

    def difference(self, other: Treap[KT, VT]) -> None:
        """
        Removes keys contained in Treap 'other' from this treap
        """
        # Just parse through the other treap, removing each key
        # Should run in O(m log(n/m)) time.

        # Parse through other, remove() each key
        # This runs in O(m log(n)) time:
        # Optimize somehow
        for key in other:
            self.remove(key)

    def balance_factor(self) -> float:
        """
        Ratio between the height and the minimum possible height.
        """
        def height_helper(node: TreapNode, height: int = 0):
            if node is None:
                return
            yield height
            yield from height_helper(node.left_child, height+1)
            yield from height_helper(node.right_child, height + 1)
        heights = list(height_helper(self.root))
        n = len(heights)
        h = max(heights)

        hmin = math.floor(math.log(n, 2))  # minimum height is floor(logbase2(n))
        if hmin == 0:
            return 1
        return h/hmin

    def __str__(self) -> str:
        """
        Constructs a string representation of the current tree.
        Used for debugging.
        Represents each level with a greater tab than the past.
        Shows the L & R child for each node, provided they have one.
        """

        def helper(node: TreapNode, level: int = 0, node_type: str = 'Root'):
            if node is None:
                return
            yield node, level, node_type
            yield from helper(node.left_child, level + 1, 'L')
            yield from helper(node.right_child, level + 1, 'R')

        nodes = helper(self.root)
        lines = []
        for node, lvl, node_type in nodes:
            lines.append('\t'*lvl + f'{node_type}: {(node.key, node.priority)}')

        return '\n'.join(lines)

    def __iter__(self) -> typing.Iterator[KT]:
        """
        Returns an iterator object of the trees keys.
        Uses in-order traversal, ie keys are from low to high.
        """
        def helper(node):
            if node is None:
                return
            yield from helper(node.left_child)
            yield node.key
            yield from helper(node.right_child)

        yield from helper(self.root)

    def __len__(self) -> int:
        return len(list(iter(self)))