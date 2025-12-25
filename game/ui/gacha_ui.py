# game/ui/gacha_ui.py
import pygame
import asyncio
import random

async def gacha_ui(screen, clock):
    font = pygame.font.Font(None, 48)
    msg = "點擊抽蛋!"
    result = None
    pool = ["貓A", "貓B", "貓C", "SSR神貓"]

    while True:
        screen.fill((255,240,200))
        screen.blit(font.render(msg, True, (0,0,0)), (500,200))
        if result:
            screen.blit(font.render("🎉 你抽到: " + result, True, (0,0,0)), (500,300))

        screen.blit(font.render("⬅ 返回", True, (0,0,0)), (500, 450))
        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return
            elif e.type == pygame.MOUSEBUTTONDOWN:
                mx,my = e.pos
                if 500 < mx < 800:
                    if 200 < my < 250:
                        result = random.choice(pool)
                    elif 450 < my < 500:
                        return

        clock.tick(60)
        await asyncio.sleep(0)
