




# Meld

# Difference

# Balance
The balance of the tree, as defined by the project handout is the ratio of the height of the tree and the minimum possible height.

$bal = h/h_{min}$

Where the minimum height is the floor of the log base two of the number of nodes.

Thus, the balance is 1 for a perfectly balanced tree and n/floor(log2(n)) for the worst case scenerio (i.e. a straight line, where all children are the same type of child.)

## Characterization
In /experiments/balance_characterization.py the treaps are observed to have balances of 2.1 +/- 0.3.
The balances are not exceptional, compared to options like AVLs or Red-Black trees which will have balances much closer to 1.