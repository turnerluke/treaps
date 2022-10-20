




# Meld
Melding two Treaps is similar to the process of inserting a node, however there are some key differences.
Instead of inserting a node, we act as if we are inserting the root of the next Treap.
Then, when we find the right leaf to insert the node, we must check its children to see if they're also in valid positions.
We do so by checking down the right and left paths from the inserted node, and if they are invalid removing them to be inserted as new melds later.

The logic for checking subtrees is as follows:

1. If the inserted node is a right child.
   1. Its entire lineage of left children must be greater than the new nodes parent.
   2. If the new node has a grandparent, the entire lineage of right children must be greater than the grandparent.
2. If the inserted node is a left child.
   1. Its entire lineage of right children must be greater than the new nodes parent.
   2. If the new node has a grandparent, the entire lineage of left children must be greater than the grandparent.

Then, the Heap property is balanced the same as in the insert, however, each time a subsection of new tree is 'transplanted' onto a section of old tree it must also be rebalanced.

## Time bound
This algorithm meets the specification of O(m log(n/m)) (where m < n)), because there is at worst m occasions (number of nodes in smaller treap)
of insertions into the larger tree (n nodes) which is O(m log(n)) this is adjusted by -m log(m) due to the efficiency of inserting sections
of the smaller treap, as opposed to each node.

# Difference

# Balance
The balance of the tree, as defined by the project handout is the ratio of the height of the tree and the minimum possible height.

$bal = h/h_{min}$

Where the minimum height is the floor of the log base two of the number of nodes.

Thus, the balance is 1 for a perfectly balanced tree and n/floor(log2(n)) for the worst case scenerio (i.e. a straight line, where all children are the same type of child.)

## Characterization
In /experiments/balance_characterization.py the treaps are observed to have balances of 2.1 +/- 0.3.
The balances are not exceptional, compared to options like AVLs or Red-Black trees which will have balances much closer to 1.