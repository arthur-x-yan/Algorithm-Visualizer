import random
from collections import deque

#leetcode tree node
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
    def __hash__(self):
        return id(self)

    def __eq__(self, other):
        return self is other

import random

def build_random_tree(
    min_nodes: int = 7,
    max_nodes: int = 15,
    max_depth: int = 6
) -> TreeNode:

    if min_nodes < 1 or max_nodes < min_nodes:
        raise ValueError("Bad min/max")

    target = random.randint(min_nodes, max_nodes)

    root   = TreeNode()                 # leave val blank for now
    nodes  = [(root, 0)]                # (node, depth)
    pool   = [root]                     # list for picking parents

    # build tree
    while len(nodes) < target:
        parent = random.choice(pool)
        depth  = next(d for (n, d) in nodes if n is parent)

        if depth >= max_depth - 1:
            continue

        for side in random.sample(["left", "right"], 2):
            if getattr(parent, side) is None and len(nodes) < target:
                child = TreeNode()                   # unlabeled for now
                setattr(parent, side, child)
                nodes.append((child, depth + 1))
                pool.append(child)
                break   # add only one child per loop-iteration

    # label nodes
    q = deque([root])
    label = 1
    while q:
        node = q.popleft()
        node.val = label
        label   += 1
        if node.left:  q.append(node.left)
        if node.right: q.append(node.right)

    return root