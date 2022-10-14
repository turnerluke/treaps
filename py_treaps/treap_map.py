from __future__ import annotations
import random
import typing
from collections.abc import Iterator
from typing import List, Optional, cast

from py_treaps.treap import KT, VT, Treap
from py_treaps.treap_node import TreapNode


# Example usage found in test_treaps.py
class TreapMap(Treap[KT, VT]):
    # Add an __init__ if you want. Make the parameters optional, though.
    def get_root_node(self) -> Optional[TreapNode]:
        pass # Your code here
    def lookup(self, key: KT) -> Optional[VT]:
        pass # Your code here
    def insert(self, key: KT, value: VT) -> None:
        pass # Your code here
    def remove(self, key: KT) -> Optional[VT]:
        pass # Your code here
    def split(self, threshold: KT) -> List[Treap[KT, VT]]:
        pass # Your code here
    def join(self, _other: Treap[KT, VT]) -> None:
        pass # Your code here
    def meld(self, other: Treap[KT, VT]) -> None: # KARMA
        raise AttributeError
    def difference(self, other: Treap[KT, VT]) -> None: # KARMA
        raise AttributeError
    def balance_factor(self) -> float: # KARMA
        raise AttributeError
    def __str__(self) -> str:
        pass # Your code here (optional method, ungraded)
    def __iter__(self) -> typing.Iterator[KT]:
        pass # Your code here
