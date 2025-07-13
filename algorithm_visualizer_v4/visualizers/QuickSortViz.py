import random, pygame
from config import SIDEBAR, BAR_COLOR, HIGHLIGHT_COLOR, POINTER_COLOR
import my_algorithms.sorting as sorting

class QuickSortViz:
    title = "Quick Sort"
    description = [
        "Quick Sort: selects a pivot element",
        "and partitions the array so that",
        "elements less than the pivot go left,",
        "and greater go right.",
        "",
        "Then it recursively sorts both sides.",
        "",
        "Yellow = pivot element",
        "Red = comparison/swap in progress"
    ]
    step_interval = 60

    def __init__(self, screen_rect, bar_count=30):
        self.width, self.height = screen_rect.size
        self.data = [random.randint(10, self.height - 10) for _ in range(bar_count)]
        self.gen = sorting.quick_sort(self.data)
        self.highlight = ()
        self.steps = 0

    def step(self):
        self.steps += 1
        self.data, self.highlight = next(self.gen)

    def draw(self, surf, font):
        bar_w = (self.width - SIDEBAR) // len(self.data)
        for i, val in enumerate(self.data):
            x = SIDEBAR + i * bar_w
            if not self.highlight:
                color = BAR_COLOR
            elif i == self.highlight[-1]:
                color = POINTER_COLOR  # pivot
            elif i in self.highlight:
                color = HIGHLIGHT_COLOR
            else:
                color = BAR_COLOR
            pygame.draw.rect(surf, color, (x, self.height - val, bar_w - 1, val))