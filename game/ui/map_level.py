# game/ui/cat_selection.py
import pygame
import os
from game.game_loop import main_game_loop
from game.entities import levels  # 假設 levels 是你所有關卡的列表

_level_selection_background_image = None
_level_selection_background_image_path = "images/background/level_selection_bg.png"

# 用於存儲每個關卡的圖標位置
level_icon_positions = {}

def load_map_level_selection_background_image(screen_width, screen_height):
    global _level_selection_background_image
    if _level_selection_background_image is None:
        try:
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            image_path = os.path.join(base_dir, _level_selection_background_image_path)
            image = pygame.image.load(image_path).convert()
            _level_selection_background_image = pygame.transform.scale(image, (screen_width, screen_height))
        except pygame.error as e:
            print(f"Error loading level selection background image: {e}")
            _level_selection_background_image = None
    return _level_selection_background_image


def draw_map_level_selection(screen, selected_level=0, completed_levels=set()):
    """
    繪製地圖關卡選單。
    selected_level: 當前選擇的關卡索引
    completed_levels: 已完成關卡集合
    返回每個關卡的矩形
    """
    screen_width, screen_height = screen.get_size()
    background_image = load_map_level_selection_background_image(screen_width, screen_height)
    if background_image:
        screen.blit(background_image, (0, 0))
    else:
        screen.fill((0, 0, 0))

    # 關卡圖標大小和顏色
    icon_radius = 25
    icon_color_default = (200, 200, 200)
    icon_color_selected = (255, 255, 0)
    icon_color_completed = (100, 255, 100)

    # 初始化關卡位置
    global level_icon_positions
    if not level_icon_positions:
        margin_x, margin_y = 100, 150
        spacing_x, spacing_y = 200, 150
        for i, level in enumerate(levels):
            row = i // 5
            col = i % 5
            x = margin_x + col * spacing_x
            y = margin_y + row * spacing_y
            level_icon_positions[i] = (x, y)

    # 畫圖標並返回矩形
    level_rects = {}
    for idx, pos in level_icon_positions.items():
        x, y = pos
        rect = pygame.Rect(x - icon_radius, y - icon_radius, icon_radius * 2, icon_radius * 2)
        level_rects[idx] = rect

        color = icon_color_default
        if idx == selected_level:
            color = icon_color_selected
        elif idx in completed_levels:
            color = icon_color_completed

        pygame.draw.circle(screen, color, (x, y), icon_radius)
        font = pygame.font.SysFont(None, 30)
        text_surf = font.render(str(idx + 1), True, (0, 0, 0))
        screen.blit(text_surf, (x - text_surf.get_width() // 2, y - text_surf.get_height() // 2))

    return level_rects


def handle_level_selection_movement(selected_level, key):
    """
    根據鍵盤方向更新選中的關卡
    """
    positions = list(level_icon_positions.items())
    idx = selected_level
    current_pos = level_icon_positions[idx]
    x, y = current_pos

    # 找到上下左右最接近的關卡
    closest_idx = idx
    min_distance = float('inf')
    for i, pos in positions:
        if i == idx:
            continue
        dx = pos[0] - x
        dy = pos[1] - y

        if key == pygame.K_RIGHT and dx > 0 and abs(dy) < 50:
            distance = dx**2 + dy**2
            if distance < min_distance:
                min_distance = distance
                closest_idx = i
        elif key == pygame.K_LEFT and dx < 0 and abs(dy) < 50:
            distance = dx**2 + dy**2
            if distance < min_distance:
                min_distance = distance
                closest_idx = i
        elif key == pygame.K_DOWN and dy > 0 and abs(dx) < 50:
            distance = dx**2 + dy**2
            if distance < min_distance:
                min_distance = distance
                closest_idx = i
        elif key == pygame.K_UP and dy < 0 and abs(dx) < 50:
            distance = dx**2 + dy**2
            if distance < min_distance:
                min_distance = distance
                closest_idx = i

    return closest_idx
