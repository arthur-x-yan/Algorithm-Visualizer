import random, pygame
from config import SIDEBAR, BAR_COLOR, HIGHLIGHT_COLOR
import my_algorithms.sorting as sorting
class MergeSortViz:
    title = "Merge Sort"
    description = [
        "Phase 1: divide array into small segments.",
        "Phase 2: merge segments back together",
        "while maintaining order.",
        "",
        "Top: full array",
        "Bottom: current merge step.",
        "Red: compared elements in this merge."
    ]
    step_interval = 60


    def __init__(self, screen_rect, bar_count=50):
        self.width, self.height = screen_rect.size
        self.data = [random.randint(10, self.height // 2 - 20) for _ in range(bar_count)]
        self.gen = sorting.merge_sort(self.data[:])
        self.full_arr = self.data[:]
        self.segment = []
        self.highlight = ()
        self.steps = 0
        self.max_val = max(self.data) if self.data else 1  # avoid div by zero

    def _scale_top(self, val):
        return int(val * (self.height//3 - 20) / self.max_val)

    def _scale_bottom(self, val):
        return int(val * (self.height//3 - 40) / self.max_val)

    def step(self):
        self.steps += 1
        self.full_arr, self.segment, self.highlight = next(self.gen)

    def draw(self, surf, font):
        bar_w = (self.width - SIDEBAR) // len(self.full_arr)

        # panel baselines
        base_top    = self.height // 3
        base_bottom = self.height - 40
        

        # draw top bars
        for i, val in enumerate(self.full_arr):
            x = SIDEBAR + i * bar_w
            h = self._scale_top(val)
            pygame.draw.rect(surf, BAR_COLOR, (x, base_top - h, bar_w - 1, h))

        # draw bottom bars
        if self.segment:
            seg_len = len(self.segment)
            start_idx = self.full_arr.index(self.segment[0])

            for i, val in enumerate(self.segment):
                idx = start_idx + i
                x = SIDEBAR + idx * bar_w
                h = self._scale_bottom(val)
                color = HIGHLIGHT_COLOR if idx in self.highlight else BAR_COLOR
                pygame.draw.rect(surf, color, (x, base_bottom - h, bar_w - 1, h))

            # draw guard rails
            ORANGE = (255, 165,  0)
            left_x  = SIDEBAR + start_idx * bar_w
            right_x = SIDEBAR + (start_idx + seg_len) * bar_w
            pygame.draw.line(surf, ORANGE, (left_x,  20), (left_x,  self.height - 30), 2)
            pygame.draw.line(surf, ORANGE, (right_x, 20), (right_x, self.height - 30), 2)