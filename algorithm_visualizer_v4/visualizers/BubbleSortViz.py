import random, pygame
from config import SIDEBAR, BAR_COLOR, HIGHLIGHT_COLOR
import my_algorithms.sorting as sorting

class BubbleSortViz:
    title = "Bubble Sort"
    description = [
        "Bubble Sort: repeatedly compares",
        "adjacent elements and swaps if out",
        "of order; largest values 'bubbles'",
        "to the end each pass.",
        "",
        "Red = elements being compared.",
    ]
    step_interval = 60

    def __init__(self, screen_rect, bar_count=30):
        self.width, self.height = screen_rect.size
        self.data = [random.randint(10, self.height-10) for _ in range(bar_count)]
        self.gen  = sorting.bubble_sort(self.data)
        self.highlight = ()
        self.steps = 0

    def step(self):
        self.steps += 1
        self.data, self.highlight = next(self.gen)

    # draw frame
    def draw(self, surf, font):
        bar_w = (self.width - SIDEBAR) // len(self.data)
        for i, val in enumerate(self.data):
            x = SIDEBAR + i * bar_w
            color = HIGHLIGHT_COLOR if i in self.highlight else BAR_COLOR
            pygame.draw.rect(surf, color, (x, self.height - val, bar_w-1, val))
