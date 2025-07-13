import pygame
from config import SIDEBAR
import my_algorithms.searches as searches
from data_structures import build_random_tree

class DFSTreeViz:
    title = "DFS (Binary Tree)"
    description = [
        "backtracking search over a binary tree.",
        "fully explores one branch before",
        "moving to the next.",
        "",
        "Red = currently visiting.",
        "Green = visited."
    ]
    step_interval = 500

    def __init__(self, screen_rect):
        self.width, self.height = screen_rect.size
        self.root = build_random_tree()
        self.gen = searches.dfs_tree(self.root) 
        self.current = None
        self.steps = 0
        self.positions = {}
        self._compute_layout(self.root)
        self.visited = set()
        self.done = False

    def step(self):
        if self.done:
            return
        try:
            self.current = next(self.gen)  
            self.visited.add(self.current)
            self.steps += 1
        except StopIteration:
            self.current = None
            self.done = True

    def _compute_layout(self, root):
        """Assign (x, y) positions to each TreeNode using DFS."""
        levels = {}  

        def dfs(node, depth=0):
            if not node: return
            if depth not in levels:
                levels[depth] = []
            levels[depth].append(node)
            dfs(node.left, depth+1)
            dfs(node.right, depth+1)
        dfs(root)

        y_spacing = 100
        for depth in levels:
            nodes = levels[depth]
            count = len(nodes)
            x_spacing = (self.width - SIDEBAR) // (count + 1)
            for i, node in enumerate(nodes):
                x = SIDEBAR + (i + 1) * x_spacing
                y = 40 + depth * y_spacing
                self.positions[node] = (x, y)

    def draw(self, surf, font):
        # draw edges
        def draw_edges(node):
            if not node: return
            x1, y1 = self.positions[node]
            if node.left:
                x2, y2 = self.positions[node.left]
                pygame.draw.line(surf, (100,100,100), (x1, y1), (x2, y2), 2)
                draw_edges(node.left)
            if node.right:
                x2, y2 = self.positions[node.right]
                pygame.draw.line(surf, (100,100,100), (x1, y1), (x2, y2), 2)
                draw_edges(node.right)
        draw_edges(self.root)

        # draw nodes
        for node, (x, y) in self.positions.items():
            if node == self.current:
                color = (255, 0, 0)  # current
            elif node in self.visited:
                color = (0, 200, 0)  # visited
            else:
                color = (100, 100, 100)  # not yet visited

            pygame.draw.circle(surf, color, (x, y), 20)
            label = font.render(str(node.val), True, (0,0,0))
            surf.blit(label, label.get_rect(center=(x, y)))