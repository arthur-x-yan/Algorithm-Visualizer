import random, pygame
from config import SIDEBAR, BAR_COLOR, HIGHLIGHT_COLOR, POINTER_COLOR
import my_algorithms.sorting as sorting

class SelectionSortViz:
    title = "Selection Sort"
    description = [
        "Selection Sort: finds the minimum",
        "in the unsorted part and swaps it",
        "with the first unsorted element.",
        "",
        "Yellow = minimum found in this pass",
        "Red = current selection.",
        "Blue = destination for swap."
    ]
    step_interval = 60

    def __init__(self, screen_rect, bar_count=30):
        self.width, self.height = screen_rect.size
        self.data = [random.randint(10, self.height - 10) for _ in range(bar_count)]
        self.gen = sorting.selection_sort(self.data)
        self.highlight = None
        self.min_idx = None
        self.dest = None
        self.steps = 0

    def step(self):
        self.steps += 1
        self.data, self.highlight, self.dest, self.min_idx = next(self.gen)

    def draw(self, surf, font):
        bar_w = (self.width - SIDEBAR) // len(self.data)
        for i, val in enumerate(self.data):
            x = SIDEBAR + i * bar_w
            if i == self.highlight:
                color = HIGHLIGHT_COLOR
            elif i == self.min_idx:
                color = POINTER_COLOR
            elif i == self.dest:
                color = (0, 120, 255)
            else:
                color = BAR_COLOR
            pygame.draw.rect(surf, color, (x, self.height - val, bar_w-1, val))