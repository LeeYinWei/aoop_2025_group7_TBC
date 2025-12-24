# game/player_character.py
import pygame

class PlayerCharacter:
    def __init__(self, start_x, start_y):
        self.x = start_x
        self.y = start_y
        self.speed = 5
        # 載入角色圖（先用單張，未來可加 Sprite Sheet 動畫）
        self.image = pygame.image.load("images/character/snail.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (60, 60))  # 調整大小

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.y += self.speed

        # 限制在地圖範圍內（1280x600）
        self.x = max(30, min(1250, self.x))
        self.y = max(30, min(570, self.y))

    def draw(self, screen):
        screen.blit(self.image, (self.x - 30, self.y - 30))  # 置中