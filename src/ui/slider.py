"""Slider UI component for adjusting values"""
import pygame


class Slider:
    """Interactive slider for adjusting numeric values"""
    
    def __init__(self, x, y, width, height, min_value=0, max_value=100, 
                 initial_value=50, callback=None, label="", font=None):
        """
        Initialize slider
        
        Args:
            x: X position
            y: Y position
            width: Slider width
            height: Slider height (track height)
            min_value: Minimum value
            max_value: Maximum value
            initial_value: Starting value
            callback: Function to call when value changes
            label: Label text
            font: pygame.font.Font for label
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.min_value = min_value
        self.max_value = max_value
        self.value = initial_value
        self.callback = callback
        self.label = label
        self.font = font
        
        # Handle dimensions
        self.handle_radius = height
        self.handle_x = self._value_to_x(initial_value)
        self.is_dragging = False
        
        # Colors
        self.track_color = (100, 100, 100)
        self.handle_color = (200, 200, 200)
        self.handle_hover_color = (255, 255, 255)
        self.is_hovered = False
        
        # Pre-render label
        self.label_surface = None
        if self.label and self.font:
            self.label_surface = self.font.render(self.label, True, (255, 255, 255))
    
    def _value_to_x(self, value):
        """Convert value to handle x position"""
        ratio = (value - self.min_value) / (self.max_value - self.min_value)
        return self.rect.x + int(ratio * self.rect.width)
    
    def _x_to_value(self, x):
        """Convert x position to value"""
        x = max(self.rect.x, min(x, self.rect.x + self.rect.width))
        ratio = (x - self.rect.x) / self.rect.width
        return self.min_value + ratio * (self.max_value - self.min_value)
    
    def handle_event(self, event):
        """
        Handle pygame events
        
        Args:
            event: pygame event
        """
        handle_rect = pygame.Rect(
            self.handle_x - self.handle_radius,
            self.rect.y - self.handle_radius // 2,
            self.handle_radius * 2,
            self.handle_radius * 2
        )
        
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = handle_rect.collidepoint(event.pos)
            
            if self.is_dragging:
                self.handle_x = max(self.rect.x, min(event.pos[0], self.rect.x + self.rect.width))
                old_value = self.value
                self.value = self._x_to_value(self.handle_x)
                
                if self.callback and old_value != self.value:
                    self.callback(self.value)
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and handle_rect.collidepoint(event.pos):
                self.is_dragging = True
        
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.is_dragging = False
    
    def update(self):
        """Update slider state"""
        mouse_pos = pygame.mouse.get_pos()
        handle_rect = pygame.Rect(
            self.handle_x - self.handle_radius,
            self.rect.y - self.handle_radius // 2,
            self.handle_radius * 2,
            self.handle_radius * 2
        )
        self.is_hovered = handle_rect.collidepoint(mouse_pos)
    
    def draw(self, screen):
        """
        Draw slider to screen
        
        Args:
            screen: pygame.Surface to draw on
        """
        # Draw label
        if self.label_surface:
            label_rect = self.label_surface.get_rect(
                midright=(self.rect.x - 10, self.rect.centery)
            )
            screen.blit(self.label_surface, label_rect)
        
        # Draw track
        pygame.draw.rect(screen, self.track_color, self.rect)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 1)
        
        # Draw handle
        handle_color = self.handle_hover_color if self.is_hovered or self.is_dragging else self.handle_color
        pygame.draw.circle(screen, handle_color, (self.handle_x, self.rect.centery), self.handle_radius)
        pygame.draw.circle(screen, (255, 255, 255), (self.handle_x, self.rect.centery), self.handle_radius, 2)
        
        # Draw value text
        if self.font:
            value_text = f"{int(self.value)}"
            value_surface = self.font.render(value_text, True, (255, 255, 255))
            value_rect = value_surface.get_rect(midleft=(self.rect.right + 10, self.rect.centery))
            screen.blit(value_surface, value_rect)
    
    def set_value(self, value):
        """
        Set slider value
        
        Args:
            value: New value
        """
        self.value = max(self.min_value, min(value, self.max_value))
        self.handle_x = self._value_to_x(self.value)
    
    def get_value(self):
        """Get current slider value"""
        return self.value
