from py_treaps.treap_map import TreapMap
from py_treaps.stack import Stack

import pytest
from typing import Any



def test_empty_lookup_starter() -> None:
    """
    Test `lookup` on an empty Treap.
    """

    treap: TreapMap[Any, Any] = TreapMap()

    assert not treap.lookup(6)
    assert not treap.lookup(0)
    assert not treap.lookup("hi")


def test_single_insert_starter() -> None:
    """Test minimal insert/lookup functionality."""

    treap: TreapMap[str, str] = TreapMap()
    treap.insert("one", "one")

    assert treap.lookup("one") == "one"


def test_double_insert_starter() -> None:
    """
    Tests slightly greater insert/lookup functionality.
    Added because the second insert was fdiling.
    """
    treap: TreapMap[str, str] = TreapMap()
    treap.insert("one", "one")
    assert treap.lookup("one") == "one"
    treap.insert("two", "two")
    assert treap.lookup("two") == "two"


def test_multiple_insert_starter() -> None:
    """Test the insertion and lookup of multiple elements."""

    treap: TreapMap[int, str] = TreapMap()
    N = 21

    for i in range(N):
        treap.insert(i, str(i))
        assert treap.lookup(i) == str(i)

    # make sure all nodes are still there
    for i in range(N):
        assert treap.lookup(i) == str(i)


def test_multiple_insert_starter_reversed() -> None:
    """
    Test the insertion and lookup of multiple elements.
    Repeat of the above, except in reverse order, to ensure right rotations work
    along with the left rotations.
    """

    treap: TreapMap[int, str] = TreapMap()
    N = 21

    for i in reversed(range(N)):
        treap.insert(i, str(i))
        assert treap.lookup(i) == str(i)

    # make sure all nodes are still there
    for i in range(N):
        assert treap.lookup(i) == str(i)


def test_insert_overwrite_starter() -> None:
    """Test whether multiple insertions to the same key overwrites
    the value.
    """

    treap: TreapMap[int, str] = TreapMap()
    for i in range(10):
        treap.insert(i, str(i))

    for value in ("hi", "foo", "bar"):
        treap.insert(2, value)
        assert treap.lookup(2) == value


def test_empty_remove_starter() -> None:
    """Test `remove` on an empty Treap."""

    treap: TreapMap[str, int] = TreapMap()
    assert treap.remove("hi") is None


def test_remove() -> None:
    """
    Test a wide range of functionality of `remove`.
    """

    treap: TreapMap[int, int] = TreapMap()
    assert treap.remove(1) is None

    for i in range(6):
        treap.insert(i, i)

    assert treap.remove(3) == 3
    assert treap.remove(3) is None

    assert treap.remove(4) == 4
    treap.insert(5, 'ABC')
    assert treap.remove(5) == 'ABC'
    assert treap.remove(5) is None


def test_iterator_exception_starter() -> None:
    """Test that the TreapMap iterator raises a StopIteration
    when exhausted.
    """
    treap: TreapMap[int, str] = TreapMap()

    it = iter(treap)
    with pytest.raises(StopIteration):
        next(it)


def test_split_by_median_starter() -> None:
    """
    Test `split` with the median key.
    """

    original_treap = TreapMap()
    for i in range(21):
        original_treap.insert(i, str(i))
    left, right = original_treap.split(10)

    for key in left:
        assert 0 <= key < 10
    for i in range(10, 21):
        assert right.lookup(i) == str(i)


def test_get_root_node_starter() -> None:
    """Test that the root node works as expected"""

    t = TreapMap()
    for i in range(10):
        t.insert(i, i)
    root_node = t.get_root_node()
    assert root_node.key in list(range(10))
    assert root_node.value in list(range(10))
    assert root_node.parent is None
    assert root_node.left_child is not None or root_node.right_child is not None


def is_heap(t: TreapMap) -> bool:
    """
    Returns true if the TreapMap, t, obeys the heap property.
    """
    root = t.get_root_node()
    stack = Stack()
    stack.push(root)
    while stack:
        x = stack.pop()
        if x.has_right_child():
            if x.priority < x.right_child.priority:
                return False
            stack.push(x.right_child)
        if x.has_left_child():
            if x.priority < x.left_child.priority:
                return False
            stack.push(x.left_child)
    return True


def test_heap_property_simple_starter() -> None:
    """
    Test heap property in a basic way
    """

    for _ in range(50):  # Run this test a bunch to account for randomness
        t = TreapMap()
        for i in range(10):
            t.insert(str(i), str(i))
        assert is_heap(t), "TreapMap does not obey heap property."


def is_bst(t: TreapMap) -> bool:
    root = t.get_root_node()
    stack = Stack()
    stack.push(root)
    while stack:
        x = stack.pop()
        if x.has_right_child():
            if x.key > x.right_child.key:
                return False
            stack.push(x.right_child)
        if x.has_left_child():
            if x.key < x.left_child.key:
                return False
            stack.push(x.left_child)
    return True


def test_bst_property_simple_starter() -> None:
    """
    Test BST property in a basic way
    """

    for _ in range(50):  # Run this test a bunch to account for randomness
        t = TreapMap()
        for i in range(10):
            t.insert(str(i), str(i))
        assert is_bst(t), "TreapMap did not obey BST property."


def test_join() -> None:
    t = TreapMap()
    t2 = TreapMap()

    for i in range(10):
        t.insert(i, str(i))
    for i in range(10, 20):
        t2.insert(i, str(i))

    t.join(t2)
    for i in range(20):
        assert i in t
        assert t.lookup(i) == str(i)


def test_empty_join_l() -> None:
    t = TreapMap()
    t2 = TreapMap()

    for i in range(10):
        t.insert(i, str(i))

    t.join(t2)
    for i in range(10):
        assert i in t
        assert t.lookup(i) == str(i)


def test_empty_join_r() -> None:
    t = TreapMap()
    t2 = TreapMap()

    for i in range(10):
        t2.insert(i, str(i))

    t.join(t2)
    for i in range(10):
        assert i in t
        assert t.lookup(i) == str(i)


def test_double_empty_join() -> None:
    t = TreapMap()
    t2 = TreapMap()

    t.join(t2)
    for i in range(-100, 101, 10):
        assert i not in t
    assert t.get_root_node() is None


def test_iterator_independence() -> None:
    for _ in range(50):  # Run this test a bunch to account for randomness
        t = TreapMap()
        for i in range(10):
            t.insert(str(i), str(i))

    it1 = iter(t)
    it2 = iter(t)

    assert next(it1) == next(it2)
    assert next(it1) == next(it2)
    assert next(it1) == next(it2)
    next(it1)
    assert next(it1) != next(it2)
    assert next(it1) != next(it2)


def test_meld() -> None:

    for pairs in [(range(0, 21, 2), range(1, 22, 2)), (range(0, 21), range(21, 41)), (range(-20, 1), range(1, 21))]:
        t = TreapMap()
        for i in pairs[0]:
            t.insert(i, i)
        t2 = TreapMap()
        for i in pairs[1]:
            t2.insert(i, i)

        t.meld(t2)

        assert is_heap(t), "Doesn't obey heap property"
        assert is_bst(t), "Doesn't obey BST property"


def test_difference():

    t = TreapMap()
    for i in range(0, 100):
        t.insert(i, i)
    t2 = TreapMap()
    for i in range(51, 100):
        t2.insert(i, i)

    t.difference(t2)

    for i in range(0, 51):
        assert i in t, "`Difference` did not function properly"
