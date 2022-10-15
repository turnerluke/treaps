from py_treaps.treap_map import TreapMap

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
        print(f"\n------------------")
        print(f"Number of elements: {treap.get_num_elements()}")
        print(treap)
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
        print(f"\n------------------")
        print(f"Number of elements: {treap.get_num_elements()}")
        print(treap)
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

# TODO: Real removal testing


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
    print('\n')
    print('ORIGINAL')
    print(original_treap)
    left, right = original_treap.split(3)
    print("FINAL LEFT")
    print(left)
    print("FINAL RIGHT")
    print(right)

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
    print('\n')
    print('Original')
    print(original_treap)
    left, right = original_treap.split(5)
    print("Left")
    print(left)
    print("Right")
    print(right)

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

# TODO: Return and make better
def test_heap_property_simple_starter() -> None:
    """Test heap property in a basic way"""

    for _ in range(50):  # Run this test a bunch to account for randomness
        t = TreapMap()
        for i in range(10):
            t.insert(str(i), str(i))
        root_node = t.get_root_node()

        # Is this sufficient to test the heap property?

        if (
            root_node.key != "0"
        ):  # why does this if statement exist? What if you remove it?
            assert root_node.priority >= root_node.left_child.priority
        if root_node.key != "9":
            assert root_node.priority >= root_node.right_child.priority


def test_bst_property_simple_starter() -> None:
    """Test BST property in a basic way"""

    for _ in range(50):  # Run this test a bunch to account for randomness
        t = TreapMap()
        for i in range(10):
            t.insert(str(i), str(i))
        root_node = t.get_root_node()

        # Is this sufficient to test the BST property?

        if root_node.key != "0":
            assert root_node.key >= root_node.left_child.key
        if root_node.key != "9":
            assert root_node.key <= root_node.right_child.key

#TODO: Test join