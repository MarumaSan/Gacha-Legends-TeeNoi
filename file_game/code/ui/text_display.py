"""Text display UI component"""
import pygame


class TextDisplay:
    """Component for rendering text on screen"""
    
    def __init__(self, text, font, color=(255, 255, 255), position=(0, 0), 
                 align='left', antialias=True, centered=False):
        """
        Initialize text display
        
        Args:
            text: Text string to display
            font: pygame.font.Font object
            color: RGB color tuple
            position: (x, y) position tuple
            align: Text alignment ('left', 'center', 'right')
            antialias: Whether to use antialiasing
            centered: If True, use 'center' alignment (overrides align)
        """
        self.text = text
        self.font = font
        self.color = color
        self.position = position
        self.align = 'center' if centered else align
        self.antialias = antialias
        self.surface = None
        self.rect = None
        
        # Render initial text
        self._render()
    
    def _render(self):
        """Render text to surface"""
        if self.text:
            self.surface = self.font.render(self.text, self.antialias, self.color)
            self.rect = self.surface.get_rect()
            
            # Apply alignment
            if self.align == 'left':
                self.rect.topleft = self.position
            elif self.align == 'center':
                self.rect.center = self.position
            elif self.align == 'right':
                self.rect.topright = self.position
        else:
            self.surface = None
            self.rect = None
    
    def set_text(self, text):
        """
        Update displayed text
        
        Args:
            text: New text string
        """
        if self.text != text:
            self.text = text
            self._render()
    
    def set_color(self, color):
        """
        Update text color
        
        Args:
            color: RGB color tuple
        """
        if self.color != color:
            self.color = color
            self._render()
    
    def set_position(self, position):
        """
        Update text position
        
        Args:
            position: (x, y) position tuple
        """
        self.position = position
        self._render()
    
    def draw(self, screen):
        """
        Draw text to screen
        
        Args:
            screen: pygame.Surface to draw on
        """
        if self.surface and self.rect:
            screen.blit(self.surface, self.rect)
    
    def get_width(self):
        """Get rendered text width"""
        return self.rect.width if self.rect else 0
    
    def get_height(self):
        """Get rendered text height"""
        return self.rect.height if self.rect else 0
    
    def get_rect(self):
        """Get text rectangle"""
        return self.rect
