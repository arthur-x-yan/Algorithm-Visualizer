import sys, pygame
from visualizers import VIZ_REGISTRY

WIDTH, HEIGHT = 1000, 600
SIDEBAR_WIDTH = 500
BACKGROUND    = (30, 30, 30)
FONT_COLOR    = (255,255,255)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Algorithm Visualizer")
font   = pygame.font.SysFont(None, 28)
clock  = pygame.time.Clock()

# button widget
class Button:
    def __init__(self, text, rect):
        self.text = text
        self.rect = pygame.Rect(rect)

    def draw(self, mouse):
        clr = (100,100,255) if self.rect.collidepoint(mouse) else (70,70,200)
        pygame.draw.rect(screen, clr, self.rect)
        txt = font.render(self.text, True, FONT_COLOR)
        screen.blit(txt, txt.get_rect(center=self.rect.center))

# menu function
def show_menu():
    global WIDTH, HEIGHT
    # categorize visualizers
    categories = {"Sorting": [], "Searches": []}
    for title in VIZ_REGISTRY:
        if "Sort" in title:
            categories["Sorting"].append(title)
        else:
            categories["Searches"].append(title)

    btn_w, btn_h    = 200, 40
    v_gap, h_gap    = 20, 80
    label_offset_y  = 60
    first_btn_y     = label_offset_y + 30
    bottom_padding  = 80  

    columns = list(categories.items())
    total_cols_w = len(columns)*btn_w + (len(columns)-1)*h_gap
    start_x = (WIDTH - total_cols_w)//2

    # create buttons
    buttons = []
    for col_idx, (cat, titles) in enumerate(columns):
        col_x = start_x + col_idx*(btn_w + h_gap)
        for row_idx, title in enumerate(titles):
            x = col_x
            y = first_btn_y + row_idx*(btn_h + v_gap)
            buttons.append(Button(title, (x, y, btn_w, btn_h)))

    max_btns = max(len(v) for _, v in columns)
    last_y = first_btn_y + max_btns*(btn_h + v_gap)
    exit_btn_y = min(HEIGHT - bottom_padding, last_y + 40)
    exit_btn = Button("Exit", ((WIDTH - btn_w)//2, exit_btn_y, btn_w, btn_h))

    # event loop
    while True:
        mouse = pygame.mouse.get_pos()
        screen.fill(BACKGROUND)

        # draw headers
        for col_idx, (cat, _) in enumerate(columns):
            col_x = start_x + col_idx*(btn_w + h_gap)
            header = font.render(cat, True, FONT_COLOR)
            screen.blit(header, header.get_rect(center=(col_x + btn_w//2, label_offset_y)))

        # draw visualizer buttons
        for b in buttons:
            b.draw(mouse)

        # draw Exit button
        exit_btn.draw(mouse)

        pygame.display.flip()

        # handle events
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                for b in buttons:
                    if b.rect.collidepoint(mouse):
                        run_visualizer(VIZ_REGISTRY[b.text])
                if exit_btn.rect.collidepoint(mouse):
                    pygame.quit(); sys.exit()
            if e.type == pygame.VIDEORESIZE:
                WIDTH, HEIGHT = e.w, e.h
                pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)


# runner
def run_visualizer(viz_cls):
    viz = viz_cls(screen.get_rect())
    paused = False

    # milliseconds between steps
    step_interval = getattr(viz, "step_interval", 500)
    last_step_ts  = pygame.time.get_ticks()

    while True:
        now = pygame.time.get_ticks()

        # events
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    return                          # back to menu
                if e.key == pygame.K_p:
                    paused = not paused             # play / pause
                if e.key == pygame.K_RIGHT:         # single step
                    paused = True
                    try: viz.step()
                    except StopIteration: pass
                if e.key == pygame.K_r:             # reset visualizer
                    try:
                        viz.reset()  
                    except AttributeError:
                        viz = viz_cls(screen.get_rect())

        # autoplay step
        if not paused and now - last_step_ts >= step_interval:
            try:
                viz.step()
                last_step_ts = now
            except StopIteration:
                paused = True

        # draw everything
        screen.fill(BACKGROUND)
        pygame.draw.rect(screen, (50,50,50), (0,0,SIDEBAR_WIDTH,HEIGHT))
        screen.blit(font.render(viz.title, True, FONT_COLOR), (20, 20))
        screen.blit(font.render(f"Steps: {viz.steps}", True, FONT_COLOR), (20, 60))
        for i, line in enumerate(viz.description):
            screen.blit(font.render(line, True, FONT_COLOR), (20, 100 + i*25))

        # draw controls at bottom
        screen.blit(font.render("Controls:", True, FONT_COLOR), (20, HEIGHT - 150))
        screen.blit(font.render("Press R to reset", True, FONT_COLOR), (20, HEIGHT - 120))
        screen.blit(font.render("Press RIGHT to step once", True, FONT_COLOR), (20, HEIGHT - 90))
        screen.blit(font.render("Press P to pause/resume", True, FONT_COLOR), (20, HEIGHT - 60))
        screen.blit(font.render("Press ESC to return to menu", True, FONT_COLOR), (20, HEIGHT - 30))
        
        

        viz.draw(screen, font)
        pygame.display.flip()
        clock.tick(60)           # 60 FPS window refresh


# start the program
if __name__ == "__main__":
    show_menu()