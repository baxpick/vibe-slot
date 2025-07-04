#!/usr/bin/env python3
import random
import sys
import pygame
import os, urllib.request
import asyncio

# Map fruit names to colors
COLOR_MAP = {
    '🍒': (220, 20, 60),      # red
    '🍋': (255, 255, 102),   # yellow
    '🍊': (255, 165, 0),     # orange
    '🍉': (0, 200, 0),       # green
    '🍇': (128, 0, 128),     # purple
    '🍓': (255, 105, 180),   # pink
}
SYMBOLS = list(COLOR_MAP.keys())

# Prepare asset directory and download Twemoji images
ASSET_DIR = 'assets'
os.makedirs(ASSET_DIR, exist_ok=True)
CODEPOINTS = {'🍒':'1f352','🍋':'1f34b','🍊':'1f34a','🍉':'1f349','🍇':'1f347','🍓':'1f353'}
for sym, cp in CODEPOINTS.items():
    fp = os.path.join(ASSET_DIR, f'{cp}.png')
    if not os.path.exists(fp):
        try: urllib.request.urlretrieve(f'https://abs.twimg.com/emoji/v2/72x72/{cp}.png', fp)
        except: pass

# Prepare lines: 3 horizontals and 2 diagonals, with distinct colors
LINES = [
    [(0,0),(0,1),(0,2)],  # top row
    [(1,0),(1,1),(1,2)],  # middle row
    [(2,0),(2,1),(2,2)],  # bottom row
    [(0,0),(1,1),(2,2)],  # main diagonal
    [(0,2),(1,1),(2,0)],  # anti-diagonal
]
# distinct color per line for overlay
LINE_COLORS = [
    (255, 0, 0),      # top row
    (255, 165, 0),    # middle row
    (255, 255, 0),    # bottom row
    (0, 255, 0),      # main diagonal
    (0, 255, 255),    # anti-diagonal
]

# Betting mode options
MODES = ['Horizontal', 'Diagonal', 'Both']
bet_mode = 0
# Multiplier options
MULTIPLIERS = [1, 2, 3, 4, 5]
multiplier_idx = 0

def get_selected_lines() -> list[list[tuple[int,int]]]:
    # return list of line coordinate groups based on bet mode
    if bet_mode == 0:
        return LINES[:3]
    if bet_mode == 1:
        return LINES[3:]
    return LINES

def spin() -> list[list[str]]:
    # generate 3x3 grid of random symbols
    return [random.choices(SYMBOLS, k=3) for _ in range(3)]

def evaluate_line(line: list[str]) -> int:
    # three of a kind
    if line[0] == line[1] == line[2]:
        return 5
    # two adjacent matching symbols
    for i in range(2):
        if line[i] == line[i+1]:
            return 2
    return 0

def evaluate_all(grid: list[list[str]]) -> list[tuple[list[tuple[int,int]], int]]:
    wins = []
    for coords in get_selected_lines():
        # only evaluate bet-selected lines
        line_syms = [grid[r][c] for r,c in coords]
        payout = evaluate_line(line_syms)
        if payout > 0:
            wins.append((coords, payout))
    return wins

SCREEN_WIDTH, SCREEN_HEIGHT = 600, 500
BUTTON_WIDTH, BUTTON_HEIGHT = 180, 40

def draw(screen, grid, credits, message, font, highlight_win=None, selected_lines=None):
    screen.fill((30, 30, 30))
    # compute offsets to center slot
    offset_x = (SCREEN_WIDTH - 264) // 2
    offset_y = (SCREEN_HEIGHT - 204) // 2
    # prepare fancy lines selection button with fixed width based on widest label
    padding_x, padding_y = 20, 10
    # compute max width among all mode labels
    max_label_w = max(font.size(f'Lines: {mode}')[0] for mode in MODES)
    btn_w = max_label_w + padding_x * 2
    btn_h = BUTTON_HEIGHT
    btn_x = SCREEN_WIDTH // 2 - btn_w // 2
    btn_y = 10
    btn_rect = pygame.Rect(btn_x, btn_y, btn_w, btn_h)
    # render current label
    label = font.render(f'Lines: {MODES[bet_mode]}', True, (255,255,255))
    lbl_rect = label.get_rect(center=btn_rect.center)

    # draw fancy button: shadow, background, border, label
    pygame.draw.rect(screen, (0, 0, 0), btn_rect.move(3, 3), border_radius=8)
    pygame.draw.rect(screen, (30, 144, 255), btn_rect, border_radius=8)
    pygame.draw.rect(screen, (255, 255, 255), btn_rect, 2, border_radius=8)
    screen.blit(label, lbl_rect)

    # draw fancy multiplier button below lines button
    # compute max width for multiplier labels
    max_mult_w = max(font.size(f'Multiplier: x{m}')[0] for m in MULTIPLIERS)
    mbtn_w = max_mult_w + padding_x * 2
    mbtn_h = BUTTON_HEIGHT
    mbtn_x = SCREEN_WIDTH // 2 - mbtn_w // 2
    mbtn_y = btn_y + btn_h + 5
    mbtn_rect = pygame.Rect(mbtn_x, mbtn_y, mbtn_w, mbtn_h)
    # draw multiplier button
    pygame.draw.rect(screen, (0,0,0), mbtn_rect.move(3,3), border_radius=8)
    pygame.draw.rect(screen, (255,165,0), mbtn_rect, border_radius=8)  # orange background
    pygame.draw.rect(screen, (255,255,255), mbtn_rect, 2, border_radius=8)
    mult_label = font.render(f'Multiplier: x{MULTIPLIERS[multiplier_idx]}', True, (255,255,255))
    mult_lbl_rect = mult_label.get_rect(center=mbtn_rect.center)
    screen.blit(mult_label, mult_lbl_rect)

    # draw 3x3 grid
    for r, row in enumerate(grid):
        for c, sym in enumerate(row):
            img = pygame.image.load(os.path.join(ASSET_DIR, f"{CODEPOINTS[sym]}.png")).convert_alpha()
            img = pygame.transform.smoothscale(img, (64,64))
            x = offset_x + c * 100
            y = offset_y + r * 70
            screen.blit(img, (x, y))
            # highlight winning cells
            if highlight_win and (r, c) in highlight_win:
                pygame.draw.rect(screen, (255,215,0), (x-4, y-4, 64+8, 64+8), 4)
    # draw selected bet lines as colored connectors when passed
    if selected_lines:
        for idx, line in enumerate(selected_lines):
            color = LINE_COLORS[idx]
            points = []
            for r, c in line:
                px = offset_x + c * 100 + 32
                py = offset_y + r * 70 + 32
                points.append((px, py))
            pygame.draw.lines(screen, color, False, points, 4)
    # draw credits, bet, lines count, and message
    cred_text = font.render(f'Credits: {credits}', True, (255,255,255))
    screen.blit(cred_text, (10, btn_y + btn_h + 10))
    bet_amount = len(get_selected_lines()) * MULTIPLIERS[multiplier_idx]
    bet_text = font.render(f'Bet: {bet_amount}', True, (255,255,255))
    screen.blit(bet_text, (10, btn_y + btn_h + 40))
    msg_text = font.render(message, True, (255,255,255))
    screen.blit(msg_text, (10, SCREEN_HEIGHT - 40))
    pygame.display.flip()

async def main():
    global bet_mode, multiplier_idx
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Fruit Slot')
    spin_active = False
    show_selection = False  # initialize before any draw or event

    # prepare dynamic button rect for input detection (must match draw)
    padding_x, padding_y = 20, 10
    max_label_w = max(pygame.font.Font(None, 32).size(f'Lines: {mode}')[0] for mode in MODES)
    btn_w = max_label_w + padding_x * 2
    btn_h = BUTTON_HEIGHT
    btn_x = SCREEN_WIDTH // 2 - btn_w // 2
    btn_y = 10
    button_rect = pygame.Rect(btn_x, btn_y, btn_w, btn_h)
    # prepare multiplier button rect for input detection
    max_mult_w = max(pygame.font.Font(None, 32).size(f'Multiplier: x{m}')[0] for m in MULTIPLIERS)
    mbtn_w = max_mult_w + padding_x * 2
    mbtn_h = BUTTON_HEIGHT
    mbtn_x = SCREEN_WIDTH // 2 - mbtn_w // 2
    mbtn_y = btn_y + btn_h + 5
    mult_button_rect = pygame.Rect(mbtn_x, mbtn_y, mbtn_w, mbtn_h)

    # preload images after video mode is set
    IMAGES = {sym: pygame.transform.smoothscale(pygame.image.load(os.path.join(ASSET_DIR, f"{cp}.png")).convert_alpha(), (64,64)) for sym, cp in CODEPOINTS.items()}
    font = pygame.font.Font(None, 32)
    credits = 100
    grid = spin()
    message = 'Press SPACE to spin'
    # initial display: show overlays if selection active
    draw(screen, grid, credits, message, font, None, get_selected_lines() if show_selection else None)
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # cycle betting mode on button click (disabled during spin)
            if event.type == pygame.MOUSEBUTTONDOWN and not spin_active and button_rect.collidepoint(event.pos):
                bet_mode = (bet_mode + 1) % len(MODES)
                show_selection = True
                draw(screen, grid, credits, message, font, None, get_selected_lines())
            # cycle multiplier on multiplier button click
            if event.type == pygame.MOUSEBUTTONDOWN and not spin_active and mult_button_rect.collidepoint(event.pos):
                multiplier_idx = (multiplier_idx + 1) % len(MULTIPLIERS)
                draw(screen, grid, credits, message, font, None, get_selected_lines() if show_selection else None)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                # start spin: disable buttons only now
                spin_active = True
                show_selection = False
                # determine bet cost as number of selected lines * multiplier
                cost = len(get_selected_lines()) * MULTIPLIERS[multiplier_idx]
                if credits < cost:
                    message = 'Not enough credits'
                    draw(screen, grid, credits, message, font, None, get_selected_lines())
                    # re-enable UI so player can adjust lines/multiplier
                    spin_active = False
                    continue
                credits -= cost
                if credits < 0:
                    credits = 0
                 # spin animation: cycle symbols, no overlays
                for _ in range(15):
                    temp_grid = [random.choices(SYMBOLS, k=3) for _ in range(3)]
                    draw(screen, temp_grid, credits, '', font, None, None)
                    await asyncio.sleep(0.05)
                # final spin result
                grid = spin()
                # evaluate wins and apply multiplier to each line, then immediately credit total win
                raw_wins = evaluate_all(grid)
                wins = [(coords, payout * MULTIPLIERS[multiplier_idx]) for coords, payout in raw_wins]
                total = sum(p for _, p in wins)
                credits += total
                skip_post_win = False
                # continuously highlight winning lines until player spins again
                if wins:
                    idx = 0
                    highlighting = True
                    while highlighting:
                        coords, payout = wins[idx]
                        message = f'Line {idx+1} wins {payout}'
                        draw(screen, grid, credits, message, font, highlight_win=coords, selected_lines=None)
                        await asyncio.sleep(0.8)
                        idx = (idx + 1) % len(wins)
                        # handle quitting or new spin
                        for ev in pygame.event.get():
                            if ev.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                            # allow stopping highlight with space key
                            if ev.type == pygame.KEYDOWN and ev.key == pygame.K_SPACE:
                                # re-post SPACE to trigger immediate new spin
                                pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE))
                                skip_post_win = True
                                highlighting = False
                                break
                            # allow changing bet_mode during highlight
                            if ev.type == pygame.MOUSEBUTTONDOWN and button_rect.collidepoint(ev.pos):
                                bet_mode = (bet_mode + 1) % len(MODES)
                                draw(screen, grid, credits, '', font, None, get_selected_lines())
                                highlighting = False
                                break
                            # allow changing multiplier during highlight
                            if ev.type == pygame.MOUSEBUTTONDOWN and mult_button_rect.collidepoint(ev.pos):
                                multiplier_idx = (multiplier_idx + 1) % len(MULTIPLIERS)
                                # redraw with current highlight but updated multiplier UI
                                draw(screen, grid, credits, message, font, highlight_win=coords, selected_lines=None)
                                highlighting = False
                                break
                # display final message unless skipped
                if not skip_post_win:
                    if total > 0:
                        message = f'Total win {total}'
                    else:
                        message = 'No win'
                    if credits <= 0:
                        message = 'Game over!'
                    # redraw final grid without overlays (credits already updated)
                    draw(screen, grid, credits, message, font, None, None)
                # spin complete: re-enable mode toggling
                spin_active = False
        await asyncio.sleep(0)
        clock.tick(30)

if __name__ == '__main__':
    asyncio.run(main())
