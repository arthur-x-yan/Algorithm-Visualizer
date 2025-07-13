import random, pygame
from config import SIDEBAR, BAR_COLOR, HIGHLIGHT_COLOR, POINTER_COLOR
import my_algorithms.sorting as sorting

class InsertionSortViz:
    title = "Insertion Sort"
    description = [
        "Iteratively builds a sorted array by",
        "inserting each element into its correct",
        "position among the already sorted elements.",
        "",
        "Yellow = key element",
        "Red    = element compared / shifted",
        "Heights change only on actual shifts"
    ]
    step_interval = 60  # ms between steps

    def __init__(self, screen_rect, bar_count=30):
        self.width, self.height = screen_rect.size
        self.data = [random.randint(10, self.height - 10) for _ in range(bar_count)]
        self.gen = sorting.insertion_sort(self.data)
        self.red_idx = self.key_idx = None
        self.steps = 0

    def step(self):
        self.steps += 1
        self.data, self.red_idx, self.key_idx = next(self.gen)

    def draw(self, surf, font):
        bar_w = (self.width - SIDEBAR) // len(self.data)
        for i, val in enumerate(self.data):
            x = SIDEBAR + i * bar_w

            if i == self.key_idx:
                color = POINTER_COLOR        # yellow key
            elif i == self.red_idx:
                color = HIGHLIGHT_COLOR      # red shifting element
            else:
                color = BAR_COLOR      

            pygame.draw.rect(
                surf, color, (x, self.height - val, bar_w - 1, val)
            )