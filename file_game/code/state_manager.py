"""State manager for handling game state transitions"""
import pygame
from file_game.code.ui.animation import FadeTransition


class StateManager:
    """Manages game states and transitions between them"""
    def __init__(self):
        self.states = {}
        self.current_state_name = None
        self.current_state = None

        self.transition = None
        self.transitioning = False
        self.next_state_name = None

    def add_state(self, name, state):
        self.states[name] = state

    def change_state(self, name, use_transition=True):
        """
        พฤติกรรมเดิม: เฟดออก -> เปลี่ยน -> เฟดเข้า
        """
        if name not in self.states:
            raise KeyError(f"State '{name}' not found in state manager")

        if use_transition and not self.transitioning:
            self.transition = FadeTransition(duration=0.3, fade_in=False)  # ใส -> ดำ
            self.next_state_name = name
            self.transitioning = True
        else:
            self._perform_state_change(name)

    # -----------------------------
    # เพิ่ม: เปลี่ยนฉากก่อน แล้วค่อยเฟดเข้า
    # -----------------------------
    def change_state_then_fade_in(self, name, duration=0.3):
        if name not in self.states:
            raise KeyError(f"State '{name}' not found in state manager")

        if self.transitioning:
            return  # กันสั่งซ้อน

        # เตรียม overlay ก่อนเพื่อกันเฟรมแรกวาบ
        self.transition = FadeTransition(duration=duration, fade_in=True)  # ดำ -> ใส
        self.transitioning = True

        # เปลี่ยนฉากทันที
        self._perform_state_change(name)

    def _perform_state_change(self, name):
        # ออกจาก state เดิม
        if self.current_state:
            self.current_state.exit()

        # เปลี่ยนเป็น state ใหม่
        self.current_state_name = name
        self.current_state = self.states[name]

        # เข้า state ใหม่
        self.current_state.enter()

        # สำหรับ flow เดิม (เฟดออก->เข้า): จบขั้นออกแล้วเริ่มเข้า
        if self.transitioning and self.transition and (self.transition.fade_in is False):
            self.transition = FadeTransition(duration=0.3, fade_in=True)

    def get_current_state(self):
        return self.current_state

    def handle_event(self, event):
        if self.current_state:
            self.current_state.handle_event(event)

    def update(self, dt):
        # อัปเดตทรานซิชัน
        if self.transitioning and self.transition:
            complete = self.transition.update(dt)
            if complete:
                if self.transition.fade_in is False:
                    # เฟดออกจบ -> เปลี่ยนฉาก แล้วย้ายไปเฟดเข้า
                    self._perform_state_change(self.next_state_name)
                    self.next_state_name = None
                else:
                    # เฟดเข้าเสร็จ -> จบทรานซิชัน
                    self.transitioning = False
                    self.transition = None

        # อัปเดต state ปัจจุบัน
        if self.current_state:
            self.current_state.update(dt)

    def draw(self, screen):
        if self.current_state:
            self.current_state.draw(screen)

        # วาด overlay ทับท้ายสุด
        if self.transitioning and self.transition:
            self.transition.draw(screen)
