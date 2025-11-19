"""Panel UI component for grouping elements"""
import pygame


class Panel:
    """Container for grouping UI elements"""
    
    def __init__(self, x, y, width, height, background_color=None, 
                 background_image=None, border_color=None, border_width=0):
        """
        Initialize panel
        
        Args:
            x: X position
            y: Y position
            width: Panel width
            height: Panel height
            background_color: RGB color tuple for background (optional)
            background_image: pygame.Surface for background (optional)
            border_color: RGB color tuple for border (optional)
            border_width: Width of border in pixels
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.background_color = background_color
        self.background_image = background_image
        self.border_color = border_color
        self.border_width = border_width
        self.children = []
        self.visible = True
        
        # Scale background image if provided
        if self.background_image:
            self.background_image = pygame.transform.scale(
                self.background_image, (width, height)
            )
    
    def add_child(self, component):
        """
        Add a UI component to the panel
        
        Args:
            component: UI component (Button, TextDisplay, etc.)
        """
        self.children.append(component)
    
    def remove_child(self, component):
        """
        Remove a UI component from the panel
        
        Args:
            component: UI component to remove
        """
        if component in self.children:
            self.children.remove(component)
    
    def clear_children(self):
        """Remove all child components"""
        self.children.clear()
    
    def handle_event(self, event):
        """
        Handle events for all child components
        
        Args:
            event: pygame event
        """
        if not self.visible:
            return
        
        for child in self.children:
            if hasattr(child, 'handle_event'):
                child.handle_event(event)
    
    def update(self):
        """Update all child components"""
        if not self.visible:
            return
        
        for child in self.children:
            if hasattr(child, 'update'):
                child.update()
    
    def draw(self, screen):
        """
        Draw panel and all child components
        
        Args:
            screen: pygame.Surface to draw on
        """
        if not self.visible:
            return
        
        # Draw background
        if self.background_image:
            screen.blit(self.background_image, self.rect)
        elif self.background_color:
            pygame.draw.rect(screen, self.background_color, self.rect)
        
        # Draw border
        if self.border_color and self.border_width > 0:
            pygame.draw.rect(screen, self.border_color, self.rect, self.border_width)
        
        # Draw all children
        for child in self.children:
            if hasattr(child, 'draw'):
                child.draw(screen)
    
    def set_position(self, x, y):
        """
        Update panel position
        
        Args:
            x: New X position
            y: New Y position
        """
        # Calculate offset
        dx = x - self.rect.x
        dy = y - self.rect.y
        
        # Update panel position
        self.rect.x = x
        self.rect.y = y
        
        # Update children positions
        for child in self.children:
            if hasattr(child, 'set_position'):
                if hasattr(child, 'rect'):
                    child.set_position(child.rect.x + dx, child.rect.y + dy)
                elif hasattr(child, 'position'):
                    child.set_position((child.position[0] + dx, child.position[1] + dy))
    
    def set_visible(self, visible):
        """
        Set panel visibility
        
        Args:
            visible: Boolean visibility state
        """
        self.visible = visible
    
    def contains_point(self, point):
        """
        Check if point is inside panel
        
        Args:
            point: (x, y) tuple
            
        Returns:
            True if point is inside panel
        """
        return self.rect.collidepoint(point)