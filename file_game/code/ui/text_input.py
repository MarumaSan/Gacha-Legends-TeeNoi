"""Text input UI component"""
import pygame


class TextInput:
    """Interactive text input field"""
    
    def __init__(self, x, y, width, height, font=None, placeholder="", 
                 max_length=20, text_color=(255, 255, 255), 
                 bg_color=(50, 50, 50), active_color=(70, 70, 70)):
        """
        Initialize text input
        
        Args:
            x: X position
            y: Y position
            width: Input width
            height: Input height
            font: pygame.font.Font for text
            placeholder: Placeholder text
            max_length: Maximum character length
            text_color: Color for text
            bg_color: Background color when inactive
            active_color: Background color when active
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.font = font or pygame.font.Font(None, 32)
        self.placeholder = placeholder
        self.max_length = max_length
        self.text_color = text_color
        self.bg_color = bg_color
        self.active_color = active_color
        
        self.text = ""
        self.is_active = False
        self.cursor_visible = True
        self.cursor_timer = 0
        self.cursor_blink_time = 0.5  # seconds
    
    def handle_event(self, event):
        """
        Handle pygame events
        
        Args:
            event: pygame event
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.is_active = self.rect.collidepoint(event.pos)
        
        elif event.type == pygame.KEYDOWN and self.is_active:
            if event.key == pygame.K_RETURN:
                self.is_active = False
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_ESCAPE:
                self.is_active = False
            elif len(self.text) < self.max_length:
                # Add character if it's printable
                if event.unicode.isprintable():
                    self.text += event.unicode
    
    def update(self, dt=0):
        """
        Update text input state
        
        Args:
            dt: Delta time in seconds
        """
        # Update cursor blink
        if self.is_active:
            self.cursor_timer += dt
            if self.cursor_timer >= self.cursor_blink_time:
                self.cursor_visible = not self.cursor_visible
                self.cursor_timer = 0
        else:
            self.cursor_visible = False
    
    def draw(self, screen):
        """
        Draw text input to screen
        
        Args:
            screen: pygame.Surface to draw on
        """
        # Draw background
        color = self.active_color if self.is_active else self.bg_color
        pygame.draw.rect(screen, color, self.rect)
        
        # Draw border (thicker if active)
        border_width = 3 if self.is_active else 1
        pygame.draw.rect(screen, (255, 255, 255), self.rect, border_width)
        
        # Draw text or placeholder
        display_text = self.text if self.text else self.placeholder
        text_color = self.text_color if self.text else (150, 150, 150)
        
        if display_text:
            text_surface = self.font.render(display_text, True, text_color)
            text_rect = text_surface.get_rect(midleft=(self.rect.x + 10, self.rect.centery))
            
            # Clip text to input bounds
            clip_rect = self.rect.inflate(-20, -10)
            screen.set_clip(clip_rect)
            screen.blit(text_surface, text_rect)
            screen.set_clip(None)
        
        # Draw cursor
        if self.is_active and self.cursor_visible and self.text:
            text_width = self.font.size(self.text)[0]
            cursor_x = self.rect.x + 10 + text_width
            cursor_y1 = self.rect.y + 10
            cursor_y2 = self.rect.bottom - 10
            pygame.draw.line(screen, self.text_color, (cursor_x, cursor_y1), (cursor_x, cursor_y2), 2)
    
    def get_text(self):
        """Get current text"""
        return self.text
    
    def set_text(self, text):
        """
        Set text
        
        Args:
            text: New text string
        """
        self.text = text[:self.max_length]
    
    def clear(self):
        """Clear text"""
        self.text = ""
