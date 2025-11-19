"""Button UI component with click detection and hover effects"""
import pygame


class Button:
    """Interactive button with hover effects and click callbacks"""
    
    def __init__(self, x, y, width, height, text="", image=None, callback=None, 
                 font=None, text_color=(255, 255, 255), bg_color=(100, 100, 100),
                 hover_color=(150, 150, 150)):
        """
        Initialize button
        
        Args:
            x: X position
            y: Y position
            width: Button width
            height: Button height
            text: Button text (optional)
            image: Button image surface (optional)
            callback: Function to call on click
            font: pygame.font.Font for text
            text_color: Color for text
            bg_color: Background color when not hovered
            hover_color: Background color when hovered
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.image = image
        self.callback = callback
        self.font = font
        self.text_color = text_color
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.is_hovered = False
        self.is_pressed = False
        
        # Animation properties
        self.hover_progress = 0.0  # 0.0 = not hovered, 1.0 = fully hovered
        self.hover_speed = 5.0  # Speed of hover transition
        self.scale = 1.0
        self.target_scale = 1.0
        
        # Pre-render text if provided
        self.text_surface = None
        self.text_surfaces = []  # For multi-line text
        if self.text and self.font:
            self._render_text()
    
    def handle_event(self, event):
        """
        Handle pygame events
        
        Args:
            event: pygame event
            
        Returns:
            True if button was clicked, False otherwise
        """
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.is_hovered:
                self.is_pressed = True
                
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and self.is_pressed and self.is_hovered:
                self.is_pressed = False
                if self.callback:
                    self.callback()
                return True
            self.is_pressed = False
            
        return False
    
    def update(self, dt=0.016):
        """
        Update button state (for animations, etc.)
        
        Args:
            dt: Delta time in seconds (default 60 FPS)
        """
        # Check hover state based on current mouse position
        mouse_pos = pygame.mouse.get_pos()
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        
        # Smooth hover transition
        target_progress = 1.0 if self.is_hovered else 0.0
        if self.hover_progress < target_progress:
            self.hover_progress = min(self.hover_progress + self.hover_speed * dt, target_progress)
        elif self.hover_progress > target_progress:
            self.hover_progress = max(self.hover_progress - self.hover_speed * dt, target_progress)
        
        # Scale animation on hover
        self.target_scale = 1.05 if self.is_hovered else 1.0
        scale_diff = self.target_scale - self.scale
        self.scale += scale_diff * 10.0 * dt
    
    def draw(self, screen):
        """
        Draw button to screen
        
        Args:
            screen: pygame.Surface to draw on
        """
        # Calculate interpolated color
        r = int(self.bg_color[0] + (self.hover_color[0] - self.bg_color[0]) * self.hover_progress)
        g = int(self.bg_color[1] + (self.hover_color[1] - self.bg_color[1]) * self.hover_progress)
        b = int(self.bg_color[2] + (self.hover_color[2] - self.bg_color[2]) * self.hover_progress)
        current_color = (r, g, b)
        
        # Calculate scaled rect
        if self.scale != 1.0:
            scaled_width = int(self.rect.width * self.scale)
            scaled_height = int(self.rect.height * self.scale)
            scaled_rect = pygame.Rect(
                self.rect.centerx - scaled_width // 2,
                self.rect.centery - scaled_height // 2,
                scaled_width,
                scaled_height
            )
        else:
            scaled_rect = self.rect
        
        # Draw background only if not transparent
        if not self.image and self.bg_color != (0, 0, 0, 0):
            # Draw colored rectangle with smooth color transition
            pygame.draw.rect(screen, current_color, scaled_rect)
            pygame.draw.rect(screen, (255, 255, 255), scaled_rect, 2)  # Border
        
        # Draw image if provided
        if self.image:
            # If no text, use full button size for image
            if not self.text or self.text == "":
                if self.scale != 1.0:
                    scaled_img_width = int(self.rect.width * self.scale)
                    scaled_img_height = int(self.rect.height * self.scale)
                    scaled_image = pygame.transform.scale(self.image, (scaled_img_width, scaled_img_height))
                    img_x = scaled_rect.centerx - scaled_img_width // 2
                    img_y = scaled_rect.centery - scaled_img_height // 2
                    screen.blit(scaled_image, (img_x, img_y))
                else:
                    scaled_image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))
                    screen.blit(scaled_image, self.rect.topleft)
            else:
                # Has text - image at top, text at bottom
                img_height = int(self.rect.height * 0.75)
                img_width = self.rect.width - 10
                
                if self.scale != 1.0:
                    scaled_img_width = int(img_width * self.scale)
                    scaled_img_height = int(img_height * self.scale)
                    scaled_image = pygame.transform.scale(self.image, (scaled_img_width, scaled_img_height))
                    img_x = scaled_rect.centerx - scaled_img_width // 2
                    img_y = scaled_rect.top + 5
                    screen.blit(scaled_image, (img_x, img_y))
                else:
                    scaled_image = pygame.transform.scale(self.image, (img_width, img_height))
                    img_x = self.rect.centerx - img_width // 2
                    img_y = self.rect.top + 5
                    screen.blit(scaled_image, (img_x, img_y))
        
        # Draw text if provided
        if self.text and (self.text_surface or self.text_surfaces):
            # If image exists, draw text at bottom
            if self.image:
                # Draw dark background for text label
                label_height = int(self.rect.height * 0.25)
                label_rect = pygame.Rect(
                    scaled_rect.left,
                    scaled_rect.bottom - label_height,
                    scaled_rect.width,
                    label_height
                )
                pygame.draw.rect(screen, (20, 15, 10), label_rect)
                pygame.draw.rect(screen, (100, 80, 60), label_rect, 2)
                
                # Draw text centered in label area
                if self.text_surface:
                    text_rect = self.text_surface.get_rect(center=label_rect.center)
                    screen.blit(self.text_surface, text_rect)
            else:
                # No image - draw text in center as before
                if self.text_surface:
                    # Single line text
                    if self.scale != 1.0:
                        scaled_text = pygame.transform.scale(
                            self.text_surface,
                            (int(self.text_surface.get_width() * self.scale),
                             int(self.text_surface.get_height() * self.scale))
                        )
                        text_rect = scaled_text.get_rect(center=scaled_rect.center)
                        screen.blit(scaled_text, text_rect)
                    else:
                        text_rect = self.text_surface.get_rect(center=self.rect.center)
                        screen.blit(self.text_surface, text_rect)
                elif self.text_surfaces:
                    # Multi-line text
                    total_height = sum(surf.get_height() for surf in self.text_surfaces)
                    line_spacing = 5
                    total_height += line_spacing * (len(self.text_surfaces) - 1)
                    
                    start_y = scaled_rect.centery - total_height // 2
                    
                    for i, surf in enumerate(self.text_surfaces):
                        if self.scale != 1.0:
                            scaled_text = pygame.transform.scale(
                                surf,
                                (int(surf.get_width() * self.scale),
                                 int(surf.get_height() * self.scale))
                            )
                            text_rect = scaled_text.get_rect(center=(scaled_rect.centerx, start_y + i * (surf.get_height() + line_spacing)))
                            screen.blit(scaled_text, text_rect)
                        else:
                            text_rect = surf.get_rect(center=(self.rect.centerx, start_y + i * (surf.get_height() + line_spacing)))
                            screen.blit(surf, text_rect)
    
    def _render_text(self):
        """Render text, supporting multi-line text with \\n"""
        if not self.font or not self.text:
            return
        
        lines = self.text.split('\n')
        if len(lines) == 1:
            # Single line text
            self.text_surface = self.font.render(self.text, True, self.text_color)
            self.text_surfaces = []
        else:
            # Multi-line text
            self.text_surface = None
            self.text_surfaces = [self.font.render(line, True, self.text_color) for line in lines]
    
    def set_text(self, text):
        """
        Update button text
        
        Args:
            text: New text string
        """
        self.text = text
        if self.font:
            self._render_text()
    
    def set_position(self, x, y):
        """
        Update button position
        
        Args:
            x: New X position
            y: New Y position
        """
        self.rect.x = x
        self.rect.y = y
