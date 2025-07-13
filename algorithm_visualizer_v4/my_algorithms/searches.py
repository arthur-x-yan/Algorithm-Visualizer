from collections import deque

def bfs_tree(root):
    """Yield nodes in BFS order"""
    if not root:
        return
    visited = set()
    q = deque([root])
    visited.add(root)
    
    while q:
        node = q.popleft()
        yield node
        for child in (node.left, node.right):
            if child and child not in visited:
                visited.add(child)
                q.append(child)

def dfs_tree(root):
    """Yield nodes in DFS order"""
    if not root:
        return
    yield root
    yield from dfs_tree(root.left)
    yield from dfs_tree(root.right)

def binary_search(arr, target):
    """Yield (array_snapshot, low, high)"""
    low, high = 0, len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        yield arr[:], low, high  # show current search range
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1  # target not found