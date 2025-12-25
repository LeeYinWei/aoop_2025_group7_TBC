# game/ui/battle_menu.py
# ui/battle_map.py

import pygame

def draw_battle_map_selection(
    screen,
    level_map_bg,           # 地圖背景圖片 (Surface)
    snail_image,            # 玩家蝸牛圖片 (Surface)
    LEVEL_NODES,            # list[tuple[int, int]] 關卡節點座標
    completed_levels,       # set[int] 已通關關卡索引
    player_pos,             # list[int] 或 tuple，可修改的 [x, y]
    player_speed=6,         # 移動速度
    select_font=None        # 用來顯示關卡數字的字型
):
    """
    繪製並處理戰鬥地圖選擇關卡的完整邏輯
    返回值：
        - selected_level_idx: int | None  如果玩家按下 ENTER/SPACE 選擇了關卡，返回關卡索引，否則 None
        - new_game_state: str | None      如果按 ESC，返回 "main_menu"，否則 None
    """
    SCREEN_WIDTH = screen.get_width()
    SCREEN_HEIGHT = screen.get_height()

    # 背景
    screen.blit(level_map_bg, (0, 0))

    # 玩家移動
    keys = pygame.key.get_pressed()
    player_x, player_y = player_pos

    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player_x += player_speed
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        player_y -= player_speed
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        player_y += player_speed

    # 邊界限制（蝸牛半徑約35）
    player_x = max(35, min(SCREEN_WIDTH - 35, player_x))
    player_y = max(35, min(SCREEN_HEIGHT - 35, player_y))

    # 更新玩家位置（因為傳進來的是 list，會直接修改外部變數）
    player_pos[0] = player_x
    player_pos[1] = player_y

    # 畫玩家蝸牛
    screen.blit(snail_image, (player_x - 35, player_y - 35))

    # 畫關卡節點
    selected_level_idx = None
    near_node_idx = None

    for idx, (x, y) in enumerate(LEVEL_NODES):
        unlocked = idx == 0 or (idx - 1) in completed_levels
        color = (0, 255, 0) if unlocked else (100, 100, 100)

        # 主圓圈
        pygame.draw.circle(screen, color, (x, y), 50)
        pygame.draw.circle(screen, (255, 255, 255), (x, y), 50, 5)

        # 關卡數字
        num_text = select_font.render(str(idx + 1), True, (255, 255, 255))
        screen.blit(num_text, (x - num_text.get_width() // 2, y - num_text.get_height() // 2))

        # 距離檢測
        dist = ((player_x - x)**2 + (player_y - y)**2)**0.5
        if dist < 80:
            near_node_idx = idx
            # 高亮外圈
            pygame.draw.circle(screen, (255, 255, 0), (x, y), 60, 8)

    # 顯示返回提示
    font = pygame.font.SysFont(None, 36)
    back_text = font.render("Press ESC to return to main menu", True, (255, 255, 255))
    screen.blit(back_text, (20, 20))

    # 處理事件（只處理 QUIT 和 ESC）
    new_game_state = None
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # 讓主程式處理退出
            pygame.event.post(event)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                new_game_state = "main_menu"

    # 檢查是否按下選擇鍵（ENTER 或 SPACE）且靠近可解鎖關卡
    if near_node_idx is not None:
        unlocked = near_node_idx == 0 or (near_node_idx - 1) in completed_levels
        if unlocked and (keys[pygame.K_RETURN] or keys[pygame.K_SPACE]):
            selected_level_idx = near_node_idx

    pygame.display.flip()

    return selected_level_idx, new_game_state