# ui/gacha_developing.py

import pygame
import json
import time

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


def draw_gacha_screen(screen, font, select_font, gacha_bg, gacha_anim_frames, cat_previews, key_action_sfx=None):
    from ..gacha_manager import perform_gacha
    from ..constants import GACHA_COST_GOLD, GACHA_COST_SOULS, RESOURCE_FILE
    
    # 這些狀態通常建議存在一個類別屬性或全域變數中，這裡為了示範使用 global
    global gacha_state, pending_result, anim_index
    if 'gacha_state' not in globals():
        gacha_state = "idle"
        pending_result = None
        anim_index = 0

    SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
    current_time = pygame.time.get_ticks()
    new_game_state = None

    # --- 1. 繪製基礎層 ---
    screen.blit(gacha_bg, (0, 0))
    
    # 讀取顯示用的資源
    with open(RESOURCE_FILE, "r") as f:
        res_data = json.load(f)
    gold_txt = font.render(f"Gold: {res_data['gold']}", True, (255, 215, 0))
    soul_txt = font.render(f"Souls: {res_data['souls']}", True, (200, 100, 255))
    screen.blit(gold_txt, (SCREEN_WIDTH - 250, 40))
    screen.blit(soul_txt, (SCREEN_WIDTH - 250, 80))

    # --- 2. 狀態機繪製邏輯 ---
    
    if gacha_state == "idle":
        # 繪製主按鈕
        btn_rect = pygame.Rect(SCREEN_WIDTH//2 - 125, SCREEN_HEIGHT//2, 250, 100)
        pygame.draw.rect(screen, (70, 40, 120), btn_rect, border_radius=15)
        label = font.render("Roll Single", True, (255, 255, 255))
        screen.blit(label, label.get_rect(center=btn_rect.center))
        
        # 返回按鈕
        back_rect = pygame.Rect(50, SCREEN_HEIGHT - 100, 150, 60)
        pygame.draw.rect(screen, (150, 50, 50), back_rect, border_radius=10)
        screen.blit(font.render("Back", True, (255,255,255)), back_rect.move(40, 15))

    elif gacha_state == "playing":
        # 播放錄好的動畫幀
        # 假設每 50 毫秒換一幀
        frame_idx = (anim_index // 3) % len(gacha_anim_frames)
        current_frame = gacha_anim_frames[frame_idx]
        screen.blit(current_frame, current_frame.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)))
        
        anim_index += 1
        if anim_index >= len(gacha_anim_frames) * 3: # 動畫播完
            gacha_state = "result"
            anim_index = 0

    elif gacha_state == "result":
        # 繪製半透明黑底
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0,0))
        
        # 顯示抽中結果
        if pending_result["won_id"]:
            # 顯示角色大圖
            char_img = cat_previews.get(pending_result["won_id"])
            if char_img:
                screen.blit(char_img, char_img.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50)))
        
        msg_txt = select_font.render(pending_result["msg"], True, (255, 255, 255))
        screen.blit(msg_txt, msg_txt.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 200)))
        
        tip_txt = font.render("Click anywhere to continue", True, (200, 200, 200))
        screen.blit(tip_txt, tip_txt.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT - 100)))

    # --- 3. 事件處理 ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.event.post(event)
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if gacha_state == "idle":
                if btn_rect.collidepoint(event.pos):
                    success, res = perform_gacha()
                    if success:
                        pending_result = res
                        gacha_state = "playing"
                        anim_index = 0
                        if key_action_sfx and 'laser' in key_action_sfx: key_action_sfx['laser'].play()
                    else:
                        print(res["msg"]) # 不夠錢
                elif back_rect.collidepoint(event.pos):
                    new_game_state = "main_menu"
            
            elif gacha_state == "result":
                # 點擊任何地方回到初始狀態
                gacha_state = "idle"
                pending_result = None

    pygame.display.flip()
    return new_game_state