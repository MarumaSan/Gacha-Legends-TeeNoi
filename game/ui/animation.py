"""Animation utilities for smooth transitions and effects"""
import pygame
import math


class FadeTransition:
    """
    เฟดดำเข้า/ออกแบบนิ่ง (แก้อาการกะพริบ)
    - fade_in=True  : ดำ -> ใส   (ใช้หลังเปลี่ยนฉาก เสกให้สว่างขึ้น)
    - fade_in=False : ใส  -> ดำ  (ใช้ก่อนเปลี่ยนฉาก ทำให้มืดลง)
    """
    def __init__(self, duration=0.5, fade_in=True):
        self.duration = max(1e-6, float(duration))
        self.fade_in = bool(fade_in)
        self.timer = 0.0
        self.progress = 0.0  # 0..1
        self.active = True

    def update(self, dt: float):
        """เดินเวลาเฟดทีละเฟรม; คืน True เมื่อจบ"""
        if not self.active:
            return True
        self.timer += float(dt)
        self.progress = min(self.timer / self.duration, 1.0)
        if self.progress >= 1.0:
            self.active = False
            return True
        return False

    def draw(self, screen: pygame.Surface):
        """วาดเลเยอร์ดำทับตาม progress"""
        # คิด alpha แบบตรงไปตรงมา
        if self.fade_in:
            # ดำ -> ใส : alpha 255 -> 0
            alpha = int(255 * (1.0 - self.progress))
        else:
            # ใส -> ดำ : alpha 0 -> 255
            alpha = int(255 * self.progress)

        if alpha <= 0:
            return

        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, alpha))
        screen.blit(overlay, (0, 0))

    def reset(self, fade_in=None):
        if fade_in is not None:
            self.fade_in = bool(fade_in)
        self.timer = 0.0
        self.progress = 0.0
        self.active = True


class CardFlipAnimation:
    """Card flip animation with 3D-like effect"""
    def __init__(self, duration=0.5):
        self.duration = max(1e-6, float(duration))
        self.timer = 0.0
        self.active = False
        self.flip_progress = 0.0

    def start(self):
        self.timer = 0.0
        self.active = True
        self.flip_progress = 0.0

    def update(self, dt):
        if not self.active:
            return True
        self.timer += float(dt)
        self.flip_progress = min(self.timer / self.duration, 1.0)
        if self.flip_progress >= 1.0:
            self.active = False
            return True
        return False

    def get_scale_x(self):
        angle = self.flip_progress * math.pi
        return abs(math.cos(angle))

    def is_back_visible(self):
        return self.flip_progress < 0.5


class PulseAnimation:
    """Pulsing scale animation"""
    def __init__(self, duration=1.0, min_scale=0.95, max_scale=1.05):
        self.duration = max(1e-6, float(duration))
        self.min_scale = float(min_scale)
        self.max_scale = float(max_scale)
        self.timer = 0.0

    def update(self, dt):
        self.timer += float(dt)
        if self.timer >= self.duration:
            self.timer -= self.duration

    def get_scale(self):
        progress = self.timer / self.duration
        scale_range = self.max_scale - self.min_scale
        return self.min_scale + scale_range * (0.5 + 0.5 * math.sin(progress * 2 * math.pi))


class SlideAnimation:
    """Slide in/out animation"""
    def __init__(self, start_pos, end_pos, duration=0.3):
        self.start_pos = tuple(start_pos)
        self.end_pos = tuple(end_pos)
        self.duration = max(1e-6, float(duration))
        self.timer = 0.0
        self.active = False

    def start(self):
        self.timer = 0.0
        self.active = True

    def update(self, dt):
        if not self.active:
            return True
        self.timer += float(dt)
        progress = min(self.timer / self.duration, 1.0)
        if progress >= 1.0:
            self.active = False
            return True
        return False

    def get_position(self):
        if not self.active:
            return self.end_pos
        t = self.timer / self.duration
        t = 1 - pow(1 - t, 3)  # ease-out cubic
        x = self.start_pos[0] + (self.end_pos[0] - self.start_pos[0]) * t
        y = self.start_pos[1] + (self.end_pos[1] - self.start_pos[1]) * t
        return (x, y)


class ParticleEffect:
    """Simple particle effect for celebrations"""
    def __init__(self, position, count=20, color=(255, 215, 0)):
        self.particles = []
        self.color = tuple(color)
        pos = pygame.math.Vector2(position)
        for i in range(count):
            angle = pygame.math.Vector2(1, 0).rotate(360 * i / count)
            speed = 100 + 50 * ((i % 3) / 3)
            self.particles.append({
                'pos': pos.copy(),
                'vel': angle * speed,
                'life': 1.0,
                'size': 3 + (i % 3),
            })

    def update(self, dt):
        all_dead = True
        fdt = float(dt)
        for p in self.particles:
            if p['life'] > 0:
                all_dead = False
                p['pos'] += p['vel'] * fdt
                p['vel'] *= 0.95
                p['life'] -= fdt
        return all_dead

    def draw(self, screen: pygame.Surface):
        for p in self.particles:
            if p['life'] > 0:
                alpha = int(255 * p['life'])
                size = int(p['size'] * p['life'])
                if size > 0 and alpha > 0:
                    diameter = size * 2
                    bubble = pygame.Surface((diameter, diameter), pygame.SRCALPHA)
                    pygame.draw.circle(bubble, (*self.color, alpha), (size, size), size)
                    screen.blit(bubble, (int(p['pos'].x) - size, int(p['pos'].y) - size))
