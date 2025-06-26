#!/usr/bin/env python3
import random
import sys
import pygame
import os, urllib.request

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

def spin() -> list[str]:
    return random.choices(SYMBOLS, k=3)

def evaluate(results: list[str]) -> int:
    unique = set(results)
    if len(unique) == 1:
        return 5
    if len(unique) == 2:
        return 2
    return 0

SCREEN_WIDTH, SCREEN_HEIGHT = 360, 240

def draw(screen, results, credits, message, font):
    screen.fill((30, 30, 30))
    # draw fruit images
    for i, sym in enumerate(results):
        img = pygame.image.load(os.path.join(ASSET_DIR, f"{CODEPOINTS[sym]}.png")).convert_alpha()
        img = pygame.transform.smoothscale(img, (64,64))
        x = 48 + i * 100
        screen.blit(img, (x, 50))
    # draw credits and message
    cred_text = font.render(f'Credits: {credits}', True, (255,255,255))
    screen.blit(cred_text, (10, 10))
    msg_text = font.render(message, True, (255,255,255))
    screen.blit(msg_text, (10, SCREEN_HEIGHT - 40))
    pygame.display.flip()


def main():
    pygame.init()
    # initialize display before loading images
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Fruit Slot')
    # preload images after video mode is set
    IMAGES = {sym: pygame.transform.smoothscale(pygame.image.load(os.path.join(ASSET_DIR, f"{cp}.png")).convert_alpha(), (64,64)) for sym, cp in CODEPOINTS.items()}
    font = pygame.font.Font(None, 32)
    credits = 10
    results = spin()
    message = 'Press SPACE to spin'
    draw(screen, results, credits, message, font)
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if credits <= 0:
                    message = 'Game over!'
                else:
                    credits -= 1
                    # spin animation: cycle random symbols
                    for _ in range(15):
                        temp = random.choices(SYMBOLS, k=3)
                        draw(screen, temp, credits, '', font)
                        pygame.time.delay(50)
                    # final spin result
                    results = spin()
                    payout = evaluate(results)
                    if payout:
                        credits += payout
                        message = f'You win {payout}!'
                    else:
                        message = 'No win'
                    if credits <= 0:
                        message = 'Game over!'
                draw(screen, results, credits, message, font)
        clock.tick(30)

if __name__ == '__main__':
    main()
