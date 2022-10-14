from __future__ import annotations
import random
import typing
from collections.abc import Iterator
from typing import List, Optional, cast

from py_treaps.stack import Stack
from py_treaps.treap import KT, VT, Treap
from py_treaps.treap_node import TreapNode


# Example usage found in test_treaps.py
class TreapMap(Treap[KT, VT]):
    # Add an __init__ if you want. Make the parameters optional, though.
    def __init__(self, root: TreapNode = None):
        self.root = root
        if self.root is not None:
            self.root.parent = None

    def get_root_node(self) -> Optional[TreapNode]:
        return self.root

    def lookup_helper(self, key: KT, node: TreapNode) -> Optional[VT]:
        if node is None:
            return None
        if node.key == key:
            return node.value

        if key > node.key:
            return self.lookup_helper(key, node.right_child)
        if key < node.key:
            return self.lookup_helper(key, node.left_child)

    def lookup(self, key: KT) -> Optional[VT]:
        return self.lookup_helper(key, self.root)
        '''x = self.root
        # Traverse BST
        while x is not None:
            if x.key == key:
                return x.value
            if x.key > key:
                x = x.left_child
            elif x.key < key:
                x = x.right_child
        return None'''

    def insert(self, key: KT, value: VT) -> None:
        if self.root is None:
            self.root = TreapNode(key, value)
        else:
            x = self.root
            # Perform the BST insertion
            while True:
                if x.key > key:
                    if x.left_child is None:
                        new = TreapNode(key, value, x)
                        x.left_child = new
                        break
                    x = x.left_child
                elif x.key < key:
                    if x.right_child is None:
                        new = TreapNode(key, value, x)
                        x.right_child = new
                        break
                    x = x.right_child
                else:
                    if x.key == key:
                        raise ValueError(f"Key:{key} already in TreapMap")
                    raise ValueError(f"Cannot add key:{key} to TreapMap")

            # Rebalance maxheap
            if new.priority > x.priority:  # The heap is imbalanced
                self.rebalance_heap(new, x)

    def rebalance_heap(self, child, parent):
        grandparent = parent.parent

        if grandparent is None:  # The parent is the root
            if child == parent.left_child:  # Rotate around parent to the right
                parent.left_child = child.right_child
                child.right_child = parent
                parent.parent = child
                self.root = child

            elif child == parent.right_child:  # Rotate around parent to the left
                parent.right_child = child.left_child
                child.left_child = parent
                parent.parent = child
                self.root = child
        else:
            parent_type_of_child = 'L' if parent == grandparent.left_child else 'R'

            if child == parent.left_child:  # Rotate around parent to the right
                parent.left_child = child.right_child
                child.right_child = parent
                parent.parent = child

            elif child == parent.right_child:  # Rotate around parent to the left
                parent.right_child = child.left_child
                child.left_child = parent
                parent.parent = child

            if parent_type_of_child == 'L':
                grandparent.left_child = child
            elif parent_type_of_child == 'R':
                grandparent.right_child = child
            child.parent = grandparent

            # Check for new imbalances (first child had too large priority, check if this is still the case
            # btw child & it's new parent
            if child.priority > grandparent.priority:
                self.rebalance_heap(child, grandparent)

    def remove(self, key: KT) -> Optional[VT]:
        x = self.root

        while True:
            if x is None:
                raise ValueError(f"Key: {key} is not in the TreapMap.")
            if key > x.key:
                x = x.right_child
            elif key < x.key:
                x = x.left_child
            elif key == x.key:
                break
            else:
                raise ValueError

        type_of_child = 'L' if x.parent.left_child == x else 'R'

        # x is now the node to be removed
        # The child taking it's place should have the largest priority

        if x.left_child.priority > x.right_child.priority:
            new_x = x.left_child
        else:
            new_x = x.right_child

        if type_of_child == 'L':
            x.parent.left_child = new_x
            new_x.parent = x.parent
        else:
            x.parent.right_child = new_x
            new_x.parent = x.parent

        # TODO: Fix
        # Maybe use join to add new tree after creating orphan

    def split(self, threshold: KT) -> List[Treap[KT, VT]]:

        if self.root is None:
            return [None, None]
        else:
            x = self.root
            # Perform the BST insertion
            while True:
                if x.key >= threshold:  # The choice to move left when equal is arbitrary
                    if x.left_child is None:
                        new = TreapNode(threshold, None, x)
                        new.set_priority_to_max()
                        x.left_child = new
                        break
                    x = x.left_child
                elif x.key < threshold:
                    if x.right_child is None:
                        new = TreapNode(threshold, None, x)
                        new.set_priority_to_max()
                        x.right_child = new
                        break
            # Rebalance heap so that threshold node is the root
            self.rebalance_heap(new, x)
            L = TreapMap(self.root.left_child)
            R = TreapMap(self.root.right_child)
            return [L, R]


        '''First implementation
        # We search the tree looking for the following position:
        # x.key > threshold and x.left_child.key < threshold
        #   Then l_child is it's own Treap

        # x.key < threshold and x.right_child.key > threshold
        #   Then r_child is it's own Treap

        root = self.root
        x = self.root

        while True:
            if x.key > threshold:
                l_child = x.left_child
                if l_child.key < threshold:
                    # Make l_child its own tree, return
                    l_child.parent = None
                    l_child = TreapMap(l_child)
                    x.left_child = None
                    return [l_child, root]
                x = x.left_child
            if x.key < threshold:
                r_child = x.right_child
                if r_child.key > threshold:
                    # Make r_child its own tree, return
                    r_child.parent = None
                    r_child = TreapMap(r_child)
                    x.right_child = None
                    return [root, r_child]
                x = x.right_chlid'''

    def join(self, _other: Treap[KT, VT]) -> None:
        '''
        Note it's assumed that all keys in T1 are smaller than keys in T2.

        '''
        # Create new TreapMap with arbitrary root, x
        T = TreapMap(TreapNode(0, 0))
        # Make T1 & T2 the subtreaps
        T1, T2 = (self, _other) if self.root.key < _other.root.key else (_other, self)
        T.root.left_child = T1.root
        T1.root.parent = T.root
        T.root.right_child = T2
        T2.root.parent = T.root
        self.root = T.root
        # Delete x
        self.remove(0)

    def meld(self, other: Treap[KT, VT]) -> None: # KARMA
        raise AttributeError

    def difference(self, other: Treap[KT, VT]) -> None: # KARMA
        raise AttributeError

    def balance_factor(self) -> float: # KARMA
        raise AttributeError

    def str_helper(self, node: TreapNode, level: int = 0, type: str=''):
        if node is None:
            return
        yield node, level, type
        yield from self.str_helper(node.left_child, level + 1, 'L')
        yield from self.str_helper(node.left_child, level + 1, 'L')

    def __str__(self) -> str:
        nodes = self.str_helper(self.root)
        lines = []
        for node, lvl, type in nodes:
            lines.append('\t'*lvl + f'{type}: {(node.key, node.value)}')

        return '\n'.join(lines)

        '''lines = []
        stack = Stack()
        # Stack elements will be (node, level)
        stack.push((self.root, 0))

        lines += [f'Root: {(self.root.key, self.root.value)}']
        
        while stack:
            current, lvl = stack.pop()
            L = current.left_child
            R = current.right_child
            if L is not None:
                lines += [lvl+1*'\t' + f'L: {(L.key, L.value)}']
            if R is not None:
                lines += [lvl + 1 * '\t' + f'R: {(R.key, R.value)}']
            lines += [lvl*'\t' + f'{(x.key, x.value)}']
            for x in zip([x.left_child, x.right_child]'''

    def iter_helper(self, node):
        if node is None:
            return
        yield from self.iter_helper(node.left_child)
        yield node.key
        yield from self.iter_helper(node.right_child)

    def __iter__(self) -> typing.Iterator[KT]:
        x = self.root
        yield from self.iter_helper(x)

        '''
        # TODO: Fix, this only yields leafs
        stack = Stack()
        stack.push(self.root)

        while stack:
            prev_node = stack.pop()

            if prev_node.is_leaf():
                yield prev_node.key

            if prev_node.right_child is not None:
                stack.push(prev_node.right_child)
            if prev_node.left_child is not None:
                stack.push(prev_node.left_child)'''
