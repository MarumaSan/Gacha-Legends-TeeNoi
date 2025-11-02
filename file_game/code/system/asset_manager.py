"""Asset management system for loading and caching game assets"""

import pygame
import os
from typing import Dict, Optional, Tuple
from file_game.code.config import ASSET_PATHS, FONTS


class AssetNotFoundError(Exception):
    """Exception raised when an asset cannot be found"""
    pass


class AssetManager:
    """Manages loading and caching of game assets (images, fonts, sounds)"""
    
    _instance = None
    
    def __new__(cls):
        """Singleton pattern to ensure only one AssetManager exists"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Initialize the asset manager"""
        if self._initialized:
            return
            
        self._images: Dict[str, pygame.Surface] = {}
        self._fonts: Dict[str, pygame.font.Font] = {}
        self._sounds: Dict[str, pygame.mixer.Sound] = {}
        self._initialized = True
    
    def load_image(self, path: str, scale: Optional[Tuple[int, int]] = None) -> pygame.Surface:
        """
        Load an image from the given path
        
        Args:
            path: Path to the image file
            scale: Optional tuple (width, height) to scale the image
            
        Returns:
            pygame.Surface containing the loaded image
            
        Raises:
            AssetNotFoundError: If the image file cannot be found or loaded
        """
        # Create cache key including scale if provided
        cache_key = f"{path}_{scale}" if scale else path
        
        # Return cached image if available
        if cache_key in self._images:
            return self._images[cache_key]
        
        # Check if file exists
        if not os.path.exists(path):
            raise AssetNotFoundError(f"Image file not found: {path}")
        
        try:
            # Load the image
            image = pygame.image.load(path)
            
            # Scale if requested
            if scale:
                image = pygame.transform.scale(image, scale)
            
            # Convert for better performance (only if display is initialized)
            try:
                image = image.convert_alpha()
            except pygame.error:
                # Display not initialized yet, skip conversion
                pass
            
            # Cache the image
            self._images[cache_key] = image
            
            return image
            
        except pygame.error as e:
            raise AssetNotFoundError(f"Failed to load image {path}: {e}")
    
    def load_font(self, path: str, size: int) -> pygame.font.Font:
        """
        Load a font from the given path
        
        Args:
            path: Path to the font file
            size: Font size in points
            
        Returns:
            pygame.font.Font object
            
        Raises:
            AssetNotFoundError: If the font file cannot be found or loaded
        """
        # Create cache key
        cache_key = f"{path}_{size}"
        
        # Return cached font if available
        if cache_key in self._fonts:
            return self._fonts[cache_key]
        
        # Check if file exists
        if not os.path.exists(path):
            raise AssetNotFoundError(f"Font file not found: {path}")
        
        try:
            # Load the font
            font = pygame.font.Font(path, size)
            
            # Cache the font
            self._fonts[cache_key] = font
            
            return font
            
        except pygame.error as e:
            raise AssetNotFoundError(f"Failed to load font {path}: {e}")
    
    def load_sound(self, path: str) -> pygame.mixer.Sound:
        """
        Load a sound from the given path
        
        Args:
            path: Path to the sound file
            
        Returns:
            pygame.mixer.Sound object
            
        Raises:
            AssetNotFoundError: If the sound file cannot be found or loaded
        """
        # Return cached sound if available
        if path in self._sounds:
            return self._sounds[path]
        
        # Check if file exists
        if not os.path.exists(path):
            raise AssetNotFoundError(f"Sound file not found: {path}")
        
        try:
            # Load the sound
            sound = pygame.mixer.Sound(path)
            
            # Cache the sound
            self._sounds[path] = sound
            
            return sound
            
        except pygame.error as e:
            raise AssetNotFoundError(f"Failed to load sound {path}: {e}")
    
    def get_image(self, key: str) -> pygame.Surface:
        """
        Get a cached image by key
        
        Args:
            key: Cache key for the image
            
        Returns:
            pygame.Surface containing the image
            
        Raises:
            AssetNotFoundError: If the image is not in cache
        """
        if key not in self._images:
            raise AssetNotFoundError(f"Image not found in cache: {key}")
        return self._images[key]
    
    def get_font(self, key: str) -> pygame.font.Font:
        """
        Get a cached font by key
        
        Args:
            key: Cache key for the font
            
        Returns:
            pygame.font.Font object
            
        Raises:
            AssetNotFoundError: If the font is not in cache
        """
        if key not in self._fonts:
            raise AssetNotFoundError(f"Font not found in cache: {key}")
        return self._fonts[key]
    
    def get_sound(self, key: str) -> pygame.mixer.Sound:
        """
        Get a cached sound by key
        
        Args:
            key: Cache key for the sound
            
        Returns:
            pygame.mixer.Sound object
            
        Raises:
            AssetNotFoundError: If the sound is not in cache
        """
        if key not in self._sounds:
            raise AssetNotFoundError(f"Sound not found in cache: {key}")
        return self._sounds[key]
    
    def preload_assets(self):
        """
        Preload all game assets based on ASSET_PATHS configuration
        This should be called during the loading screen
        """
        # Load backgrounds
        for key, path in ASSET_PATHS['backgrounds'].items():
            try:
                self.load_image(path)
                self._images[f"bg_{key}"] = self._images[path]
            except AssetNotFoundError as e:
                print(f"Warning: {e}")
        
        # Load portraits
        for key, path in ASSET_PATHS['portraits'].items():
            try:
                self.load_image(path)
                self._images[f"portrait_{key}"] = self._images[path]
            except AssetNotFoundError as e:
                print(f"Warning: {e}")
        
        # Load card fronts
        for key, path in ASSET_PATHS['cards']['front'].items():
            try:
                self.load_image(path)
                self._images[f"card_front_{key}"] = self._images[path]
            except AssetNotFoundError as e:
                print(f"Warning: {e}")
        
        # Load card backs
        for key, path in ASSET_PATHS['cards']['back'].items():
            try:
                self.load_image(path)
                self._images[f"card_back_{key}"] = self._images[path]
            except AssetNotFoundError as e:
                print(f"Warning: {e}")
        
        # Load UI elements
        for key, path in ASSET_PATHS['ui'].items():
            try:
                self.load_image(path)
                self._images[f"ui_{key}"] = self._images[path]
            except AssetNotFoundError as e:
                print(f"Warning: {e}")
        
        # Load fonts
        for key, (path, size) in FONTS.items():
            try:
                self.load_font(path, size)
                self._fonts[f"font_{key}"] = self._fonts[f"{path}_{size}"]
            except AssetNotFoundError as e:
                print(f"Warning: {e}")
    
    def clear_cache(self):
        """Clear all cached assets"""
        self._images.clear()
        self._fonts.clear()
        self._sounds.clear()
    
    def get_background(self, name: str) -> pygame.Surface:
        """Helper method to get background by name"""
        return self.get_image(f"bg_{name}")
    
    def get_portrait(self, hero_id: int) -> pygame.Surface:
        """Helper method to get hero portrait by ID"""
        return self.get_image(f"portrait_hero{hero_id}")
    
    def get_card_front(self, hero_id: int) -> pygame.Surface:
        """Helper method to get card front by hero ID"""
        return self.get_image(f"card_front_hero{hero_id}")
    
    def get_card_back(self, rarity: str) -> pygame.Surface:
        """Helper method to get card back by rarity"""
        return self.get_image(f"card_back_{rarity}")
    
    def get_ui_element(self, ui_id: int) -> pygame.Surface:
        """Helper method to get UI element by ID"""
        return self.get_image(f"ui_ui{ui_id}")
    
    def get_game_font(self, font_type: str) -> pygame.font.Font:
        """Helper method to get font by type (title, normal, small)"""
        return self.get_font(f"font_{font_type}")
