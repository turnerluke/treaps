from py_treaps.treap_map import TreapMap
import math

"""
Test how well TreapMaps tend to balance.
"""
balances = []
for _ in range(1_000):  # Perform 1000 replications
    t = TreapMap()

    for i in range(60):
        t.insert(i, i)

    bal = t.balance_factor()
    balances.append(bal)


avg_bal = sum(balances) / len(balances)
std_bal = math.sqrt(sum([(b - avg_bal)**2 for b in balances]) / (len(balances) - 1))

print(f"Average balance of Treap: {avg_bal}")
print(f"Standard deviation: {std_bal}")
