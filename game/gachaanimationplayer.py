import pygame

class GachaAnimationPlayer:
    def __init__(self, frame_paths, pos, frame_duration=50):
        """
        frame_paths: 圖片路徑列表
        pos: (x, y) 播放位置 (中心點)
        frame_duration: 每幀播放多少毫秒
        """
        self.frames = [pygame.image.load(p).convert_alpha() for p in frame_paths]
        self.pos = pos
        self.frame_duration = frame_duration
        self.start_time = 0
        self.is_playing = False
        self.current_frame_idx = 0

    def start(self, current_time):
        self.is_playing = True
        self.start_time = current_time
        self.current_frame_idx = 0

    def draw(self, screen, current_time):
        if not self.is_playing:
            return False

        # 計算目前應該播放到哪一幀
        elapsed = current_time - self.start_time
        self.current_frame_idx = elapsed // self.frame_duration

        if self.current_frame_idx >= len(self.frames):
            self.is_playing = False # 動畫結束
            return False

        current_frame = self.frames[self.current_frame_idx]
        rect = current_frame.get_rect(center=self.pos)
        screen.blit(current_frame, rect)
        return True # 代表還在播放中