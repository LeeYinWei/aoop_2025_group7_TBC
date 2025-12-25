import pygame
import sys
import asyncio
# 從 game 包中導入我們重寫好的同步主迴圈
from game.game_loop import main_game_loop

async def main():
    pygame.init()
    pygame.display.set_caption("The Snail Adventure")
    
    # 這裡的視窗大小需與您遊戲邏輯中的螢幕座標匹配
    screen = pygame.display.set_mode((1280, 600)) 
    clock = pygame.time.Clock()

    # 直接呼叫同步的 main_game_loop
    await main_game_loop(screen, clock)



if __name__ == "__main__":
    if sys.platform == "emscripten":  # 瀏覽器環境 (pygbag)
        asyncio.ensure_future(main())
    else:  # 本地 PC 環境
        try:
            asyncio.run(main())
        except KeyboardInterrupt:
            pass
