# ui/gacha_developing.py

import pygame

def draw_gacha_developing_screen(
    screen,
    select_font,
    font,
    key_action_sfx=None
):
    """
    繪製「轉蛋系統開發中」的畫面並處理返回邏輯
    
    返回值：
        new_game_state (str | None): 
            - 如果玩家點擊「back」或按 ESC，返回 "main_menu"
            - 否則返回 None
    """
    SCREEN_WIDTH = screen.get_width()
    SCREEN_HEIGHT = screen.get_height()

    # 背景顏色（深紫色）
    screen.fill((50, 0, 100))

    # 標題
    title = select_font.render("Gacha System Developing Now!", True, (255, 255, 200))
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 200))

    # 小提示
    tip = font.render("Have fun!", True, (255, 255, 0))
    screen.blit(tip, (SCREEN_WIDTH // 2 - tip.get_width() // 2, 300))

    # 返回按鈕
    back_rect = pygame.Rect(50, SCREEN_HEIGHT - 100, 200, 60)
    pygame.draw.rect(screen, (200, 0, 0), back_rect, border_radius=20)
    
    back_text = font.render("Back", True, (255, 255, 255))
    screen.blit(back_text, back_text.get_rect(center=back_rect.center))

    # 更新畫面
    pygame.display.flip()

    # 事件處理
    new_game_state = None
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # 讓主程式處理退出
            pygame.event.post(event)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if back_rect.collidepoint(event.pos):
                new_game_state = "main_menu"
                if key_action_sfx and key_action_sfx.get('other_button'):
                    key_action_sfx['other_button'].play()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                new_game_state = "main_menu"
                if key_action_sfx and key_action_sfx.get('other_button'):
                    key_action_sfx['other_button'].play()

    return new_game_state

import pygame
import time

def draw_gacha_screen(screen, font, select_font, gacha_bg, key_action_sfx=None):
    from ..gacha_manager import perform_gacha
    from ..constants import GACHA_COST_GOLD, GACHA_COST_SOULS, RESOURCE_FILE
    import json

    # 每次繪製時重新讀取檔案，確保顯示最新數值
    with open(RESOURCE_FILE, "r") as f:
        player_data = json.load(f)

    SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
    new_game_state = None

    # 1. 繪製背景
    screen.blit(gacha_bg, (0, 0))

    # 2. 繪製資源 (右上角)
    gold_txt = font.render(f"Gold: {player_data['gold']}", True, (255, 215, 0))
    soul_txt = font.render(f"Souls: {player_data['souls']}", True, (200, 100, 255))
    screen.blit(gold_txt, (SCREEN_WIDTH - 250, 40))
    screen.blit(soul_txt, (SCREEN_WIDTH - 250, 80))

    # 3. 繪製轉蛋按鈕
    btn_rect = pygame.Rect(SCREEN_WIDTH // 2 - 125, SCREEN_HEIGHT // 2, 250, 100)
    pygame.draw.rect(screen, (70, 40, 120), btn_rect, border_radius=15)
    pygame.draw.rect(screen, (255, 255, 255), btn_rect, width=3, border_radius=15)
    
    label = font.render(f"Roll Single", True, (255, 255, 255))
    cost_label = font.render(f"{GACHA_COST_GOLD} G / {GACHA_COST_SOULS} S", True, (200, 200, 200))
    
    screen.blit(label, label.get_rect(center=(btn_rect.centerx, btn_rect.centery - 20)))
    screen.blit(cost_label, cost_label.get_rect(center=(btn_rect.centerx, btn_rect.centery + 20)))

    # 4. 返回按鈕
    back_rect = pygame.Rect(40, SCREEN_HEIGHT - 90, 150, 50)
    pygame.draw.rect(screen, (150, 50, 50), back_rect, border_radius=10)
    back_txt = font.render("Exit Menu", True, (255, 255, 255))
    screen.blit(back_txt, back_txt.get_rect(center=back_rect.center))

    # 事件處理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.event.post(event)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if back_rect.collidepoint(event.pos):
                new_game_state = "main_menu"
            
            if btn_rect.collidepoint(event.pos):
                success, msg, updated_data = perform_gacha()
                if success:
                    # 簡易成功特效：螢幕閃爍
                    screen.fill((255, 255, 255))
                    pygame.display.flip()
                    if key_action_sfx and 'laser' in key_action_sfx: # 借用雷射音效當出貨音
                        key_action_sfx['laser'].play()
                    time.sleep(0.1)
                else:
                    if key_action_sfx and 'cannot_deploy' in key_action_sfx:
                        key_action_sfx['cannot_deploy'].play()
                
                print(f"[Gacha] {msg}") # 這邊可以用之後教的 Popup 視窗取代

    return new_game_state