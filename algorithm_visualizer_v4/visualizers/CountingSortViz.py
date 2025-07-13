import random, pygame
from config import SIDEBAR, BAR_COLOR, HIGHLIGHT_COLOR, POINTER_COLOR
import my_algorithms.sorting as sorting

class CountingSortViz:
    title = "Counting Sort"
    description = [
        "Phase 1: store frequency of each value in an array.",
        "Phase 2: write values back from left to right.",
        "",
        "Yellow = scan element",
        "Red    = array slot written",
        "Orange = freq bar just updated"
    ]
    step_interval = 80      # ms between steps

    def __init__(self, screen_rect, bar_count=60, value_range=59):
        self.width, self.height = screen_rect.size
        self.array = [random.randint(0, value_range) for _ in range(bar_count)]
        self.gen   = sorting.counting_sort(self.array[:])   # generator defined earlier

        # state updated each step
        self.freq      = []
        self.info      = {}
        self.steps     = 0
        self.max_val   = value_range       # for array scaling

    def _scale_array(self, v: int) -> int:
        """Scale array height to top panel."""
        return int(v * (self.height//3 - 20) / self.max_val)

    def _scale_freq(self, cnt: int) -> int:
        """Scale histogram bar height (dynamic until counting done)."""
        if hasattr(self, "fixed_max_cnt"):
            max_cnt = self.fixed_max_cnt
        else:
            max_cnt = max(self.freq) if self.freq else 1
        return int(cnt * (self.height//3 - 40) / max_cnt) if max_cnt else 0


    def step(self):
        self.steps += 1
        self.array, self.freq, self.info = next(self.gen)

        # freeze histogram scale & start banner when counting ends
        if self.info.get("phase") == "write" and not hasattr(self, "fixed_max_cnt"):
            self.fixed_max_cnt = max(self.freq) or 1
            self.count_phase_done = True


    def draw(self, surf, font):
        ORANGE = (255, 165, 0)  

        num_bars = max(len(self.array), len(self.freq) or 1)
        bar_w    = (self.width - SIDEBAR) // num_bars

        top_base    = self.height // 3
        bottom_base = self.height - 40

        phase  = self.info.get("phase")
        a_idx  = self.info.get("idx")
        val    = self.info.get("val")

        # top pannel
        for i, v in enumerate(self.array):
            x = SIDEBAR + i * bar_w
            h = self._scale_array(v)

            if phase == "count" and i == a_idx:
                color = POINTER_COLOR
            elif phase == "write" and i == a_idx:
                color = HIGHLIGHT_COLOR
            else:
                color = BAR_COLOR

            pygame.draw.rect(surf, color,
                             (x, top_base - h, bar_w - 1, h))

        # bottom panel
        if self.freq:
            for v, cnt in enumerate(self.freq):
                x = SIDEBAR + v * bar_w
                h = self._scale_freq(cnt)
                pygame.draw.rect(surf, BAR_COLOR,
                                 (x, bottom_base - h, bar_w - 1, h))
            # draw highlighted bar
            if phase in ("count", "write"):
                x = SIDEBAR + val * bar_w
                h = self._scale_freq(self.freq[val])
                pygame.draw.rect(surf, ORANGE,
                                 (x, bottom_base - h, bar_w - 1, h), 2)

        if getattr(self, "count_phase_done", False):
            msg = font.render("COUNTING DONE", True, ORANGE)
            surf.blit(msg, msg.get_rect(
                center=(SIDEBAR + (self.width - SIDEBAR)//2,
                        self.height // 3 + 10)))
            
        # draw step count
        step_txt = font.render(f"Steps: {self.steps}", True, (255,255,255))
        surf.blit(step_txt, (SIDEBAR + 10, 10))