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


def test_small_split_by_median_starter() -> None:
    """
    Test `split` with the median key.
    """

    original_treap = TreapMap()
    for i in range(6):
        original_treap.insert(i, str(i))
    left, right = original_treap.split(3)

    for key in left:
        assert 0 <= key < 3
    for i in range(3, 6):
        assert right.lookup(i) == str(i)


def test_split_by_median_starter() -> None:
    """
    Test `split` with the median key.
    """

    original_treap = TreapMap()
    for i in range(11):
        original_treap.insert(i, str(i))
    left, right = original_treap.split(5)

    for key in left:
        assert 0 <= key < 5
    for i in range(5, 11):
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


def test_heap_property_simple_starter() -> None:
    """
    Test heap property in a basic way
    """

    for _ in range(50):  # Run this test a bunch to account for randomness
        t = TreapMap()
        for i in range(10):
            t.insert(str(i), str(i))
        root = t.get_root_node()
        stack = Stack()
        stack.push(root)
        while stack:
            x = stack.pop()
            if x.has_right_child():
                assert x.priority >= x.right_child.priority
                stack.push(x.right_child)
            if x.has_left_child():
                assert x.priority >= x.left_child.priority
                stack.push(x.left_child)


def test_bst_property_simple_starter() -> None:
    """
    Test BST property in a basic way
    """

    for _ in range(50):  # Run this test a bunch to account for randomness
        t = TreapMap()
        for i in range(10):
            t.insert(str(i), str(i))
        root = t.get_root_node()
        stack = Stack()
        stack.push(root)
        while stack:
            x = stack.pop()
            if x.has_right_child():
                assert x.key <= x.right_child.key
                stack.push(x.right_child)
            if x.has_left_child():
                assert x.key >= x.left_child.key
                stack.push(x.left_child)


# TODO: See if priorities can match
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