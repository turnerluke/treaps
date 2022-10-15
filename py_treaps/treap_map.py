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
        self.num_nodes = 0
        if self.root is not None:
            self.root.parent = None
            self.num_nodes += 1

    def get_root_node(self) -> Optional[TreapNode]:
        return self.root

    def get_num_elements(self):
        return self.num_nodes

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

    def insert(self, key: KT, value: VT) -> None:
        self.num_nodes += 1
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
                elif x.key == key:
                    x.value = value
                    return

            # Rebalance maxheap
            if new.priority > x.priority:  # The heap is imbalanced
                self.rebalance_heap(new)


    def left_rotate(self, node):
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

    def right_rotate(self, node):
        """
        Helper for rebalancing. Performs a left rotation around node.
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

        ''' These were the first rotate functions, with superfluous code. Remove once confident in the new ones.
        def left_rotate(self, node):
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
                # if node.right_child is not None: node.right_child.parent = node
                child.left_child = node
                node.parent = child

                if node_child_type == 'L':
                    grandparent.left_child = child
                elif node_child_type == 'R':
                    grandparent.right_child = child
                child.parent = grandparent

            elif grandparent is None:
                node.right_child = child.left_child
                node.correct_children()
                # if node.right_child is not None: node.right_child.parent = node

                child.left_child = node
                node.parent = child
                self.root = child
                child.parent = None
                
        def right_rotate(self, node):
            """
            Helper for rebalancing. Performs a left rotation around node.
            """
            # Get relational nodes
            child = node.left_child
            grandparent = node.parent
            if grandparent is not None:
                node_child_type = 'L' if node.is_left_child() else 'R'
    
                node.left_child = child.right_child
                node.correct_children()
                #if node.left_child is not None: node.left_child.parent = node
    
                child.right_child = node
                node.parent = child
    
                if node_child_type == 'L':
                    grandparent.left_child = child
                elif node_child_type == 'R':
                    grandparent.right_child = child
                child.parent = grandparent
    
            elif grandparent is None:
                node.left_child = child.right_child
                node.correct_children()
                #if node.left_child is not None: node.left_child.parent = node
    
                child.right_child = node
                node.parent = child
                self.root = child
                child.parent = None            
                '''



    def rebalance_heap(self, child):
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
        x = self.root

        while True:
            if x is None:
                return None
            if key > x.key:
                x = x.right_child
            elif key < x.key:
                x = x.left_child
            elif key == x.key:
                victim = x
                val = victim.value
                break
            else:
                raise ValueError

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
        if victim.is_left_child():
            victim.parent.left_child = None
        elif victim.is_right_child():
            victim.parent.right_child = None

        return val

    def insert_with_max_priority(self, key: KT) -> None:
        """
        Helper for `split`. Same function as insert, however sets the priority
        of the new node to the max priority.
        """
        value = None
        if self.root is None:
            self.root = TreapNode(key, value)
        else:
            x = self.root
            # Perform the BST insertion
            while True:
                if x.key >= key:
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
            new.set_priority_to_max()
            self.rebalance_heap(new)

    def split(self, threshold: KT) -> List[Treap[KT, VT]]:
        # 1) Insert new entry x with key threshold, and priority = MAXPRIORITY
        self.insert_with_max_priority(threshold)
        # 2) T1 is the left subtree, T2 is the right
        T1 = TreapMap(self.root.left_child)
        T2 = TreapMap(self.root.right_child)
        return [T1, T2]

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

    def str_helper(self, node: TreapNode, level: int = 0, type: str='Root'):
        if node is None:
            return
        yield node, level, type
        yield from self.str_helper(node.left_child, level + 1, 'L')
        yield from self.str_helper(node.right_child, level + 1, 'R')

    def __str__(self) -> str:
        nodes = self.str_helper(self.root)
        lines = []
        for node, lvl, type in nodes:
            lines.append('\t'*lvl + f'{type}: {(node.key, node.priority)}')

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
