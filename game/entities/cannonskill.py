import pygame
import math

class CannonSkill:
    def __init__(
        self,
        origin_pos,                 # (x, y) 砲口中心 level_tower位置決定
        sweep_start_x,              # 掃射起點（地面 x） level_tower位置決定
        sweep_end_x,                # 掃射終點（地面 x） 遊戲開始時根據砲等級決定
        ground_y,                   # 地面 y     level_tower位置決定
        sweep_duration=1200,        # 掃射時間（ms） 遊戲開始時根據砲等級決定
        cooldown=5000,              # 冷卻時間（ms） 遊戲開始時根據砲等級決定
        damage=300,                 # 傷害 遊戲開始時根據砲等級決定

        origin_frames=None,         # origin.png 動畫 same
        beam_frames=None,           # beam.png（水平）same
        sweep_fx_frames=None,       # 掃射地面 splash（掃射中）same
        after_fx_frames=None        # 掃射後沿地面移動特效 same
    ):
        # --- 基本設定 ---
        self.origin_x, self.origin_y = origin_pos
        self.sweep_start_x = sweep_start_x
        self.sweep_end_x = sweep_end_x
        self.ground_y = ground_y
        self.sweep_duration = sweep_duration
        self.cooldown = cooldown
        self.damage = damage

        # --- 圖片 ---
        self.origin_frames = origin_frames or []
        self.beam_frames = beam_frames or []
        self.sweep_fx_frames = sweep_fx_frames or []
        self.after_fx_frames = after_fx_frames or []

        # --- 狀態 ---
        self.state = "ready"
        self.start_time = 0
        self.cooldown_start = 0

        # --- 動畫 ---
        self.anim_index = 0
        self.after_x = sweep_start_x

    # ======================================================
    # 觸發技能
    # ======================================================
    def activate(self, current_time):
        if self.state == "ready":
            self.state = "sweeping"
            self.start_time = current_time
            self.anim_index = 0

    # ======================================================
    # 更新
    # ======================================================
    def update(self, current_time, enemies):
        self.anim_index += 1

        # ---------- 掃射中 ----------
        if self.state == "sweeping":
            progress = (current_time - self.start_time) / self.sweep_duration

            if progress >= 1.0:
                # 掃射結束 → 進入後效
                self.state = "after"
                self.after_x = self.sweep_start_x

                # 結算傷害（只在這裡一次）
                self._apply_damage(enemies)

        # ---------- 掃射後地面殘影 ----------
        elif self.state == "after":
            speed = (self.sweep_end_x - self.sweep_start_x) / (self.sweep_duration / 16)
            self.after_x += speed

            if self.after_x >= self.sweep_end_x:
                self.state = "cooldown"
                self.cooldown_start = current_time

        # ---------- 冷卻 ----------
        elif self.state == "cooldown":
            if current_time - self.cooldown_start >= self.cooldown:
                self.state = "ready"

    # ======================================================
    # 繪製
    # ======================================================
    def draw(self, screen):
        # ---------- 掃射中 ----------
        if self.state == "sweeping":
            self._draw_origin(screen)
            self._draw_beam(screen)
            self._draw_sweep_fx(screen)

        # ---------- 掃射後 ----------
        elif self.state == "after":
            self._draw_after_fx(screen)

    # ======================================================
    # 子功能
    # ======================================================
    def _draw_origin(self, screen):
        if not self.origin_frames:
            return
        img = self.origin_frames[self.anim_index % len(self.origin_frames)]
        rect = img.get_rect(center=(self.origin_x, self.origin_y))
        screen.blit(img, rect)

    def _draw_beam(self, screen):
        if not self.beam_frames:
            return

        progress = (pygame.time.get_ticks() - self.start_time) / self.sweep_duration
        progress = max(0, min(1, progress))

        tx = self.sweep_start_x + (self.sweep_end_x - self.sweep_start_x) * progress
        ty = self.ground_y

        dx = tx - self.origin_x
        dy = ty - self.origin_y
        angle = -math.degrees(math.atan2(dy, dx))

        beam = self.beam_frames[self.anim_index % len(self.beam_frames)]
        rotated = pygame.transform.rotate(beam, angle)

        rect = rotated.get_rect(midleft=(self.origin_x, self.origin_y))
        screen.blit(rotated, rect)

    def _draw_sweep_fx(self, screen):
        if not self.sweep_fx_frames:
            return

        progress = (pygame.time.get_ticks() - self.start_time) / self.sweep_duration
        tx = self.sweep_start_x + (self.sweep_end_x - self.sweep_start_x) * progress
        ty = self.ground_y

        fx = self.sweep_fx_frames[self.anim_index % len(self.sweep_fx_frames)]
        rect = fx.get_rect(center=(tx, ty))
        screen.blit(fx, rect)

    def _draw_after_fx(self, screen):
        if not self.after_fx_frames:
            return

        ty = self.ground_y
        fx = self.after_fx_frames[self.anim_index % len(self.after_fx_frames)]

        for offset in (0, -40):
            rect = fx.get_rect(center=(self.after_x + offset, ty))
            screen.blit(fx, rect)

    # ======================================================
    # 傷害計算（只在掃射結束）
    # ======================================================
    def _apply_damage(self, enemies):
        for e in enemies:
            if self.sweep_start_x <= e.x <= self.sweep_end_x:
                e.hp -= self.damage
