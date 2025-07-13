import random, pygame
from config import SIDEBAR, BAR_COLOR, HIGHLIGHT_COLOR, POINTER_COLOR
import my_algorithms.searches as searches

class BinarySearchViz:
    title = "Binary Search"
    description = [
        "Searches a sorted array for a target value.",
        "Divides the search range in half each step.",
        "",
        "Yellow = lowest bound",
        "Red    = highest bound",
        "Blue   = target value",
        "Orange arrow = mid index",
        "",
        "Stops when target is found or range is empty."
    ]
    step_interval = 800    # ms between comparisons

    def __init__(self, screen_rect, arr = None, bar_count=60):
        self.width, self.height = screen_rect.size

        # build a sorted list of unique values
        raw = random.sample(range(10, self.height - 20), bar_count)
        self.array = sorted(raw)


        self.target = random.choice(
            self.array 
        )

        self.gen = searches.binary_search(self.array, self.target)
        self.low = self.high = None
        self.steps = 0
        self.found      = False   # becomes True when search ends
        self.found_idx  = None    # index of the target if it was found

    def _scale(self, v):
        max_val = max(self.array)
        return int(v * (self.height - 120) / max_val)   # leave some headroom
    
    # comparison
    def step(self):
        try:
            self.array, self.low, self.high = next(self.gen)
            self.steps += 1
        except StopIteration:
            # low, high, mid from previous frame
            if self.low is not None and self.high is not None and self.low <= self.high:
                self.found_idx = (self.low + self.high) // 2
                self.found = True

    # draw frame
    def draw(self, surf, font):
        ORANGE = (255, 165, 0)
        bar_w = (self.width - SIDEBAR) // len(self.array)
        base  = self.height - 40

        mid = (self.low + self.high) // 2 if self.low is not None else None

        for i, v in enumerate(self.array):
            if self.found and i != self.found_idx:
                continue                     # skip non-target bars

            x = SIDEBAR + i * bar_w
            h = self._scale(v)

            if self.found and i == self.found_idx:
                color = ORANGE               # highlight final target bar
            elif i == self.low:
                color = POINTER_COLOR        # yellow low
            elif v == self.target:
                color = (0, 200, 255)        # blue target
            elif i == self.high:
                color = HIGHLIGHT_COLOR      # red high
            else:
                color = BAR_COLOR

            pygame.draw.rect(surf, color,
                            (x, base - h, bar_w - 1, h))

        # draw orange arrow for mid
        if mid is not None and not self.found:
            arrow_x = SIDEBAR + mid * bar_w + bar_w // 2
            h = self._scale(self.array[mid])           # height of the pivot bar
            bar_top = base - h                         # y-coordinate of bar’s top
            arrow_y = bar_top - 20                     # a small gap above the bar

            pygame.draw.polygon(
                surf, (255, 165, 0),                   # ORANGE
                [(arrow_x - 6, arrow_y),               # left corner
                (arrow_x + 6, arrow_y),               # right corner
                (arrow_x,     arrow_y + 8)]           # tip
            )

        # draw target label
        tgt_txt = font.render(f"Target: {self.target}", True, (255,255,255))
        surf.blit(tgt_txt, (SIDEBAR + 10, 10))

        # draw step counter
        step_txt = font.render(f"Steps: {self.steps}", True, (255,255,255))
        surf.blit(step_txt, (SIDEBAR + 10, 35))
