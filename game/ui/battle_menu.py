# game/ui/battle_menu.py
import pygame
import asyncio
import os
from game.ui.map_level import cat_selection

LEVEL_PATH = "level_folder"

async def battle_menu(screen, clock):
    font = pygame.font.Font(None, 48)
    levels = [d for d in os.listdir(LEVEL_PATH) if d.startswith("level_")]

    while True:
        screen.fill((240,240,240))
        y = 150
        for lvl in levels:
            txt = font.render(lvl, True, (0,0,0))
            screen.blit(txt, (500, y))
            y += 60
        
        back = font.render("⬅ 返回", True, (0,0,0))
        screen.blit(back, (500, y + 50))

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx,my = event.pos
                # detect click
                idx = (my-150) // 60
                if 0 <= idx < len(levels):
                    await cat_selection(screen, clock, levels[idx])
                elif y+50 < my < y+100:
                    return

        clock.tick(60)
        await asyncio.sleep(0)
